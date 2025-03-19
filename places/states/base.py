from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
import helper.funcs
from main import bot
from main import dp
from helper.texts import *
from db.mongo_database import *

from helper.funcs import *
# from helper.keyboards import *

from main import logger
from places.states.conditions import Transitions


class Location:
    def __init__(self, location, controller):
        self.location = location
        self.controller = controller

    def register(self):
        raise NotImplementedError('unknown type:' + self.handler_type)

    async def get_keyboard(self, state: FSMContext):
        builder = InlineKeyboardBuilder()
        for place, place_text, keyboard_type, condition, extra in self.can_reach:
            if extra.get('coords',None) is not None:
                x,y = extra['coords']
                place += f'__{x},{y}'
            elif extra.get('action',None) is not None:
                action = extra['action']
                place += f'--{action}'
            if condition:
                if await condition(self.location, state):
                    if keyboard_type == 'inline':
                        builder.row(InlineKeyboardButton(text=place_text, callback_data=place))
            else:
                if keyboard_type == 'inline':
                    builder.row(InlineKeyboardButton(text=place_text, callback_data=place))
        keyboard = builder.as_markup()
        return keyboard

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
