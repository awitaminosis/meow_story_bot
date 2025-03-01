from places.states.base import *

class WormsDig(LocationCallbackQuery):
    location = 'worms_dig'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await bot.send_message(chat_id=chat_id,
                                   text="Тигр помогает Ёжику копать червей. Ёжик облизывается и помогает",
                                   )
            state_data = await state.get_data()
            worms = state_data.get('worms', 0)
            worms += await add_worms(state)
            worms = await maybe_eat_worms(worms, message, bot, message.message.chat.id, state)

            await state.update_data(worms=worms)
            await bot.send_message(chat_id=chat_id, text="Червей: " + str(worms))

            await state.update_data(location='worms_dig')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_dig_for_worms
