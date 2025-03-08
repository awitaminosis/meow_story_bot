import asyncio
import random


from aiogram.fsm.state import State, StatesGroup
from logger.airtables import setup_logger
from helper.app import *

from places.controller import *

logger = setup_logger()
version = '1.8.1'


class Story(StatesGroup):
    guesses = State()
    finish = State()


async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
