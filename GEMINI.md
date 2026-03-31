# Project: Minimalistic E-commerce Backend

## Overview
This project is a clean and minimal e-commerce backend built with Django and Django REST Framework.

The goal is to support:
- Product browsing
- Cart management
- Order creation
- Payment integration
- Basic inventory handling

Avoid over-engineering. Keep everything simple, readable, and production-ready.

---

## Tech Stack
- Django
- Django REST Framework
- Simple JWT (for authentication)

---

## Architecture Rules

- Use function-based views (FBVs)
- Use request.data.get() for accessing request data
- Keep logic simple and readable
- Avoid unnecessary abstractions
- No class-based views unless absolutely necessary
- Keep apps modular and focused

---

## Apps Structure

Create the following Django apps:

- users
- products
- categories
- cart
- orders
- payments

---

## Core Models

### User
- email (unique)
- username
- password
- is_active
- date_joined

---

### Category
- name
- slug
- is_active

---

### Product
- title
- description
- price
- stock_quantity
- category (FK)
- image
- is_active
- created_at

---

### Cart
- user (FK, nullable for guest support)
- created_at

---

### CartItem
- cart (FK)
- product (FK)
- quantity

---

### Order
- user (FK)
- total_amount
- status (pending, paid, shipped, delivered, cancelled)
- payment_status (pending, paid)
- created_at

---

### OrderItem
- order (FK)
- product (FK)
- quantity
- price

---

### Payment
- order (FK)
- reference
- amount
- status
- created_at

---

## API Design

All endpoints should be RESTful and simple.

### Auth
- POST /api/auth/register/
- POST /api/auth/login/

---

### Products
- GET /api/products/
- GET /api/products/<id>/
- GET /api/products/?category=<slug>
- GET /api/products/search/?q=<query>

---

### Categories
- GET /api/categories/

---

### Cart
- GET /api/cart/
- POST /api/cart/add/
- POST /api/cart/update/
- POST /api/cart/remove/

---

### Orders
- POST /api/orders/create/
- GET /api/orders/
- GET /api/orders/<id>/

---

### Payments
- POST /api/payments/initiate/
- POST /api/payments/verify/

---

## Business Logic Rules

### Cart
- Prevent adding out-of-stock products
- Quantity must not exceed stock
- Recalculate totals on every update

---

### Orders
- Validate cart before creating order
- Copy cart items into OrderItem
- Store price at time of purchase
- Clear cart after order creation

---

### Payments
- Do not mark order as paid until verified
- Update order.payment_status after verification

---

### Inventory
- Reduce stock only after successful payment
- Prevent negative stock

---

## Validation Rules

- Never trust frontend data
- Always validate:
  - price
  - quantity
  - stock availability
- Recalculate totals on backend

---

## Admin Panel

Use Django admin for:
- Managing products
- Managing categories
- Viewing orders
- Updating order status

---

## Coding Style

- Keep functions small and focused
- Use clear variable names
- Avoid deeply nested logic
- Add comments where necessary

---

## Important Notes

- Do NOT add:
  - wishlist
  - reviews
  - coupons
  - vendor system

These are not part of MVP.

---

## Goal

Deliver a clean, minimal, working e-commerce backend that supports:

1. Product listing
2. Cart functionality
3. Order creation
4. Payment verification
5. Basic inventory handling

Nothing more.