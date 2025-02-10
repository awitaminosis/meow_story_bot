import random
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from helper.constants import *


async def add_worms(state: FSMContext):
    state_data = await state.get_data()
    showel = state_data.get('showel_taken', False)
    worms_dig_max = worms_dig_max_pcs_by_showel if showel else worms_dig_max_pcs_by_hand
    return random.randint(1, worms_dig_max)


async def maybe_eat_worms(worms, message: Message, bot, chat_id, state: FSMContext):
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
            'Раз, два, три, четыре, пять - Ёж червей идёт считать!',
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
        is_showel_mentioned = state_data.get('showel_mentioned', False)
        if not is_showel_mentioned:
            await bot.send_message(chat_id=chat_id, text='Кстати, Тигр, а я тут вспомнил... Я недавно лопату забыл в лесу... Лопатой бы копать поудобнее было бы...')
            await bot.send_message(chat_id=chat_id, text='Внимание! Открыта новая локация')
            await state.update_data(showel_mentioned=True)

    return worms

async def feed_hedgehog_level(bot, chat_id, state: FSMContext):
    state_data = await state.get_data()
    hedgehog_hints_level = state_data.get('hedgehog_hints_level', 0)
    worms = state_data.get('worms', 0)
    pool_fish_pcs = state_data.get('pool_fish_pcs', 0)
    if hedgehog_hints_level == 0:
        if worms >= 10:
            photo_path = "./imgs/Hedgehog_worms.png"
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=chat_id, photo=photo)
            await bot.send_message(chat_id=chat_id, text="Чем крупнее водоём, тем рыба вкуснее, но тем сложнее её поймать")
            worms -= 10
            hedgehog_hints_level += 1
            await state.update_data(worms=worms)
            await state.update_data(hedgehog_hints_level=hedgehog_hints_level)
        else:
            await bot.send_message(chat_id=chat_id, text="Ёжик смотрит на червяка. Червяк смотрит на Ежа. Ёжик вздыхает и говорит, что силы слишком не равны. Вот если бы червей было 10 штук...")
    elif hedgehog_hints_level == 1:
        if worms >= 50 and pool_fish_pcs >= 5:
            photo_path = "./imgs/Hedgehog_worms.png"
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=chat_id, photo=photo)
            await bot.send_message(chat_id=chat_id, text="Я недавно видел в лесу Мышку. Тебе стоит сходить к ней - она может научить тебя плезным штукам")
            worms -= 50
            pool_fish_pcs -= 5
            hedgehog_hints_level += 1
            await state.update_data(worms=worms)
            await state.update_data(river_fish_pcs=pool_fish_pcs)
            await state.update_data(hedgehog_hints_level=hedgehog_hints_level)
            await state.update_data(mouse_mentioned=True)
            await bot.send_message(chat_id=chat_id, text='Внимание! В лесу открыта новая локация')
        else:
            await bot.send_message(chat_id=chat_id, text="Тигр, вот если бы червей было штук 50...а Ещё мне нужно 5 рыб из ближайшей лужи - я опарышей хочу развести")
    else:
        photo_path = "./imgs/Hedgehog_worms.png"
        photo = FSInputFile(photo_path)
        await bot.send_photo(chat_id=chat_id, photo=photo)
        await bot.send_message(chat_id=chat_id, text="Нет, Тигр, спасибо. Я пока ещё не дожевал...")


