from datetime import datetime, date
from uuid import UUID
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError

from apps.core.models import ServiceMainCategory, Testimonial
from apps.services.models import Service
from apps.specialists.models import Specialist
from apps.appointments.models import Appointment

from .forms import ServiceSelectionForm, DateTimeSelectionForm, ClientInfoForm
from .services.validation_service import get_available_slots_for_service
from .services.booking_service import create_booking


def booking_step1(request):
    form = ServiceSelectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        service = form.cleaned_data['service']
        request.session['booking_service_id'] = str(service.id)
        request.session['booking_service_name'] = service.name
        request.session['booking_service_duration'] = service.duration_minutes
        request.session['booking_service_price'] = str(service.price)
        return redirect('public:step2')

    services = Service.objects.filter(is_active=True).select_related('service_category')
    categories_order = ['nail', 'eyebrow', 'lash', 'waxing', 'other']
    category_labels = dict(ServiceMainCategory.choices)
    grouped = {}
    for cat in categories_order:
        cat_services = [s for s in services if s.category == cat]
        if cat_services:
            grouped[cat] = {
                'label': category_labels.get(cat, cat),
                'services': cat_services,
            }
    for s in services:
        if s.category not in categories_order:
            grouped.setdefault('other', {
                'label': 'Otros',
                'services': [],
            })['services'].append(s)

    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    return render(request, 'public/booking_step1_service.html', {
        'form': form,
        'grouped_services': grouped,
        'testimonials': testimonials,
    })


def booking_step2(request):
    service_id = request.session.get('booking_service_id')
    if not service_id:
        return redirect('public:step1')

    service = get_object_or_404(Service, id=service_id, is_active=True)
    specialist = Specialist.objects.filter(is_active=True, is_primary=True).first()
    if not specialist:
        messages.error(request, 'No hay especialistas disponibles en este momento.')
        return redirect('public:step1')

    slots = []
    selected_date = request.POST.get('date') or request.GET.get('date')
    show_slots = False

    if request.method == 'POST':
        selected_date = request.POST.get('date')
        if selected_date:
            try:
                parsed_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
                today = date.today()
                if parsed_date < today:
                    messages.warning(request, 'La fecha debe ser hoy o posterior.')
                else:
                    slots = get_available_slots_for_service(
                        specialist.id, parsed_date, service.duration_minutes
                    )
                    show_slots = True

                    # Dar feedback sobre por qué no hay slots
                    if not slots:
                        day_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                        day_name = day_names[parsed_date.weekday()]
                        messages.info(
                            request,
                            f'No hay horarios disponibles para {day_name} {selected_date}. '
                            f'Intenta con otra fecha o verifica que la especialista tenga horarios configurados.'
                        )
            except ValueError:
                messages.error(request, 'Fecha inválida.')

    if request.method == 'POST' and 'time_slot' in request.POST:
        time_str = request.POST.get('time_slot')
        if time_str and selected_date:
            request.session['booking_date'] = selected_date
            request.session['booking_time'] = time_str
            return redirect('public:step3')

    form = DateTimeSelectionForm(
        data=request.POST or None,
        slots=slots,
    )

    return render(request, 'public/booking_step2_datetime.html', {
        'form': form,
        'service': service,
        'selected_date': selected_date,
        'slots': slots,
        'show_slots': show_slots,
        'specialist': specialist,
    })


def booking_step3(request):
    service_id = request.session.get('booking_service_id')
    selected_date = request.session.get('booking_date')
    selected_time = request.session.get('booking_time')

    if not all([service_id, selected_date, selected_time]):
        return redirect('public:step1')

    service = get_object_or_404(Service, id=service_id, is_active=True)
    specialist = Specialist.objects.filter(is_active=True, is_primary=True).first()

    form = ClientInfoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']

        try:
            parsed_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            parsed_time = datetime.strptime(selected_time, '%H:%M').time()

            appointment = create_booking(
                service_id=service.id,
                specialist_id=specialist.id,
                appointment_date=parsed_date,
                start_time=parsed_time,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
            )

            request.session.pop('booking_service_id', None)
            request.session.pop('booking_service_name', None)
            request.session.pop('booking_service_duration', None)
            request.session.pop('booking_service_price', None)
            request.session.pop('booking_date', None)
            request.session.pop('booking_time', None)

            return redirect('public:success', appointment_id=appointment.id)

        except (ValidationError, Service.DoesNotExist, Specialist.DoesNotExist) as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al crear la cita: {str(e)}')

    return render(request, 'public/booking_step3_confirm.html', {
        'form': form,
        'service': service,
        'date': selected_date,
        'time': selected_time,
    })


def booking_success(request, appointment_id):
    appointment = get_object_or_404(
        Appointment.objects.select_related('client', 'service', 'specialist'),
        id=appointment_id,
    )
    return render(request, 'public/booking_success.html', {
        'appointment': appointment,
    })
