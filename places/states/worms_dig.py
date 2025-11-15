# from places.states.base import *
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from places.states.conditions import Transitions
from helper.app import bot
from helper.funcs import say, add_worms, maybe_eat_worms
from logger.airtables import logger
from helper.texts import (
    t_feed_hedgehog,
    t_go_to_tiger_home,
    t_dig_for_worms,
    t_go_to_forest,
)


from places.states.base import LocationCallbackQuery


class WormsDig(LocationCallbackQuery):
    location = "worms_dig"
    can_reach = [
        ("tiger_home", t_go_to_tiger_home, "inline", "", {}),
        ("worms_dig", t_dig_for_worms, "inline", "", {}),
        # ('go_fishing', t_go_fishing, 'inline', '', {}),
        ("enter_forest", t_go_to_forest, "inline", Transitions.can_go_to_forest, {}),
        ("feed_hedgehog", t_feed_hedgehog, "inline", Transitions.can_feed_hedgehog, {}),
    ]

    def __init__(self, controller):
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
            worms = await maybe_eat_worms(
                worms, message, bot, message.message.chat.id, state
            )

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

    async def filter(self, F):
        return F.data == self.location
