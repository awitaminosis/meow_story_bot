import json
from aiogram.fsm.context import FSMContext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select

from kernel.models import Journey
from kernel.models import db_helper


async def get_by_filter(chat_id, session: AsyncSession):
    try:
        stmt = select(Journey).filter(Journey.chat_id == chat_id)
        result = await session.execute(stmt)
        journeys = result.scalars().all()
        return journeys
    except Exception as e:
        print(f"Error: {e}")
        raise


async def load_journey(chat_id: int):
    async with db_helper.session_factory() as session:
        record_data = await get_by_filter(chat_id, session)
        if record_data:
            record_data = record_data[0]
            state_data = json.loads(record_data.journey_data)
            if state_data["visited_places"] == []:
                state_data["visited_places"] = set()
            return state_data
        else:
            return None


async def upsert(
    chat_id: int, state: FSMContext = None, first_name=None, full_name=None
):
    journey_data_dict = await state.get_data()
    if len(journey_data_dict["visited_places"]) == 0:
        journey_data_dict["visited_places"] = list()
    journey_data = json.dumps(journey_data_dict)
    async with db_helper.session_factory() as session:
        try:
            stmt = select(Journey).filter(Journey.chat_id == chat_id)
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            if record:
                # Update existing record
                record.journey_data = journey_data
                record.user_first_name = first_name
                record.user_full_name = full_name
            else:
                # Insert new record
                new_journey = Journey(
                    chat_id=chat_id,
                    journey_data=journey_data,
                    user_first_name=first_name,
                    user_full_name=full_name,
                )
                session.add(new_journey)
            await session.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise


async def save_journey(chat_id: int, state: FSMContext, first_name, full_name):
    await upsert(chat_id, state, first_name, full_name)
    return "успешно"
