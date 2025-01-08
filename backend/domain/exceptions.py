class RepositoryError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def to_dict(self):
        return {"error": self.message}


class EntityNotFoundError(RepositoryError):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(f"{entity_name} with ID {entity_id} not found")


class InvalidIdError(RepositoryError):
    def __init__(self, product_id: str, message: str):
        super().__init__(f"ID: {product_id} is invalid: {message}")
