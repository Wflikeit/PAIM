class RepositoryError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def to_dict(self):
        return {"error": self.message}


class ClientNotFoundError(RepositoryError):
    def __init__(self, user_id: str):
        super().__init__(f"Client with ID {user_id} not found")


class ProductNotFoundError(RepositoryError):
    def __init__(self, product_id: str):
        super().__init__(f"Product with ID {product_id} not found")


class ProductImageNotFoundError(RepositoryError):
    def __init__(self, product_id: str):
        super().__init__(f"Image for product with ID {product_id} not found")
