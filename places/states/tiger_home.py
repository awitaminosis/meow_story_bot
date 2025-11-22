from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from helper.app import bot
from helper.funcs import t_say
from helper.texts import (
    t_go_fishing,
    t_go_to_hedgehog_home,
    t_take_the_rods,
)
from logger.airtables import logger
from places.states.base import LocationCallbackQuery
from places.states.conditions import Transitions


class TigerHomeLocation(LocationCallbackQuery):
    location = "tiger_home"

    def __init__(self, controller):
        self.can_reach = [
            ("hedgehog_home", t_go_to_hedgehog_home, "inline", "", {}),
            ("go_fishing", t_go_fishing, "inline", "", {}),
            ("take_the_rods", t_take_the_rods, "inline", Transitions.can_take_rods, {}),
        ]
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await t_say(
                bot,
                chat_id,
                [
                    "Вот я и дома. Хорошо тут среди множества рыболовных принадлежностей."
                ],
            )

            await state.update_data(location="tiger_home")
            await bot.send_message(
                chat_id=chat_id,
                text="Что будем делать?",
                reply_markup=await self.get_keyboard(state),
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
