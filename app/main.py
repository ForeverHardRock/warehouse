from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import products, orders
from app.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(products.router)
app.include_router(orders.router)


