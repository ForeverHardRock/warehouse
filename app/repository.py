import datetime

from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from sqlalchemy.future import select
from app import schemas
from app.models import Product, Order, OrderItem
from app.database import my_session


class ProductRepository:
    @classmethod
    async def get_products(cls) -> list:
        async with my_session() as session:
            query = select(Product)
            result = await session.execute(query)
            products = result.scalars().all()
            products_list = [product.name for product in products]
            return products_list

    @classmethod
    async def get_product_info(cls, product_id: int) -> schemas.Product:
        async with my_session() as session:
            query = select(Product).where(Product.id == product_id)
            result = await session.execute(query)
            product = result.scalars().one_or_none()

            if not product:
                raise HTTPException(status_code=404, detail="Нет такого продукта")

            return schemas.Product.model_validate(product)

    @classmethod
    async def create_product(cls, data: schemas.ProductBase) -> schemas.Product:
        async with my_session() as session:
            product_dict = data.model_dump()
            product = Product(**product_dict)
            session.add(product)
            await session.flush()
            await session.commit()
            return schemas.Product.model_validate(product)

    @classmethod
    async def update_product(cls, product_id: int, data: schemas.ProductBase) -> schemas.Product:
        async with my_session() as session:
            query = select(Product).where(Product.id == product_id)
            result = await session.execute(query)
            product = result.scalars().one_or_none()

            if not product:
                raise HTTPException(status_code=404, detail="Нет такого продукта")

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)

            await session.flush()
            await session.commit()
            return schemas.Product.model_validate(product)

    @classmethod
    async def delete_product(cls, product_id: int) -> dict:
        async with my_session() as session:
            query = select(Product).where(Product.id == product_id)
            result = await session.execute(query)
            product = result.scalars().one_or_none()

            if not product:
                raise HTTPException(status_code=404, detail="Нет такого продукта")

            await session.delete(product)
            await session.flush()
            await session.commit()
            return {"result": f"Продукт c ID - {product_id} удален"}


class OrderRepository:
    @classmethod
    async def create_order(cls, data: schemas.OrderCreate) -> schemas.Order:
        async with my_session() as session:
            order_items = []
            total = 0

            for item in data.items:
                get_product = select(Product).where(Product.id == item.product_id)
                result = await session.execute(get_product)
                product = result.scalars().one_or_none()

                if not product:
                    raise HTTPException(status_code=404, detail="Нет такого продукта")
                if product.quantity < item.quantity:
                    raise HTTPException(status_code=404, detail="Нет такого количества")

                product.quantity -= item.quantity
                total += product.price * item.quantity

                order_item = OrderItem(product=product, quantity=item.quantity)
                order_items.append(order_item)

            order = Order(
                items=order_items,
                created_at=datetime.datetime.now(),
                total=total
            )
            session.add(order)
            await session.flush()
            await session.commit()
            return schemas.Order.model_validate(order)

    @classmethod
    async def get_orders(cls) -> list:
        async with my_session() as session:
            query = select(Order)
            result = await session.execute(query)
            orders = result.scalars().all()
            orders_list = [f"{order.id}" for order in orders]
            return orders_list

    @classmethod
    async def get_order_info(cls, order_id: int) -> schemas.Order:
        async with my_session() as session:
            query = (
                select(Order)
                .options(selectinload(Order.items).selectinload(OrderItem.product))
                .where(Order.id == order_id)
            )
            result = await session.execute(query)
            order = result.scalars().one_or_none()

            if not order:
                raise HTTPException(status_code=404, detail="Нет такого заказа")

            return schemas.Order.model_validate(order)

    @classmethod
    async def update_order_status(cls, order_id: int, data: schemas.OrderStatusUpdate) -> dict:
        async with my_session() as session:
            order = select(Order).where(Order.id == order_id)
            result = await session.execute(order)
            order = result.scalars().one_or_none()

            if not order:
                raise HTTPException(status_code=404, detail="Нет такого заказа")

            order.status = data.status

            session.add(order)
            await session.commit()

            return {"result": f"Статус у заказа с ID - {order_id} обновлен на {data.status}"}
