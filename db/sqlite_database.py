import json
from aiogram.fsm.context import FSMContext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DB_PATH = 'journey_data_sqlalch.db'

Base = declarative_base()


class Journey(Base):
    __tablename__ = 'journeys'

    chat_id = Column(Integer, primary_key=True)
    journey_data = Column(String)
    user_first_name = Column(String)
    user_full_name = Column(String)


engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_all():
    db = SessionLocal()
    try:
        all_journeys = db.query(Journey).all()
        for journey in all_journeys:
            print(journey)
    finally:
        db.close()


def get_by_filter(chat_id):
    db = SessionLocal()
    try:
        journeys = db.query(Journey).filter(Journey.chat_id == chat_id).all()
        return journeys
    finally:
        db.close()


async def load_journey(chat_id: int):
    record_data = get_by_filter(chat_id)
    if record_data:
        record_data = record_data[0]
        state_data = json.loads(record_data.journey_data)
        return state_data
    else:
        return None


async def upsert(chat_id: int, state: FSMContext = None, first_name=None, full_name=None):
    journey_data_dict = await state.get_data()
    journey_data = json.dumps(journey_data_dict)
    db = SessionLocal()
    try:
        existing = db.query(Journey).filter(Journey.chat_id == chat_id).first()
        if existing:
            # Update existing record
            existing.journey_data = journey_data
            existing.user_first_name = first_name
            existing.user_full_name = full_name
        else:
            # Insert new record
            new_journey = Journey(
                chat_id=chat_id,
                journey_data=journey_data,
                user_first_name=first_name,
                user_full_name=full_name
            )
            db.add(new_journey)
        db.commit()
    finally:
        db.close()


async def save_journey(chat_id: int, state: FSMContext, first_name, full_name):
    await upsert(chat_id, state, first_name, full_name)
    return 'успешно'
