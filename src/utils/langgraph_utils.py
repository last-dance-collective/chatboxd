from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage, HumanMessage


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


def rewrite_tool_responses(state: State) -> list:
    if isinstance(state["messages"][-1], HumanMessage):
        messages = []
        for msg in state["messages"]:
            if isinstance(msg, ToolMessage):
                msg.content = "<La respuesta de la tool está omitida>"
            messages.append(msg)
        return messages
    else:
        return state["messages"]
