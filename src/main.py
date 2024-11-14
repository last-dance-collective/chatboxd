import asyncio
from utils.init_utils import initialize_app


async def main():
    initialize_app()


if __name__ == "__main__":
    asyncio.run(main())
