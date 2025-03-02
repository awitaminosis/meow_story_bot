from places.states.base import *

class Save(LocationMessage):
    location = 'save'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.chat.id
            await save_journey(chat_id, state, message.chat.first_name, message.chat.full_name)
            await m_say(bot, chat_id, [
                'Готово, приключение записано. Вот держи книжку. Если захочешь загрузиться, и вспомнить приключение - просто прочитай его из книжки.'])
            await state.update_data(location='t_visit_mouse')
            await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.text == 'Сохранить'
