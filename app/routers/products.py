from typing import Annotated
from fastapi import APIRouter, Depends
from app import schemas
from app.repository import ProductRepository

router = APIRouter(
    prefix='/products',
    tags=["Продукты"]
)


@router.post("")
async def create_product(product: Annotated[schemas.ProductBase, Depends()]) -> schemas.Product:
    return await ProductRepository.create_product(product)


@router.get("")
async def get_products() -> list:
    return await ProductRepository.get_products()


@router.get("/{product_id}")
async def get_product_info(product_id: int) -> schemas.Product:
    return await ProductRepository.get_product_info(product_id)


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    product: Annotated[schemas.ProductBase, Depends()]
) -> schemas.Product:
    return await ProductRepository.update_product(product_id, product)


@router.delete("/{product_id}")
async def delete_product(product_id: int) -> dict:
    return await ProductRepository.delete_product(product_id)
