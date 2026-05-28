"""
Script para crear superusuario inicial desde variables de entorno.
Ejecutar: python manage.py shell < scripts/create_superuser.py
"""
from decouple import config
from django.contrib.auth.models import User

username = config('ADMIN_USERNAME', default='admin')
email = config('ADMIN_EMAIL', default='admin@diananails.com')
password = config('ADMIN_PASSWORD', default='admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superusuario "{username}" creado exitosamente.')
else:
    print(f'El superusuario "{username}" ya existe.')
