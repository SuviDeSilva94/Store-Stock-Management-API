import pytest
from fastapi.testclient import TestClient
class TestProductAPI:
    def test_create_product_success(self, client: TestClient):
        response = client.post(
            "/api/v1/products",
            json={
                "name": "Apple iPhone 16",
                "sku": "IP16-256-BLK",
                "stock": 20
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Apple iPhone 16"
        assert data["sku"] == "IP16-256-BLK"
        assert data["stock"] == 20
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    def test_create_product_duplicate_sku(self, client: TestClient):
        client.post(
            "/api/v1/products",
            json={"name": "Product 1", "sku": "TEST-001", "stock": 10}
        )
        response = client.post(
            "/api/v1/products",
            json={"name": "Product 2", "sku": "TEST-001", "stock": 5}
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    def test_create_product_invalid_data(self, client: TestClient):
        response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST", "stock": -5}
        )
        assert response.status_code == 422
    def test_get_all_products(self, client: TestClient):
        client.post("/api/v1/products", json={"name": "P1", "sku": "P1", "stock": 10})
        client.post("/api/v1/products", json={"name": "P2", "sku": "P2", "stock": 20})
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    def test_get_all_products_with_pagination(self, client: TestClient):
        for i in range(5):
            client.post(
                "/api/v1/products",
                json={"name": f"P{i}", "sku": f"P{i}", "stock": 10}
            )
        response = client.get("/api/v1/products?skip=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    def test_get_product_by_id_success(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.get(f"/api/v1/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Test"
    def test_get_product_by_id_not_found(self, client: TestClient):
        response = client.get("/api/v1/products/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    def test_update_product_success(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Old Name", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.put(
            f"/api/v1/products/{product_id}",
            json={"name": "New Name", "stock": 20}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["stock"] == 20
    def test_update_product_partial(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Old Name", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.put(
            f"/api/v1/products/{product_id}",
            json={"name": "New Name"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["stock"] == 10
    def test_update_product_not_found(self, client: TestClient):
        response = client.put(
            "/api/v1/products/999",
            json={"name": "Test"}
        )
        assert response.status_code == 404
    def test_delete_product_success(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.delete(f"/api/v1/products/{product_id}")
        assert response.status_code == 204
        get_response = client.get(f"/api/v1/products/{product_id}")
        assert get_response.status_code == 404
    def test_delete_product_not_found(self, client: TestClient):
        response = client.delete("/api/v1/products/999")
        assert response.status_code == 404
    def test_increment_stock_success(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/increment",
            json={"amount": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 15
    def test_increment_stock_default_amount(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.post(f"/api/v1/products/{product_id}/increment")
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 11
    def test_increment_stock_invalid_amount(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/increment",
            json={"amount": 0}
        )
        assert response.status_code == 422
    def test_decrement_stock_success(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 10}
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/decrement",
            json={"amount": 3}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 7
    def test_decrement_stock_to_zero(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 5}
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/decrement",
            json={"amount": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stock"] == 0
    def test_decrement_stock_insufficient(self, client: TestClient):
        create_response = client.post(
            "/api/v1/products",
            json={"name": "Test", "sku": "TEST-001", "stock": 5}
        )
        product_id = create_response.json()["id"]
        response = client.post(
            f"/api/v1/products/{product_id}/decrement",
            json={"amount": 10}
        )
        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
