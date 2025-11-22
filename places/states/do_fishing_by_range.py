from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from helper.app import bot
from helper.constants import pool_range, river_range, sea_range
from helper.funcs import add_fish, maybe_eat_worms, say
from helper.texts import t_go_fishing, t_go_to_tiger_home
from logger.airtables import logger
from places.states.base import LocationMessage
from places.states.conditions import Transitions


class DoFishingByRange(LocationMessage):
    location = "do_fishing_by_range"

    def __init__(self, controller):
        self.can_reach = [
            ("tiger_home", t_go_to_tiger_home, "inline", "", {}),
            ("go_fishing", t_go_fishing, "inline", Transitions.can_fish, {}),
        ]
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.chat.id
            state_data = await state.get_data()
            applicable_fishing_range = int(state_data.get("fishing_range", 0))

            requested_range = int(message.text)
            if requested_range > 0 and requested_range <= applicable_fishing_range:
                worms = state_data.get("worms", 0)
                worms -= 1
                worms = await maybe_eat_worms(worms, bot, message.chat.id, state)
                await state.update_data(worms=worms)

                if worms > 0:
                    try:
                        the_number = int(state_data.get("the_number"))
                        a_number = int(message.text)
                        if a_number == the_number:
                            await say(bot, chat_id, ["Клюёт!"])
                            if applicable_fishing_range == pool_range:
                                photo_path = "./imgs/Fish_caught.png"
                            if applicable_fishing_range == river_range:
                                photo_path = "./imgs/Fish_caught_big.png"
                            if applicable_fishing_range == sea_range:
                                photo_path = "./imgs/Fish_caught_bigest.png"
                            photo = FSInputFile(photo_path)
                            await bot.send_photo(chat_id=message.chat.id, photo=photo)

                            await state.update_data(fishing_range=0)

                            await state.update_data(location="fishing_did_fished")
                            await add_fish(state, applicable_fishing_range)

                            await bot.send_message(
                                chat_id=chat_id,
                                text="Что будем делать?",
                                reply_markup=await self.get_keyboard(state),
                            )

                        # не отгадал. дадим подсказку
                        elif the_number > a_number:
                            await say(
                                bot,
                                chat_id,
                                [
                                    "Ёжик подсказывает, что забрасывать удочку нужно дальше"
                                ],
                            )
                        else:
                            await say(
                                bot,
                                chat_id,
                                [
                                    "Ёжик подсказывает, что забрасывать удочку нужно ближе"
                                ],
                            )
                    except Exception:
                        await say(bot, chat_id, ["Это не число"])
                else:
                    await state.update_data(location="fishing_worms_ended")
                    await bot.send_message(
                        chat_id=chat_id,
                        text="Всё, Тигр, черви закончились. Пойдём отсюда",
                        reply_markup=await self.get_keyboard(state),
                    )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self, message):
        return message.text in ([str(x) for x in range(1, 101)])
