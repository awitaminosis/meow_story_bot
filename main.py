import asyncio
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters.command import Command
from decouple import config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random
from aiogram.types import FSInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import F

bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
bot_router = Router()


class Story(StatesGroup):
    guesses = State()
    finish = State()


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.reply("Это небольшое приключение из жизни Тигра и Ёжика.")
    await message.reply("Остальные приключения можно увидеть https://awitaminosis.github.io/pi_meow_fir/")

    kb = [
        [KeyboardButton(text="Начать новое приключение")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.reply(text="Начинаем?", reply_markup=keyboard)

@dp.message(F.text == 'Начать новое приключение')
async def start_new_story(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Однажды Тигр проснулся на полянке и подумал, а почему бы не пойти на рыбалку",
        reply_markup=ReplyKeyboardRemove(),
    )
    photo_path = "./imgs/Tiger.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

    kb = [
        [KeyboardButton(text="Пойти в домик Тигра")],
        [KeyboardButton(text="Пойти в домик к Ёжику")],
        [KeyboardButton(text="Пойти на рыбалку")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.reply(text="Куда пойдём?", reply_markup=keyboard)

@dp.message(F.text == 'Пойти в домик Тигра')
async def go_to_tiger_home(message: Message, state: FSMContext):
    await message.answer(
        "Тигр пришёл в свой дом. Хорошо тут среди множества рыболовных принадлежностей",
        reply_markup=ReplyKeyboardRemove(),
    )
    kb = [
        [KeyboardButton(text="Взять удочки")],
        [KeyboardButton(text="Пойти в домик к Ёжику")],
        [KeyboardButton(text="Пойти на рыбалку")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.reply(text="Что будем делать?", reply_markup=keyboard)

@dp.message(F.text == 'Взять удочки')
async def take_the_rods(message: Message, state: FSMContext):
    await message.answer(
        "Вот они, любимые инструменты Тигра. Теперь и на рыбалку можно",
        reply_markup=ReplyKeyboardRemove(),
    )
    state_data = await state.get_data()
    state_data['fishing_rods'] = True
    await state.set_data(state_data)

    kb = [
        [KeyboardButton(text="Пойти в домик к Ёжику")],
        [KeyboardButton(text="Пойти на рыбалку")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.reply(text="Что будем делать?", reply_markup=keyboard)

@dp.message(F.text == 'Пойти в домик к Ёжику')
async def go_to_hedgehog_home(message: Message, state: FSMContext):
    await message.answer(
        "Ёжик встречает Тигра рядом с компостной ямой, в которой он разводит червей. Ёжик тепло приветствует Тигра и намекает, что было бы хорошо помочь ему в выкапывании вкусных червей",
        reply_markup=ReplyKeyboardRemove(),
    )
    photo_path = "./imgs/Hedgehog.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    kb = [
        [KeyboardButton(text="Пойти в домик Тигра")],
        [KeyboardButton(text="Копать червей")],
        [KeyboardButton(text="Пойти на рыбалку")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.reply(text="Что будем делать?", reply_markup=keyboard)

@dp.message(F.text == 'Копать червей')
async def dig_for_worms(message: Message, state: FSMContext):
    await message.answer(
        "Тигр помогает Ёжику копать червей. Ёжик облизывается и помогает",
        reply_markup=ReplyKeyboardRemove(),
    )
    state_data = await state.get_data()
    worms = state_data.get('worms', 0)
    worms += 5
    state_data['worms'] = worms
    await state.set_data(state_data)
    await message.reply(text="Червей: " + str(worms))
    kb = [
        [KeyboardButton(text="Пойти в домик Тигра")],
        [KeyboardButton(text="Копать червей")],
        [KeyboardButton(text="Пойти на рыбалку")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.reply(text="Что будем делать?", reply_markup=keyboard)

@dp.message(F.text == 'Пойти на рыбалку')
async def go_fishing(message: Message, state: FSMContext):
    state_data = await state.get_data()
    has_fishing_rods = state_data.get('fishing_rods')
    worms = int(state_data.get('worms', 0))
    if not has_fishing_rods:
        await message.answer(
            "Эх, без удочек тяжело ловить... Вот бы где-ниубдь добыть рыболовный инструмент...",
            reply_markup=ReplyKeyboardRemove(),
        )
        kb = [
            [KeyboardButton(text="Пойти в домик Тигра")],
            [KeyboardButton(text="Пойти в домик к Ёжику")],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb)
        await message.reply(text="Что будем делать?", reply_markup=keyboard)
    elif worms <= 0:
        await message.answer(
            "Что-то подсказывает Тигру, что без червей рыба сегодня ловиться не будет... Вот бы где-ниубдь добыть червей...",
            reply_markup=ReplyKeyboardRemove(),
        )
        kb = [
            [KeyboardButton(text="Пойти в домик Тигра")],
            [KeyboardButton(text="Пойти в домик к Ёжику")],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb)
        await message.reply(text="Что будем делать?", reply_markup=keyboard)
    else:
        await message.answer(
            "Начинаем рыбалку",
            reply_markup=ReplyKeyboardRemove(),
        )
        await message.reply(text="Червей осталось: " + str(worms))
        kb = [
            [KeyboardButton(text="Ловить в луже")],
            [KeyboardButton(text="Ловить в речке")],
            [KeyboardButton(text="Ловить в море")],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb)
        await message.reply(text="Ловить можно где помельче - там легче поймать, но и рыба не такая интересная. Или же ловить там где поглубже - но и рыба там поинтересней", reply_markup=keyboard)

@dp.message(F.text == 'Ловить в речке')
@dp.message(F.text == 'Ловить в море')
async def go_fishing_further(message: Message, state: FSMContext):
    await message.answer(
        text="Пока нет - там сегодня непогода",
    )


@dp.message(F.text == 'Ловить в луже')
async def go_fish_in_pool(message: Message, state: FSMContext):
    await message.answer(
        "Тут рыба полеге. Моно забрасывать удочку на расстояние от 1 до 5 метров",
        reply_markup=ReplyKeyboardRemove(),
    )

    the_number = random.randint(1, 5)
    await state.update_data(the_number=the_number)

    kb = [
        [KeyboardButton(text="Пойти в домик Тигра")],
        [KeyboardButton(text="Пойти в домик к Ёжику")],
        [KeyboardButton(text="Ловить")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.reply(text="На какое расстояние забрасывать удочку?", reply_markup=keyboard)

@dp.message(F.text == '1')
@dp.message(F.text == '2')
@dp.message(F.text == '3')
@dp.message(F.text == '4')
@dp.message(F.text == '5')
async def do_fishing_in_pool(message: Message, state: FSMContext):
    state_data = await state.get_data()
    worms = state_data.get('worms', 0)
    worms -= 1
    state_data['worms'] = worms
    await state.set_data(state_data)

    try:
        the_number = int(state_data.get('the_number'))
        a_number = int(message.text)
        if a_number == the_number:
            await message.answer('Клюёт!')
            photo_path = "./imgs/Fish_caught.png"
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        else:
            # не отгадал. дадим подсказку
            if the_number > a_number:
                await message.answer('Ёжик подсказывает, что забрасывать удочку нужно дальше')
            else:
                await message.answer('Ёжик подсказывает, что забрасывать удочку нужно ближе')
    except Exception as e:
        await message.answer('Это не число')

    # await message.answer("Начнём игру. Я загадал число от 1 до 100 (1 тоже может быть, и 100 тоже может быть). Число целое. Попробуй угадать какое за наименьшее количество попыток.")
    # await state.set_state(Story.guesses)
    # the_number = random.randint(1, 100)
    # await state.update_data(the_number=the_number)
    # await state.update_data(attempt=0)



# @dp.message(Story.guesses)
# async def ask(message: Message, state: FSMContext):
#     storage_data = await state.get_data()
#     attempt = int(storage_data.get('attempt', 0))
#     the_number = int(storage_data.get('the_number'))
#     attempt = attempt + 1
#
#     await state.update_data(attempt=attempt)
#     try:
#         a_number = int(message.text)
#         if a_number == the_number:
#             await message.answer('Молодец, ты отгадал!')
#             await message.answer(f'За {attempt} попыток')
#         else:
#             # не отгадал. дадим подсказку
#             if the_number > a_number:
#                 await message.answer('Загаданное число больше')
#             else:
#                 await message.answer('Загаданное число меньше')
#     except Exception as e:
#         await message.answer('Это не число')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
