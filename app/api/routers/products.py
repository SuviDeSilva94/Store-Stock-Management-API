from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.api.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    StockAdjustment,
    ErrorResponse
)
from app.api.dependency_factories import get_product_service
from app.api.error_handlers import handle_service_error
from app.domain.services import ProductService
from app.core.exceptions import (
    ProductNotFoundError,
    DuplicateSKUError,
    InvalidAmountError,
    InsufficientStockError
)


router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    responses={
        201: {"description": "Product created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input or duplicate SKU"}
    }
)
def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    try:
        created = service.create_product(
            name=product.name,
            sku=product.sku,
            stock=product.stock
        )
        return ProductResponse.model_validate(created)
    
    except (DuplicateSKUError, InvalidAmountError) as e:
        raise handle_service_error(e)


@router.get(
    "",
    response_model=List[ProductResponse],
    summary="Get all products",
    responses={
        200: {"description": "List of products"}
    }
)
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service)
) -> List[ProductResponse]:
    products = service.get_all_products(skip=skip, limit=limit)
    return [ProductResponse.model_validate(p) for p in products]


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
    responses={
        200: {"description": "Product found"},
        404: {"model": ErrorResponse, "description": "Product not found"}
    }
)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    try:
        product = service.get_product_by_id(product_id)
        return ProductResponse.model_validate(product)
    
    except ProductNotFoundError as e:
        raise handle_service_error(e)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
    responses={
        200: {"description": "Product updated"},
        404: {"model": ErrorResponse, "description": "Product not found"},
        400: {"model": ErrorResponse, "description": "Invalid input"}
    }
)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    try:
        updated = service.update_product(
            product_id=product_id,
            name=product_update.name,
            stock=product_update.stock
        )
        return ProductResponse.model_validate(updated)
    
    except (ProductNotFoundError, InvalidAmountError) as e:
        raise handle_service_error(e)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    responses={
        204: {"description": "Product deleted"},
        404: {"model": ErrorResponse, "description": "Product not found"}
    }
)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
) -> None:
    try:
        service.delete_product(product_id)
    
    except ProductNotFoundError as e:
        raise handle_service_error(e)


@router.post(
    "/{product_id}/increment",
    response_model=ProductResponse,
    summary="Increment product stock",
    responses={
        200: {"description": "Stock incremented"},
        400: {"model": ErrorResponse, "description": "Invalid amount"},
        404: {"model": ErrorResponse, "description": "Product not found"}
    }
)
def increment_stock(
    product_id: int,
    adjustment: StockAdjustment = StockAdjustment(),
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    try:
        updated = service.increment_stock(
            product_id=product_id,
            amount=adjustment.amount
        )
        return ProductResponse.model_validate(updated)
    
    except (ProductNotFoundError, InvalidAmountError) as e:
        raise handle_service_error(e)


@router.post(
    "/{product_id}/decrement",
    response_model=ProductResponse,
    summary="Decrement product stock",
    responses={
        200: {"description": "Stock decremented"},
        400: {"model": ErrorResponse, "description": "Invalid amount or insufficient stock"},
        404: {"model": ErrorResponse, "description": "Product not found"}
    }
)
def decrement_stock(
    product_id: int,
    adjustment: StockAdjustment = StockAdjustment(),
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    try:
        updated = service.decrement_stock(
            product_id=product_id,
            amount=adjustment.amount
        )
        return ProductResponse.model_validate(updated)
    
    except (ProductNotFoundError, InvalidAmountError, InsufficientStockError) as e:
        raise handle_service_error(e)
