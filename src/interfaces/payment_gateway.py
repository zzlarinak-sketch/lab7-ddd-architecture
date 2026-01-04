from abc import ABC, abstractmethod
from ..domain.money import Money


class PaymentGateway(ABC):
    """Интерфейс платежного шлюза."""
    
    @abstractmethod
    def charge(self, order_id: str, amount: Money) -> bool:
        """
        Списать деньги.
        
        Returns:
            bool: True если платеж прошел успешно
        """
        pass
