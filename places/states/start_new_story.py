from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from helper.app import bot
from helper.funcs import init_new_state, t_say
from helper.texts import (
    t_go_fishing,
    t_go_to_hedgehog_home,
    t_go_to_tiger_home,
    t_start_new_story,
)
from logger.airtables import logger
from places.states.base import LocationCallbackQuery


class StartNewStory(LocationCallbackQuery):
    location = "clearing"

    def __init__(self, controller):
        self.can_reach = [
            ("tiger_home", t_go_to_tiger_home, "inline", "", {}),
            ("hedgehog_home", t_go_to_hedgehog_home, "inline", "", {}),
            ("go_fishing", t_go_fishing, "inline", "", {}),
        ]
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await state.clear()
            await init_new_state(state)
            await t_say(
                bot,
                chat_id,
                [
                    "Однажды Тигр проснулся на полянке и подумал, а почему бы не пойти на рыбалку"
                ],
            )
            await state.update_data(location="clearing")
            await bot.send_message(
                chat_id=chat_id,
                text="Куда пойдём?",
                reply_markup=await self.get_keyboard(state),
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self, F):  # TODO
        return F.data == t_start_new_story
