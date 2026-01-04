from decimal import Decimal
from typing import Tuple
from ..domain.order import Order
from ..domain.money import Money
from ..interfaces.repositories import OrderRepository
from ..interfaces.payment_gateway import PaymentGateway


class PayOrderUseCase:
    """Use Case для оплаты заказа."""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_gateway: PaymentGateway
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> Tuple[bool, str]:
        """
        Оплатить заказ.
        
        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        # 1. Загружаем заказ
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return False, f"Заказ {order_id} не найден"
        
        # 2. Проверяем можно ли оплатить
        if not order.can_be_paid():
            return False, f"Заказ {order_id} нельзя оплатить"
        
        # 3. Выполняем доменную операцию
        try:
            order.pay()
        except ValueError as e:
            return False, str(e)
        
        # 4. Вызываем платежный шлюз
        amount = order.total_amount()
        success = self.payment_gateway.charge(order_id, amount)
        
        if not success:
            return False, "Ошибка платежа"
        
        # 5. Сохраняем заказ
        self.order_repository.save(order)
        
        return True, f"Заказ {order_id} успешно оплачен на сумму {amount}"
