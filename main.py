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
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import F

bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
bot_router = Router()


class Story(StatesGroup):
    guesses = State()
    finish = State()


t_start_new_story = "Начать новое приключение"
t_go_to_tiger_home = "Пойти в домик Тигра"
t_go_to_hedgehog_home = "Пойти в домик к Ёжику"
t_go_fishing = "Пойти на рыбалку"
t_take_the_rods = "Взять удочки"
t_dig_for_worms = "Копать червей"
t_go_fish_in_pool = "Ловить в луже"
t_go_fish_in_river = "Ловить в речке"
t_go_fish_in_sea = "Ловить в море"


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.reply("Это небольшое приключение из жизни Тигра и Ёжика.")
    await message.reply("Остальные приключения можно увидеть https://awitaminosis.github.io/pi_meow_fir/")

    builder = InlineKeyboardBuilder()
    builder.button(text=t_start_new_story, callback_data=t_start_new_story)
    keyboard = builder.as_markup()
    await message.reply(text="Начинаем?", reply_markup=keyboard)


@dp.callback_query(F.data == t_start_new_story)
async def start_new_story(message: Message, state: FSMContext):
    await state.clear()
    await message.message.reply(
        "Однажды Тигр проснулся на полянке и подумал, а почему бы не пойти на рыбалку",
        reply_markup=ReplyKeyboardRemove(),
    )
    photo_path = "./imgs/Tiger.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=message.message.chat.id, photo=photo)

    # kb = [
    #     [KeyboardButton(text=t_go_to_tiger_home)],
    #     [KeyboardButton(text=t_go_to_hedgehog_home)],
    #     [KeyboardButton(text=t_go_fishing)],
    # ]
    # keyboard = ReplyKeyboardMarkup(keyboard=kb)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t_go_to_tiger_home, callback_data=t_go_to_tiger_home))
    builder.row(InlineKeyboardButton(text=t_go_to_hedgehog_home, callback_data=t_go_to_hedgehog_home))
    builder.row(InlineKeyboardButton(text=t_go_fishing, callback_data=t_go_fishing))
    keyboard = builder.as_markup()
    await message.message.reply(text="Куда пойдём?", reply_markup=keyboard)


@dp.callback_query(F.data == t_go_to_tiger_home)
async def go_to_tiger_home(message: Message, state: FSMContext):
    await message.message.reply(
        "Тигр пришёл в свой дом. Хорошо тут среди множества рыболовных принадлежностей",
        reply_markup=ReplyKeyboardRemove(),
    )
    # kb = [
    #     [KeyboardButton(text=t_take_the_rods)],
    #     [KeyboardButton(text=t_go_to_hedgehog_home)],
    #     [KeyboardButton(text=t_go_fishing)],
    # ]
    # keyboard = ReplyKeyboardMarkup(keyboard=kb)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t_take_the_rods, callback_data=t_take_the_rods))
    builder.row(InlineKeyboardButton(text=t_go_to_hedgehog_home, callback_data=t_go_to_hedgehog_home))
    builder.row(InlineKeyboardButton(text=t_go_fishing, callback_data=t_go_fishing))
    keyboard = builder.as_markup()
    await message.message.reply(text="Что будем делать?", reply_markup=keyboard)


@dp.callback_query(F.data == t_take_the_rods)
async def take_the_rods(message: Message, state: FSMContext):
    await message.message.reply(
        "Вот они, любимые инструменты Тигра. Теперь и на рыбалку можно",
        reply_markup=ReplyKeyboardRemove(),
    )
    state_data = await state.get_data()
    state_data['fishing_rods'] = True
    await state.set_data(state_data)

    # kb = [
    #     [KeyboardButton(text=t_go_to_hedgehog_home)],
    #     [KeyboardButton(text=t_go_fishing)],
    # ]
    # keyboard = ReplyKeyboardMarkup(keyboard=kb)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t_go_to_hedgehog_home, callback_data=t_go_to_hedgehog_home))
    builder.row(InlineKeyboardButton(text=t_go_fishing, callback_data=t_go_fishing))
    keyboard = builder.as_markup()
    await message.message.reply(text="Что будем делать?", reply_markup=keyboard)


@dp.callback_query(F.data == t_go_to_hedgehog_home)
async def go_to_hedgehog_home(message: Message, state: FSMContext):
    await message.message.reply(
        "Ёжик встречает Тигра рядом с компостной ямой, в которой он разводит червей. Ёжик тепло приветствует Тигра и намекает, что было бы хорошо помочь ему в выкапывании вкусных червей",
        reply_markup=ReplyKeyboardRemove(),
    )
    photo_path = "./imgs/Hedgehog.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=message.message.chat.id, photo=photo)
    # kb = [
    #     [KeyboardButton(text=t_go_to_tiger_home)],
    #     [KeyboardButton(text=t_dig_for_worms)],
    #     [KeyboardButton(text=t_go_fishing)],
    # ]
    # keyboard = ReplyKeyboardMarkup(keyboard=kb)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t_go_to_tiger_home, callback_data=t_go_to_tiger_home))
    builder.row(InlineKeyboardButton(text=t_dig_for_worms, callback_data=t_dig_for_worms))
    builder.row(InlineKeyboardButton(text=t_go_fishing, callback_data=t_go_fishing))
    keyboard = builder.as_markup()
    await message.message.reply(text="Что будем делать?", reply_markup=keyboard)


