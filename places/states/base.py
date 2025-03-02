from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
import helper.funcs
import helper.keyboards
from main import bot
from main import dp
from helper.texts import *
from db.mongo_database import *

from helper.funcs import *
from helper.keyboards import *

from main import logger


class Location:
    def __init__(self, location):
        self.location = location

    def register(self):
        raise NotImplementedError('unknown type:' + self.handler_type)


class LocationCallbackQuery(Location):
    def register(self):
        dp.callback_query.register(self.handler, self.filter)


class LocationCommand(Location):
    def register(self):
        dp.message.register(self.handler, self.filter)


class LocationMessage(Location):
    def register(self):
        dp.message.register(self.handler, self.filter)


class LocationWebApp(Location):
    def register(self):
        dp.message.register(self.handler, self.filter)
