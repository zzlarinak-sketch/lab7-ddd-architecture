from enum import Enum


class OrderStatus(Enum):
    """Статусы заказа."""
    CREATED = "created"
    PAID = "paid"
    CANCELLED = "cancelled"
    
    def __str__(self) -> str:
        return self.value
