from places.states.base import *


class HedgehogHome(LocationCallbackQuery):
    location = 'hedgehog_home'
    can_reach = [
        ('tiger_home', t_go_to_tiger_home, 'inline', ''),
        ('worms_dig', t_dig_for_worms, 'inline', ''),
        # ('go_fishing', t_go_fishing, 'inline', ''),
        ('feed_hedgehog', t_feed_hedgehog, 'inline', Transitions.can_feed_hedgehog),
        ('enter_forest', t_go_to_forest, 'inline', Transitions.can_go_to_forest),
    ]

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await bot.send_message(chat_id=chat_id,
                                   text="Ёжик машет Тигру и позывает его к компостной яме, в которой он разводит червей.")
            await h_say(bot, chat_id, ["Тигр, поможешь мне с червяками?"])

            await state.update_data(location='hedgehog_home')
            await bot.send_message(chat_id=chat_id, text="Что будем делать?", reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == self.location
