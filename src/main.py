import asyncio
from utils.init_utils import initialize_app
from utils.chat_utils import process_user_input, display_chat_msg


async def handle_user_input(prompt):
    if prompt:
        display_chat_msg("Hola, soy Chatboxd, un bot de ChatGPT para LetterBoxd!", "ai")


async def main():
    initialize_app()

    prompt = process_user_input()
    await handle_user_input(prompt)


if __name__ == "__main__":
    asyncio.run(main())
