from places.states.base import *


class VisitMouse(LocationCallbackQuery):
    location = 'visit_mouse'
    can_reach = [
        # ('tiger_home', t_go_to_tiger_home, 'inline', '', {}),
        ('hedgehog_home', t_go_to_hedgehog_home, 'inline', '', {}),
        ('go_fishing', t_go_fishing, 'inline', '', {}),
        ('feed_hedgehog', t_feed_hedgehog, 'inline', Transitions.can_feed_hedgehog, {}),
        ('mouse_give_quest', t_mouse_quest, 'inline', Transitions.mouse_not_missing, {}),
        ('night_forest', t_night_forest, 'inline', Transitions.mouse_is_missing, {}),
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            state_data = await state.get_data()
            await state.update_data(location='t_visit_mouse')
            mouse_quest_level = state_data.get('mouse_quest_level', 0)
            mouse_owl_story_stage = state_data.get('mouse_owl_story_stage', 0)

            if mouse_quest_level == 0:
                await say(bot,chat_id,["Пыхтя и фырча они пробираются через заросли лесной чащи. Потом через кусты крыжовника. Потом через овраги. Потом, уже отчаявшись найти Мышку, решают отдохнуть под кустом барбариса. Там они и встречают Мышку"])
            elif mouse_quest_level == 1:
                await say(bot,chat_id,["У куста барбариса Мышки нет. На земле лежит несколько надгрызанных ягод. И видны следы, уходящие в направлении берёзовой рощицы. Там Мышка собирает опавшую бересту. Она замечает Тигра и Ёжика, и приветственно машет им лапкой"])
            elif mouse_quest_level == 2:
                await say(bot,chat_id,["Тигр и Ёжик при входе в лес слышат какие-то звуки лёгких ударов. Они идут на звук. Оказывается в ближайшем ельнике Мышка чеканит мячик ракеткой"])
            elif mouse_quest_level == 3:
                if mouse_owl_story_stage != 4:
                    await say(bot,chat_id,["Тигр и Ёжик обшаривают всю полянку, кусты барбариса, крыжовника, берёзовый бурелом, овраг, и даже ведро с червями. Мышки нигде не видно."])
                    await h_say(bot, chat_id, ['Эх, жаль мы не догадались следы сразу посмотреть, а сейчас уже всё затоптано...', 'Да и вечереет уже и становится плохо видно...'])
                    await t_say(bot, chat_id, ['Ёжик, что-то я волнуюсь за Мышку. Думаю, что нам надо бы её найти, мало ли чего случилось. Вот например, я помню, что в прошлый раз Мышка в теннис играла. И, смотри, ракетку не убрала, а в ёлку закинула - не похоже это на неё.'])
                    await h_say(bot, chat_id, ['Я тоже так считаю. Но, думаю, что в ночной лес идти надо подготовленным. Это очень удачно, что у тебя есть светящаяся удочка. А чтобы нам самим не заблудиться, я буду отмечать дорогу с помощью червяков. Пойдём?'])
                else:
                    await say(bot, chat_id, ["Рядом с тем кустом, куда была заброшена ракетка, стоит Мышка и чеканит мячик, который зачем-то привязан к полуободранной ёлке"])
                    await m_say(bot, chat_id, ["Привет, Тигр. Привет, Ёжик."])
                    await h_say(bot, chat_id, ["Привет, Мышка!"])
                    await t_say(bot, chat_id, ["Мышка, ты тут? Мы пол леса облазили, пока тебя искали. Кажется всё в порядке. Что произошло"])
                    await m_say(bot, chat_id, [
                        "Да, в принципе всё хорошо.",
                        "Сначала я чеканила мячик, и он нечаянно улетел далеко в лес.",
                        "Я догадалась, что Сова зхочет меня подкараулить и будет поджидать у мячика",
                        "Сначала я позвала вас, но видимо вы были далеко и не услышали. Поэтому я стала думать как добыть мячик самостоятельно",
                        'Вспомнился Ёжик. И я решила воспользоваться решением Ёжика',
                    ])
                    await h_say(bot, chat_id, ["Каким решением?"])
                    await m_say(bot, chat_id, [
                        "Да колючками!",
                        "Примотала колючу хвою верёвкой и за мячиком",
                        "Сова меня на самом деле поджидала. Да только колючки мои помогли! Не смогла она меня ухватить!",
                        "Вот я и тут, вновь с мячиком",
                    ])
                    await m_say(bot, chat_id, ["Вот даже книжка есть про это приключение: https://awitaminosis.github.io/pi_meow_fir/#XXI"])
                    mouse_quest_level = 4
                    await state.update_data(mouse_quest_level=mouse_quest_level)
            if mouse_quest_level != 3:
                await m_say(bot, chat_id, ["Привет, Тигр. Привет, Ёжик."])
                menu_kb = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text="Инвентарь")],
                    [KeyboardButton(text="Сохранить")],
                ], resize_keyboard=True)
                await bot.send_message(chat_id=chat_id, text="Я сейчас гуляю с книжкой - могу записать приключение",
                                       reply_markup=menu_kb)

            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == self.location
