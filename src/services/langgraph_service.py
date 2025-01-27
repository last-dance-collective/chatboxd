import os
from datetime import datetime
from typing import AsyncIterator

from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from yaml import StreamEndEvent

from config import CONVERS_TURNS
from catalog.prompts import PROMPTS
from utils.logger_utils import logger
from utils.langgraph_utils import State, rewrite_tool_responses
from utils.session_utils import get_session_val
from services.agent_tools import (
    get_movies,
    get_reviews,
    get_graph,
    get_movie_details,
    get_movie_details_extended,
)


class ChatboxdAgent:
    def __init__(
        self,
        llm: ChatOllama | AzureChatOpenAI,
        username: str = "",
    ):
        language = get_session_val("language")

        self.sys_msg = SystemMessage(
            content=PROMPTS[language]["AGENT_SYSTEM_PROMPT"].format(
                current_date=datetime.today().strftime("%Y-%m-%d"),
                username=username,
            )
        )
        self.tools = [get_movies, get_reviews, get_graph]

        if os.environ.get("OMDB_API_KEY"):
            logger.info("🎞️✅ OMDB key is present, get details tool extended enabled")
            self.tools.append(get_movie_details_extended)
        else:
            logger.info(
                "🎞️❌ OMDB key is NOT present, get details tool extended disabled"
            )
            self.tools.append(get_movie_details)

        self.llm = llm.bind_tools(self.tools).with_config({"run_name": "chatboxd_llm"})
        ## Create graph
        self.create_graph()
        logger.info("✅ Agent initialized")

    def filter_messages(self, state: State):
        turn_start_indices = [
            i
            for i, msg in enumerate(state["messages"])
            if isinstance(msg, HumanMessage)
        ]

        if len(turn_start_indices) > CONVERS_TURNS + 1:
            first_keep_index = turn_start_indices[-(CONVERS_TURNS + 1)]

            delete_messages = [
                RemoveMessage(id=m.id) for m in state["messages"][:first_keep_index]
            ]

            logger.info(f"🗑️  {len(delete_messages)} messages removed from chat history")

            return {"messages": delete_messages}

        else:
            return

    def chatbot(self, state: State):
        """Main node that passes the message history into the chain."""
        messages = rewrite_tool_responses(state)
        return {"messages": [self.llm.invoke([self.sys_msg] + messages)]}

    def create_graph(self):
        # Create graph
        graph_builder = StateGraph(State)

        ## Add Nodes
        graph_builder.add_node("filter_messages", self.filter_messages)
        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_node("tools", ToolNode(self.tools))

        ## Add Edges
        graph_builder.add_edge(START, "filter_messages")
        graph_builder.add_edge("filter_messages", "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")

        checkpointer = MemorySaver()
        self.graph = graph_builder.compile(checkpointer=checkpointer)

    def run(self, user_msg: str, thread_id: str = "1"):
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke(
            {
                "messages": HumanMessage(content=user_msg),
            },
            config,
        )

    def run_async(
        self,
        user_msg: str,
        thread_id: str = "1",
    ) -> AsyncIterator[StreamEndEvent]:
        config = {"configurable": {"thread_id": thread_id}}
        logger.info("▶️ Running")
        return self.graph.astream_events(
            {"messages": HumanMessage(content=user_msg)},
            config,
            version="v2",
        )
