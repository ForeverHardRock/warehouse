import pytest
from fastapi import HTTPException
from contextlib import nullcontext

from app.repository import ProductRepository
from app import schemas

test_product = {
    "name": "Тестовый продукт 1",
    "description": "Тестовое описание 1",
    "price": 100.0,
    "quantity": 10,
    "id": 1
}

test_product2 = {
    "name": "Тестовый продукт 2",
    "description": "Тестовое описание 2",
    "price": 200.0,
    "quantity": 20,
    "id": 2
}

updated_product = test_product.copy()
updated_product['price'] = 150.0
non_existent_product = test_product.copy()
non_existent_product['id'] = 999


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product, expected_result",
    [
        (
                schemas.ProductBase(
                    name='Тестовый продукт 1',
                    price=100,
                    quantity=10,
                    description='Тестовое описание 1'
                ),
                test_product
        ),
        (
                schemas.ProductBase(
                    name='Тестовый продукт 2',
                    price=200,
                    quantity=20,
                    description='Тестовое описание 2'
                ),
                test_product2
        ),
    ]
)
async def test_create_product(product, expected_result):
    result = await ProductRepository.create_product(product)
    assert result.model_dump() == expected_result


@pytest.mark.asyncio
async def test_get_products():
    result = await ProductRepository.get_products()
    assert result == [test_product['name'], test_product2['name']]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_id,expected_result,expected_exception",
    [
        (1, test_product, nullcontext()),
        (999, None, pytest.raises(HTTPException)),
    ]
)
async def test_get_product_info(product_id, expected_result, expected_exception):
    with expected_exception:
        result = await ProductRepository.get_product_info(product_id)
        assert result.model_dump() == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_id, expected_result, expected_exception",
    [
        (1, updated_product, nullcontext()),
        (999, None, pytest.raises(HTTPException)),
    ]
)
async def test_update_product(product_id, expected_result, expected_exception):
    with expected_exception:
        data = schemas.ProductBase(
            name='Тестовый продукт 1',
            price=150,
            quantity=10,
            description='Тестовое описание 1'
        )

        result = await ProductRepository.update_product(product_id, data)
        assert result.model_dump() == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_id, expected_exception",
    [
        (2, nullcontext()),
        (999, pytest.raises(HTTPException)),
    ]
)
async def test_delete_product(product_id, expected_exception):
    with expected_exception:
        result = await ProductRepository.delete_product(product_id)
        assert result == {"result": f"Продукт c ID - {product_id} удален"}
