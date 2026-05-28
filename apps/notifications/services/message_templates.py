"""
Plantillas de mensajes para notificaciones.
Cada función retorna el texto formateado listo para enviar.
"""
from datetime import datetime


def reminder_message(
    client_name: str,
    service_name: str,
    date: str,
    time: str,
    specialist_name: str = ''
) -> str:
    """
    Mensaje de recordatorio de cita.
    Se envía 24h y 2h antes de la cita.
    """
    specialist_line = f' con {specialist_name}' if specialist_name else ''
    return (
        f'Hola {client_name} 👋\n\n'
        f'Te recordamos que tienes una cita en *Diana Nails*{specialist_line}.\n\n'
        f'💅 Servicio: {service_name}\n'
        f'📅 Fecha: {date}\n'
        f'⏰ Hora: {time}\n\n'
        f'📍 Dirección: [Dirección del spa]\n\n'
        f'Si necesitas cancelar o reagendar, por favor avísanos '
        f'con al menos 2 horas de anticipación.\n\n'
        f'¡Te esperamos! 💕'
    )


def confirmation_message(
    client_name: str,
    service_name: str,
    date: str,
    time: str,
    price: str = ''
) -> str:
    """
    Mensaje de confirmación de cita.
    Se envía cuando la cita cambia a estado 'confirmed'.
    """
    price_line = f'\n💰 Valor: ${price}' if price else ''
    return (
        f'✅ *Cita confirmada* {client_name}.\n\n'
        f'Servicio: {service_name}{price_line}\n'
        f'Fecha: {date}\n'
        f'Hora: {time}\n\n'
        f'¡Gracias por preferir Diana Nails! 💅\n'
        f'Te esperamos para consentirte.'
    )


def cancellation_message(
    client_name: str,
    service_name: str,
    date: str,
    reason: str = ''
) -> str:
    """
    Mensaje de cancelación de cita.
    """
    reason_line = f'\nMotivo: {reason}' if reason else ''
    return (
        f'Hola {client_name},\n\n'
        f'Tu cita de *{service_name}* del día {date} '
        f'ha sido cancelada.{reason_line}\n\n'
        f'Si deseas reagendar, contáctanos y con gusto '
        f'te asignamos un nuevo horario.\n\n'
        f'💅 Diana Nails'
    )


def follow_up_message(
    client_name: str,
    service_name: str,
    date: str
) -> str:
    """
    Mensaje de seguimiento post-servicio.
    Se envía al día siguiente de la cita completada.
    """
    return (
        f'Hola {client_name} 🌸\n\n'
        f'Esperamos que hayas disfrutado tu servicio de '
        f'{service_name} en Diana Nails.\n\n'
        f'Si tienes alguna recomendación o sugerencia, '
        f'nos encantaría escucharla.\n\n'
        f'¡Te esperamos pronto! 💅\n'
        f'*Diana Nails — Tu spa de confianza*'
    )


def reschedule_message(
    client_name: str,
    service_name: str,
    old_date: str,
    new_date: str,
    new_time: str
) -> str:
    """
    Mensaje cuando se reagenda una cita.
    """
    return (
        f'Hola {client_name} 👋\n\n'
        f'Tu cita de *{service_name}* ha sido reagendada.\n\n'
        f'📅 *Fecha anterior:* {old_date}\n'
        f'📅 *Nueva fecha:* {new_date}\n'
        f'⏰ *Nueva hora:* {new_time}\n\n'
        f'Gracias por tu comprensión.\n'
        f'💅 Diana Nails'
    )
