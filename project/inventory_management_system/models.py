"""
Inventory Management System - Data Models
"""
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Product(SQLModel, table=True):
    """Product model representing items in inventory"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    price: float
    stock_quantity: int
    category: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    # Session 2: Threshold for low stock alerts
    low_stock_threshold: int = Field(default=10)
    
    # Session 2: Relationship with sales
    sales: List["Sale"] = Relationship(back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price=${self.price:.2f}, stock={self.stock_quantity})>"


# Session 2: New model for sales tracking
class Sale(SQLModel, table=True):
    """Sale model representing product sales"""
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    sale_price: float
    sale_date: datetime = Field(default_factory=datetime.now)
    
    # Relationship with Product
    product: Product = Relationship(back_populates="sales")
    
    def __repr__(self):
        return f"<Sale(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, price=${self.sale_price:.2f})>" 