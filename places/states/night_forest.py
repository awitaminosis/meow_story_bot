import random

from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

from helper.app import bot
from helper.coords import Coords
from helper.funcs import h_say, hw_say, say, t_say
from helper.texts import NightForestTexts as NF  # noqa: N814
from logger.airtables import logger
from places.states.base import LocationCallbackQuery

# карта https://github.com/awitaminosis/meow_story_bot/blob/main/docs/map.png


class NightForest(LocationCallbackQuery):
    MAP_URL = "https://awitaminosis.github.io/meow_story_bot/night_forest_map.html"
    location = "night_forest"

    WORMS_MAX_BREADCRUMBS = 20

    def __init__(self, controller):
        self.can_reach = [
            (
                "night_forest",
                "пойти на север",
                "inline",
                "",
                {"coords": (Coords.NIGHT_FOREST_EXIT_X, Coords.NIGHT_FOREST_EXIT_Y)},
            ),
            ("night_forest", "осмотреться", "inline", "", {"action": "lookup"}),
        ]
        self.x = Coords.NIGHT_FOREST_START_X
        self.y = Coords.NIGHT_FOREST_START_Y
        self.previous_coords = None
        self.map = {}
        # обычное перемещение
        self.step_phrases = [
            "В лесу темно",
            "Эх, поскорее бы Мышку найти",
            "Что это хрустнуло!? А, ничего страшного, это прсто Ёжик хрустит червяками...",
            "Мышка, ты где!?",
        ]

        super().__init__(self.location, controller)
        self.construct_map()

    async def construct_map_url(self, state: FSMContext):
        url = f"{self.MAP_URL}?x={self.x}&y={self.y}"
        state_data = await state.get_data()
        visited_places = state_data.get("visited_places", set())
        visited_str = str(visited_places).replace("{", "").replace("}", "")
        url += f"&visited={visited_str}"
        url = url.replace(" ", "%20")
        print(url)
        return url

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            is_lookup = "--" in message.data

            if "__" in message.data:
                x, y = message.data.split("__")[1].split(",")
            else:
                x = self.x
                y = self.y
                if not is_lookup:
                    await h_say(
                        bot,
                        chat_id,
                        [
                            "Тигр, я буду помечать дорогу червяками, чтобы мы смогли найти обратный путь. Чтобы тебя не отвлекать лишний раз - я буду делать это молча - если нужно будет - загляни в инвентарь",
                            'Да и поговорка такая была - "Когда я помечаю дорогу червяками - я глух и нем"',
                        ],
                    )

            refuse = await self.update_reachable_coords(x, y, state, chat_id, is_lookup)
            if refuse:
                await say(bot, chat_id, [refuse])
            else:
                state_data = await state.get_data()
                visited_places = state_data.get("visited_places", set())
                visited_places.add(f"{self.x},{self.y}")
                await state.update_data(visited_places=visited_places)

                if is_lookup:
                    lookup = await self.lookup(x, y, state, bot, chat_id)
                    await t_say(bot, chat_id, [lookup])

                await h_say(
                    bot,
                    chat_id,
                    [
                        f"Тигр, если тебе интересно, то по моим подсчётам мы сдвинулись на восток на {x} и на север на {y}"
                    ],
                )
                map_url = await self.construct_map_url(state)
                menu_kb = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="Инвентарь")],
                        [
                            KeyboardButton(
                                text="Посмотреть карту", web_app=WebAppInfo(url=map_url)
                            )
                        ],
                    ],
                    resize_keyboard=True,
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text="И я заодно карту стараюсь вести...",
                    reply_markup=menu_kb,
                )
                await say(bot, chat_id, [random.choice(self.step_phrases)])

            await bot.send_message(
                chat_id=chat_id,
                text="Что будем делать?",
                reply_markup=await self.get_keyboard(state),
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self, callback_query):
        return self.location in callback_query.data

    async def update_reachable_coords(self, x, y, state, chat_id, is_lookup):
        new_x = int(x)
        new_y = int(y)
        refuse = self.map[f"{new_x},{new_y}"].get("refuse", None)
        if not refuse:
            refuse = await self.is_not_enough_light(new_x, new_y, state)
        if not refuse:
            self.x = new_x
            self.y = new_y
            self.previous_coords = (self.x, self.y)
            if Coords.is_night_forest_start(self.x, self.y):
                # вход в лес - можно только вверх
                self.can_reach = [
                    (
                        "night_forest",
                        "пойти на север",
                        "inline",
                        "",
                        {"coords": (self.x, str(self.y + 1))},
                    ),
                    ("visit_mouse", "назад из тёмного леса", "inline", "", {}),
                ]
            else:
                state_data = await state.get_data()
                worms = int(state_data.get("worms"))
                if not is_lookup:
                    worms = worms - random.randint(1, self.WORMS_MAX_BREADCRUMBS)
                if worms > 0:
                    if Coords.is_cave_mushrooms(x, y):
                        # из пещеры прямого хода на болото нет
                        self.can_reach = [
                            (
                                "night_forest",
                                "пойти на север",
                                "inline",
                                "",
                                {"coords": (self.x, str(self.y + 1))},
                            ),
                            (
                                "night_forest",
                                "пойти на юг",
                                "inline",
                                "",
                                {"coords": (self.x, str(self.y - 1))},
                            ),
                            (
                                "night_forest",
                                "пойти на восток",
                                "inline",
                                "",
                                {"coords": (str(self.x + 1), self.y)},
                            ),
                            (
                                "night_forest",
                                "осмотреться",
                                "inline",
                                "",
                                {"action": "lookup"},
                            ),
                        ]
                    else:
                        self.can_reach = [
                            (
                                "night_forest",
                                "пойти на север",
                                "inline",
                                "",
                                {"coords": (self.x, str(self.y + 1))},
                            ),
                            (
                                "night_forest",
                                "пойти на юг",
                                "inline",
                                "",
                                {"coords": (self.x, str(self.y - 1))},
                            ),
                            (
                                "night_forest",
                                "пойти на запад",
                                "inline",
                                "",
                                {"coords": (str(self.x - 1), self.y)},
                            ),
                            (
                                "night_forest",
                                "пойти на восток",
                                "inline",
                                "",
                                {"coords": (str(self.x + 1), self.y)},
                            ),
                            (
                                "night_forest",
                                "осмотреться",
                                "inline",
                                "",
                                {"action": "lookup"},
                            ),
                        ]
                    # Ёжик, а почему ты червей расходуешь всегда, независимо от того, были мы тут или нет?
                else:
                    worms = 0
                    await hw_say(
                        bot,
                        chat_id,
                        [
                            "Тигр, прости, я больше не могу отслеживать дорогу. Закончились черви, которыми я помечал тропинку. Мы сейчас заблудимся в ночном лесу! Я вывожу нас ко входу, пока не поздно"
                        ],
                    )
                    self.can_reach = [
                        ("visit_mouse", "назад из тёмного леса", "inline", "", {}),
                    ]
                    self.x = Coords.NIGHT_FOREST_START_X
                    self.y = Coords.NIGHT_FOREST_START_Y
                    return "Нам нужно подготовиться получше"
                await state.update_data(worms=worms)
        else:
            self.x, self.y = self.previous_coords

        return refuse

    async def lookup(self, x, y, state, bot, chat_id):
        state_data = await state.get_data()
        glowing_mushroom = state_data.get("glowing_mushroom")
        key = "light" if glowing_mushroom else "dark"
        if Coords.is_cave_mushrooms(x, y) and not glowing_mushroom:
            await state.update_data(glowing_mushroom=True)
            await h_say(
                bot,
                chat_id,
                [
                    "Тигр, осторожно! Давай лучше я понесу этот гриб - он может быть червивым. Зато нам теперь виднее будет!"
                ],
            )
        if Coords.is_ball(x, y):
            # мячик
            state_data = await state.get_data()
            mouse_owl_story_stage = state_data.get("mouse_owl_story_stage", 0)
            if mouse_owl_story_stage == 0:
                self.map["6,9"] = {
                    "refuse": "",
                    "dark": "",
                    "light": "Мышки тут нет. Но на пеньке лежит мячик, как буд-то Мышкин.",
                }
                await t_say(
                    bot,
                    chat_id,
                    [
                        "Ёжик, не уверен, может мне почудилось, но мне всё казалось, что откуда-то с дерева за мячиком пристально наблюдают большие глаза"
                    ],
                )
                mouse_owl_story_stage = 1
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)
            if mouse_owl_story_stage == 2:  # noqa: PLR2004
                self.map["6,9"] = {
                    "refuse": "",
                    "dark": "",
                    "light": "Мячик исчез. Рядом с пеньком отчего-то валяется куча хвои и несколько больших перьев, обрывки верёвки",
                }
                await t_say(bot, chat_id, ["Что бы это всё могло значить?"])
                mouse_owl_story_stage = 3
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)
        if Coords.is_owl(x, y):
            # Сова
            state_data = await state.get_data()
            mouse_owl_story_stage = state_data.get("mouse_owl_story_stage", 0)
            if mouse_owl_story_stage == 0:
                self.map["10,9"] = {
                    "refuse": "",
                    "dark": "",
                    "light": "На ветке, рядом с большим дуплом, сидит Сова",
                }
                await t_say(bot, chat_id, ["Сова, ты Мышку не видела?"])
                await say(
                    bot,
                    chat_id,
                    [
                        "Сова, отрицательно машет головой и хищно добавляет, что Мышку ещё не видела"
                    ],
                )
            if mouse_owl_story_stage == 1:
                self.map["10,9"] = {
                    "refuse": "",
                    "dark": "",
                    "light": "На ветке, рядом с большим дуплом, сейчас никого нет",
                }
                await h_say(bot, chat_id, ["Интересно, куда Сова полетела?"])
                mouse_owl_story_stage = 2
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)
            if mouse_owl_story_stage == 3:  # noqa: PLR2004
                self.map["10,9"] = {
                    "refuse": "",
                    "dark": "",
                    "light": 'Из дупла раздаётся раздражённое, болезненное уханье и причитание. "Вот почему так?", "Колючий монстр", "Забрал мячик", и в том же духе...',
                }
                await t_say(bot, chat_id, ['Ёжик, что это за "Колючи монстр"?'])
                await h_say(
                    bot,
                    chat_id,
                    ["Откуда мне знать, Тигр? Может приснилось чего-то..."],
                )
                mouse_owl_story_stage = 4
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)

        return self.map[f"{x},{y}"].get(key, None)

    def construct_map(self):
        self.map = {
            # start
            "3,2": {
                "refuse": "",
                "dark": "Вход в лес",
                "light": "Вход в лес",
            },
            "6,1": {
                "refuse": "",
                "dark": "Болото. В тусклом свете выглядит неприветливо",
                "light": "При более ярком свете болото выглядит ещё более неприветливо",
            },
            "8,1": {
                "refuse": "",
                "dark": "Тут в пещере растут светящиеся грибы",
                "light": "Не смотря на сорванный гриб, этот уголок пещеры всё ещё сильно освещён",
            },
            "4,5": {
                "refuse": "",
                "dark": "Очень похоже, что это место было выбрано Мышкой длля постройки домика",
                "light": "На земле видны вкопанные палочки - вероятно Мышка уже наметила какие-то габариты будущей постройки. Но обычно Мышка их ещё верёвкой связывала - тут же верёвки не видно",
            },
            "8,5": {
                "refuse": "",
                "dark": "Тут находится здоровенный трухлявый пень",
                "light": "Этот пень очень по вкусу Ёжику. Большой, внутри слышно поскрипывание личинок короедов. Ёжик запомнил это место.",
            },
            "10,1": {
                "refuse": "",
                "dark": "В пещере тут глухая стена",
                "light": "При усиленном свете удочки и грба видно, что стена покрыта трещинами. Трещины пахнут сыростью",
            },
            "10,6": {
                "refuse": "",
                "dark": "Где-то сверху, но вне зоны досигаемости, болтается верёвочная лестница",
                "light": "Сверху, на дереве расположен корабль! С него свешивается вниз свёрнутая трубочкой верёвочна лестница. Но всё равно высоко - не достать",
            },
            "2,9": {
                "refuse": "",
                "dark": "Берег с удобным местом для домика рыбака",
                "light": "А при улучшенном свете это место ещё больше похоже на отличное место для домика рыбака!",
            },
            # зависящее от состояния
            "6,9": {
                "refuse": "",
                "dark": "Мячик",
                "light": "Мячик",
            },
            "10,9": {
                "refuse": "",
                "dark": "Сова",
                "light": "Сова",
            },
        }

        self.construct_map_border_refuse()
        self.construct_map_blocked_refuse()
        self.construct_map_location_closed_yet()
        self.construct_map_passable()

    def construct_map_border_refuse(self):
        for i in range(1, 11):
            self.map[str(f"0,{i}")] = {
                "refuse": NF.border_text,
            }
            self.map[str(f"11,{i}")] = {
                "refuse": NF.border_text,
            }
            self.map[str(f"{i},0")] = {
                "refuse": NF.border_text,
            }
            self.map[str(f"{i},11")] = {
                "refuse": NF.border_text,
            }

    def construct_map_blocked_refuse(self):  # noqa: C901
        blocked_around_entrance = ["2,1", "2,2", "3,1", "4,1", "4,2"]
        blocked_around_swamp = ["7,1", "6,2", "7,2"]
        blocked_around_cave = ["8,2", "10,2"]
        blocked_around_desert = ["1,4"]
        blocked_around_mouse_new_house = ["3,4", "4,4", "5,4", "3,5", "3,6", "4,6"]
        blocked_around_hedgehog_new_house = [
            "7,4",
            "8,4",
            "9,4",
            "7,5",
            "7,6",
            "8,6",
            "9,6",
        ]
        blocked_around_ship_house = ["9,7", "10,7"]
        blocked_around_tiger_new_house = ["1,7", "1,8", "1,9", "1,10", "2,10", "3,10"]
        blocked_around_ball = ["4,8", "5,8", "5,10", "7,8"]
        blocked_around_owl = ["9,10", "10,10", "10,8"]

        for place in blocked_around_entrance:
            self.map[place] = {"refuse": NF.entrance_refusal}
        for place in blocked_around_swamp:
            self.map[place] = {"refuse": NF.swamp_refusal}
        for place in blocked_around_cave:
            self.map[place] = {"refuse": NF.cave_refusal}
        for place in blocked_around_desert:
            self.map[place] = {"refuse": NF.desert_refusal}
        for place in blocked_around_mouse_new_house:
            self.map[place] = {"refuse": NF.mouse_new_house_refusal}
        for place in blocked_around_hedgehog_new_house:
            self.map[place] = {"refuse": NF.hedgehog_new_house_refusal}
        for place in blocked_around_ship_house:
            self.map[place] = {"refuse": NF.ship_refusal}
        for place in blocked_around_tiger_new_house:
            self.map[place] = {"refuse": NF.tiger_new_house_refusal}
        for place in blocked_around_ball:
            self.map[place] = {"refuse": NF.ball_refusal}
        for place in blocked_around_owl:
            self.map[place] = {"refuse": NF.owl_refusal}

    def construct_map_location_closed_yet(self):
        # закрытые локации
        self.map["0,5"][
            "refuse"
        ] = "Дальше начинается пустыня. Пока что там, видимо, пыльная буря - потому что завывает ветер, секут песчинки, и дорога туда сейчас совершенно не видима"
        self.map["6,0"][
            "refuse"
        ] = "Громко квакают лягушки, шуршит болотная трава, раздаётся протяжный крик выпи, как бы говорящий, что на болото ночью идти не надо"
        self.map["8,11"][
            "refuse"
        ] = "Тропка далее поведёт к горам. Но сейчас туда не добраться - путь перегородило огроменное бревно - ни обойти, ни перелезть"

    def construct_map_passable(self):  # noqa: PLR0912, C901
        for i in range(1, 11):
            for j in range(1, 11):
                key = f"{i},{j}"
                if not self.map.get(key):
                    if Coords.is_night_forest_entry(i, j):
                        # рядом со входом в лес
                        passable = NF.get_passable_for_entry()
                    elif Coords.is_swamp(i, j):
                        # рядом со входом на болото
                        passable = NF.get_passable_for_swamp()
                    elif Coords.is_cave_maw(i, j):
                        # рядом со входом в пещеру
                        passable = NF.get_passable_for_cave_maw()
                    elif Coords.is_inside_cave(i, j):
                        # в пещере
                        passable = NF.get_passable_for_inside_cave()
                    elif Coords.is_hedgehog_house(i, j):
                        # пень для Ежа и корабль
                        passable = NF.get_passable_for_hedgehog_house()
                    elif Coords.is_mouse_house(i, j):
                        # рядом с Мышкиным домиком
                        passable = NF.get_passable_for_mouse_house()
                    elif Coords.is_desert(i, j):
                        # у входа в пустыню
                        passable = NF.get_passable_for_desert()
                    elif Coords.is_sea(i, j):
                        # у моря
                        passable = NF.get_passable_for_sea()
                    elif Coords.is_northern_road(i, j):
                        # северная дорога
                        passable = NF.get_passable_for_northern_road()
                    elif Coords.is_ball_vicinity(i, j):
                        # рядом с мячиком
                        passable = NF.get_passable_for_ball_vicinity()
                    elif Coords.is_mountain_spur(i, j):
                        # у отрогов гор
                        passable = NF.get_passable_for_mountain_spur()
                    elif Coords.is_owl_vicinity(i, j):
                        # рядом с Совой
                        passable = NF.get_passable_for_owl_vicinity()
                    else:
                        passable = NF.get_passable_default()

                    self.map[key] = {
                        "refuse": "",
                        "dark": random.choice(passable)[0],
                        "light": random.choice(passable)[1],
                    }

    async def is_not_enough_light(self, new_x, new_y, state):
        state_data = await state.get_data()
        glowing_mushroom = state_data.get("glowing_mushroom")
        has_extra_light = glowing_mushroom
        if has_extra_light:
            # светло - можно всё рассмотреть
            return None
        # недостаточно светло - далеко не уйти

        if Coords.is_dark_line(new_x, new_y):
            return None
        return "Пожалуй одной только удочки для освещения не хватит. Без какого-то дополнительного источника освещения далеко не уйти"
