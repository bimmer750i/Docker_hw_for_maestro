from models import Click
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base
from config import settings

class Database:
    def __init__(self):
        self.__URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"\
                     f"{settings.DB_HOST}:5432/{settings.POSTGRES_DB}"
        self.__engine = create_async_engine(self.__URL)
        self.__asf = async_sessionmaker(self.__engine, expire_on_commit=False)

    async def init_db(self):
        async with self.__engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def __get_first_click(self) -> Click|None :
        async with self.__asf() as session:
            click = await session.execute(select(Click).where(Click.id == 1))
            return click.scalar_one_or_none()

    async def __fill_if_empty(self) -> Click:
        async with self.__asf() as session:
            # Проверка ДБ на пустоту, если не пустая - возвращаем результат
            click = await self.__get_first_click()
            if click is None:
                first_click = Click(counter=0)
                session.add(first_click)
                await session.commit()
                return await self.__get_first_click()
            else:
                return click

    async def __set_clicks(self, clicks: int):
        async with self.__asf() as session:
            stmt_update = update(Click).where(Click.id == 1).values(counter=clicks)
            await session.execute(stmt_update)
            await session.commit()

    async def increment_and_get_clicks(self):
        async with self.__asf():
            # Получаем число и/или заполняем БД
            click = await self.__fill_if_empty()
            result = click.counter
             # Добавляем клики
            await self.__set_clicks(result+1)
            return result

    async def reset_and_get_clicks(self):
        async with self.__asf() as session:
            # Заполняем БД, если пустая
            await self.__fill_if_empty()
            # Сбрасываем клики
            await self.__set_clicks(0)
            return {"Reset to zero"}


    async def dispose(self):
        await self.__engine.dispose()




