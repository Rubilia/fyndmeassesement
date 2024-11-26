from threading import Lock
from pydantic import BaseModel, Field, UUID4
from typing import Literal, Optional

CATEGORIES = [
    "Electronics", "Home Appliances", "Books", "Fashion", "Toys",
    "Furniture", "Groceries", "Fitness", "Beauty", "Automotive"
]

class Product(BaseModel):
    id: UUID4  # Validate as a UUID
    name: str = Field(min_length=6, description="Product name must be at least 6 characters long")
    description: str
    price: float = Field(gt=0, description="Price must be greater than 0")
    quantity: int = Field(ge=1, le=10, description="Quantity must be between 1 and 10")
    category: Literal[
        "Electronics", "Home Appliances", "Books", "Fashion", "Toys",
        "Furniture", "Groceries", "Fitness", "Beauty", "Automotive"
    ]


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=6)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=1, le=10)
    category: Optional[str] = None


def validate_product_update(data):
    return ProductUpdate(**data)


# Shared in-memory data structure. In the future can be expanded to interact with Database or Redis for processing parallelism as opposed to threading
products = {}
product_lock = Lock()
