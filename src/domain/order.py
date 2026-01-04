from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from decimal import Decimal
from .money import Money
from .status import OrderStatus


@dataclass
class OrderLine:
    """Строка заказа (часть агрегата)."""
    product_id: str
    product_name: str
    price: Money
    quantity: int
    
    def total(self) -> Money:
        return self.price * self.quantity
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Количество должно быть положительным")


@dataclass
class Order:
    """Агрегат заказа."""
    id: str
    customer_id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: datetime = None
    
    def add_line(self, product_id: str, product_name: str, price: Money, quantity: int):
        """Добавить строку в заказ."""
        if self.status == OrderStatus.PAID:
            raise ValueError("Нельзя изменять оплаченный заказ")
        
        line = OrderLine(
            product_id=product_id,
            product_name=product_name,
            price=price,
            quantity=quantity
        )
        self.lines.append(line)
    
    def total_amount(self) -> Money:
        """Общая сумма заказа."""
        if not self.lines:
            return Money(Decimal('0'))
        
        total = self.lines[0].total()
        for line in self.lines[1:]:
            total = total + line.total()
        return total
    
    def pay(self):
        """Оплатить заказ."""
        if self.status == OrderStatus.PAID:
            raise ValueError("Заказ уже оплачен")
        
        if not self.lines:
            raise ValueError("Нельзя оплатить пустой заказ")
        
        self.status = OrderStatus.PAID
        self.paid_at = datetime.now()
    
    def can_be_paid(self) -> bool:
        """Можно ли оплатить заказ."""
        return (
            self.status == OrderStatus.CREATED and
            len(self.lines) > 0
        )
    
    def __str__(self) -> str:
        return f"Order {self.id} ({self.status.value}) - {self.total_amount()}"
