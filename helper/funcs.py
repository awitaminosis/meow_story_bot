import random
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from helper.constants import *
g_showel_taken = False

async def add_worms(state: FSMContext):
    state_data = await state.get_data()
    showel = state_data.get('showel_taken', False)
    worms_dig_max = worms_dig_max_pcs_by_showel if showel else worms_dig_max_pcs_by_hand
    return random.randint(1, worms_dig_max)


async def maybe_eat_worms(worms, message: Message, bot, chat_id, state: FSMContext):
    global g_showel_taken

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
        if not state_data.get('swowel_mentioned', False):
            await bot.send_message(chat_id=chat_id, text='Кстати, Тигр, а я тут вспомнил... Я недавно лопату забыл в лесу... Лопатой бы копать поудобнее было бы...')
            await message.message.reply(text='Внимание! Открыта новая локация')
            await state.update_data(swowel_mentioned=True)
            g_showel_taken = True

    return worms