async def mouse_quest_levels(bot, chat_id, state: FSMContext):
    state_data = await state.get_data()
    mouse_quest_level = state_data.get('mouse_quest_level', 0)
    worms = state_data.get('worms', 0)
    river_fish_pcs = state_data.get('river_fish_pcs', 0)
    sea_fish_pcs = state_data.get('sea_fish_pcs', 0)

    photo_path = "./imgs/Mouse.png"
    photo = FSInputFile(photo_path)
    await bot.send_photo(chat_id=chat_id, photo=photo)

    if mouse_quest_level == 0:
        await bot.send_message(chat_id=chat_id, text="Да у меня разные книжки есть, и в них разные истории записаны... Давай подумаем, что тебе интересно...")
        await bot.send_message(chat_id=chat_id, text="Мышка смотрит на удочки Тигра...")
        await bot.send_message(chat_id=chat_id, text="Ну, например... Я знаю, что вдоль речки сейчас много крапивы растёт, а тебе наверное на речку хотелось бы попасть. Вот в этой книжке написано как можно идти через крапиву, чтобы она не жалилась.")
        await bot.send_message(chat_id=chat_id, text="Внимание, рыбалка в речке стала доступна!")
        await bot.send_message(chat_id=chat_id, text="Мышка продолжает что-то рассказывать, но Тигр и Ёжик уже уходт и не слышат подробностей...")
        mouse_quest_level += 1
        await state.update_data(mouse_quest_level=mouse_quest_level)
    elif mouse_quest_level == 1:
        if river_fish_pcs <= 10:
            river_fish_pcs -= 10
            await state.update_data(river_fish_pcs=river_fish_pcs)
            await bot.send_message(chat_id=chat_id, text="Ой. Спасибо. Хм... Кажется это караси. Но ничего, я буду звать их барбусы.")
            await bot.send_message(chat_id=chat_id, text="Кстати, ты знаешь, я тут на днях прочитала ещё одну интересную книжку. Буквально проглотила её от корки до корки.")
            await bot.send_message(chat_id=chat_id, text="О том, что, представляешь, вполне себе можно ходить по углям. И по снегу. Но и для того и для того нужна особая техника - сейчас я тебе покажу её!")
            await bot.send_message(chat_id=chat_id, text="Внимание, рыбалка в море стала доступна!")
            await bot.send_message(chat_id=chat_id, text="Мышка продолжает что-то рассказывать, но Тигр и Ёжик уже уходт и не слышат подробностей...")
            mouse_quest_level += 1
            await state.update_data(mouse_quest_level=mouse_quest_level)
        else:
            await bot.send_message(chat_id=chat_id,
                                   text="Тигр, я сейчас книжку по аквариумистике дочитываю - мне совершенно необходимо 10 барбусов (речные рыбки). Обитают в Амазонке. Но вдруг и в нашей речке тоже...)")
    elif mouse_quest_level == 2:
        if sea_fish_pcs <= 15:
            sea_fish_pcs -= 15
            await state.update_data(river_fish_pcs=sea_fish_pcs)
            await bot.send_message(chat_id=chat_id, text="Так, аккуратно извлекаем фосфор. Осталное не нужно. Тигр, будь так любезен, доешь эти кусочки")
            await bot.send_message(chat_id=chat_id, text="Мышка достаёт из рюкзака какие-то фляжки и другие принадлежности. Что-то рассказывает...")
            await bot.send_message(chat_id=chat_id, text="Тигр не слышит подробностей того, что Мышка рассказывает - он слишком занят")
            await bot.send_message(chat_id=chat_id, text="Ёжик не слышит подробностей того, что Мышка рассказывает - Тигр слишком громко занят рыбой")
            await bot.send_message(chat_id=chat_id, text="Вот, готово! Держи. Теперь у тебя есть светящаяся удочка. Возможно с её помощью даже ночью в лесу сможешь ориентироваться")
            await bot.send_message(chat_id=chat_id, text="Мышка продолжает что-то рассказывать, но Тигр и Ёжик уже уходт и не слышат подробностей...")
            mouse_quest_level += 1
            await state.update_data(mouse_quest_level=mouse_quest_level)

            await state.update_data(glowing_rod=True)
            photo_path = "./imgs/Hedgehog_worms.png"
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=chat_id, photo=photo)
            await bot.send_message(chat_id=chat_id,
                                   text="Тигр, это хорошо, что у нас появилась такая светящаяся штука, я думаю нам она скоро понадобится")

        else:
            await bot.send_message(chat_id=chat_id,
                                   text="Тигр, а вот тут напиисано, что в морской рыбе содержится много фосфора. А вот в той книжке, сразу под пятном от сыра написано, как сделать фосфоресцирующую подсветку. Для этого требуется 15 морских рыб")
    else:
        await bot.send_message(chat_id=chat_id,
                               text="Мышка слишком увлечённо шуршит страницами книги и не слышит обращённые к ней вопросы")

    # elif hedgehog_hints_level == 1:
    #     if worms >= 50 and pool_fish_pcs >= 5:
    #         photo_path = "./imgs/Hedgehog_worms.png"
    #         photo = FSInputFile(photo_path)
    #         await bot.send_photo(chat_id=chat_id, photo=photo)
    #         await bot.send_message(chat_id=chat_id, text="Я недавно видел в лесу Мышку. Тебе стоит сходить к ней - она может научить тебя плезным штукам")
    #         worms -= 50
    #         pool_fish_pcs -= 5
    #         hedgehog_hints_level += 1
    #         await state.update_data(worms=worms)
    #         await state.update_data(river_fish_pcs=pool_fish_pcs)
    #         await state.update_data(hedgehog_hints_level=hedgehog_hints_level)
    #         await state.update_data(mouse_mentioned=True)
    #         await bot.send_message(chat_id=chat_id, text='Внимание! В лесу открыта новая локация')
    #     else:
    #         await bot.send_message(chat_id=chat_id, text="Тигр, вот если бы червей было штук 50...а Ещё мне нужно 5 рыб из ближайшей лужи - я опарышей хочу развести")
    # else:
    #     photo_path = "./imgs/Hedgehog_worms.png"
    #     photo = FSInputFile(photo_path)
    #     await bot.send_photo(chat_id=chat_id, photo=photo)
    #     await bot.send_message(chat_id=chat_id, text="Нет, Тигр, спасибо. Я пока ещё не дожевал...")


async def add_fish(state: FSMContext, applicable_fishing_range):
    state_data = await state.get_data()
    if applicable_fishing_range == pool_range:
        pool_fish_pcs = state_data.get('pool_fish_pcs', 0)
        pool_fish_pcs = int(pool_fish_pcs) + 1
        await state.update_data(pool_fish_pcs=pool_fish_pcs)
    if applicable_fishing_range == river_range:
        river_fish_pcs = state_data.get('river_fish_pcs', 0)
        river_fish_pcs = int(river_fish_pcs) + 1
        await state.update_data(river_fish_pcs=river_fish_pcs)
    if applicable_fishing_range == sea_range:
        sea_fish_pcs = state_data.get('sea_fish_pcs', 0)
        sea_fish_pcs = int(sea_fish_pcs) + 1
        await state.update_data(sea_fish_pcs=sea_fish_pcs)

async def init_new_state(state: FSMContext):
    await state.update_data(location='clearing')
    await state.update_data(worms=0)
    await state.update_data(pool_fish_pcs=0)
    await state.update_data(river_fish_pcs=0)
    await state.update_data(sea_fish_pcs=0)
    await state.update_data(fishing_rods=False)
    await state.update_data(pool_fish_pcs=0)
    await state.update_data(river_fish_pcs=0)
    await state.update_data(sea_fish_pcs=0)
    await state.update_data(showel_mentioned=False)
    await state.update_data(showel_taken=False)
    await state.update_data(hedgehog_hints_level=0)
    await state.update_data(mouse_quest_level=0)
