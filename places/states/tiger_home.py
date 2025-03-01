from places.states.base import *

class TigerHomeLocation(Location):
    def __init__(self, location, handler_type):
        super().__init__(location, handler_type)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await helper.funcs.t_say(bot, chat_id, ["Вот я и дома. Хорошо тут среди множества рыболовных принадлежностей."])

            await state.update_data(location='tiger_home')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await helper.keyboards.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_go_to_tiger_home
