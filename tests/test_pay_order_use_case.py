import pytest
from decimal import Decimal
from src.domain.order import Order, OrderLine
from src.domain.money import Money
from src.domain.status import OrderStatus
from src.infrastructure.repositories import InMemoryOrderRepository
from src.infrastructure.payment_gateway import FakePaymentGateway
from src.application.pay_order_use_case import PayOrderUseCase


class TestPayOrderUseCase:
    """Тесты Use Case оплаты заказа."""
    
    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.repository, self.payment_gateway)
    
    def test_successful_payment(self):
        """Успешная оплата корректного заказа."""
        # Создаем заказ
        order = Order(id="order-123", customer_id="customer-1")
        order.add_line("prod-1", "Книга", Money(Decimal("500")), 2)
        
        # Сохраняем заказ
        self.repository.save(order)
        
        # Оплачиваем
        success, message = self.use_case.execute("order-123")
        
        # Проверяем
        assert success is True
        assert "успешно оплачен" in message
        assert order.status == OrderStatus.PAID
        assert order.paid_at is not None
    
    def test_payment_empty_order(self):
        """Ошибка при оплате пустого заказа."""
        # Создаем пустой заказ
        order = Order(id="order-empty", customer_id="customer-1")
        self.repository.save(order)
        
        # Пытаемся оплатить
        success, message = self.use_case.execute("order-empty")
        
        # Проверяем
        assert success is False
        assert "пустой" in message.lower() or "нельзя" in message.lower()
    
    def test_double_payment(self):
        """Ошибка при повторной оплате."""
        # Создаем и оплачиваем заказ
        order = Order(id="order-paid", customer_id="customer-1")
        order.add_line("prod-1", "Книга", Money(Decimal("300")), 1)
        order.pay()
        self.repository.save(order)
        
        # Пытаемся оплатить еще раз
        success, message = self.use_case.execute("order-paid")
        
        # Проверяем
        assert success is False
        assert "уже оплачен" in message.lower() or "нельзя" in message.lower()
    
    def test_cannot_modify_after_payment(self):
        """Нельзя изменить заказ после оплаты."""
        # Создаем и оплачиваем заказ
        order = Order(id="order-modify", customer_id="customer-1")
        order.add_line("prod-1", "Книга", Money(Decimal("200")), 1)
        order.pay()
        
        # Пытаемся добавить строку
        with pytest.raises(ValueError) as exc:
            order.add_line("prod-2", "Ручка", Money(Decimal("50")), 3)
        
        assert "оплаченный" in str(exc.value)
    
    def test_correct_total_calculation(self):
        """Корректный расчет итоговой суммы."""
        order = Order(id="order-total", customer_id="customer-1")
        
        # Добавляем товары
        order.add_line("prod-1", "Книга", Money(Decimal("500")), 2)  # 1000
        order.add_line("prod-2", "Ручка", Money(Decimal("50")), 5)   # 250
        order.add_line("prod-3", "Блокнот", Money(Decimal("300")), 1) # 300
        
        # Проверяем сумму
        total = order.total_amount()
        assert total.amount == Decimal("1550")
        assert total.currency == "USD"
        
        # Проверяем что каждая строка считает правильно
        assert order.lines[0].total().amount == Decimal("1000")
        assert order.lines[1].total().amount == Decimal("250")
        assert order.lines[2].total().amount == Decimal("300")
    
    def test_order_not_found(self):
        """Ошибка если заказ не найден."""
        success, message = self.use_case.execute("non-existent-order")
        
        assert success is False
        assert "не найден" in message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
