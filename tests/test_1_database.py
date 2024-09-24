import pytest
import pytest_asyncio

from sqlalchemy import inspect

from app.settings import settings
from app.models import MyModel
from app.database import engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    assert settings.MODE == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(MyModel.metadata.drop_all)
        await conn.run_sync(MyModel.metadata.create_all)


@pytest.mark.asyncio
async def test_tables_creation():
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda c: inspect(c).get_table_names())

    print("Созданные таблицы:", tables)
    assert len(tables) == 3
