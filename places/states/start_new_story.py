from places.states.base import *


class StartNewStory(LocationCallbackQuery):
    location = 'clearing'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.message.chat.id
            await state.clear()
            await init_new_state(state)
            await bot.send_message(chat_id=chat_id,
                                   text="Однажды Тигр проснулся на полянке и подумал, а почему бы не пойти на рыбалку",
                                   )
            photo_path = "./imgs/Tiger.png"
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=chat_id, photo=photo)

            await state.update_data(location='clearing')
            await bot.send_message(chat_id=chat_id, text="Куда пойдём?", reply_markup=await get_keyboard(state))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.data == t_start_new_story
