import asyncio
import random

from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F

from helper.keyboards import *
from db.mongo_database import *


version = '1.8.0'


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

    keyboad_actions = [[KeyboardButton(text="Инвентарь")],
        [KeyboardButton(text="Что нового?")],
    ]

    menu_kb = ReplyKeyboardMarkup(keyboard=keyboad_actions,resize_keyboard=True)

    await bot.send_message(chat_id=chat_id, text="Версия: " + version, reply_markup=menu_kb)

    builder = InlineKeyboardBuilder()
    builder.button(text=t_start_new_story, callback_data=t_start_new_story)
    if await load_journey(chat_id):
        builder.button(text="Загрузить", callback_data="Загрузить")
    keyboard = builder.as_markup()
    await bot.send_message(chat_id=chat_id, text="Начинаем?", reply_markup=keyboard)


@dp.callback_query(F.data == t_start_new_story)
async def start_new_story(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await state.clear()
    await init_new_state(state)
    await bot.send_message(chat_id=chat_id,
        text="Однажды Тигр проснулся на полянке и подумал, а почему бы не пойти на рыбалку",
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
    )

    await state.update_data(location='tiger_home')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_take_the_rods)
async def take_the_rods(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Вот они, любимые инструменты Тигра. Теперь и на рыбалку можно",
    )
    await state.update_data(fishing_rods=True)

    await state.update_data(location='rods_taken')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_go_to_hedgehog_home)
