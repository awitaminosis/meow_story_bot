from places.states.base import *

class VisitMouse(LocationCallbackQuery):
    location = 'visit_mouse'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
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
        return F.data == t_visit_mouse
