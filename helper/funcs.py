import random
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from helper.constants import *

# g_showel_taken = False
g_showel_mentioned = False
g_rods_taken = False

async def add_worms(state: FSMContext):
    state_data = await state.get_data()
    showel = state_data.get('showel_taken', False)
    worms_dig_max = worms_dig_max_pcs_by_showel if showel else worms_dig_max_pcs_by_hand
    return random.randint(1, worms_dig_max)


async def maybe_eat_worms(worms, message: Message, bot, chat_id, state: FSMContext):
    global g_showel_mentioned
    chance = random.randint(1, 100)
    if chance > 100 - WORMS_EAT_CHANCE:
        worms = worms - random.randint(1, hedgehog_eat_worms_max_pcs)
        hedgehog_phrases = [
            'Тигр, они первые начали',
            'Смотри как я могу!',
            'Тигр, Тигр, они убегают! Не волнуйся, я догоню их!',
            'Как там считать надо... раз, два, три, четыре... сбился',
            'А это лишние червяки были',
            'Тигр, я ничего не смог поделать, они убежали...',
            'А вдруг без червей будет лучше ловится?',
            'Тигр, ну не знаю, придумай сам что-нибудь',
            'Тигр, ну ты же мне друг!',
            'Зато я в следующий раз тебе помогу',
            'Ой, а что произошло?',
            'А я думал, что это была рыба...',
        ]
        phrase_index = random.randint(0, len(hedgehog_phrases) - 1)

        photo_path = "./imgs/Hedgehog_worms.png"
        photo = FSInputFile(photo_path)
        await bot.send_photo(chat_id=chat_id, photo=photo)
        await bot.send_message(chat_id=chat_id, text=hedgehog_phrases[phrase_index])
        if worms < 0:
            worms = 0

        # открываем дорогу в лес
        state_data = await state.get_data()
        if not g_showel_mentioned:
            await bot.send_message(chat_id=chat_id, text='Кстати, Тигр, а я тут вспомнил... Я недавно лопату забыл в лесу... Лопатой бы копать поудобнее было бы...')
            await bot.send_message(chat_id=chat_id, text='Внимание! Открыта новая локация')
            await state.update_data(showel_mentioned=True)
            g_showel_mentioned = True

    return worms, state


async def add_fish(state: FSMContext, applicable_fishing_range):
    state_data = await state.get_data()
    if applicable_fishing_range == pool_range:
        pool_fish_pcs = state_data.get('pool_fish_pcs', 0)
        pool_fish_pcs = int(pool_fish_pcs) + 1
        await state.update_data(pool_fish_pcs=pool_fish_pcs)
        weight = random.randint(weight_pool_fish_min, weight_pool_fish_max)
        pool_fish_weight = state_data.get('pool_fish_weight', 0)
        pool_fish_weight = int(pool_fish_weight) + weight
        await state.update_data(pool_fish_weight=pool_fish_weight)
    if applicable_fishing_range == river_range:
        river_fish_pcs = state_data.get('river_fish_pcs', 0)
        river_fish_pcs = int(river_fish_pcs) + 1
        await state.update_data(river_fish_pcs=river_fish_pcs)
        weight = random.randint(weight_river_fish_min, weight_river_fish_max)
        river_fish_weight = state_data.get('river_fish_weight', 0)
        river_fish_weight = int(river_fish_weight) + weight
        await state.update_data(river_fish_weight=river_fish_weight)
    if applicable_fishing_range == sea_range:
        sea_fish_pcs = state_data.get('sea_fish_pcs', 0)
        sea_fish_pcs = int(sea_fish_pcs) + 1
        await state.update_data(sea_fish_pcs=sea_fish_pcs)
        weight = random.randint(weight_sea_fish_min, weight_sea_fish_max)
        sea_fish_weight = state_data.get('sea_fish_weight', 0)
        sea_fish_weight = int(sea_fish_weight) + weight
        await state.update_data(sea_fish_weight=sea_fish_weight)

async def init_new_state(state: FSMContext):
    await state.update_data(location='clearing')
    await state.update_data(worms=0)
    await state.update_data(pool_fish_pcs=0)
    await state.update_data(pool_fish_weight=0)
    await state.update_data(river_fish_pcs=0)
    await state.update_data(river_fish_weight=0)
    await state.update_data(sea_fish_pcs=0)
    await state.update_data(sea_fish_weight= 0)
    await state.update_data(fishing_rods=False)
    await state.update_data(pool_fish_pcs=0)
    await state.update_data(pool_fish_weight=0)
    await state.update_data(river_fish_pcs=0)
    await state.update_data(river_fish_weight=0)
    await state.update_data(sea_fish_pcs=0)
    await state.update_data(sea_fish_weight=0)
    await state.update_data(showel_mentioned=False)
    await state.update_data(showel_taken=False)