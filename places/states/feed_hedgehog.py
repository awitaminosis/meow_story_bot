from places.states.base import *

class FeedHedgehog(Location):
    def __init__(self, location, handler_type):
        super().__init__(location, handler_type)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await t_say(bot, chat_id, ["Ёжик, будешь червяка? Расскажи мне что-нибудь интересное."])

            state_data = await state.get_data()
            print(state_data)
            await feed_hedgehog_level(bot, chat_id, state)
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_feed_hedgehog
