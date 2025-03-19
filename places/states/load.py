from places.states.base import *


class Load(LocationCallbackQuery):
    location = 'load'
    can_reach = [
        ('tiger_home', t_go_to_tiger_home, 'inline', '', {}),
        ('hedgehog_home', t_go_to_hedgehog_home, 'inline', '', {}),
        ('go_fishing', t_go_fishing, 'inline', '', {}),
        ('feed_hedgehog', t_feed_hedgehog, 'inline', Transitions.can_feed_hedgehog, {}),
        ('mouse_give_quest', t_mouse_quest, 'inline', '', {}),
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            loaded_data = await load_journey(chat_id)
            print(loaded_data)
            if loaded_data:
                await bot.send_message(chat_id=chat_id,
                                       text='Тигр читает, что Мышка записала в книжке про приключение. Вроде всё вспомнил')
                await state.set_data(loaded_data)
                await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await self.get_keyboard(state))
            else:
                await bot.send_message(chat_id=chat_id, text='Ошибка загрузки')
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == 'Загрузить'
