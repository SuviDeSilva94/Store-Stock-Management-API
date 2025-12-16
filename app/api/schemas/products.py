from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    sku: str = Field(..., min_length=1, max_length=50, description="Stock Keeping Unit")
    stock: int = Field(default=0, ge=0, description="Current stock level")


class ProductCreate(ProductBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Apple iPhone 16",
                "sku": "IP16-256-BLK",
                "stock": 20
            }
        }
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    stock: Optional[int] = Field(None, ge=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Name",
                "stock": 10
            }
        }
    )


class ProductResponse(ProductBase):
    id: int = Field(..., description="Unique product identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Apple iPhone 16",
                "sku": "IP16-256-BLK",
                "stock": 20,
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:30:00Z"
            }
        }
    )


class StockAdjustment(BaseModel):
    amount: int = Field(default=1, gt=0, description="Amount to adjust stock by")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 5
            }
        }
    )


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Product with ID 123 not found"
            }
        }
    )
