from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.models import MyModel
from app.settings import settings

engine = create_async_engine(settings.DB_URL)
my_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(MyModel.metadata.create_all)
