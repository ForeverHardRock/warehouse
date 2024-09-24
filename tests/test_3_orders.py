import pytest
import datetime

from fastapi import HTTPException
from contextlib import nullcontext

from app.repository import OrderRepository, ProductRepository
from app import schemas


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "order, expected_exception",
    [
        (schemas.OrderCreate(items=[schemas.OrderItemCreate(product_id=1, quantity=5)]),
         nullcontext()),
        (schemas.OrderCreate(items=[schemas.OrderItemCreate(product_id=999, quantity=5)]),
         pytest.raises(HTTPException)),
        (schemas.OrderCreate(items=[schemas.OrderItemCreate(product_id=1, quantity=999)]),
         pytest.raises(HTTPException)),
    ]
)
async def test_create_order(order, expected_exception):
    with (expected_exception):
        result = await OrderRepository.create_order(order)
        product = await ProductRepository.get_product_info(order.items[0].product_id)
        assert product.quantity == 5
        assert result.items[0].product == product
        assert result.items[0].quantity == order.items[0].quantity
        assert result.items[0].id == 1
        assert result.id == 1
        assert result.status == "in_process"
        assert float(result.total) == 750.0
        assert isinstance(result.created_at, datetime.datetime)


@pytest.mark.asyncio
async def test_get_orders():
    result = await OrderRepository.get_orders()
    assert result == ['1']


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "order_id, expected_exception",
    [
        (1, nullcontext()),
        (999, pytest.raises(HTTPException)),
    ]
)
async def test_get_order_info(order_id, expected_exception):
    with (expected_exception):
        result = await OrderRepository.get_order_info(order_id)
        product = await ProductRepository.get_product_info(result.items[0].id)

        assert result.items[0].product == product
        assert result.items[0].quantity == 5
        assert result.items[0].id == 1
        assert result.id == 1
        assert result.status == "in_process"
        assert float(result.total) == 750.0
        assert isinstance(result.created_at, datetime.datetime)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "order_id, status, expected_exception",
    [
        (1, schemas.OrderStatusUpdate(status='Completed'), nullcontext()),
        (999, schemas.OrderStatusUpdate(status='Completed'), pytest.raises(HTTPException)),
    ]
)
async def test_update_order(order_id, status, expected_exception):
    with (expected_exception):
        result = await OrderRepository.update_order_status(order_id, status)
        assert result == {"result": "Статус у заказа с ID - 1 обновлен на Completed"}
