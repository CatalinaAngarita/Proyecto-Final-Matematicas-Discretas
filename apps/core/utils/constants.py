"""
Módulo de constantes del sistema.
Las definiciones PRINCIPALES están en apps.core.models como TextChoices.
Este archivo re-exporta para conveniencia y mantiene valores fijos del negocio.
"""
from apps.core.models import (
    AppointmentStatus,
    NotificationType,
    NotificationStatus,
    ServiceMainCategory,
    BusinessDayChoices,
)

# Re-export de choices para uso en forms, templates, etc.
APPOINTMENT_STATUS_CHOICES = AppointmentStatus.choices
NOTIFICATION_TYPE_CHOICES = NotificationType.choices
NOTIFICATION_STATUS_CHOICES = NotificationStatus.choices
SERVICE_CATEGORY_CHOICES = ServiceMainCategory.choices
BUSINESS_DAYS = BusinessDayChoices.choices

# Constantes individuales (para comparaciones directas)
APPOINTMENT_PENDING = AppointmentStatus.PENDING
APPOINTMENT_CONFIRMED = AppointmentStatus.CONFIRMED
APPOINTMENT_IN_PROGRESS = AppointmentStatus.IN_PROGRESS
APPOINTMENT_COMPLETED = AppointmentStatus.COMPLETED
APPOINTMENT_CANCELLED = AppointmentStatus.CANCELLED
APPOINTMENT_NO_SHOW = AppointmentStatus.NO_SHOW

NOTIFICATION_REMINDER = NotificationType.REMINDER
NOTIFICATION_CONFIRMATION = NotificationType.CONFIRMATION
NOTIFICATION_CANCELLATION = NotificationType.CANCELLATION
NOTIFICATION_FOLLOW_UP = NotificationType.FOLLOW_UP

# ---------------------------------------------------------------------------
# BUSINESS HOURS (valores fijos del spa)
# ---------------------------------------------------------------------------
MORNING_START = '08:00'
MORNING_END = '12:00'
AFTERNOON_START = '13:00'
AFTERNOON_END = '20:00'

# ---------------------------------------------------------------------------
# NAMING
# ---------------------------------------------------------------------------
SYSTEM_NAME = 'Diana Nails Smart Booking'
SYSTEM_SHORT_NAME = 'Diana Nails'
