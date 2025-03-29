from places.states.base import *


class News(LocationMessage):
    location = 'news'

    def __init__(self, controller):
        super().__init__(self.location, controller)

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
                    'Мышка присмотрела новый участок леса для домика',
                    'В пустыню сейчас не попасть',
                    'На болото пока лучше не ходить',
                    'Путь в горы сейчас закрыт',
                    'Возможно пригодится карта',
                    ]
            a_news = random.choice(news)
            await say(bot, chat_id,[a_news])
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.text == 'Что нового?'
