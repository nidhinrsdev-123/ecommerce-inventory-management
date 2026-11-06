# E-commerce & Inventory Management Backend
Django + PostgreSQL backend for product catalogs, inventory, customer orders, and order lifecycle management.

## Features
- Product SKU, price, stock, and active status.
- Customer-owned orders and line items with historical unit-price snapshots.
- Atomic checkout validates stock, locks product rows, and decrements inventory.
- Customers can cancel pending orders; staff advance paid/shipped/delivered states.
- Public product reads, staff-only product writes, owner/staff order access.
- Filtering, search, pagination, Django admin, and Swagger documentation.

## Setup
Python 3.11+ and PostgreSQL 14+. Create a database and configure .env from .env.example.
Run: python -m venv .venv; activate it; pip install -r requirements.txt; python manage.py migrate; python manage.py createsuperuser; python manage.py runserver.
Docs: http://127.0.0.1:8000/api/docs/

## API
- GET/POST /api/products/ — browse products; staff can create.
- GET/PATCH/DELETE /api/products/{id}/ — product detail; staff can modify.
- GET/POST /api/orders/ — list orders or checkout.
- GET /api/orders/{id}/ — order detail.
- POST /api/orders/{id}/transition/ — validated order status change.
- GET /api/schema/ and /api/docs/ — OpenAPI.

Checkout payload: {"items":[{"product":1,"quantity":2}]}. The server determines price and stock; clients cannot submit prices. Staff must mark orders paid, shipped, or delivered. A customer may cancel a pending order.

## Data model
Product has unique SKU and non-negative stock. Order belongs to a customer and stores status and total. OrderItem stores quantity and unit-price snapshot to preserve the historical price.

## Tests
Run pytest. SQLite is the default fallback; DATABASE_URL selects PostgreSQL.

## Structure
- config/: settings and root URL routing.
- shop/: product/order models, serializers, permissions, checkout service, API.
- tests/: checkout, inventory consistency, and workflow tests.
- .env.example, requirements.txt, pytest.ini, manage.py.

## Engineering notes
Checkout uses a database transaction and row locks to reduce overselling. Payment-card details are intentionally out of scope. Production systems should add payment-provider webhooks, idempotency keys, audit logs, background jobs, and monitoring.
