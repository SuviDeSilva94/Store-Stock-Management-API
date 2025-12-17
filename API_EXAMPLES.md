# API Examples

Quick reference for testing the API with curl.

## Setup

First, start the application:
```bash
docker-compose up -d
```

Base URL: http://localhost:8001

## 1. Register a User

```bash
curl -X POST "http://localhost:8001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

Response:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "is_active": true
}
```

## 2. Login (Get Access Token)

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

Save your token:
```bash
TOKEN="your_access_token_here"
```

---

## Product Endpoints (All require authentication)

### 3. Create a Product

```bash
curl -X POST "http://localhost:8001/api/v1/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "iPhone 16 Pro",
    "sku": "IP16PRO-256-BLK",
    "stock": 50
  }'
```

Response:
```json
{
  "id": 1,
  "name": "iPhone 16 Pro",
  "sku": "IP16PRO-256-BLK",
  "stock": 50,
  "created_at": "2024-12-17T10:30:00",
  "updated_at": "2024-12-17T10:30:00"
}
```

### 4. Get All Products

```bash
curl "http://localhost:8001/api/v1/products" \
  -H "Authorization: Bearer $TOKEN"
```

With pagination:
```bash
curl "http://localhost:8001/api/v1/products?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Get Product by ID

```bash
curl "http://localhost:8001/api/v1/products/1" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Update Product

```bash
curl -X PUT "http://localhost:8001/api/v1/products/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "iPhone 16 Pro Max",
    "stock": 75
  }'
```

### 7. Delete Product

```bash
curl -X DELETE "http://localhost:8001/api/v1/products/1" \
  -H "Authorization: Bearer $TOKEN"
```

Response: 204 No Content

### 8. Increment Stock

```bash
curl -X POST "http://localhost:8001/api/v1/products/1/increment" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "amount": 10
  }'
```

Default (increment by 1):
```bash
curl -X POST "http://localhost:8001/api/v1/products/1/increment" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{}'
```

### 9. Decrement Stock

```bash
curl -X POST "http://localhost:8001/api/v1/products/1/decrement" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "amount": 5
  }'
```

Default (decrement by 1):
```bash
curl -X POST "http://localhost:8001/api/v1/products/1/decrement" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{}'
```

---

## Complete Workflow Example

```bash
# 1. Register
curl -X POST "http://localhost:8001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "test123"}'

# 2. Login and save token
TOKEN=$(curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123" -s | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"

# 3. Create a product
curl -X POST "http://localhost:8001/api/v1/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "MacBook Pro", "sku": "MBP-M3-16", "stock": 25}'

# 4. Get all products
curl "http://localhost:8001/api/v1/products" \
  -H "Authorization: Bearer $TOKEN"

# 5. Increment stock
curl -X POST "http://localhost:8001/api/v1/products/1/increment" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"amount": 10}'

# 6. Decrement stock
curl -X POST "http://localhost:8001/api/v1/products/1/decrement" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"amount": 3}'
```

---

## Error Examples

Without authentication (401):
```bash
curl "http://localhost:8001/api/v1/products"
```

Response:
```json
{
  "detail": "Not authenticated"
}
```

Product not found (404):
```bash
curl "http://localhost:8001/api/v1/products/99999" \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
{
  "detail": "Product with id 99999 not found"
}
```

Insufficient stock (400):
```bash
curl -X POST "http://localhost:8001/api/v1/products/1/decrement" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"amount": 1000}'
```

Response:
```json
{
  "detail": "Insufficient stock: requested 1000, available 10"
}
```

---

## Using Postman

Import these as a collection:

1. Set base URL as variable: {{base_url}} = http://localhost:8001
2. Set auth token as variable: {{token}} (get from login response)
3. Add Authorization: Bearer {{token}} to all product requests
4. Use the examples above as request bodies

Or use the Swagger UI:
Open http://localhost:8001/docs for an interactive API explorer.

