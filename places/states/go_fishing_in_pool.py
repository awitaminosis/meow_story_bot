# from places.states.base import *
import random

from places.states.base import LocationCallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from helper.funcs import say
from helper.constants import pool_range
from logger.airtables import logger
from helper.app import bot


class GoFishingInPool(LocationCallbackQuery):
    location = "go_fishing_in_pool"

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            global fishing_range
            fishing_range = pool_range
            await state.update_data(fishing_range=fishing_range)
            the_number = random.randint(1, fishing_range)
            await state.update_data(the_number=the_number)

            await say(
                bot,
                chat_id,
                [
                    "Тут рыба полеге. Можно забрасывать удочку на расстояние от 1 до "
                    + str(fishing_range)
                    + " метров"
                ],
            )

            await say(
                bot,
                chat_id,
                ["Напиши цифру, на сколько метров от берега забрасывать удочку?"],
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self, F):
        return F.data == self.location
