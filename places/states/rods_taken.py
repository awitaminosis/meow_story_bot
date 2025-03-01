from places.states.base import *

class RodsTaken(Location):
    def __init__(self, location, handler_type):
        super().__init__(location, handler_type)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await t_say(bot, chat_id, ["Вот они, мои любимые инструменты. Теперь и на рыбалку можно!"])

            await state.update_data(fishing_rods=True)
            await state.update_data(location='rods_taken')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_take_the_rods
