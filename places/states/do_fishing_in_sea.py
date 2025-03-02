from places.states.base import *
from helper.filters import *

class DoFishingInSea(LocationWebApp):
    location = 'do_fishing_in_sea'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            if message.web_app_data:
                chat_id = message.chat.id
                state_data = await state.get_data()
                print(message.web_app_data)

                worms = state_data.get('worms', 0)
                worms -= 1
                worms = await maybe_eat_worms(worms, message, bot, message.chat.id, state)
                await state.update_data(worms=worms)
                photo_path = "./imgs/Fish_caught_bigest.png"
                photo = FSInputFile(photo_path)
                await bot.send_photo(chat_id=message.chat.id, photo=photo)

                await state.update_data(fishing_range=0)

                await state.update_data(location='fishing_did_fished')
                applicable_fishing_range = int(state_data.get('fishing_range', 0))
                await add_fish(state, applicable_fishing_range)

                keyboad_actions = [[KeyboardButton(text="Инвентарь")],
                                   [KeyboardButton(text="Что нового?")],
                                   ]

                menu_kb = ReplyKeyboardMarkup(keyboard=keyboad_actions, resize_keyboard=True)
                await bot.send_message(chat_id=chat_id, text="Поймал!", reply_markup=menu_kb)
                await bot.send_message(chat_id=chat_id, text="Что будем делать?",
                                       reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")
    async def filter(self,message):
        return dict(web_app_data=message.web_app_data) if message.web_app_data else False
