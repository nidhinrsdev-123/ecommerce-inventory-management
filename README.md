# E-commerce & Inventory Management Backend

A Django backend for a small e-commerce workflow: product catalog, stock tracking, customer checkout, order items, and order-status transitions. Built with **Python, Django, PostgreSQL, and Pytest**.

## Features
- Product catalog with unique SKU, price, stock quantity, and active flag.
- Staff-only product creation, update, and deletion; public users can browse active products.
- Authenticated customers can create orders and view their own order history.
- Checkout calculates prices on the server; clients submit product IDs and quantities, not prices.
- Database transaction and row locking during checkout to help prevent overselling.
- Order items preserve the unit price at purchase time.
- Customers can cancel pending orders; staff can move orders through paid, shipped, and delivered.
- Filtering, search, pagination, Django admin, and Swagger documentation.

## Technology
Python 3.11+, Django 5, Django REST Framework, django-filter, drf-spectacular, PostgreSQL (SQLite fallback), and pytest.

## Exact repository structure

This tree matches the files currently committed to GitHub:

~~~text
ecommerce-inventory-management/
├── .github/
│   └── workflows/
│       └── tests.yml
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/
│   ├── __init__.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── admin.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── services.py
│   └── views.py
├── tests/
│   ├── __init__.py
│   └── test_orders.py
├── .env.example
├── .gitignore
├── LICENSE
├── manage.py
├── pytest.ini
├── README.md
└── requirements.txt
~~~

## Step-by-step: run locally (Windows)

### 1. Install prerequisites
Install Python 3.11 or newer. PostgreSQL 14+ is optional; SQLite is used automatically when DATABASE_URL is not configured.

~~~powershell
py --version
~~~

### 2. Clone the repository

~~~powershell
git clone https://github.com/nidhinrsdev-123/ecommerce-inventory-management.git
cd ecommerce-inventory-management
~~~

### 3. Create and activate a virtual environment

~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

If PowerShell blocks activation, use Command Prompt:

~~~bat
.venv\Scripts\activate.bat
~~~

### 4. Install dependencies

~~~powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

### 5. Configure the database

**Quick start with SQLite:** Skip this step.

**Use PostgreSQL:** Create a database and user, then copy the environment template:

~~~powershell
Copy-Item .env.example .env
~~~

Edit DATABASE_URL in .env with your own database credentials. Example:

~~~text
DATABASE_URL=postgresql://shop_user:your_password@localhost:5432/shop_db
~~~

Never commit .env or passwords.

### 6. Create database tables

~~~powershell
python manage.py migrate
~~~

### 7. Create an administrator

~~~powershell
python manage.py createsuperuser
~~~

Use this account to sign in to Django admin. Add products through the admin interface. Also create a separate normal user in admin to test customer checkout.

### 8. Start the server

~~~powershell
python manage.py runserver
~~~

Open:
- Swagger API docs: http://127.0.0.1:8000/api/docs/
- OpenAPI schema: http://127.0.0.1:8000/api/schema/
- Django admin: http://127.0.0.1:8000/admin/
- Products: http://127.0.0.1:8000/api/products/

Stop with Ctrl+C.

## Authentication and permissions

This project uses Django REST Framework Basic Authentication and Session Authentication (not JWT).
- Product GET requests are public; non-staff users see active products only.
- Product create/update/delete requires a staff account.
- Order endpoints require an authenticated account.
- Customers can only see their own orders; staff can see all orders.
- Swagger UI can prompt for Basic Authentication. Use a Django user's username and password.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/products/ | List active products |
| POST | /api/products/ | Create product (staff only) |
| GET | /api/products/{id}/ | Product detail |
| PATCH, DELETE | /api/products/{id}/ | Update/delete product (staff only) |
| GET | /api/orders/ | List current user's orders |
| POST | /api/orders/ | Create an order / checkout |
| GET | /api/orders/{id}/ | Retrieve an order |
| POST | /api/orders/{id}/transition/ | Change order status when permitted |

### Example checkout request

POST /api/orders/ as an authenticated customer:

~~~json
{
  "items": [
    {
      "product": 1,
      "quantity": 2
    }
  ]
}
~~~

The product value is the product database ID. The server checks active status and available stock, then calculates the total using the database price. Clients cannot submit the unit price or order total.

### Order status workflow
- A customer can change pending to cancelled; the stock is returned.
- Staff can change paid to shipped.
- Staff can change shipped to delivered.
- Other transitions are rejected.

## Run automated tests

~~~powershell
pytest
~~~

Tests cover successful checkout and stock decrement, insufficient-stock rollback, and customer restrictions on order status transitions. SQLite is used by default; set DATABASE_URL to use PostgreSQL.

## Code explanation
- config/settings.py: Django apps, database, REST permissions, filters, pagination, and schema.
- config/urls.py: API router and documentation endpoints.
- shop/models.py: Product, Order, and OrderItem relational models.
- shop/serializers.py: product/order representations and checkout validation.
- shop/services.py: transactional checkout and stock decrement.
- shop/permissions.py: staff write access and order ownership.
- shop/views.py: product, order, and status-transition endpoints.
- shop/admin.py: product and order administration.
- shop/migrations/: database schema history.
- tests/: checkout and inventory tests.

## Production improvements
Payment processing is not implemented; staff currently advance the paid state. Before production, integrate a payment provider with verified webhooks and idempotency keys, add audit logging and monitoring, and review concurrency behavior using the target production database. Do not store card details in this application.
