from places.states.base import *


class RodsTaken(LocationCallbackQuery):
    location = 'take_the_rods'
    can_reach = [
        ('hedgehog_home', t_go_to_hedgehog_home, 'inline', ''),
        ('go_fishing', t_go_fishing, 'inline', ''),
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await t_say(bot, chat_id, ["Вот они, мои любимые инструменты. Теперь и на рыбалку можно!"])

            await state.update_data(fishing_rods=True)
            await state.update_data(location='rods_taken')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == self.location
