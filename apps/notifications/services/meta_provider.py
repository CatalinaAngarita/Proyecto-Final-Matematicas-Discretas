"""
Proveedor: Meta WhatsApp Cloud API.
Documentación: https://developers.facebook.com/docs/whatsapp/cloud-api
"""
from decouple import config
import requests
import logging
from .base import NotificationProvider

logger = logging.getLogger(__name__)


class MetaWhatsAppProvider(NotificationProvider):
    """
    Implementación para Meta WhatsApp Cloud API v21.0+.

    Variables de entorno requeridas:
    - WHATSAPP_API_URL (ej: https://graph.facebook.com/v21.0)
    - WHATSAPP_API_TOKEN (token de acceso permanente)
    - WHATSAPP_PHONE_NUMBER_ID (ID del número de teléfono Business)
    - WHATSAPP_BUSINESS_PHONE (número que envía, ej: 15551234567)
    """

    def __init__(self):
        self.api_url = config('WHATSAPP_API_URL', default='').rstrip('/')
        self.api_token = config('WHATSAPP_API_TOKEN', default='')
        self.phone_number_id = config('WHATSAPP_PHONE_NUMBER_ID', default='')
        self.business_phone = config('WHATSAPP_BUSINESS_PHONE', default='')
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update({
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json',
            })
        return self._session

    def get_provider_name(self) -> str:
        return 'meta'

    def is_configured(self) -> bool:
        return bool(self.api_url and self.api_token and self.phone_number_id)

    def send_message(self, to: str, message: str) -> dict:
        """
        Envía mensaje de texto vía Meta WhatsApp Cloud API.

        Args:
            to: Número destino en formato internacional (+573001112233)
            message: Texto del mensaje

        Returns:
            dict con resultado estandarizado
        """
        if not self.is_configured():
            logger.warning('[Meta] WhatsApp no configurado. Revisa .env')
            return {
                'success': False,
                'provider_message_id': '',
                'error': 'Provider not configured',
            }

        if not self.validate_phone(to):
            return {
                'success': False,
                'provider_message_id': '',
                'error': f'Invalid phone number: {to}',
            }

        payload = {
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': to,
            'type': 'text',
            'text': {
                'preview_url': False,
                'body': message,
            },
        }

        url = f'{self.api_url}/{self.phone_number_id}/messages'

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            whatsapp_id = (
                data.get('messages', [{}])[0].get('id', '')
            )
            logger.info(f'[Meta] Mensaje enviado a {to}, ID: {whatsapp_id}')
            return {
                'success': True,
                'provider_message_id': whatsapp_id,
                'raw_response': data,
                'error': '',
            }

        except requests.exceptions.Timeout:
            logger.error(f'[Meta] Timeout enviando mensaje a {to}')
            return {
                'success': False,
                'provider_message_id': '',
                'error': 'Timeout connecting to Meta API',
            }

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else 0
            error_body = e.response.text if e.response else ''
            logger.error(
                f'[Meta] HTTP {status_code} enviando a {to}: {error_body}'
            )
            return {
                'success': False,
                'provider_message_id': '',
                'error': f'HTTP {status_code}: {error_body[:200]}',
            }

        except requests.exceptions.RequestException as e:
            logger.error(f'[Meta] Error enviando mensaje a {to}: {e}')
            return {
                'success': False,
                'provider_message_id': '',
                'error': str(e),
            }

    def send_template_message(
        self, to: str, template_name: str, parameters: dict
    ) -> dict:
        """
        Envía un mensaje usando una plantilla aprobada por Meta.
        Útil para mensajes con formato enriquecido.

        Args:
            to: Número destino
            template_name: Nombre de la plantilla aprobada en Meta Business
            parameters: Diccionario con valores para los parámetros
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Not configured'}

        components = [
            {
                'type': 'body',
                'parameters': [
                    {'type': 'text', 'text': str(v)}
                    for v in parameters.values()
                ],
            }
        ]

        payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'template',
            'template': {
                'name': template_name,
                'language': {'code': 'es'},
                'components': components,
            },
        }

        url = f'{self.api_url}/{self.phone_number_id}/messages'

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return {
                'success': True,
                'provider_message_id': response.json().get('messages', [{}])[0].get('id', ''),
                'raw_response': response.json(),
                'error': '',
            }
        except requests.RequestException as e:
            logger.error(f'[Meta] Error template: {e}')
            return {'success': False, 'error': str(e)}
