# Inventory Management System

A simple command-line inventory management system built with Python, SQLModel, and Typer.

## Features (Session 1)

- Add, edit, and delete products
- List all products in the inventory
- Store data in SQLite database using SQLModel ORM
- User-friendly command-line interface

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

## Project Structure

```
inventory_management_system/
├── main.py           # CLI entry point with Typer
├── models.py         # Product data model
├── database.py       # Database connection and initialization
├── operations.py     # CRUD operations for products
└── inventory.db      # SQLite database file (created on init)
```

## Future Enhancements (Coming in Sessions 2 & 3)

- Search functionality
- Low stock alerts
- Sales tracking
- Reporting features
- More advanced data models 