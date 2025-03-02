from places.states.base import *

class MouseGiveQuest(LocationCallbackQuery):
    location = 'mouse_give_quest'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await t_say(bot, chat_id,
                        ["Мышка, а что у тебя там в книжках ещё интересного пишут? Научи меня чему-нибудь."])

            await mouse_quest_levels(bot, chat_id, state)
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_mouse_quest
