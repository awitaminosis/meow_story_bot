from places.states.base import *

class GoFishingInRiver(LocationCallbackQuery):
    location = 'go_fishing_in_river'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            global fishing_range
            fishing_range = river_range
            await state.update_data(fishing_range=fishing_range)
            the_number = random.randint(1, fishing_range)
            await state.update_data(the_number=the_number)

            state_data = await state.get_data()
            mouse_quest_level = state_data.get('mouse_quest_level', 0)

            # действует ли ограничение?
            if fishing_range == river_range and mouse_quest_level < 1:
                await state.update_data(location='fishing_go_fishing_requisites_ok')
                await bot.send_message(chat_id=chat_id,
                                       text="Похоже, что вся речка заросла крапивой. Жжётся, однако. Не добраться...",
                                       reply_markup=await self.get_keyboard(state))
            else:
                await bot.send_message(chat_id=chat_id,
                                       text="Тут рыба хороша! Аж слюнки текут! Можно забрасывать удочку на расстояние от 1 до " + str(
                                           fishing_range) + " метров",
                                       )

                await bot.send_message(chat_id=chat_id,
                                       text="Напиши цифру, на сколько метров от берега забрасывать удочку?")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_go_fish_in_river
