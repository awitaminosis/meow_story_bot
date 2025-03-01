from places.states.base import *
from main import version

class Start(Location):
    def __init__(self, location, handler_type):
        super().__init__(location, handler_type)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.chat.id
            await bot.send_message(chat_id=chat_id, text="Это небольшое приключение из жизни Тигра и Ёжика.")
            await bot.send_message(chat_id=chat_id,
                                   text="Остальные приключения можно увидеть https://awitaminosis.github.io/pi_meow_fir/")

            keyboad_actions = [[KeyboardButton(text="Инвентарь")],
                               [KeyboardButton(text="Что нового?")],
                               ]

            menu_kb = ReplyKeyboardMarkup(keyboard=keyboad_actions, resize_keyboard=True)

            await bot.send_message(chat_id=chat_id, text="Версия: " + version, reply_markup=menu_kb)

            builder = InlineKeyboardBuilder()
            builder.button(text=t_start_new_story, callback_data=t_start_new_story)
            if await load_journey(chat_id):
                builder.button(text="Загрузить", callback_data="Загрузить")
            keyboard = builder.as_markup()
            await bot.send_message(chat_id=chat_id, text="Начинаем?", reply_markup=keyboard)
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,message):
        return message.text == '/start'
