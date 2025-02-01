from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helper.texts import *

locations = {
    'clearing': [t_go_to_tiger_home, t_go_to_hedgehog_home, t_go_fishing],
    'tiger_home': [t_take_the_rods, t_go_to_hedgehog_home, t_go_fishing],
    'rods_taken': [t_go_to_hedgehog_home, t_go_fishing],
    'hedgehog_home': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
    'worms_dig': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
    'fishing_requisites_missing': [t_go_to_tiger_home, t_go_to_hedgehog_home],
    'fishing_go_fishing_requisites_ok': [t_go_fish_in_pool, t_go_fish_in_river, t_go_fish_in_sea],
    'fishing_did_fished': [t_go_to_tiger_home, t_dig_for_worms, t_go_fishing],
    'fishing_worms_ended': [t_go_to_tiger_home, t_go_to_hedgehog_home]
}


async def get_keyboard(state: FSMContext):
    state_data = await state.get_data()
    location = state_data.get('location')

    builder = InlineKeyboardBuilder()
    for place in locations[location]:
        builder.row(InlineKeyboardButton(text=place, callback_data=place))
    keyboard = builder.as_markup()
    return keyboard

