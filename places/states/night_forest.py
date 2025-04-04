from places.states.base import *
from aiogram.types import WebAppInfo
import random

class NightForest(LocationCallbackQuery):
    MAP_URL = 'https://awitaminosis.github.io/meow_story_bot/night_forest_map.html'
    location = 'night_forest'
    can_reach = [
        ('night_forest', 'пойти на север', 'inline', '', {'coords':(3,3)}),
        ('night_forest', 'осмотреться', 'inline', '', {'action':'lookup'}),
    ]
    x = 3
    y = 2
    previous_coords = None
    map = dict()
    WORMS_MAX_BREADCRUMBS = 20

    # обычное перемещение
    step_phrases = [
        'В лесу темно',
        'Эх, поскорее бы Мышку найти',
        'Что это хрустнуло!? А, ничего страшного, это прсто Ёжик хрустит червяками...',
        'Мышка, ты где!?',
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)
        self.construct_map()

    async def construct_map_url(self, state: FSMContext):
        url = f'{self.MAP_URL}?x={self.x}&y={self.y}'
        state_data = await state.get_data()
        visited_places = state_data.get('visited_places',set())
        visited_str = str(visited_places).replace('{','').replace('}','')
        url += f'&visited={visited_str}'
        url = url.replace(' ','%20')
        print(url)
        return url

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            is_lookup = '--' in message.data

            if '__' in message.data:
                x,y = message.data.split('__')[1].split(',')
            else:
                x = self.x
                y = self.y
                if not is_lookup:
                    await h_say(bot, chat_id, [
                        'Тигр, я буду помечать дорогу червяками, чтобы мы смогли найти обратный путь. Чтобы тебя не отвлекать лишний раз - я буду делать это молча - если нужно будет - загляни в инвентарь',
                        'Да и поговорка такая была - "Когда я помечаю дорогу червяками - я глух и нем"'
                        ])

            refuse = await self.update_reachable_coords(x, y, state, chat_id, is_lookup)
            if refuse:
                await say(bot, chat_id,[refuse])
            else:

                state_data = await state.get_data()
                visited_places = state_data.get('visited_places',set())
                visited_places.add(f'{self.x},{self.y}')
                await state.update_data(visited_places=visited_places)

                if is_lookup:
                    lookup = await self.lookup(x, y, state, bot, chat_id)
                    await t_say(bot, chat_id,[lookup])

                await h_say(bot, chat_id, [f'Тигр, если тебе интересно, то по моим подсчётам мы сдвинулись на восток на {x} и на север на {y}'])
                map_url = await self.construct_map_url(state)
                menu_kb = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text="Инвентарь")],
                    [KeyboardButton(text="Посмотреть карту", web_app=WebAppInfo(url=map_url))],
                ], resize_keyboard=True)
                await bot.send_message(chat_id=chat_id,
                                       text="И я заодно карту стараюсь вести...",
                                       reply_markup=menu_kb)
                await say(bot, chat_id, [random.choice(self.step_phrases)])

            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return self.location in F.data

    async def update_reachable_coords(self, x, y, state, chat_id, is_lookup):
        new_x = int(x)
        new_y = int(y)
        refuse = self.map[f'{new_x},{new_y}'].get('refuse',None)
        if not refuse:
            refuse = await self.is_not_enough_light(new_x, new_y, state)
        if not refuse:
            self.x = new_x
            self.y = new_y
            self.previous_coords = (self.x, self.y)
            if self.x==3 and self.y==2:
                # вход в лес - можно только вверх
                self.can_reach = [
                    ('night_forest', 'пойти на север', 'inline', '', {'coords': (self.x, str(self.y + 1))}),
                    ('visit_mouse', 'назад из тёмного леса', 'inline', '', {}),
                ]
            else:
                state_data = await state.get_data()
                worms = int(state_data.get('worms'))
                if not is_lookup:
                    worms = worms - random.randint(1, self.WORMS_MAX_BREADCRUMBS)
                if worms > 0:
                    if self.x == 8 and self.y == 1:
                        # из пещеры прямого хода на болото нет
                        self.can_reach = [
                            ('night_forest', 'пойти на север', 'inline', '', {'coords': (self.x, str(self.y + 1))}),
                            ('night_forest', 'пойти на юг', 'inline', '', {'coords': (self.x, str(self.y - 1))}),
                            ('night_forest', 'пойти на восток', 'inline', '', {'coords': (str(self.x + 1), self.y)}),
                            ('night_forest', 'осмотреться', 'inline', '', {'action': 'lookup'}),
                        ]
                    else:
                        self.can_reach = [
                            ('night_forest', 'пойти на север', 'inline', '', {'coords': (self.x, str(self.y + 1))}),
                            ('night_forest', 'пойти на юг', 'inline', '', {'coords': (self.x, str(self.y - 1))}),
                            ('night_forest', 'пойти на запад', 'inline', '', {'coords': (str(self.x - 1), self.y)}),
                            ('night_forest', 'пойти на восток', 'inline', '', {'coords': (str(self.x + 1), self.y)}),
                            ('night_forest', 'осмотреться', 'inline', '', {'action': 'lookup'}),
                        ]
                    #Ёжик, а почему ты червей расходуешь всегда, независимо от того, были мы тут или нет?
                else:
                    worms = 0
                    await hw_say(bot, chat_id,['Тигр, прости, я больше не могу отслеживать дорогу. Закончились черви, которыми я помечал тропинку. Мы сейчас заблудимся в ночном лесу! Я вывожу нас ко входу, пока не поздно'])
                    self.can_reach = [
                        ('visit_mouse', 'назад из тёмного леса', 'inline', '', {}),
                    ]
                    self.x = 3
                    self.y = 2
                    return 'Нам нужно подготовиться получше'
                await state.update_data(worms=worms)
        else:
            self.x, self.y = self.previous_coords
            return refuse

    async def lookup(self, x, y, state, bot, chat_id):
        state_data = await state.get_data()
        glowing_mushroom = state_data.get('glowing_mushroom')
        key = 'light' if glowing_mushroom else 'dark'
        if x == 8 and y == 1:
            if not glowing_mushroom:
                await state.update_data(glowing_mushroom=True)
                await h_say(bot, chat_id, ['Тигр, осторожно! Давай лучше я понесу этот гриб - он может быть червивым. Зато нам теперь виднее будет!'])
        if x == 6 and y == 9:
            #мячик
            state_data = await state.get_data()
            mouse_owl_story_stage = state_data.get('mouse_owl_story_stage',0)
            if mouse_owl_story_stage == 0:
                self.map['6,9'] = {
                    'refuse': '',
                    'dark': '',
                    'light': 'Мышки тут нет. Но на пеньке лежит мячик, как буд-то Мышкин.',
                }
                await t_say(bot, chat_id, ['Ёжик, не уверен, может мне почудилось, но мне всё казалось, что откуда-то с дерева за мячиком пристально наблюдают большие глаза'])
                mouse_owl_story_stage = 1
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)
            if mouse_owl_story_stage == 2:
                self.map['6,9'] = {
                    'refuse': '',
                    'dark': '',
                    'light': 'Мячик исчез. Рядом с пеньком отчего-то валяется куча хвои и несколько больших перьев, обрывки верёвки',
                }
                await t_say(bot, chat_id, ['Что бы это всё могло значить?'])
                mouse_owl_story_stage = 3
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)
        if x == 10 and y == 9:
            #Сова
            state_data = await state.get_data()
            mouse_owl_story_stage = state_data.get('mouse_owl_story_stage',0)
            if mouse_owl_story_stage == 0:
                self.map['10,9'] = {
                    'refuse': '',
                    'dark': '',
                    'light': 'На ветке, рядом с большим дуплом, сидит Сова',
                }
                await t_say(bot, chat_id, ['Сова, ты Мышку не видела?'])
                await say(bot, chat_id, ['Сова, отрицательно машет головой и хищно добавляет, что Мышку ещё не видела'])
            if mouse_owl_story_stage == 1:
                self.map['10,9'] = {
                    'refuse': '',
                    'dark': '',
                    'light': 'На ветке, рядом с большим дуплом, сейчас никого нет',
                }
                await h_say(bot, chat_id, ['Интересно, куда Сова полетела?'])
                mouse_owl_story_stage = 2
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)
            if mouse_owl_story_stage == 3:
                self.map['10,9'] = {
                    'refuse': '',
                    'dark': '',
                    'light': 'Из дупла раздаётся раздражённое, болезненное уханье и причитание. "Вот почему так?", "Колючий монстр", "Забрал мячик", и в том же духе...',
                }
                await t_say(bot, chat_id, ['Ёжик, что это за "Колючи монстр"?'])
                await h_say(bot, chat_id, ['Откуда мне знать, Тигр? Может приснилось чего-то...'])
                mouse_owl_story_stage = 4
                await state.update_data(mouse_owl_story_stage=mouse_owl_story_stage)

        return self.map[f'{x},{y}'].get(key, None)

    def construct_map(self):
        self.map = {
            # start
            '3,2': {
                'refuse': '',
                'dark': 'Вход в лес',
                'light': 'Вход в лес',
            },
            '6,1': {
                'refuse': '',
                'dark': 'Болото. В тусклом свете выглядит неприветливо',
                'light': 'При более ярком свете болото выглядит ещё более неприветливо',
            },
            '8,1': {
                'refuse': '',
                'dark': 'Тут в пещере растут светящиеся грибы',
                'light': 'Не смотря на сорванный гриб, этот уголок пещеры всё ещё сильно освещён',
            },
            '4,5': {
                'refuse': '',
                'dark': 'Очень похоже, что это место было выбрано Мышкой длля постройки домика',
                'light': 'На земле видны вкопанные палочки - вероятно Мышка уже наметила какие-то габариты будущей постройки. Но обычно Мышка их ещё верёвкой связывала - тут же верёвки не видно',
            },
            '8,5': {
                'refuse': '',
                'dark': 'Тут находится здоровенный трухлявый пень',
                'light': 'Этот пень очень по вкусу Ёжику. Большой, внутри слышно поскрипывание личинок короедов. Ёжик запомнил это место.',
            },
            '10,1': {
                'refuse': '',
                'dark': 'В пещере тут глухая стена',
                'light': 'При усиленном свете удочки и грба видно, что стена покрыта трещинами. Трещины пахнут сыростью',
            },
            '10,6': {
                'refuse': '',
                'dark': 'Где-то сверху, но вне зоны досигаемости, болтается верёвочная лестница',
                'light': 'Сверху, на дереве расположен корабль! С него свешивается вниз свёрнутая трубочкой верёвочна лестница. Но всё равно высоко - не достать',
            },
            '2,9': {
                'refuse': '',
                'dark': 'Берег с удобным местом для домика рыбака',
                'light': 'А при улучшенном свете это место ещё больше похоже на отличное место для домика рыбака!',
            },
            # зависящее от состояния
            '6,9': {
                'refuse': '',
                'dark': 'Мячик',
                'light': 'Мячик',
            },
            '10,9': {
                'refuse': '',
                'dark': 'Сова',
                'light': 'Сова',
            },
        }

        #impassible
        border_text = 'Нет, что-то подсказывает, что Мышка сейчас туда точно не могла пойти. И мы сейчас туда тоже не пойдём.'
        entrance_refusal = 'Вокруг этой части леса колючие ветки растут слишком густо - лучше не сходить с тропы'
        swamp_refusal = 'Воздух пронизан болотными миазмами. Ночью тут лучше не ходить несмотря на зазывающий звон комаров'
        cave_refusal = 'Хвойные породы деревьев тут с трудом цепляются за обветренные развалы горной породы. Интерено, как они получают нужную воду. Быть может где-то рядом пещера'
        desert_refusal = 'Тут возвышаются наносы барханов из ближайшей пустыни. Днём они обжигающе горячие, а ночью так же обжгающе холодные'
        mouse_new_house_refusal = 'Эти деревья, перемежающиеся кустами и клочками воздеываемых грядок, наверняка пиглянулись Мышке для постройки там её домика. Не будем топтать'
        hedgehog_new_house_refusal = 'В окрестностях этой местности маячит силуэт огромного трухлявого пня. Ёжик заинтересовано фыркает и принюхивается. Тигр, ходи аккуратнее, не распугай личинок и жучков, возможно я туда свой домик перенесу'
        ship_refusal = 'Повсюду раскиданы карты, гербарии, рисунки скрещённых костей и черепа. Карамба, что-то не хочется туда идти'
        tiger_new_house_refusal = 'Вдали слышится шум прибоя, а также плеск волн и рыбы. Пожалуй это удобное место, чтобы тут мог обосноваться Тигр - думает Тигр. Ёжик замечает размышления Тигра о постройке домика у моря и предлагает не отвлекаться'
        ball_refusal = 'Тут повсюду деревья с очень густыми ветками'
        owl_refusal = 'В эти деревья идти совершенно не хочется. Они какие-то неправильные. Даже эхо в них раздаётся какое-то угукающее'

        for i in range(1, 11):
            self.map[str(f'0,{i}')] = {
                'refuse': border_text,
            }
            self.map[str(f'11,{i}')] = {
                'refuse': border_text,
            }
            self.map[str(f'{i},0')] = {
                'refuse': border_text,
            }
            self.map[str(f'{i},11')] = {
                'refuse': border_text,
            }

        blocked_around_entrance = ['2,1', '2,2', '3,1', '4,1', '4,2']
        blocked_around_swamp = ['7,1', '6,2', '7,2']
        blocked_around_cave = ['8,2', '10,2']
        blocked_around_desert = ['1,4']
        blocked_around_mouse_new_house = ['3,4', '4,4', '5,4', '3,5', '3,6', '4,6']
        blocked_around_hedgehog_new_house = ['7,4', '8,4', '9,4', '7,5', '7,6', '8,6', '9,6']
        blocked_around_ship_house = ['9,7', '10,7']
        blocked_around_tiger_new_house = ['1,7', '1,8', '1,9', '1,10', '2,10', '3,10']
        blocked_around_ball = ['4,8', '5,8', '5,10', '7,8']
        blocked_around_owl = ['9,10', '10,10', '10,8']

        for place in blocked_around_entrance:
            self.map[place] = {'refuse': entrance_refusal}
        for place in blocked_around_swamp:
            self.map[place] = {'refuse': swamp_refusal}
        for place in blocked_around_cave:
            self.map[place] = {'refuse': cave_refusal}
        for place in blocked_around_desert:
            self.map[place] = {'refuse': desert_refusal}
        for place in blocked_around_mouse_new_house:
            self.map[place] = {'refuse': mouse_new_house_refusal}
        for place in blocked_around_hedgehog_new_house:
            self.map[place] = {'refuse': hedgehog_new_house_refusal}
        for place in blocked_around_ship_house:
            self.map[place] = {'refuse': ship_refusal}
        for place in blocked_around_tiger_new_house:
            self.map[place] = {'refuse': tiger_new_house_refusal}
        for place in blocked_around_ball:
            self.map[place] = {'refuse': ball_refusal}
        for place in blocked_around_owl:
            self.map[place] = {'refuse': owl_refusal}

        #закрытые локации
        self.map['0,5']['refuse'] = 'Дальше начинается пустыня. Пока что там, видимо, пыльная буря - потому что завывает ветер, секут песчинки, и дорога туда сейчас совершенно не видима'
        self.map['6,0']['refuse'] = 'Громко квакают лягушки, шуршит болотная трава, раздаётся протяжный крик выпи, как бы говорящий, что на болото ночью идти не надо'
        self.map['8,11']['refuse'] = 'Тропка далее поведёт к горам. Но сейчас туда не добраться - путь перегородило огроменное бревно - ни обойти, ни перелезть'

        for i in range(1,11):
            for j in range(1,11):
                key = f'{i},{j}'
                if not self.map.get(key):
                    if i < 4 and j < 3:
                        #рядом со входом в лес
                        passable = [
                            ('В этой части леса деревья густые и тропки труднопроходимы','Хорошо, что Ёжик отмечает дорогу, иначе вернуться к их домикам было бы сложно. Есть в этом какое-то очарование'),
                            ('Тропки тут едва хожены','Из следов на лесной подстилке тут видно только червяков'),
                            ('Отсюда виднеется дорожка, по которой они попали в эту часть леса.','Эты часть леса выглядит симпатичнее. Вероятно тут им всем понравится'),
                            ('Мышки поблизости не видно','Наверняка Мышка где-то далеко'),
                        ]
                    elif i in [5,6] and j < 3:
                        #рядом со входом на болото
                        passable = [
                            ('В воздухе писутствуют болотные миазмы','В воздухе писутствуют болотные миазмы - это потому что рядом болото'),
                            ('Тут туча комаров','Тут туча комаров. Чуть дальше слышны лягушки. Какие-то мелкие болотные птицы'),
                            ('Хлюп!','Если тут и были Мышкины следы, то они бы уже давно затянулись'),
                            ('Под ногами что-о извивается','Ёжик, тут копать нет смысла - Мышки тут нет, тут только мотыль'),
                            ('Вокруг растёт камыш','Стена камыша выглядит очень камышово. А кое-где выглядывает осока'),
                            ('Интересно, тут есть рыба?','Тигр, тут нет смысла светить удочкой в воду - Мышки тут нет, там только рыба'),
                            ('Ой, почва тут не надёжна','По бокам тропы видно много вкусных болотных ягод'),
                            ('Мокро','Мышка ягоды то любит, но тут ягоды выглядят не тронутыми'),
                        ]
                    elif i > 6 and j == 3:
                        #рядом со входом в пещеру
                        passable = [
                            ('Камни, камни, нет камней, опять камни','Кварц, известняк, песчаник, дыра, песчаник, кварц'),
                            ('С одной стороны шумят деревья, с другой стороны не шумят камни','Напротив сплошного древесного массива, массив камня, в котором виднеется дырка'),
                            ('А может это Мышка дыру в песчанике прогрызла?','После тщательного исследования Ёжик утверждает что края пещеры совершенно не прогрызаны'),
                            ('Эхо!','Эхо!!'),
                            ('Есть тут кто-нибудь?','Ёжик, а вот эта пещера поблизости - она не от того, что ты червей копать пытался?'),
                        ]
                    elif i >= 8 and j <= 2:
                        #в пещере
                        passable = [
                            ('Прохладно','Кап-кап-кап. Вроде не видно, а по звуку - где-то должно быть подземное озеро'),
                            ('Это сталагмит?','Нет, это сталактит'),
                            ('Пол тут твёрдый, каменный','На таком полу не могло остаться никаких следов. Вот-вот, знаешь сколько червей требуется, чтобы надёжно пометить дорогу?!'),
                            ('Интересно, но чем глубже в пещеру тем становистя светлее','Тигр, похоже в пещере есть какой-то источник освещения!'),
                            ('В пещере что-то явно светится. Может фонарик Мышки?','Видимо в пещере дотаточная сырость и вообще нужный климат, чтобы там могли расти светящиеся грибы'),
                        ]
                    elif i >= 8 and j in [4,5,6]:
                        #пень для Ежа и корабль
                        passable = [
                            ('Ого, какой огромный силуэт пня видно издалека','Ого, какой огромный пень видно издалека'),
                            ('Отличное место для зимовки. Ёжик, сейчас не время для этого!','Отличное место для зимовки. Ёжик, сейчас не время для этого!'),
                            ('',''),
                        ]
                    elif i in [5,6] and j in [4,5,6]:
                        #рядом с Мышкиным домиком
                        passable = [
                            ('','Это место однозначно приглянулось Мышке'),
                            ('','В кустах лежат инструменты, записки, какие-то заметки - Мышка явно собирается обустраиваться где-то поблизости'),
                            ('','Тут много следов Мышки. Она явно тут много ходила. Пожалуй даже слишком много следов - не разобраться'),
                            ('','Интересно, а на огороде у Мышки компостная яма есть?'),
                            ('','Хм... морковная грядка. А когда идёшь рядом - какое-то эхо снизу гулко раздаётся'),
                            ('','А тут Мышка, вероятно качели когда-то собралась приделать'),
                        ]
                    elif i in [1,2] and j in [4,5,6]:
                        #у входа в пустыню
                        passable = [
                            ('','Следы заметает песком'),
                            ('','С запада дует сильный песчаный суховей'),
                            ('','Хорошо, что сейчас ночь, а то тут столько песка, который намекает из пустыни, что западнее... -  было бы очень горячо'),
                            ('','Деревья тут чахлые, пескоустойчивые'),
                            ('','Ёжик, ты же вроде песчаные замки любил делать...'),
                            ('','Ёжик, а ты червей не потеряешь в этом песке?'),
                            ('','Следов Мышки нет. Да тут вообще следы быстро заметает.'),
                        ]
                    elif i in [2,3] and j >= 7:
                        #у моря
                        passable = [
                            ('','Тут слышен морской, рыбный прибой'),
                            ('','Пожалуй, тут будет хорошее место для домика Тигра'),
                            ('','Интересно, а рыба тут есть?'),
                            ('','Тут снуют крабы'),
                            ('','Ёжик, смотри: "Тут был Тигр". Как где? Да вот - я только что написал'),
                            ('','Сомнительно, что Мышку сюда могло приманить. Тут скорее Тигра приманит'),
                        ]
                    elif i >= 4 and j == 7:
                        #северная дорога
                        passable = [
                            ('','Деревья образуют нечто вроде коридора и тут постоянно дует холодный ветер'),
                            ('','Кажется Мышка тут вполне могла пройти'),
                            ('','Ветер заметает следы. И Мышкиных следов тут как раз не видно. Всё сходится!'),
                            ('','Если тут постоянно дует ветер, то почему на земле постоянно валяются листья?'),
                            ('','Ёжик, а червей не сдует?'),
                            ('','Ветер свистит в снастях Тигровой удочки'),
                            ('','Старнно, деревья тут, в основном, лиственные, а на земле кое-где хвоя валяется'),
                        ]
                    elif i in [4,5,6] and j in [8,9]:
                        #рядом с мячиком
                        passable = [
                            ('','Если приглядеться, то кое-где в кронах деревьев видна дырка'),
                            ('','Местность в окрестностях образует нечто вроде амфитеатра с понижением в центре. Там, недалеко, почти виднеется пенёк'),
                            ('','На земле валяются сбитые ветки'),
                            ('','Очень много следов. Всё затоптано'),
                            ('','Тут что-то катилось. И это был не Ёжик'),
                            ('','Хммм... Перья?'),
                        ]
                    elif i >= 4 and j == 10:
                        #у отрогов гор
                        passable = [
                            ('','Тут проходит старая дорожка у отогов северных гор'),
                            ('','Холодно тут'),
                            ('','Холодно и сырость, в воздухе. Интересно, Мышка могла заинтересоваться этой доржкой - тут всё-таки СЫРо?'),
                            ('','О, а вон снеговичок. А, нет - это просто на Ёжика кухта упала'),
                            ('','Следов Мышки тут не было. Если только не выпал свежий снег'),
                            ('','Идёт снег...'),
                        ]
                    elif i >= 8 and j in [8,9]:
                        #рядом с Совой
                        passable = [
                            ('','На земле валяется множество птичьих перьев'),
                            ('','Мышка сюда вот точно не хотела бы идти'),
                            ('','Откуда-то из ветвей рядом раздаётся хищный угукающий клёкот'),
                            ('','Ёжик, ты же не боишься Совы? Это хорошо. Также хорошо, что и я её не боюсь. Хорошо, что мы Сову не боимся. Но на всякий случай держись рядом со мной'),
                            ('','Эх, а Мышка то Сову боится'),
                            ('','Судя по тому, что видно на земле, где-то рядом обитает хищная Сова'),
                        ]
                    else:
                        passable = [
                            ('пусто','совсем пусто'),
                            ('тут ничего нет','ничего интересного тут не видно'),
                        ]

                    self.map[key] = {
                        'refuse': '',
                        'dark': random.choice(passable)[0],
                        'light': random.choice(passable)[1],
                    }

    async def is_not_enough_light(self, new_x, new_y, state):
        state_data = await state.get_data()
        glowing_mushroom = state_data.get('glowing_mushroom')
        has_extra_light = glowing_mushroom
        if has_extra_light:
            # светло - можно всё рассмотреть
            return None
        else:
            # недостаточно светло - далеко не уйти
            if new_y <= 3 or (new_y <= 6 and new_x >= 7):
                return None
            else:
                return 'Пожалуй одной только удочки для освещения не хватит. Без какого-то дополнительного источника освещения далеко не уйти'
