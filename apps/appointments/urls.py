from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='list'),
    path('create/', views.AppointmentCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.AppointmentDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.AppointmentUpdateView.as_view(), name='update'),
    path('<uuid:pk>/cancel/', views.AppointmentCancelView.as_view(), name='cancel'),
    path('<uuid:pk>/delete/', views.AppointmentDeleteView.as_view(), name='delete'),
]
