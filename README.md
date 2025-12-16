# Store Stock Management API

A backend API for managing product inventory built with FastAPI and PostgreSQL.

## What This Does

This is a coding assignment for managing store product stocks. The API lets you create products, update details, delete products, and adjust stock levels (increment/decrement).

## Tech Stack

- **Python 3.11** with FastAPI
- **PostgreSQL** for database
- **SQLAlchemy** ORM
- **Docker** for containerization
- **pytest** for testing

## Quick Start

1. **Clone the repo**
```bash
git clone <your-repo-url>
cd ik
```

2. **Run with Docker**
```bash
chmod +x run.sh
./run.sh
```

The API will be available at `http://localhost:8001`

API docs: `http://localhost:8001/docs`

## API Endpoints

All endpoints are under `/api/v1/products`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Create a new product |
| GET | `/products` | Get all products (with pagination) |
| GET | `/products/{id}` | Get product by ID |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |
| POST | `/products/{id}/increment` | Increase stock |
| POST | `/products/{id}/decrement` | Decrease stock |

## Example Usage

**Create a product:**
```bash
curl -X POST "http://localhost:8001/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone 16", "sku": "IP16-256-BLK", "stock": 20}'
```

**Get all products:**
```bash
curl "http://localhost:8001/api/v1/products"
```

**Increment stock:**
```bash
curl -X POST "http://localhost:8001/api/v1/products/1/increment" \
  -H "Content-Type: application/json" \
  -d '{"amount": 5}'
```

**Decrement stock:**
```bash
curl -X POST "http://localhost:8001/api/v1/products/1/decrement" \
  -H "Content-Type: application/json" \
  -d '{"amount": 3}'
```

## Product Model

| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Auto-generated |
| name | String | Required |
| sku | String | Required, unique |
| stock | Integer | Defaults to 0, never goes below 0 |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

## Running Tests

```bash
chmod +x test.sh
./test.sh
```

52 tests covering unit and integration testing.

## Project Structure

```
app/
├── api/              # API routes and schemas
├── core/             # Config and exceptions
├── domain/           # Business logic and models
└── infrastructure/   # Database and repositories

tests/
├── unit/             # Unit tests
└── integration/      # API integration tests
```

## Design Decisions

**Why FastAPI?** Modern, fast, auto-generates API docs, great for Python projects.

**Why PostgreSQL?** Reliable, handles transactions well, production-ready.

**Architecture:** Clean 3-tier architecture (API → Domain → Infrastructure) following SOLID principles. Makes the code maintainable and testable.

**Design Patterns Used:**
- Repository Pattern (data access)
- Service Layer Pattern (business logic)
- Dependency Injection (FastAPI)
- Factory Pattern (dependency creation)

## Bonus Features Implemented

- ✅ Pagination on GET /products (skip/limit parameters)
- ✅ Unit and integration tests (52 tests)
- ✅ Docker + docker-compose setup
- ✅ Database transactions
- ✅ Proper error handling

## Requirements Met

All 7 required endpoints working with proper status codes:
- 201 Created
- 200 OK
- 204 No Content
- 400 Bad Request
- 404 Not Found

Stock never goes below zero (enforced in business logic).

## Environment Variables

Default values work out of the box. To customize, create a `.env` file:

```
APP_NAME=Store Stock Management API
DATABASE_URL=postgresql://postgres:postgres@db:5432/store_stock
```

## Stopping the Application

```bash
docker-compose down
```

---

Built for IKEA Senior Software Engineer - AI position coding assignment.
