from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Click(Base):
    __tablename__ = "clicks"
    id: Mapped[int] = mapped_column(primary_key=True)
    counter: Mapped[int]

    def __init__(self, counter=1):
        self.counter = counter