async def go_to_hedgehog_home(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Ёжик встречает Тигра рядом с компостной ямой, в которой он разводит червей. Ёжик тепло приветствует Тигра и намекает, что было бы хорошо помочь ему в выкапывании вкусных червей",
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
    )
    state_data = await state.get_data()
    worms = state_data.get('worms', 0)
    worms += await add_worms(state)
    worms = await maybe_eat_worms(worms, message, bot, message.message.chat.id, state)

    await state.update_data(worms=worms)
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
        )

        await state.update_data(location='fishing_requisites_missing')
        await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
    elif worms <= 0:
        await bot.send_message(chat_id=chat_id,
            text="Что-то подсказывает Тигру, что без червей рыба сегодня ловиться не будет... Вот бы где-ниубдь добыть червей...",
        )

        await state.update_data(location='fishing_requisites_missing')
        await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
    else:
        await bot.send_message(chat_id=chat_id,
            text="Начинаем рыбалку",
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

    state_data = await state.get_data()
    mouse_quest_level = state_data.get('mouse_quest_level', 0)

    # действует ли ограничение?
    if fishing_range == river_range and mouse_quest_level < 1:
        await state.update_data(location='fishing_go_fishing_requisites_ok')
        await bot.send_message(chat_id=chat_id, text="Похоже, что вся речка заросла крапивой. Жжётся, однако. Не добраться...",
                               reply_markup=await get_keyboard(state))
    else:
        await bot.send_message(chat_id=chat_id,
            text="Тут рыба хороша! Аж слюнки текут! Можно забрасывать удочку на расстояние от 1 до " + str(fishing_range) + " метров",
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

    state_data = await state.get_data()
    mouse_quest_level = state_data.get('mouse_quest_level', 0)

    # действует ли ограничение?
    if fishing_range == sea_range and mouse_quest_level < 2:
        await state.update_data(location='fishing_go_fishing_requisites_ok')
        await bot.send_message(chat_id=chat_id, text="На море бушуют волны. Они выбрасывают солёную пену на берег. Весь берег покрыт солью и она щиплет лапки. Не подойти...",
                               reply_markup=await get_keyboard(state))
    else:
        await bot.send_message(chat_id=chat_id,
            text="Тут такая рыба, что аж даже немножко страшно! Нет, не так! Страшно интересно! Вперёд, Ёжик, поймаем её! Можно забрасывать удочку на расстояние от 1 до " + str(fishing_range) + " метров",
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
        await state.update_data(worms=worms)

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
                    await add_fish(state, applicable_fishing_range)

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


@dp.message(F.text == 'Что нового?')
async def show_changelog(message: Message, state: FSMContext):
    chat_id = message.chat.id
    news = ['Ёжик ещё не кушал червей - он может рассказать что-то интересное',
        'Угости Ёжика червяком!',
        'Фыр!',
        'Речка заросла крапивой',
        # 'Море сейчас не доступно',
        'Р-р-р-рыба!',
        'Говорят, в лесу видели Мышку',
        'Мышка опять читает книжки',
        'Какая рыба живёт в речке?',
        'Морская рыба полезна',
    ]
    a_news = random.choice(news)
    await bot.send_message(chat_id=chat_id, text=a_news)


@dp.message(F.text == 'Сохранить')
async def save(message: Message, state: FSMContext):
    chat_id = message.chat.id
    save_ok = await save_journey(chat_id, state)
    await bot.send_message(chat_id=chat_id, text='Мышка говорит, что записала приключение. Вот держи книжку. Если захочешь загрузиться, и вспомнить приключение - просто прочитай его из книжки.')
    await state.update_data(location='t_visit_mouse')
    await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await get_keyboard(state))

@dp.callback_query(F.data == 'Загрузить')
async def load(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    loaded_data = await load_journey(chat_id)
    print(loaded_data)
    if loaded_data:
        await bot.send_message(chat_id=chat_id, text='Тигр читает, что Мышка записала в книжке про приключение. Вроде всё вспомнил')
        await state.set_data(loaded_data)
        await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await get_keyboard(state))
    else:
        await bot.send_message(chat_id=chat_id, text='Ошибка загрузки')


@dp.message(F.text == 'Инвентарь')
async def show_invenotry(message: Message, state: FSMContext):
    chat_id = message.chat.id
    state_data = await state.get_data()
    print('Инвентарь: ',state_data)
    worms = state_data.get('worms', 0)
    pool_fish_pcs = state_data.get('pool_fish_pcs', 0)
    river_fish_pcs = state_data.get('river_fish_pcs', 0)
    sea_fish_pcs = state_data.get('sea_fish_pcs', 0)
    rods_taken = state_data.get('fishing_rods', False)
    showel_taken = state_data.get('showel_taken', False)
    glowing_rod = state_data.get('glowing_rod', False)

    if worms:
        text = f'червей: {worms}'
        await bot.send_message(chat_id=chat_id, text=text)
    if rods_taken:
        text = f'удочки: есть'
        await bot.send_message(chat_id=chat_id, text=text)
    if showel_taken:
        text = f'лопата: есть'
        await bot.send_message(chat_id=chat_id, text=text)
    if pool_fish_pcs:
        text = f'рыбы из лужи (штук): {pool_fish_pcs}'
        await bot.send_message(chat_id=chat_id, text=text)
    if river_fish_pcs:
        text = f'рыбы из речки (штук): {river_fish_pcs}'
        await bot.send_message(chat_id=chat_id, text=text)
    if sea_fish_pcs:
        text = f'рыбы из моря (штук): {sea_fish_pcs}'
        await bot.send_message(chat_id=chat_id, text=text)
    if glowing_rod:
        text = f'Светящаяся удочка: есть'
        await bot.send_message(chat_id=chat_id, text=text)
    if not worms and not rods_taken and not showel_taken and not pool_fish_pcs and not river_fish_pcs and not sea_fish_pcs:
        await bot.send_message(chat_id=chat_id, text='Пока что пусто')



@dp.callback_query(F.data == t_go_to_forest)
async def go_to_forest(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id,
        text="Тигр заходит в лес. Красиво зедсь, и пахнет прелыми листьями, грибами. Тут и там попадаются цветы и лесные ягоды. Кое-где виднеются раскопанные муравейники.",
    )
    state_data = await state.get_data()
    if not state_data.get('showel_taken', False):
        await bot.send_message(chat_id=chat_id,
            text="О! А вот и лопата Ёжика! Да такой лопатой до пары десятков червей можно за раз накопать! И чего её Ёжик тут забыл? Возьму."
        )
        await state.update_data(showel_taken=True)

    await state.update_data(location='forest')
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_feed_hedgehog)
async def feed_hedgehog(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id, text="Ёжик, будешь червяка? Расскажи мне что-нибудь интересно.")
    state_data = await state.get_data()
    print(state_data)
    await feed_hedgehog_level(bot, chat_id, state)
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_mouse_quest)
async def mouse_quest(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    await bot.send_message(chat_id=chat_id, text="Мышка, а что у тебя там в книжках ещё интересного пишут? Научи меня чему-нибудь. ")
    await mouse_quest_levels(bot, chat_id, state)
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


@dp.callback_query(F.data == t_visit_mouse)
async def visit_mouse(message: Message, state: FSMContext):
    chat_id = message.message.chat.id
    state_data = await state.get_data()
    await state.update_data(location='t_visit_mouse')
    mouse_quest_level = state_data.get('mouse_quest_level', 0)

    if mouse_quest_level == 0:
        await bot.send_message(chat_id=chat_id,
           text="Пыхтя и фырча они пробираются через заросли лесной чащи. Потом через кусты крыжовника. Потом через овраги. Потом, уже отчаявшись найти Мышку, решают отдохнуть под кустом барбариса. Там они и встречают Мышку",
        )
    elif mouse_quest_level == 1:
        await bot.send_message(chat_id=chat_id,
            text="У куста барбариса Мышки нет. На земле лежит несколько надгрызанных ягод. И видны следы, уходящие в направлении берёзовой рощицы. Там Мышка собирает опавшую бересту. Она замечает Тигра и Ёжика, и приветственно машет им лапкой",
        )

    photo_path = "./imgs/Mouse.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=chat_id, photo=photo)
    if mouse_quest_level == 0:
        await bot.send_message(chat_id=chat_id, text="Привет, Тигр. Привет, Ёжик.")
    menu_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Инвентарь")],
        [KeyboardButton(text="Сохранить")],
    ], resize_keyboard=True)
    await bot.send_message(chat_id=chat_id, text="Я сейчас гуляю с книжкой - могу записать приключение", reply_markup=menu_kb)
    await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
