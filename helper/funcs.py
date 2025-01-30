import random
from aiogram.types import Message
from aiogram.types import FSInputFile

WORMS_EAT_CHANCE = 30
worms_pack = 5


async def add_worms():
    return random.randint(1, worms_pack)


async def maybe_eat_worms(worms, message: Message, bot, chat_id):
    chance = random.randint(1, 100)
    if chance > 100 - WORMS_EAT_CHANCE:
        worms = worms - random.randint(1, worms_pack)
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

    return worms
