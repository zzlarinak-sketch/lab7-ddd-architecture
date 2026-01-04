from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """Value Object для работы с денежными суммами."""
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < Decimal('0'):
            raise ValueError("Сумма не может быть отрицательной")
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Нельзя складывать разные валюты")
        return Money(self.amount + other.amount, self.currency)
    
    def __mul__(self, quantity: int) -> 'Money':
        return Money(self.amount * Decimal(quantity), self.currency)
    
    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"
