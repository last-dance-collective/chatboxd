import sys

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage

from services.langgraph_service import MovementsAgent


def main():

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0,
    )

    agent = MovementsAgent(llm=llm)

    while True:
        query = input("> ")
        if query:
            r = agent.run(query)
            current_ai_response = [
                msg for msg in r["messages"] if isinstance(msg, AIMessage)
            ][-1]
            print(current_ai_response.content)


if __name__ == "__main__":
    main()
