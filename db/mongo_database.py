from pymongo import MongoClient
from aiogram.fsm.context import FSMContext
from decouple import config
import json


MONGO_USER = config('MONGO_USER')
MONGO_USER_PASS = config('MONGO_USER_PASS')
MONGO_HOST = config('MONGO_HOST')
MONGO_EXTRA_SETTINGS = config('MONGO_EXTRA_SETTINGS')
MONGO_DB = config('MONGO_DB')
MONGO_COLLECTION = config('MONGO_COLLECTION')


connection_str = f'mongodb+srv://{MONGO_USER}:{MONGO_USER_PASS}@{MONGO_HOST}/{MONGO_EXTRA_SETTINGS}'

client = MongoClient(connection_str)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


def get_all():
    all_documents = collection.find()
    for document in all_documents:
        print(document)


def get_by_filter(chat_id):
    filter_criteria = {'chat_id': chat_id}
    documents = collection.find(filter_criteria)
    return list(documents)


async def load_journey(chat_id: int):
    record_data = get_by_filter(chat_id)
    if record_data:
        record_data = record_data[0]
        state_data = json.loads(record_data.get('journey_data'))
        return state_data
    else:
        return None


async def upsert(chat_id: int, state: FSMContext = None):
    journey_data = await state.get_data()
    journey_data = json.dumps(journey_data)
    record = get_by_filter(chat_id)
    print(record)
    if record is not None and len(record):
        filter_query = {'chat_id': chat_id}
        update_query = {'$set': {'journey_data': journey_data}}
        result = collection.update_one(filter_query, update_query)
    else:
        new_entry = {
            'chat_id': chat_id,
            'journey_data': journey_data
        }
        result = collection.insert_one(new_entry)
    return result


async def save_journey(chat_id: int, state: FSMContext):
    await upsert(chat_id, state)
    return 'успешно'
