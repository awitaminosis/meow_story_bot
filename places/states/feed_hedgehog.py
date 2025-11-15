# from places.states.base import *
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from helper.app import bot
from helper.funcs import feed_hedgehog_level, t_say
from helper.texts import t_feed_hedgehog, t_go_to_hedgehog_home, t_go_to_tiger_home
from logger.airtables import logger
from places.states.base import LocationCallbackQuery
from places.states.conditions import Transitions


class FeedHedgehog(LocationCallbackQuery):
    location = "feed_hedgehog"
    can_reach = [
        ("tiger_home", t_go_to_tiger_home, "inline", "", {}),
        ("hedgehog_home", t_go_to_hedgehog_home, "inline", "", {}),
        # ('go_fishing', t_go_fishing, 'inline', '', {},
        ("feed_hedgehog", t_feed_hedgehog, "inline", Transitions.can_feed_hedgehog, {}),
        # ('enter_forest', t_go_to_forest, 'inline', Transitions.can_go_to_forest, {}),
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await t_say(
                bot,
                chat_id,
                ["Ёжик, будешь червяка? Расскажи мне что-нибудь интересное."],
            )

            state_data = await state.get_data()
            print(state_data)
            await feed_hedgehog_level(bot, chat_id, state)
            await bot.send_message(
                chat_id=chat_id,
                text="Что будем делать?",
                reply_markup=await self.get_keyboard(state),
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self, F):
        return F.data == self.location
