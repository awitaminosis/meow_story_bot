from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Journey(Base):
    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    journey_data: Mapped[str] = mapped_column(String)
    user_first_name: Mapped[str] = mapped_column(String)
    user_full_name: Mapped[str] = mapped_column(String)
