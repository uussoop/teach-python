"""
Inventory Management System - Database Operations
"""
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from database import engine
from models import Product


def add_product(name: str, description: str, price: float, stock_quantity: int, category: str) -> Product:
    """
    Add a new product to the database
    
    Args:
        name: Product name
        description: Product description
        price: Product price
        stock_quantity: Current stock quantity
        category: Product category
        
    Returns:
        Product: The created product
    """
    with Session(engine) as session:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            category=category
        )
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


def edit_product(
    product_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    stock_quantity: Optional[int] = None,
    category: Optional[str] = None
) -> bool:
    """
    Edit an existing product in the database
    
    Args:
        product_id: ID of the product to edit
        name: New product name (if provided)
        description: New product description (if provided)
        price: New product price (if provided)
        stock_quantity: New stock quantity (if provided)
        category: New product category (if provided)
        
    Returns:
        bool: True if product was updated, False if not found
    """
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).first()
        
        if not product:
            return False
        
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if stock_quantity is not None:
            product.stock_quantity = stock_quantity
        if category is not None:
            product.category = category
            
        product.updated_at = datetime.now()
        session.add(product)
        session.commit()
        return True


def delete_product(product_id: int) -> bool:
    """
    Delete a product from the database
    
    Args:
        product_id: ID of the product to delete
        
    Returns:
        bool: True if product was deleted, False if not found
    """
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).first()
        
        if not product:
            return False
        
        session.delete(product)
        session.commit()
        return True


def list_products() -> List[Product]:
    """
    List all products in the database
    
    Returns:
        List[Product]: List of all products
    """
    with Session(engine) as session:
        statement = select(Product).order_by(Product.name)
        products = session.exec(statement).all()
        return products 