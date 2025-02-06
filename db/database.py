from sqlalchemy.orm import sessionmaker
from decouple import config
from sqlalchemy import create_engine
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session
import json

from db.models.journey import Journey

db_user = config('DB_USER')
db_user_password = config('DB_USER_PASSWORD')
db_database = config('DB_DATABASE')
DATABASE_URL = f"postgresql://{db_user}:{db_user_password}@localhost:5432/{db_database}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def save_journey(chat_id: int, state: FSMContext):
    db: Session = next(get_db())
    state_data = await state.get_data()

    journey = db.query(Journey).filter(Journey.chat_id == chat_id).first()
    if journey:
        journey.state_json=json.dumps(state_data)
    else:
        journey = Journey(chat_id=chat_id, state_json=json.dumps(state_data))
        db.add(journey)

    db.commit()
    db.refresh(journey)
    return 'успешно'

async def load_journey(chat_id: int):
    with next(get_db()) as db:
        journey = db.query(Journey).filter(Journey.chat_id == chat_id).first()
        if journey:
            state_data = json.loads(journey.state_json)
            return state_data
        else:
            return None
