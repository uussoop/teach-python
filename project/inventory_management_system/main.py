#!/usr/bin/env python3
"""
Inventory Management System - CLI Interface
"""
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from database import init_db
from models import Product
from operations import (
    add_product,
    edit_product,
    delete_product,
    list_products
)

app = typer.Typer(help="Inventory Management System")
console = Console()

@app.command("init")
def initialize_database():
    """Initialize the database with tables"""
    init_db()
    console.print("[green]Database initialized successfully![/green]")

@app.command("add")
def add_product_command(
    name: str = typer.Option(..., prompt=True, help="Product name"),
    description: str = typer.Option(..., prompt=True, help="Product description"),
    price: float = typer.Option(..., prompt=True, help="Product price"),
    stock_quantity: int = typer.Option(..., prompt=True, help="Current stock quantity"),
    category: str = typer.Option(..., prompt=True, help="Product category")
):
    """Add a new product to inventory"""
    product = add_product(name, description, price, stock_quantity, category)
    console.print(f"[green]Product '{product.name}' added successfully![/green]")

@app.command("edit")
def edit_product_command(
    product_id: int = typer.Option(..., prompt=True, help="Product ID to edit"),
    name: Optional[str] = typer.Option(None, help="New product name"),
    description: Optional[str] = typer.Option(None, help="New product description"),
    price: Optional[float] = typer.Option(None, help="New product price"),
    stock_quantity: Optional[int] = typer.Option(None, help="New stock quantity"),
    category: Optional[str] = typer.Option(None, help="New product category")
):
    """Edit an existing product"""
    success = edit_product(product_id, name, description, price, stock_quantity, category)
    if success:
        console.print(f"[green]Product (ID: {product_id}) updated successfully![/green]")
    else:
        console.print(f"[red]Product with ID {product_id} not found![/red]")

@app.command("delete")
def delete_product_command(
    product_id: int = typer.Option(..., prompt=True, help="Product ID to delete")
):
    """Delete a product from inventory"""
    success = delete_product(product_id)
    if success:
        console.print(f"[green]Product (ID: {product_id}) deleted successfully![/green]")
    else:
        console.print(f"[red]Product with ID {product_id} not found![/red]")

@app.command("list")
def list_products_command():
    """List all products in inventory"""
    products = list_products()
    
    if not products:
        console.print("[yellow]No products found in inventory![/yellow]")
        return
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Price", justify="right")
    table.add_column("Stock", justify="right")
    table.add_column("Category")
    
    for product in products:
        table.add_row(
            str(product.id),
            product.name,
            product.description,
            f"${product.price:.2f}",
            str(product.stock_quantity),
            product.category
        )
    
    console.print(table)

if __name__ == "__main__":
    app() 