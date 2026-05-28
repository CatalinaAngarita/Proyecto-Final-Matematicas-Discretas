"""
Script para poblar la base de datos con datos iniciales de ejemplo.
Ejecutar: python manage.py shell < scripts/seed_data.py
"""
from django.contrib.auth.models import User
from apps.clients.models import Client
from apps.services.models import Service, ServiceCategory, NailApplicationType
from apps.specialists.models import Specialist
from apps.schedules.models import WorkSchedule

# ---------------------------------------------------------------------------
# Crear especialista principal: Diana
# ---------------------------------------------------------------------------
user, _ = User.objects.get_or_create(
    username='diana',
    defaults={'email': 'diana@diananails.com', 'first_name': 'Diana', 'last_name': 'Nails'}
)

specialist, _ = Specialist.objects.get_or_create(
    first_name='Diana',
    last_name='Nails',
    defaults={
        'phone': '+57 300 000 0000',
        'email': 'diana@diananails.com',
        'is_primary': True,
        'user': user,
    }
)

# ---------------------------------------------------------------------------
# Días laborales (Lun-Sáb)
# ---------------------------------------------------------------------------
for day in range(6):
    WorkSchedule.objects.get_or_create(
        specialist=specialist,
        day_of_week=day,
        defaults={
            'morning_start': '08:00',
            'morning_end': '12:00',
            'afternoon_start': '13:00',
            'afternoon_end': '20:00',
        }
    )

# ---------------------------------------------------------------------------
# Tipos de aplicación de uñas
# ---------------------------------------------------------------------------
nail_types = [
    'Acrílicas', 'Gel', 'Semipermanente', 'Polygel', 'Press-on',
    'Dip Powder', 'Tradiacional (esmalte)',
]
for name in nail_types:
    NailApplicationType.objects.get_or_create(name=name)

# ---------------------------------------------------------------------------
# Categorías
# ---------------------------------------------------------------------------
cat_nails, _ = ServiceCategory.objects.get_or_create(name='Uñas')
cat_eyebrows, _ = ServiceCategory.objects.get_or_create(name='Cejas')
cat_waxing, _ = ServiceCategory.objects.get_or_create(name='Depilación')

# ---------------------------------------------------------------------------
# Servicios de uñas (10+)
# ---------------------------------------------------------------------------
nail_services = [
    ('Manicura básica', 45, 35000),
    ('Pedicura básica', 45, 35000),
    ('Manicura + Pedicura', 75, 60000),
    ('Uñas acrílicas (completo)', 120, 120000),
    ('Uñas acrílicas (relleno)', 90, 80000),
    ('Uñas en gel (completo)', 120, 110000),
    ('Uñas en gel (relleno)', 90, 75000),
    ('Esmaltado semipermanente', 60, 45000),
    ('Retiro de uñas acrílicas/gel', 30, 20000),
    ('Decoración básica por uña', 15, 5000),
    ('Nail art avanzado', 60, 60000),
    ('Press-on personalizadas', 60, 55000),
    ('Tratamiento de cutículas', 30, 25000),
]

for name, duration, price in nail_services:
    Service.objects.get_or_create(
        name=name,
        defaults={
            'category': 'nail',
            'service_category': cat_nails,
            'duration_minutes': duration,
            'price': price,
        }
    )

# ---------------------------------------------------------------------------
# Servicios de cejas
# ---------------------------------------------------------------------------
eyebrow_services = [
    ('Diseño de cejas', 30, 25000),
    ('Henna en cejas', 30, 30000),
    ('Laminado de cejas', 45, 45000),
    ('Depilación de cejas con pinza', 15, 15000),
]

for name, duration, price in eyebrow_services:
    Service.objects.get_or_create(
        name=name,
        defaults={
            'category': 'eyebrow',
            'service_category': cat_eyebrows,
            'duration_minutes': duration,
            'price': price,
        }
    )

# ---------------------------------------------------------------------------
# Servicios de depilación
# ---------------------------------------------------------------------------
waxing_services = [
    ('Depilación de labio superior', 15, 15000),
    ('Depilación de cejas (cera)', 15, 15000),
    ('Depilación de axilas', 20, 20000),
    ('Depilación de piernas completas', 45, 50000),
    ('Depilación de medio brazo', 20, 25000),
]

for name, duration, price in waxing_services:
    Service.objects.get_or_create(
        name=name,
        defaults={
            'category': 'waxing',
            'service_category': cat_waxing,
            'duration_minutes': duration,
            'price': price,
        }
    )

# ---------------------------------------------------------------------------
# Clientas de ejemplo
# ---------------------------------------------------------------------------
sample_clients = [
    ('María', 'González', '+57 300 111 2233'),
    ('Carolina', 'Martínez', '+57 300 222 3344'),
    ('Andrea', 'López', '+57 300 333 4455'),
    ('Valentina', 'Ramírez', '+57 300 444 5566'),
    ('Laura', 'Hernández', '+57 300 555 6677'),
]

for first, last, phone in sample_clients:
    Client.objects.get_or_create(
        phone=phone,
        defaults={'first_name': first, 'last_name': last}
    )

print('✅ Datos iniciales cargados exitosamente.')
print(f'   - 1 especialista principal (Diana)')
print(f'   - {WorkSchedule.objects.count()} horarios laborales')
print(f'   - {NailApplicationType.objects.count()} tipos de uñas')
print(f'   - {Service.objects.count()} servicios')
print(f'   - {ServiceCategory.objects.count()} categorías')
print(f'   - {Client.objects.count()} clientas de ejemplo')
