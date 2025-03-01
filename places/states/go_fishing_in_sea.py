from aiogram.types import WebAppInfo
from places.states.base import *

class GoFishingInSea(LocationCallbackQuery):
    location = 'go_fishing_in_sea'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            global fishing_range
            fishing_range = sea_range
            await state.update_data(fishing_range=fishing_range)
            the_number = random.randint(1, fishing_range)
            await state.update_data(the_number=the_number)

            state_data = await state.get_data()
            mouse_quest_level = state_data.get('mouse_quest_level', 0)

            # builder = InlineKeyboardBuilder()
            # builder.row(InlineKeyboardButton(text="Закинуть удочку", web_app=types.WebAppInfo(url=config('SEA_FISH_URL'))))
            # fish_markup = builder.as_markup()
            #
            # await bot.send_message(chat_id=chat_id,text='fish',reply_markup=fish_markup)
            #
            #
            # keyboad_actions = [[KeyboardButton(text="fish", web_app=types.WebAppInfo(url=config('SEA_FISH_URL')))]]
            # menu_kb = ReplyKeyboardMarkup(keyboard=keyboad_actions, resize_keyboard=True)
            # await bot.send_message(chat_id=chat_id, text="Версия: " + version, reply_markup=menu_kb)

            # действует ли ограничение?
            if fishing_range == sea_range and mouse_quest_level < 2:
                await state.update_data(location='fishing_go_fishing_requisites_ok')
                await bot.send_message(chat_id=chat_id,
                                       text="На море бушуют волны. Они выбрасывают солёную пену на берег. Весь берег покрыт солью и она щиплет лапки. Не подойти...",
                                       reply_markup=await get_keyboard(state))
            else:
                # await bot.send_message(chat_id=chat_id,
                #     text="Тут такая рыба, что аж даже немножко страшно! Нет, не так! Страшно интересно! Вперёд, Ёжик, поймаем её! Можно забрасывать удочку на расстояние от 1 до " + str(fishing_range) + " метров",
                # )
                keyboad_actions = [[KeyboardButton(text="Отправиться на морскую рыбалку",
                                                   web_app=WebAppInfo(url=config('SEA_FISH_URL')))]]
                menu_kb = ReplyKeyboardMarkup(keyboard=keyboad_actions, resize_keyboard=True)
                await bot.send_message(chat_id=chat_id,
                                       text="Чтобы отправить на морскую рыбалку нажми на кнопку в меню",
                                       reply_markup=menu_kb)

                # await bot.send_message(chat_id=chat_id, text="Напиши цифру, на сколько метров от берега забрасывать удочку?")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_go_fish_in_sea
