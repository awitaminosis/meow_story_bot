from places.states.base import *

class TigerHomeLocation(LocationCallbackQuery):
    location = 'tiger_home'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await helper.funcs.t_say(bot, chat_id, ["Вот я и дома. Хорошо тут среди множества рыболовных принадлежностей."])

            await state.update_data(location='tiger_home')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_go_to_tiger_home
