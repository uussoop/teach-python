#!/usr/bin/env python3
"""
Inventory Management System - CLI Interface
"""
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from datetime import datetime

from database import init_db
from models import Product, Sale
from operations import (
    add_product,
    edit_product,
    delete_product,
    list_products,
    search_products,
    get_low_stock_products,
    record_sale,
    get_sales_history
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
    category: str = typer.Option(..., prompt=True, help="Product category"),
    low_stock_threshold: int = typer.Option(10, prompt=True, help="Low stock threshold")
):
    """Add a new product to inventory"""
    product = add_product(name, description, price, stock_quantity, category, low_stock_threshold)
    console.print(f"[green]Product '{product.name}' added successfully![/green]")

@app.command("edit")
def edit_product_command(
    product_id: int = typer.Option(..., prompt=True, help="Product ID to edit"),
    name: Optional[str] = typer.Option(None, help="New product name"),
    description: Optional[str] = typer.Option(None, help="New product description"),
    price: Optional[float] = typer.Option(None, help="New product price"),
    stock_quantity: Optional[int] = typer.Option(None, help="New stock quantity"),
    category: Optional[str] = typer.Option(None, help="New product category"),
    low_stock_threshold: Optional[int] = typer.Option(None, help="New low stock threshold")
):
    """Edit an existing product"""
    success = edit_product(product_id, name, description, price, stock_quantity, category, low_stock_threshold)
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
    table.add_column("Low Stock Threshold", justify="right")
    
    for product in products:
        table.add_row(
            str(product.id),
            product.name,
            product.description,
            f"${product.price:.2f}",
            str(product.stock_quantity),
            product.category,
            str(product.low_stock_threshold)
        )
    
    console.print(table)

@app.command("search")
def search_products_command(
    search_term: str = typer.Option(..., prompt=True, help="Search term")
):
    """Search products by name, description, or category"""
    products = search_products(search_term)
    
    if not products:
        console.print(f"[yellow]No products found matching '{search_term}'![/yellow]")
        return
    
    console.print(f"[green]Found {len(products)} products matching '{search_term}':[/green]")
    
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

@app.command("low-stock")
def low_stock_alerts_command():
    """Show products with stock below their threshold"""
    products = get_low_stock_products()
    
    if not products:
        console.print("[green]No products with low stock![/green]")
        return
    
    console.print(f"[yellow]Warning: {len(products)} products with low stock:[/yellow]")
    
    table = Table(show_header=True, header_style="bold red")
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Current Stock", justify="right")
    table.add_column("Threshold", justify="right")
    table.add_column("Category")
    
    for product in products:
        table.add_row(
            str(product.id),
            product.name,
            str(product.stock_quantity),
            str(product.low_stock_threshold),
            product.category
        )
    
    console.print(table)

@app.command("sell")
def record_sale_command(
    product_id: int = typer.Option(..., prompt=True, help="Product ID"),
    quantity: int = typer.Option(..., prompt=True, help="Quantity sold"),
    sale_price: Optional[float] = typer.Option(None, prompt=True, help="Sale price per unit (leave empty for current price)")
):
    """Record a product sale"""
    sale = record_sale(product_id, quantity, sale_price)
    
    if not sale:
        console.print("[red]Failed to record sale. Check product ID and stock availability.[/red]")
        return
    
    console.print(f"[green]Sale recorded successfully! Sale ID: {sale.id}[/green]")
    console.print(f"Product ID: {sale.product_id}, Quantity: {sale.quantity}, Price: ${sale.sale_price:.2f}")

@app.command("sales")
def view_sales_history(
    product_id: Optional[int] = typer.Option(None, help="Filter by product ID")
):
    """View sales history, optionally filtered by product"""
    sales = get_sales_history(product_id)
    
    if not sales:
        console.print("[yellow]No sales records found![/yellow]")
        return
    
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Sale ID", style="dim")
    table.add_column("Product ID")
    table.add_column("Quantity", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Date")
    
    for sale in sales:
        table.add_row(
            str(sale.id),
            str(sale.product_id),
            str(sale.quantity),
            f"${sale.sale_price:.2f}",
            f"${(sale.quantity * sale.sale_price):.2f}",
            sale.sale_date.strftime("%Y-%m-%d %H:%M:%S")
        )
    
    console.print(table)

if __name__ == "__main__":
    app() 