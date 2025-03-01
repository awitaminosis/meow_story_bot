from places.states.base import *

class News(LocationMessage):
    location = 'news'

    def __init__(self):
        super().__init__(self.location)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.chat.id
            news = ['Ёжик ещё не кушал червей - он может рассказать что-то интересное',
                    'Угости Ёжика червяком!',
                    'Фыр!',
                    'Речка заросла крапивой',
                    # 'Море сейчас не доступно',
                    'Р-р-р-рыба!',
                    'Говорят, в лесу видели Мышку',
                    'Мышка опять читает книжки',
                    'Какая рыба живёт в речке?',
                    'Морская рыба полезна',
                    ]
            a_news = random.choice(news)
            await bot.send_message(chat_id=chat_id, text=a_news)
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.text == 'Что нового?'
