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

import helper.funcs
from helper.funcs import *
from helper.texts import *
from helper.constants import *
from helper.keyboards import *


version = '1.3.1'


bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
bot_router = Router()


class Story(StatesGroup):
    guesses = State()
    finish = State()


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Это небольшое приключение из жизни Тигра и Ёжика.")
    await bot.send_message(chat_id=chat_id, text="Остальные приключения можно увидеть https://awitaminosis.github.io/pi_meow_fir/")
    await bot.send_message(chat_id=chat_id, text="Версия: " + version)
    await message.reply(text="Подсказка: теперь обновления приходят в таком виде - в виде ответа")

    builder = InlineKeyboardBuilder()
    builder.button(text=t_start_new_story, callback_data=t_start_new_story)
    keyboard = builder.as_markup()
    await bot.send_message(chat_id=chat_id, text="Начинаем?", reply_markup=keyboard)


@dp.callback_query(F.data == t_start_new_story)
async def start_new_story(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await state.clear()
    await bot.send_message(chat_id=chat_id,
        text="Однажды Тигр проснулся на полянке и подумал, а почему бы не пойти на рыбалку",
        reply_markup=ReplyKeyboardRemove(),
    )
    photo_path = "./imgs/Tiger.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=chat_id, photo=photo)

    await state.update_data(location='clearing')
    await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_go_to_tiger_home)
async def go_to_tiger_home(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Тигр пришёл в свой дом. Хорошо тут среди множества рыболовных принадлежностей",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.update_data(location='tiger_home')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_take_the_rods)
async def take_the_rods(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Вот они, любимые инструменты Тигра. Теперь и на рыбалку можно",
        reply_markup=ReplyKeyboardRemove(),
    )
    state_data = await state.get_data()
    state_data['fishing_rods'] = True
    await state.set_data(state_data)
    helper.funcs.g_rods_taken = True

    await state.update_data(location='rods_taken')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_go_to_hedgehog_home)
async def go_to_hedgehog_home(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Ёжик встречает Тигра рядом с компостной ямой, в которой он разводит червей. Ёжик тепло приветствует Тигра и намекает, что было бы хорошо помочь ему в выкапывании вкусных червей",
        reply_markup=ReplyKeyboardRemove(),
    )
    photo_path = "./imgs/Hedgehog.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=message.message.chat.id, photo=photo)

    await state.update_data(location='hedgehog_home')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_dig_for_worms)
async def dig_for_worms(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Тигр помогает Ёжику копать червей. Ёжик облизывается и помогает",
        reply_markup=ReplyKeyboardRemove(),
    )
    state_data = await state.get_data()
    worms = state_data.get('worms', 0)
    worms += await add_worms(state)
    worms = await maybe_eat_worms(worms, message, bot, message.message.chat.id, state)
    state_data['worms'] = worms
    await state.set_data(state_data)
    await bot.send_message(chat_id=chat_id, text="Червей: " + str(worms))

    await state.update_data(location='worms_dig')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_go_fishing)
