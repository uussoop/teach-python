"""
Inventory Management System - Database Operations
"""
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, or_
from database import engine
from models import Product, Sale


def add_product(name: str, description: str, price: float, stock_quantity: int, category: str, low_stock_threshold: int = 10) -> Product:
    """
    Add a new product to the database
    
    Args:
        name: Product name
        description: Product description
        price: Product price
        stock_quantity: Current stock quantity
        category: Product category
        low_stock_threshold: Threshold for low stock alerts (Session 2)
        
    Returns:
        Product: The created product
    """
    with Session(engine) as session:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            category=category,
            low_stock_threshold=low_stock_threshold  # Session 2: Added parameter
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
    category: Optional[str] = None,
    low_stock_threshold: Optional[int] = None  # Session 2: Added parameter
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
        low_stock_threshold: New low stock threshold (Session 2)
        
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
        # Session 2: Update low stock threshold if provided
        if low_stock_threshold is not None:
            product.low_stock_threshold = low_stock_threshold
            
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


# Session 2: Search functionality
def search_products(search_term: str) -> List[Product]:
    """
    Search for products by name, description, or category
    
    Args:
        search_term: Search term to look for
        
    Returns:
        List[Product]: List of matching products
    """
    search_pattern = f"%{search_term}%"
    
    with Session(engine) as session:
        statement = select(Product).where(
            or_(
                Product.name.like(search_pattern),
                Product.description.like(search_pattern),
                Product.category.like(search_pattern)
            )
        )
        products = session.exec(statement).all()
        return products


# Session 2: Low stock alert functionality
def get_low_stock_products() -> List[Product]:
    """
    Get list of products with stock below their threshold
    
    Returns:
        List[Product]: List of products with low stock
    """
    with Session(engine) as session:
        statement = select(Product).where(Product.stock_quantity <= Product.low_stock_threshold)
        products = session.exec(statement).all()
        return products


# Session 2: Sales tracking functionality
def record_sale(product_id: int, quantity: int, sale_price: Optional[float] = None) -> Optional[Sale]:
    """
    Record a sale of a product
    
    Args:
        product_id: ID of the product sold
        quantity: Quantity sold
        sale_price: Price per unit (if different from current product price)
        
    Returns:
        Sale: The recorded sale or None if product not found or insufficient stock
    """
    with Session(engine) as session:
        # Get the product
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).first()
        
        if not product:
            return None
        
        # Check if there's enough stock
        if product.stock_quantity < quantity:
            return None
        
        # Create the sale
        price = sale_price if sale_price is not None else product.price
        sale = Sale(
            product_id=product_id,
            quantity=quantity,
            sale_price=price
        )
        
        # Update stock quantity
        product.stock_quantity -= quantity
        product.updated_at = datetime.now()
        
        # Save changes
        session.add(sale)
        session.add(product)
        session.commit()
        session.refresh(sale)
        
        return sale


# Session 2: Get sales history
def get_sales_history(product_id: Optional[int] = None) -> List[Sale]:
    """
    Get sales history, optionally filtered by product
    
    Args:
        product_id: Optional product ID to filter by
        
    Returns:
        List[Sale]: List of sales
    """
    with Session(engine) as session:
        if product_id:
            statement = select(Sale).where(Sale.product_id == product_id).order_by(Sale.sale_date.desc())
        else:
            statement = select(Sale).order_by(Sale.sale_date.desc())
        
        sales = session.exec(statement).all()
        return sales 