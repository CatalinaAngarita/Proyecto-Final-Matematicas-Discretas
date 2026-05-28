from django.urls import path
from . import views

app_name = 'specialists'

urlpatterns = [
    path('', views.SpecialistListView.as_view(), name='list'),
    path('create/', views.SpecialistCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.SpecialistUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.SpecialistDeleteView.as_view(), name='delete'),
]
