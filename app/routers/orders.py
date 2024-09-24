from typing import Annotated
from fastapi import APIRouter, Depends
from app import schemas
from app.repository import OrderRepository

router = APIRouter(
    prefix='/orders',
    tags=["Заказы"]
)


@router.post("")
async def create_order(order: Annotated[schemas.OrderCreate, Depends()]) -> schemas.Order:
    return await OrderRepository.create_order(order)


@router.get("")
async def get_orders() -> list:
    return await OrderRepository.get_orders()


@router.get("/{order_id}")
async def get_order_info(order_id: int) -> schemas.Order:
    return await OrderRepository.get_order_info(order_id)


@router.patch("/{order_id}/status")
async def update_order(order_id: int, status: Annotated[schemas.OrderStatusUpdate, Depends()]) -> dict:
    return await OrderRepository.update_order_status(order_id, status)
