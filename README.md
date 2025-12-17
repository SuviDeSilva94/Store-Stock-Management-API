# Store Stock Management API

A backend API for managing product inventory built with FastAPI and PostgreSQL.

## What This Does

This is a API for managing store product stocks. The API lets you create products, update details, delete products, and adjust stock levels (increment/decrement). All endpoints are protected with JWT authentication.

## Tech Stack

- **Python 3.11** with FastAPI
- **PostgreSQL** for database
- **SQLAlchemy** ORM
- **JWT Authentication** for security
- **Docker** for containerization
- **pytest** for testing

## Quick Start

**You'll need:** Docker installed on your machine.

**1. Start the application**
```bash
docker-compose up -d
```

Wait about 10 seconds for the database to initialize.

**2. Open in your browser**
```
http://localhost:8001/docs
```

**3. Register and login**
- Use the `/api/v1/auth/register` endpoint to create a user
- Use the `/api/v1/auth/login` endpoint to get your access token
- Click the "Authorize" button (top right) and paste your token
- Now you can use all the product endpoints!

**4. Stop when done**
```bash
docker-compose down
```

That's it! 🚀

## Authentication

All product endpoints require JWT authentication. First register a user, then login to get an access token.

### Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login and get access token |
| GET | `/api/v1/auth/me` | Get current user info |

### Product Endpoints (Requires Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/products` | Create a new product |
| GET | `/api/v1/products` | Get all products (with pagination) |
| GET | `/api/v1/products/{id}` | Get product by ID |
| PUT | `/api/v1/products/{id}` | Update product |
| DELETE | `/api/v1/products/{id}` | Delete product |
| POST | `/api/v1/products/{id}/increment` | Increase stock |
| POST | `/api/v1/products/{id}/decrement` | Decrease stock |

## Example Usage

**Step 1: Register a user**
```bash
curl -X POST "http://localhost:8001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "email": "admin@example.com", "password": "admin123"}'
```

**Step 2: Login to get access token**
```bash
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Step 3: Use the token for product operations**

Set your token:
```bash
TOKEN="your_access_token_here"
```

**Create a product:**
```bash
curl -X POST "http://localhost:8001/api/v1/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "iPhone 16", "sku": "IP16-256-BLK", "stock": 20}'
```

**Get all products:**
```bash
curl "http://localhost:8001/api/v1/products" \
  -H "Authorization: Bearer $TOKEN"
```

**Increment stock:**
```bash
curl -X POST "http://localhost:8001/api/v1/products/1/increment" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"amount": 5}'
```

**Decrement stock:**
```bash
curl -X POST "http://localhost:8001/api/v1/products/1/decrement" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
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

Tests covering authentication, unit, and integration testing.

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

- ✅ **JWT Authentication** (register, login, protected endpoints)
- ✅ Pagination on GET /products (skip/limit parameters)
- ✅ Unit and integration tests
- ✅ Docker + docker-compose setup
- ✅ Database transactions
- ✅ Proper error handling

## Requirements Met

All 7 required endpoints working with proper status codes:
- 201 Created
- 200 OK
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
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
