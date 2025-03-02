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


class Location:
    # todo
    locations = {
        'clearing': [t_go_to_tiger_home, t_go_to_hedgehog_home, t_go_fishing],
        'tiger_home': [t_take_the_rods, t_go_to_hedgehog_home, t_go_fishing],
        'rods_taken': [t_go_to_hedgehog_home, t_go_fishing],
        'hedgehog_home': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
        'worms_dig': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
        'fishing_requisites_missing': [t_go_to_tiger_home, t_go_to_hedgehog_home],
        'fishing_go_fishing_requisites_ok': [t_go_fish_in_pool, t_go_fish_in_river, t_go_fish_in_sea],
        'fishing_did_fished': [t_go_to_tiger_home, t_dig_for_worms, t_go_fish_in_pool, t_go_fish_in_river,
                               t_go_fish_in_sea],
        'fishing_worms_ended': [t_go_to_tiger_home, t_go_to_hedgehog_home],
        'forest': [t_go_to_tiger_home, t_go_to_hedgehog_home, t_go_fishing],
        't_visit_mouse': [t_go_to_tiger_home, t_go_to_hedgehog_home, t_go_fishing],
    }

    def __init__(self, location):
        self.location = location

    def register(self):
        raise NotImplementedError('unknown type:' + self.handler_type)

    async def get_keyboard(self, state: FSMContext):
        try:
            state_data = await state.get_data()
            location = state_data.get('location')
            print(location)
            rods_taken = state_data.get('fishing_rods', False)
            mouse_mentioned = state_data.get('mouse_mentioned', False)

            builder = InlineKeyboardBuilder()
            for place in self.locations[location]:
                if place == t_take_the_rods and rods_taken:
                    continue
                builder.row(InlineKeyboardButton(text=place, callback_data=place))

            # special
            is_showel_mentioned = state_data.get('showel_mentioned', False)
            if is_showel_mentioned:
                if location != 'forest' and location != 't_visit_mouse':
                    builder.row(InlineKeyboardButton(text=t_go_to_forest, callback_data=t_go_to_forest))
                builder.row(InlineKeyboardButton(text=t_feed_hedgehog, callback_data=t_feed_hedgehog))
            if mouse_mentioned and location == 'forest':
                builder.row(InlineKeyboardButton(text=t_visit_mouse, callback_data=t_visit_mouse))
                #
            if location == 't_visit_mouse':
                builder.row(InlineKeyboardButton(text=t_mouse_quest, callback_data=t_mouse_quest))

            keyboard = builder.as_markup()
            return keyboard
        except Exception as e:
            logger.error(f"An error occurred: {e}")


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
