
from langchain_core.messages import AIMessage

from services.llm_service import ollama_model
from services.langgraph_service import ChatboxdAgent

def main():

    llm = ollama_model(
        model="llama3.2:3b"
    )

    agent = ChatboxdAgent(llm=llm)

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