@dp.callback_query(F.data == t_dig_for_worms)
async def dig_for_worms(message: Message, state: FSMContext):
    await message.message.reply(
        "Тигр помогает Ёжику копать червей. Ёжик облизывается и помогает",
        reply_markup=ReplyKeyboardRemove(),
    )
    state_data = await state.get_data()
    worms = state_data.get('worms', 0)
    worms += 5
    state_data['worms'] = worms
    await state.set_data(state_data)
    await message.message.reply(text="Червей: " + str(worms))
    # kb = [
    #     [KeyboardButton(text=t_go_to_tiger_home)],
    #     [KeyboardButton(text=t_dig_for_worms)],
    #     [KeyboardButton(text=t_go_fishing)],
    # ]
    # keyboard = ReplyKeyboardMarkup(keyboard=kb)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t_go_to_tiger_home, callback_data=t_go_to_tiger_home))
    builder.row(InlineKeyboardButton(text=t_dig_for_worms, callback_data=t_dig_for_worms))
    builder.row(InlineKeyboardButton(text=t_go_fishing, callback_data=t_go_fishing))
    keyboard = builder.as_markup()
    await message.message.reply(text="Что будем делать?", reply_markup=keyboard)


@dp.callback_query(F.data == t_go_fishing)
async def go_fishing(message: Message, state: FSMContext):
    state_data = await state.get_data()
    has_fishing_rods = state_data.get('fishing_rods')
    worms = int(state_data.get('worms', 0))
    if not has_fishing_rods:
        await message.message.reply(
            "Эх, без удочек тяжело ловить... Вот бы где-ниубдь добыть рыболовный инструмент...",
            reply_markup=ReplyKeyboardRemove(),
        )
        # kb = [
        #     [KeyboardButton(text=t_go_to_tiger_home)],
        #     [KeyboardButton(text=t_go_to_hedgehog_home)],
        # ]
        # keyboard = ReplyKeyboardMarkup(keyboard=kb)

        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=t_go_to_tiger_home, callback_data=t_go_to_tiger_home))
        builder.row(InlineKeyboardButton(text=t_go_to_hedgehog_home, callback_data=t_go_to_hedgehog_home))
        keyboard = builder.as_markup()
        await message.message.reply(text="Что будем делать?", reply_markup=keyboard)
    elif worms <= 0:
        await message.message.reply(
            "Что-то подсказывает Тигру, что без червей рыба сегодня ловиться не будет... Вот бы где-ниубдь добыть червей...",
            reply_markup=ReplyKeyboardRemove(),
        )
        # kb = [
        #     [KeyboardButton(text=t_go_to_tiger_home)],
        #     [KeyboardButton(text=t_go_to_hedgehog_home)],
        # ]
        # keyboard = ReplyKeyboardMarkup(keyboard=kb)

        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=t_go_to_tiger_home, callback_data=t_go_to_tiger_home))
        builder.row(InlineKeyboardButton(text=t_go_to_hedgehog_home, callback_data=t_go_to_hedgehog_home))
        keyboard = builder.as_markup()
        await message.message.reply(text="Что будем делать?", reply_markup=keyboard)
    else:
        await message.message.reply(
            "Начинаем рыбалку",
            reply_markup=ReplyKeyboardRemove(),
        )
        await message.message.reply(text="Червей осталось: " + str(worms))
        # kb = [
        #     [KeyboardButton(text=t_go_fish_in_pool)],
        #     [KeyboardButton(text=t_go_fish_in_river)],
        #     [KeyboardButton(text=t_go_fish_in_sea)],
        # ]
        # keyboard = ReplyKeyboardMarkup(keyboard=kb)

        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=t_go_fish_in_pool, callback_data=t_go_fish_in_pool))
        builder.row(InlineKeyboardButton(text=t_go_fish_in_river, callback_data=t_go_fish_in_river))
        builder.row(InlineKeyboardButton(text=t_go_fish_in_sea, callback_data=t_go_fish_in_sea))
        keyboard = builder.as_markup()
        await message.message.reply(text="Ловить можно где помельче - там легче поймать, но и рыба не такая интересная. Или же ловить там где поглубже - но и рыба там поинтересней", reply_markup=keyboard)


@dp.callback_query(F.data == t_go_fish_in_river)
@dp.callback_query(F.data == t_go_fish_in_sea)
async def go_fishing_further(message: Message, state: FSMContext):
    await message.message.reply(
        text="Пока нет - там сегодня непогода",
    )


@dp.callback_query(F.data == t_go_fish_in_pool)
async def go_fish_in_pool(message: Message, state: FSMContext):
    await message.message.reply(
        "Тут рыба полеге. Моно забрасывать удочку на расстояние от 1 до 5 метров",
        reply_markup=ReplyKeyboardRemove(),
    )

    the_number = random.randint(1, 5)
    await state.update_data(the_number=the_number)

    # kb = [
    #     [KeyboardButton(text=t_go_to_tiger_home)],
    #     [KeyboardButton(text=t_go_to_hedgehog_home)],
    #     [KeyboardButton(text="Ловить")],
    # ]
    # keyboard = ReplyKeyboardMarkup(keyboard=kb)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t_go_to_tiger_home, callback_data=t_go_to_tiger_home))
    builder.row(InlineKeyboardButton(text=t_go_to_hedgehog_home, callback_data=t_go_to_hedgehog_home))
    builder.row(InlineKeyboardButton(text="Ловить", callback_data="Ловить"))
    keyboard = builder.as_markup()
    await message.message.reply(text="На какое расстояние забрасывать удочку?", reply_markup=keyboard)


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
            await message.reply('Клюёт!')
            photo_path = "./imgs/Fish_caught.png"
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        else:
            # не отгадал. дадим подсказку
            if the_number > a_number:
                await message.reply('Ёжик подсказывает, что забрасывать удочку нужно дальше')
            else:
                await message.reply('Ёжик подсказывает, что забрасывать удочку нужно ближе')
    except Exception as e:
        await message.reply('Это не число')

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
