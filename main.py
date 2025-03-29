import asyncio

from logger.airtables import setup_logger

logger = setup_logger()
version = '1.9.3'

from helper.app import *
from places.controller import *


async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
