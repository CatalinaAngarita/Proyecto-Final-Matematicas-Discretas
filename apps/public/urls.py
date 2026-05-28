from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.booking_step1, name='step1'),
    path('horario/', views.booking_step2, name='step2'),
    path('confirmar/', views.booking_step3, name='step3'),
    path('exito/<uuid:appointment_id>/', views.booking_success, name='success'),
]
