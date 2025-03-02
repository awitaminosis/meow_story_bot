from places.states.base import *

class GoFishing(LocationCallbackQuery):
    location = 'go_fishing'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            state_data = await state.get_data()
            has_fishing_rods = state_data.get('fishing_rods')
            worms = int(state_data.get('worms', 0))
            if not has_fishing_rods:
                await t_say(bot, chat_id,
                            ["Эх, без удочек тяжело ловить... Вот бы где-ниубдь добыть рыболовный инструмент..."])

                await state.update_data(location='fishing_requisites_missing')
                await bot.send_message(chat_id=chat_id, text="Что будем делать?",
                                       reply_markup=await self.get_keyboard(state))
            elif worms <= 0:
                await t_say(bot, chat_id, [
                    "Что-то мне подсказывает, что без червей рыба сегодня ловиться не будет... Вот бы где-ниубдь добыть червей..."])

                await state.update_data(location='fishing_requisites_missing')
                await bot.send_message(chat_id=chat_id, text="Что будем делать?",
                                       reply_markup=await self.get_keyboard(state))
            else:
                await bot.send_message(chat_id=chat_id,
                                       text="Начинаем рыбалку",
                                       )
                await bot.send_message(chat_id=chat_id, text="Червей осталось: " + str(worms))

                await state.update_data(location='fishing_go_fishing_requisites_ok')
                await bot.send_message(chat_id=chat_id,
                                       text="Ловить можно где помельче - там легче поймать, но и рыба не такая интересная. Или же ловить там где поглубже - но и рыба там поинтересней",
                                       reply_markup=await self.get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_go_fishing
