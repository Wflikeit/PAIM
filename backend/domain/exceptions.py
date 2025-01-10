from typing import Any


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
    def __init__(self, entity_name: str, message: str):
        super().__init__(f"ID of {entity_name} is invalid: {message}")


class InvalidDateType(RepositoryError):
    def __init__(self, date: Any, entity_name: str):
        super().__init__(
            f"Date: {date} in {entity_name} is in invalid"
            f"type: should be datetime, is {type(date).__name__}"
        )


class EntityLinkError(RepositoryError):
    def __init__(self, entity1: str, entity2: str):
        super().__init__(f"Failed to link {entity1} to {entity2}")


class BusinessLogicError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def to_dict(self):
        return {"error": self.message}


class UnableToRealizeOrderError(BusinessLogicError):
    def __init__(self):
        super().__init__("Unable to realize order")
