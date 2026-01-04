from ..domain.money import Money
from ..interfaces.payment_gateway import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Фейковый платежный шлюз для тестов."""
    
    def charge(self, order_id: str, amount: Money) -> bool:
        """
        Всегда возвращает True для упрощения.
        В реальной системе здесь была бы интеграция с платежной системой.
        """
        print(f"[FakePaymentGateway] Списание {amount} для заказа {order_id}")
        return True
