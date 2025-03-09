from places.states.base import *


class TigerHomeLocation(LocationCallbackQuery):
    location = 'tiger_home'
    can_reach = [
        ('hedgehog_home', t_go_to_hedgehog_home, 'inline', ''),
        ('go_fishing', t_go_fishing, 'inline', ''),
        ('take_the_rods', t_take_the_rods, 'inline', ''),
        # ('enter_forest', t_go_to_forest, 'inline', Transitions.can_go_to_forest),
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await helper.funcs.t_say(bot, chat_id, ["Вот я и дома. Хорошо тут среди множества рыболовных принадлежностей."])

            await state.update_data(location='tiger_home')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == self.location
