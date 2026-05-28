"""
Módulo de integración con WhatsApp API.
Preparado para conectar con:
- Meta Cloud API
- Twilio WhatsApp API
- WATI
- O cualquier proveedor compatible con REST.

Implementación base para ser completada cuando se tenga acceso a la API.
"""
from decouple import config
import requests
import json
import logging

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """
    Cliente base para integración WhatsApp.
    Diseñado para ser extensible con diferentes proveedores.
    """

    def __init__(self):
        self.api_url = config('WHATSAPP_API_URL', default='')
        self.api_token = config('WHATSAPP_API_TOKEN', default='')
        self.phone_number_id = config('WHATSAPP_PHONE_NUMBER_ID', default='')
        self.business_phone = config('WHATSAPP_BUSINESS_PHONE', default='')

    def is_configured(self) -> bool:
        return bool(self.api_url and self.api_token)

    def send_message(self, to: str, message: str) -> dict:
        """
        Envía un mensaje de texto vía WhatsApp.

        Args:
            to: Número de teléfono destino (formato internacional)
            message: Contenido del mensaje

        Returns:
            dict con la respuesta de la API
        """
        if not self.is_configured():
            logger.warning('WhatsApp no configurado. Mensaje no enviado.')
            return {'status': 'not_configured'}

        payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'text',
            'text': {'body': message},
        }

        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(
                f'{self.api_url}/{self.phone_number_id}/messages',
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f'Error enviando WhatsApp: {e}')
            return {'status': 'error', 'message': str(e)}
