from places.states.base import *

class HedgehogHome(LocationCallbackQuery):
    location = 'hedgehog_home'
    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await bot.send_message(chat_id=chat_id,
                                   text="Ёжик встречает Тигра рядом с компостной ямой, в которой он разводит червей.")
            await h_say(bot, chat_id, ["Привет, Тигр! Поможешь мне с червяками?"])

            await state.update_data(location='hedgehog_home')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_go_to_hedgehog_home
