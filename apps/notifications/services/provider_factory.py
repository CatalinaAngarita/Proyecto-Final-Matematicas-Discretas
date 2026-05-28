"""
Factory de proveedores de notificaciones.
Retorna la implementación concreta según la configuración en .env
"""
from decouple import config
import logging
from .base import NotificationProvider
from .meta_provider import MetaWhatsAppProvider
from .twilio_provider import TwilioWhatsAppProvider

logger = logging.getLogger(__name__)


class ProviderFactory:
    """
    Factory que selecciona el proveedor de mensajería activo.

    La variable WHATSAPP_PROVIDER en .env define cuál usar:
    - 'meta' (default) → MetaWhatsAppProvider
    - 'twilio' → TwilioWhatsAppProvider

    Uso:
        provider = ProviderFactory.get_provider()
        result = provider.send_message('+573001112233', 'Hola')
    """

    _providers = {
        'meta': MetaWhatsAppProvider,
        'twilio': TwilioWhatsAppProvider,
    }

    @classmethod
    def get_provider(cls, name: str = '') -> NotificationProvider:
        """
        Retorna la instancia del proveedor configurado.

        Args:
            name: Nombre del proveedor. Si está vacío, usa WHATSAPP_PROVIDER del .env

        Returns:
            Instancia concreta de NotificationProvider

        Raises:
            ValueError: Si el proveedor no está soportado
        """
        if not name:
            name = config('WHATSAPP_PROVIDER', default='meta').lower()

        provider_class = cls._providers.get(name)
        if not provider_class:
            supported = ', '.join(cls._providers.keys())
            raise ValueError(
                f'Proveedor "{name}" no soportado. '
                f'Usa uno de: {supported}'
            )

        provider = provider_class()
        logger.info(f'Provider seleccionado: {provider.get_provider_name()}')
        return provider

    @classmethod
    def register_provider(cls, name: str, provider_class):
        """
        Permite registrar proveedores personalizados.

        Args:
            name: Nombre único del proveedor
            provider_class: Clase que implementa NotificationProvider
        """
        cls._providers[name] = provider_class
        logger.info(f'Provider registrado: {name}')
