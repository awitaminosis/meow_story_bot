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
    def __init__(self, location, handler_type):
        self.location = location
        self.handler_type = handler_type

    def register(self):
        global dp
        if self.handler_type == 'callback_query':
            dp.callback_query.register(self.handler, self.filter)
        elif self.handler_type == 'command':
            dp.message.register(self.handler, self.filter)
        elif self.handler_type == 'message':
            dp.message.register(self.handler, self.filter)
        elif self.handler_type == 'web_app':
            dp.message.register(self.handler, self.filter)
        else:
            raise NotImplementedError('unknow type:' + self.handler_type)