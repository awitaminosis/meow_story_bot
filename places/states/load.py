from places.states.base import *

class Load(Location):
    def __init__(self, location, handler_type):
        super().__init__(location, handler_type)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            loaded_data = await load_journey(chat_id)
            print(loaded_data)
            if loaded_data:
                await bot.send_message(chat_id=chat_id,
                                       text='Тигр читает, что Мышка записала в книжке про приключение. Вроде всё вспомнил')
                await state.set_data(loaded_data)
                await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await get_keyboard(state))
            else:
                await bot.send_message(chat_id=chat_id, text='Ошибка загрузки')
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == 'Загрузить'
