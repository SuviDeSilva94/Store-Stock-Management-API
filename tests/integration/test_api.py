import pytest
from fastapi.testclient import TestClient


class TestAuthAPI:
    def test_register_user_success(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
    
    def test_register_duplicate_username(self, client: TestClient, test_user: dict):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": test_user["username"],
                "email": "different@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 400
    
    def test_login_success(self, client: TestClient, test_user: dict):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user["username"], "password": test_user["password"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "wronguser", "password": "wrongpass"}
        )
        assert response.status_code == 401
    
    def test_get_current_user(self, client: TestClient, auth_headers: dict):
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"


class TestProductAPI:
    def test_create_product_success(self, client: TestClient, auth_headers: dict):
        response = client.post(
            "/api/v1/products",
            json={
                "name": "Apple iPhone 16",
                "sku": "IP16-256-BLK",
                "stock": 20
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Apple iPhone 16"
        assert data["sku"] == "IP16-256-BLK"
        assert data["stock"] == 20
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_product_without_auth(self, client: TestClient):
        response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST", "stock": 10}
        )
        assert response.status_code == 401
    
    def test_create_product_duplicate_sku(self, client: TestClient, auth_headers: dict):
        client.post(
            "/api/v1/products",
            json={"name": "Product 1", "sku": "TEST-001", "stock": 10},
            headers=auth_headers
        )
        response = client.post(
            "/api/v1/products",
            json={"name": "Product 2", "sku": "TEST-001", "stock": 5},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_create_product_invalid_data(self, client: TestClient, auth_headers: dict):
        response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST", "stock": -5},
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_get_all_products(self, client: TestClient, auth_headers: dict):
        client.post("/api/v1/products", json={"name": "P1", "sku": "P1", "stock": 10}, headers=auth_headers)
        client.post("/api/v1/products", json={"name": "P2", "sku": "P2", "stock": 20}, headers=auth_headers)
        response = client.get("/api/v1/products", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_all_products_with_pagination(self, client: TestClient, auth_headers: dict):
        for i in range(5):
            client.post(
                "/api/v1/products",
                json={"name": f"P{i}", "sku": f"P{i}", "stock": 10},
                headers=auth_headers
            )
        response = client.get("/api/v1/products?skip=1&limit=2", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_product_by_id_success(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test"
        assert data["sku"] == "TEST-001"
    
    def test_get_product_by_id_not_found(self, client: TestClient, auth_headers: dict):
        response = client.get("/api/v1/products/99999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_update_product_success(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Original", "sku": "ORIG-001", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.put(
            f"/api/v1/products/{product_id}",
            json={"name": "Updated", "stock": 15},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["stock"] == 15
        assert data["sku"] == "ORIG-001"
    
    def test_update_product_not_found(self, client: TestClient, auth_headers: dict):
        response = client.put(
            "/api/v1/products/99999",
            json={"name": "Updated"},
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_delete_product_success(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "ToDelete", "sku": "DEL-001", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.delete(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 204
        get_response = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_product_not_found(self, client: TestClient, auth_headers: dict):
        response = client.delete("/api/v1/products/99999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_increment_stock_success(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/increment",
            json={"amount": 5},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 15
    
    def test_increment_stock_default_amount(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-002", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/increment",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 11
    
    def test_increment_stock_invalid_amount(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-003", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/increment",
            json={"amount": -5},
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_decrement_stock_success(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-004", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/decrement",
            json={"amount": 3},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 7
    
    def test_decrement_stock_default_amount(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-005", "stock": 10},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/decrement",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 9
    
    def test_decrement_stock_insufficient(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-006", "stock": 5},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/decrement",
            json={"amount": 10},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Insufficient stock" in response.json()["detail"]
    
    def test_decrement_stock_to_zero(self, client: TestClient, auth_headers: dict):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-007", "stock": 5},
            headers=auth_headers
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/decrement",
            json={"amount": 5},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 0
