from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.sqlite_database import load_journey
from helper.app import bot
from helper.constants import version
from helper.funcs import say
from helper.texts import t_start_new_story
from logger.airtables import logger
from places.states.base import LocationCommand


class Start(LocationCommand):
    location = "start"

    def __init__(self, controller):
        self.can_reach = [
            ("start_new_story", "start_new_story", "inline", "", {}),
        ]
        super().__init__(self.location, controller)

    async def handler(self, message: Message):
        try:
            chat_id = message.chat.id
            await say(
                bot, chat_id, ["Это небольшое приключение из жизни Тигра и Ёжика."]
            )
            await say(
                bot,
                chat_id,
                [
                    "Остальные приключения можно увидеть https://awitaminosis.github.io/pi_meow_fir/"
                ],
            )

            keyboad_actions = [
                [KeyboardButton(text="Инвентарь")],
                [KeyboardButton(text="Что нового?")],
            ]

            menu_kb = ReplyKeyboardMarkup(
                keyboard=keyboad_actions, resize_keyboard=True
            )

            await bot.send_message(
                chat_id=chat_id, text="Версия: " + version, reply_markup=menu_kb
            )

            builder = InlineKeyboardBuilder()
            builder.button(text=t_start_new_story, callback_data=t_start_new_story)
            if await load_journey(chat_id):
                builder.button(text="Загрузить", callback_data="Загрузить")
            keyboard = builder.as_markup()
            await bot.send_message(
                chat_id=chat_id, text="Начинаем?", reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self, message):
        return message.text == "/start"
