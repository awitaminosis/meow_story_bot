from sqlalchemy import create_engine, Column, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Journey(Base):
    __tablename__ = 'journey'

    id = Column(Integer, primary_key=True)
    state_json = Column(JSON, nullable=True)
    chat_id = Column(Integer, nullable=False, unique=True)
