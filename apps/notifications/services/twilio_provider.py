"""
Proveedor: Twilio WhatsApp API.
Documentación: https://www.twilio.com/docs/whatsapp/api

Twilio usa el mismo Sandbox/Producción de WhatsApp,
pero la URL y autenticación son diferentes a Meta.
"""
from decouple import config
import requests
import base64
import logging
from .base import NotificationProvider

logger = logging.getLogger(__name__)


class TwilioWhatsAppProvider(NotificationProvider):
    """
    Implementación para Twilio WhatsApp API.

    Variables de entorno requeridas:
    - TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN
    - TWILIO_WHATSAPP_NUMBER (ej: whatsapp:+14155238886)

    Twilio no requiere WHATSAPP_API_URL porque su endpoint es fijo:
    https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json
    """

    def __init__(self):
        self.account_sid = config('TWILIO_ACCOUNT_SID', default='')
        self.auth_token = config('TWILIO_AUTH_TOKEN', default='')
        self.from_number = config('TWILIO_WHATSAPP_NUMBER', default='')

    def get_provider_name(self) -> str:
        return 'twilio'

    def is_configured(self) -> bool:
        return bool(self.account_sid and self.auth_token and self.from_number)

    def _build_auth_header(self):
        """Auth básica: Base64(account_sid:auth_token)."""
        credentials = f'{self.account_sid}:{self.auth_token}'
        encoded = base64.b64encode(credentials.encode()).decode()
        return {'Authorization': f'Basic {encoded}'}

    def send_message(self, to: str, message: str) -> dict:
        """
        Envía mensaje vía Twilio WhatsApp API.

        Args:
            to: Número destino en formato internacional (+573001112233)
                 Internamente Twilio requiere formato 'whatsapp:+573001112233'
            message: Texto del mensaje

        Returns:
            dict con resultado estandarizado
        """
        if not self.is_configured():
            logger.warning('[Twilio] No configurado. Revisa .env')
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

        url = (
            f'https://api.twilio.com/2010-04-01/Accounts'
            f'/{self.account_sid}/Messages.json'
        )

        payload = {
            'To': f'whatsapp:{to}',
            'From': self.from_number,
            'Body': message,
        }

        try:
            response = requests.post(
                url,
                data=payload,
                headers=self._build_auth_header(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            twilio_sid = data.get('sid', '')
            logger.info(f'[Twilio] Mensaje enviado a {to}, SID: {twilio_sid}')
            return {
                'success': True,
                'provider_message_id': twilio_sid,
                'raw_response': data,
                'error': '',
            }

        except requests.exceptions.Timeout:
            logger.error(f'[Twilio] Timeout enviando a {to}')
            return {
                'success': False,
                'provider_message_id': '',
                'error': 'Timeout connecting to Twilio API',
            }

        except requests.exceptions.HTTPError as e:
            error_body = e.response.text if e.response else ''
            logger.error(f'[Twilio] HTTP Error: {error_body[:200]}')
            return {
                'success': False,
                'provider_message_id': '',
                'error': f'Twilio HTTP error: {error_body[:200]}',
            }

        except requests.exceptions.RequestException as e:
            logger.error(f'[Twilio] Error: {e}')
            return {
                'success': False,
                'provider_message_id': '',
                'error': str(e),
            }

    def send_media_message(self, to: str, message: str, media_url: str) -> dict:
        """
        Envía mensaje con imagen/documento vía Twilio.
        Útil para enviar catálogos de servicios o confirmaciones visuales.
        """
        url = (
            f'https://api.twilio.com/2010-04-01/Accounts'
            f'/{self.account_sid}/Messages.json'
        )

        payload = {
            'To': f'whatsapp:{to}',
            'From': self.from_number,
            'Body': message,
            'MediaUrl': media_url,
        }

        try:
            response = requests.post(
                url, data=payload,
                headers=self._build_auth_header(),
                timeout=30,
            )
            response.raise_for_status()
            return {'success': True, 'provider_message_id': response.json().get('sid', ''), 'error': ''}
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}
