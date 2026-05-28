from datetime import datetime, date, time, timedelta
from uuid import UUID
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.appointments.models import Appointment
from apps.core.models import AppointmentStatus
from apps.specialists.models import Specialist
from apps.services.models import Service

from .client_registration import get_or_create_client
from .validation_service import validate_booking


def create_booking(
    service_id: UUID,
    specialist_id: UUID,
    appointment_date: date,
    start_time: time,
    first_name: str,
    last_name: str,
    phone: str,
) -> Appointment:
    service = Service.objects.get(id=service_id, is_active=True)
    specialist = Specialist.objects.get(id=specialist_id, is_active=True)

    duration = service.duration_minutes
    start_dt = datetime.combine(appointment_date, start_time)
    end_dt = start_dt + timedelta(minutes=duration)
    end_time = end_dt.time()

    validate_booking(specialist_id, appointment_date, start_time, end_time)

    client = get_or_create_client(first_name, last_name, phone)

    appointment = Appointment.objects.create(
        client=client,
        specialist=specialist,
        service=service,
        date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        status=AppointmentStatus.PENDING,
    )

    return appointment
