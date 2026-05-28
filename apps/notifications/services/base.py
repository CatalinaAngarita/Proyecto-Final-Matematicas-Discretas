"""
Provider base abstracto para envío de notificaciones.
Define el contrato que TODOS los proveedores deben implementar.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class NotificationProvider(ABC):
    """
    Interfaz común para todos los proveedores de mensajería.

    Cualquier nuevo proveedor (Meta, Twilio, WATI, etc.)
    debe heredar de esta clase e implementar send_message().
    """

    @abstractmethod
    def send_message(self, to: str, message: str) -> Dict:
        """
        Envía un mensaje de texto.

        Args:
            to: Número de teléfono destino (formato internacional, ej: +573001112233)
            message: Contenido del mensaje a enviar

        Returns:
            dict con:
                - success: bool
                - provider_message_id: str (ID del mensaje en el proveedor)
                - raw_response: dict (respuesta completa de la API)
                - error: str (mensaje de error si falló)
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Retorna el nombre único del proveedor (meta, twilio, etc.)."""
        pass

    def is_configured(self) -> bool:
        """
        Verifica si el proveedor tiene la configuración necesaria.
        Se sobreescribe en cada implementación concreta.
        """
        return True

    def validate_phone(self, phone: str) -> bool:
        """Validación básica de formato de teléfono internacional."""
        if not phone.startswith('+'):
            logger.warning(f'Número inválido (debe empezar con +): {phone}')
            return False
        digits = phone[1:].replace(' ', '')
        if not digits.isdigit():
            logger.warning(f'Número inválido (solo dígitos después del +): {phone}')
            return False
        if len(digits) < 10 or len(digits) > 15:
            logger.warning(f'Número inválido (longitud incorrecta): {phone}')
            return False
        return True
