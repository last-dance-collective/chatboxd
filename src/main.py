import asyncio
from utils.init_utils import initialize_app
from utils.chat_utils import (
    process_user_input,
    display_agent_response,
)
from utils.session_utils import get_session_val


async def handle_user_input(prompt):
    if prompt:
        await display_agent_response(
            get_session_val("agent").run_async(prompt, get_session_val("session_id"))
        )


async def main():
    initialize_app()

    prompt = process_user_input()
    await handle_user_input(prompt)


if __name__ == "__main__":
    asyncio.run(main())
