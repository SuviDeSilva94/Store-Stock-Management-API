from fastapi import HTTPException, status
from app.core.exceptions import (
    ApplicationError,
    ProductNotFoundError,
    DuplicateSKUError,
    InvalidAmountError,
    InsufficientStockError
)


def handle_service_error(error: Exception) -> HTTPException:
    if isinstance(error, ProductNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.message
        )
    
    if isinstance(error, DuplicateSKUError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.message
        )
    
    if isinstance(error, InvalidAmountError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.message
        )
    
    if isinstance(error, InsufficientStockError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.message
        )
    
    if isinstance(error, ApplicationError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error.message
        )
    
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred"
    )


EXCEPTION_STATUS_MAP = {
    ProductNotFoundError: status.HTTP_404_NOT_FOUND,
    DuplicateSKUError: status.HTTP_400_BAD_REQUEST,
    InvalidAmountError: status.HTTP_400_BAD_REQUEST,
    InsufficientStockError: status.HTTP_400_BAD_REQUEST,
    ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def handle_service_error_v2(error: Exception) -> HTTPException:
    status_code = EXCEPTION_STATUS_MAP.get(
        type(error),
        status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    
    detail = getattr(error, 'message', "An unexpected error occurred")
    
    return HTTPException(status_code=status_code, detail=detail)
