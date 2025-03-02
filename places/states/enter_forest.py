from places.states.base import *

class EnterForest(LocationCallbackQuery):
    location = 'enter_forest'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await bot.send_message(chat_id=chat_id,
                                   text="Тигр заходит в лес. Красиво зедсь, и пахнет прелыми листьями, грибами. Тут и там попадаются цветы и лесные ягоды. Кое-где виднеются раскопанные муравейники.",
                                   )
            state_data = await state.get_data()
            if not state_data.get('showel_taken', False):
                await bot.send_message(chat_id=chat_id,
                                       text="О! А вот и лопата Ёжика! Да такой лопатой до пары десятков червей можно за раз накопать! И чего её Ёжик тут забыл? Возьму."
                                       )
                await state.update_data(showel_taken=True)

            await state.update_data(location='forest')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_go_to_forest

