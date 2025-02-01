from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import helper.funcs
from helper.texts import *
from helper.funcs import *

locations = {
    'clearing': [t_go_to_tiger_home, t_go_to_hedgehog_home, t_go_fishing],
    'tiger_home': [t_take_the_rods, t_go_to_hedgehog_home, t_go_fishing],
    'rods_taken': [t_go_to_hedgehog_home, t_go_fishing],
    'hedgehog_home': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
    'worms_dig': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
    'fishing_requisites_missing': [t_go_to_tiger_home, t_go_to_hedgehog_home],
    'fishing_go_fishing_requisites_ok': [t_go_fish_in_pool, t_go_fish_in_river, t_go_fish_in_sea],
    'fishing_did_fished': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
    'fishing_worms_ended': [t_go_to_tiger_home, t_go_to_hedgehog_home],
    'forest': [t_go_to_tiger_home, t_go_to_hedgehog_home, t_go_fishing]
}


async def get_keyboard(state: FSMContext):
    state_data = await state.get_data()
    location = state_data.get('location')

    builder = InlineKeyboardBuilder()
    for place in locations[location]:
        if place == t_take_the_rods and helper.funcs.g_rods_taken:
            continue
        builder.row(InlineKeyboardButton(text=place, callback_data=place))

    #special
    if helper.funcs.g_showel_taken:
        if location != 'forest':
            builder.row(InlineKeyboardButton(text=t_go_to_forest, callback_data=t_go_to_forest))


    keyboard = builder.as_markup()
    return keyboard
