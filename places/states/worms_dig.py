from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from helper.app import bot
from helper.funcs import add_worms, maybe_eat_worms, say
from helper.texts import (
    t_dig_for_worms,
    t_feed_hedgehog,
    t_go_to_forest,
    t_go_to_tiger_home,
)
from logger.airtables import logger
from places.states.base import LocationCallbackQuery
from places.states.conditions import Transitions


class WormsDig(LocationCallbackQuery):
    location = "worms_dig"

    def __init__(self, controller):
        self.can_reach = [
            ("tiger_home", t_go_to_tiger_home, "inline", "", {}),
            ("worms_dig", t_dig_for_worms, "inline", "", {}),
            # ('go_fishing', t_go_fishing, 'inline', '', {}),
            (
                "enter_forest",
                t_go_to_forest,
                "inline",
                Transitions.can_go_to_forest,
                {},
            ),
            (
                "feed_hedgehog",
                t_feed_hedgehog,
                "inline",
                Transitions.can_feed_hedgehog,
                {},
            ),
        ]
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await say(
                bot,
                chat_id,
                [
                    "Тигр помогает Ёжику копать червей. Ёжик внимательно смотрит и облизывается"
                ],
            )
            state_data = await state.get_data()
            worms = state_data.get("worms", 0)
            worms += await add_worms(state)
            worms = await maybe_eat_worms(worms, bot, message.message.chat.id, state)

            await state.update_data(worms=worms)
            await say(bot, chat_id, ["Червей: " + str(worms)])

            await state.update_data(location="worms_dig")
            await bot.send_message(
                chat_id=chat_id,
                text="Что будем делать?",
                reply_markup=await self.get_keyboard(state),
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self, callback_query):
        return callback_query.data == self.location
