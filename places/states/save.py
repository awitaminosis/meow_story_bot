from places.states.base import *


class Save(LocationMessage):
    location = 'save'
    can_reach = [
        ('tiger_home', t_go_to_tiger_home, 'inline', '', {}),
        ('hedgehog_home', t_go_to_hedgehog_home, 'inline', '', {}),
        ('go_fishing', t_go_fishing, 'inline', '', {}),
        ('feed_hedgehog', t_feed_hedgehog, 'inline', Transitions.can_feed_hedgehog, {}),
        ('mouse_give_quest', t_mouse_quest, 'inline', '', {}),
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.chat.id
            state_data = state.get_data()
            mouse_quest_level = state_data.get('mouse_quest_level',0)
            await save_journey(chat_id, state, message.chat.first_name, message.chat.full_name)
            await say(bot, chat_id, ['Тигр начинает записывать приключение...'])
            if mouse_quest_level != 3:
                await h_say(bot, chat_id, ['Тигр, по-моему "Виличайший рыбак, а также его друг, просто Ёжик" пишется как-то по-другому. Давай лучше Мышка запишет...'])
                await m_say(bot, chat_id, [
                    'Готово, приключение записано. Вот держи книжку. Если захочешь загрузиться, и вспомнить приключение - просто прочитай его из книжки.'])
            else:
                await t_say(bot, chat_id,['Эх, жалко что Мышка не может сейчас записать наши параметры приключения', "Попробую сам...", "Ёжик почти совсем круглый, сколько же в нём червей..?", "Ёжик, а ты зачем записываешь колчество рыбы, которое я не поймал?"])
            await state.update_data(location='t_visit_mouse')
            await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.text == 'Сохранить'
