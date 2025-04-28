# Inventory Management System

A simple command-line inventory management system built with Python, SQLModel, and Typer.

## Features (Session 1)

- Add, edit, and delete products
- List all products in the inventory
- Store data in SQLite database using SQLModel ORM
- User-friendly command-line interface

## Features (Session 2)

- Search functionality for products by name, description, or category
- Low stock alerts with customizable thresholds
- Sales tracking and history
- Improved data models with relationships

## Prerequisites

- Python 3.7+
- Required packages:
  - sqlmodel
  - typer
  - rich

## Installation

1. Clone the repository or download the source code
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install sqlmodel typer rich
   ```

## Usage

### Initialize the Database

Before using the application for the first time, initialize the database:

```bash
python main.py init
```

### Add a Product

Add a new product to the inventory:

```bash
python main.py add
```

You will be prompted to enter:
- Product name
- Description
- Price
- Stock quantity
- Category
- Low stock threshold (Session 2)

### Edit a Product

Edit an existing product:

```bash
python main.py edit
```

You will be prompted for the product ID and can change any of its properties.

### Delete a Product

Remove a product from the inventory:

```bash
python main.py delete
```

You will be prompted for the product ID to delete.

### List All Products

Display all products in the inventory:

```bash
python main.py list
```

### Search Products (Session 2)

Search for products by name, description, or category:

```bash
python main.py search
```

You will be prompted to enter a search term.

### Low Stock Alerts (Session 2)

Check for products with stock below their threshold:

```bash
python main.py low-stock
```

### Record a Sale (Session 2)

Record a sale of a product:

```bash
python main.py sell
```

You will be prompted to enter:
- Product ID
- Quantity sold
- Sale price (optional)

### View Sales History (Session 2)

View the history of all sales, optionally filtered by product:

```bash
python main.py sales
```

## Project Structure

```
inventory_management_system/
├── main.py           # CLI entry point with Typer
├── models.py         # Product and Sale data models
├── database.py       # Database connection and initialization
├── operations.py     # CRUD operations for products and sales
└── inventory.db      # SQLite database file (created on init)
```

## Future Enhancements (Coming in Session 3)

- Reporting features
- Data visualization
- User authentication and authorization
- Export/import functionality 