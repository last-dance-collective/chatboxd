
from datetime import datetime

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

from catalog.prompts import AGENT_SYSTEM_PROMPT
from utils.logger_utils import logger
from utils.langgraph_utils import State


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

        self.llm = llm.with_config(
            {"run_name": "chatboxd_llm"}
        )

        ## Create graph
        self.create_graph()
        logger.info(
            f"✅ Agent initialized"
        )

        
    def chatbot(self, state: State):
        """Main node that passes the message history into the chain."""
        return {
            "messages": [self.llm.invoke([self.sys_msg] + state["messages"])]
        }


    def create_graph(self):
        # Create graph
        graph_builder = StateGraph(State)

        ## Add Nodes
        graph_builder.add_node("chatbot", self.chatbot)

        ## Add Edges
        graph_builder.add_edge(START, "chatbot")

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
        logger.info(f"▶️ Running")
        return self.graph.astream_events(
            {"messages": HumanMessage(content=user_msg)},
            config,
            version="v2",
        )
