"""
Inventory Management System - Data Models
"""
from typing import Optional
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

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price=${self.price:.2f}, stock={self.stock_quantity})>" 