async def go_fishing(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    state_data = await state.get_data()
    has_fishing_rods = state_data.get('fishing_rods')
    worms = int(state_data.get('worms', 0))
    if not has_fishing_rods:
        await bot.send_message(chat_id=chat_id,
            text="Эх, без удочек тяжело ловить... Вот бы где-ниубдь добыть рыболовный инструмент...",
            reply_markup=ReplyKeyboardRemove(),
        )

        await state.update_data(location='fishing_requisites_missing')
        await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
    elif worms <= 0:
        await bot.send_message(chat_id=chat_id,
            text="Что-то подсказывает Тигру, что без червей рыба сегодня ловиться не будет... Вот бы где-ниубдь добыть червей...",
            reply_markup=ReplyKeyboardRemove(),
        )

        await state.update_data(location='fishing_requisites_missing')
        await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
    else:
        await bot.send_message(chat_id=chat_id,
            text="Начинаем рыбалку",
            reply_markup=ReplyKeyboardRemove(),
        )
        await bot.send_message(chat_id=chat_id, text="Червей осталось: " + str(worms))

        await state.update_data(location='fishing_go_fishing_requisites_ok')
        await bot.send_message(chat_id=chat_id, text="Ловить можно где помельче - там легче поймать, но и рыба не такая интересная. Или же ловить там где поглубже - но и рыба там поинтересней", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_go_fish_in_pool)
async def go_fish_in_pool(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    global fishing_range
    fishing_range = pool_range
    await state.update_data(fishing_range=fishing_range)
    the_number = random.randint(1, fishing_range)
    await state.update_data(the_number=the_number)

    await bot.send_message(chat_id=chat_id,
        text="Тут рыба полеге. Можно забрасывать удочку на расстояние от 1 до " + str(fishing_range) + " метров",
        reply_markup=ReplyKeyboardRemove(),
    )

    await bot.send_message(chat_id=chat_id, text="Напиши цифру, на сколько метров от берега забрасывать удочку?")


@dp.callback_query(F.data == t_go_fish_in_river)
async def go_fish_in_river(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    global fishing_range
    fishing_range = river_range
    await state.update_data(fishing_range=fishing_range)
    the_number = random.randint(1, fishing_range)
    await state.update_data(the_number=the_number)

    await bot.send_message(chat_id=chat_id,
        text="Тут рыба хороша! Аж слюнки текут! Можно забрасывать удочку на расстояние от 1 до " + str(fishing_range) + " метров",
        reply_markup=ReplyKeyboardRemove(),
    )

    await bot.send_message(chat_id=chat_id, text="Напиши цифру, на сколько метров от берега забрасывать удочку?")


@dp.callback_query(F.data == t_go_fish_in_sea)
async def go_fish_in_sea(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    global fishing_range
    fishing_range = sea_range
    await state.update_data(fishing_range=fishing_range)
    the_number = random.randint(1, fishing_range)
    await state.update_data(the_number=the_number)

    await bot.send_message(chat_id=chat_id,
        text="Тут такая рыба, что аж даже немножко страшно! Нет, не так! Страшно интересно! Вперёд, Ёжик, поймаем её! Можно забрасывать удочку на расстояние от 1 до " + str(fishing_range) + " метров",
        reply_markup=ReplyKeyboardRemove(),
    )

    await bot.send_message(chat_id=chat_id, text="Напиши цифру, на сколько метров от берега забрасывать удочку?")


@dp.message(F.text.in_([str(x) for x in range(1, 101)]))
async def do_fishing_in_pool(message: Message, state: FSMContext):
    chat_id = message.chat.id
    state_data = await state.get_data()
    applicable_fishing_range = int(state_data.get('fishing_range', 0))
    requested_range = int(message.text)
    if requested_range > 0 and requested_range <= applicable_fishing_range:
        worms = state_data.get('worms', 0)
        worms -= 1
        worms = await maybe_eat_worms(worms, message, bot, message.chat.id, state)
        state_data['worms'] = worms
        await state.set_data(state_data)

        if worms > 0:
            try:
                the_number = int(state_data.get('the_number'))
                a_number = int(message.text)
                if a_number == the_number:
                    await bot.send_message(chat_id=chat_id,text='Клюёт!')
                    if applicable_fishing_range == pool_range:
                        photo_path = "./imgs/Fish_caught.png"
                    if applicable_fishing_range == river_range:
                        photo_path = "./imgs/Fish_caught_big.png"
                    if applicable_fishing_range == sea_range:
                        photo_path = "./imgs/Fish_caught_bigest.png"
                    photo = FSInputFile(photo_path)
                    await bot.send_photo(chat_id=message.chat.id, photo=photo)

                    await state.update_data(fishing_range=0)

                    await state.update_data(location='fishing_did_fished')
                    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))

                else:
                    # не отгадал. дадим подсказку
                    if the_number > a_number:
                        await bot.send_message(chat_id=chat_id, text='Ёжик подсказывает, что забрасывать удочку нужно дальше')
                    else:
                        await bot.send_message(chat_id=chat_id, text='Ёжик подсказывает, что забрасывать удочку нужно ближе')
            except Exception as e:
                print(e)
                await bot.send_message(chat_id=chat_id, text='Это не число')
        else:
            await state.update_data(location='fishing_worms_ended')
            await bot.send_message(chat_id=chat_id, text="Всё, Тигр, черви закончились. Пойдём отсюда", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_go_to_forest)
async def go_to_forest(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Тигр заходит в лес. Красиво зедсь, и пахнет прелыми листьями, грибами. Тут и там попадаются цветы и лесные ягоды. Кое-где виднеются раскопанные муравейники.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await bot.send_message(chat_id=chat_id,
        text="О! А вот и лопата Ёжика! Да такой лопатой до пары десятков червей можно за раз накопать! И чего её Ёжик тут забыл? Возьму.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.update_data(showel_taken=True)

    await state.update_data(location='forest')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
