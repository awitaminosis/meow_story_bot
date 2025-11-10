import sqlite3
import json
from aiogram.fsm.context import FSMContext
from decouple import config

# Database configuration
DB_PATH = 'journey_data.db'

# Connect to SQLite database
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS journeys (
    chat_id INTEGER PRIMARY KEY,
    journey_data TEXT,
    user_first_name TEXT,
    user_full_name TEXT
)
''')
connection.commit()


def get_all():
    cursor.execute("SELECT * FROM journeys")
    all_documents = cursor.fetchall()
    for document in all_documents:
        print(document)


def get_by_filter(chat_id):
    cursor.execute("SELECT * FROM journeys WHERE chat_id = ?", (chat_id,))
    documents = cursor.fetchall()
    return documents


async def load_journey(chat_id: int):
    record_data = get_by_filter(chat_id)
    if record_data:
        record_data = record_data[0]
        state_data = json.loads(record_data[1])  # Assuming journey_data is at index 1
        return state_data
    else:
        return None


async def upsert(chat_id: int, state: FSMContext = None, first_name=None, full_name=None):
    journey_data = await state.get_data()
    journey_data = json.dumps(journey_data)
    record = get_by_filter(chat_id)

    if record:
        # Update existing record
        cursor.execute('''
            UPDATE journeys
            SET journey_data = ?, user_first_name = ?, user_full_name = ?
            WHERE chat_id = ?
        ''', (journey_data, first_name, full_name, chat_id))
    else:
        # Insert new record
        cursor.execute('''
            INSERT INTO journeys (chat_id, journey_data, user_first_name, user_full_name)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, journey_data, first_name, full_name))

    connection.commit()


async def save_journey(chat_id: int, state: FSMContext, first_name, full_name):
    await upsert(chat_id, state, first_name, full_name)
    return 'успешно'


# Close the connection when done
def close_connection():
    connection.close()