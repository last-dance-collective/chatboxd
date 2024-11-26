from datetime import datetime

from langchain.globals import set_debug
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from catalog.prompts import AGENT_SYSTEM_PROMPT
from utils.logger_utils import logger
from utils.langgraph_utils import State
from services.agent_tools import (
    get_movies,
    get_reviews,
    get_graph,
    get_movie_details,
)


class ChatboxdAgent:
    def __init__(
        self,
        llm=None,
        database=None,
        username=None,
    ):
        self.sys_msg = SystemMessage(
            content=AGENT_SYSTEM_PROMPT.format(
                current_date=datetime.today().strftime("%Y-%m-%d"),
                username=username,
            )
        )
        self.tools = [get_movies, get_movie_details, get_reviews, get_graph]

        self.llm = llm.bind_tools(self.tools).with_config({"run_name": "chatboxd_llm"})
        ## Create graph
        self.create_graph()
        logger.info("✅ Agent initialized")

    def chatbot(self, state: State):
        """Main node that passes the message history into the chain."""
        return {"messages": [self.llm.invoke([self.sys_msg] + state["messages"])]}

    def create_graph(self):
        # Create graph
        graph_builder = StateGraph(State)

        ## Add Nodes
        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_node("tools", ToolNode(self.tools))

        ## Add Edges
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")

        checkpointer = MemorySaver()
        self.graph = graph_builder.compile(checkpointer=checkpointer)

    def run(self, user_msg, thread_id="1"):
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke(
            {
                "messages": HumanMessage(content=user_msg),
            },
            config,
        )

    def run_async(
        self,
        user_msg,
        thread_id="1",
    ):
        config = {"configurable": {"thread_id": thread_id}}
        logger.info("▶️ Running")
        return self.graph.astream_events(
            {"messages": HumanMessage(content=user_msg)},
            config,
            version="v2",
        )
