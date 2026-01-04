Лаба 7 - Архитектура, слои и DDD-lite

Описание

Система оплаты заказа с разделением по слоям и доменной моделью.

Архитектура

Domain: Order, OrderLine, Money, OrderStatus
Application: PayOrderUseCase
Interfaces: OrderRepository, PaymentGateway
Infrastructure: InMemoryOrderRepository, FakePaymentGateway
Тесты

Тесты покрывают все требования:

Успешная оплата корректного заказа
Ошибка при оплате пустого заказа
Ошибка при повторной оплате
Невозможность изменения заказа после оплаты
Корректный расчет итоговой суммы
