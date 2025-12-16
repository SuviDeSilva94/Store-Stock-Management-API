class ApplicationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ProductServiceError(ApplicationError):
    pass


class ProductNotFoundError(ProductServiceError):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class DuplicateSKUError(ProductServiceError):
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"Product with SKU '{sku}' already exists")


class InsufficientStockError(ProductServiceError):
    def __init__(self, current_stock: int, requested_amount: int):
        self.current_stock = current_stock
        self.requested_amount = requested_amount
        super().__init__(
            f"Insufficient stock: current={current_stock}, "
            f"requested={requested_amount}"
        )


class InvalidAmountError(ProductServiceError):
    def __init__(self, amount: int, reason: str = "Amount must be positive"):
        self.amount = amount
        self.reason = reason
        super().__init__(f"Invalid amount {amount}: {reason}")


class ValidationError(ApplicationError):
    pass
