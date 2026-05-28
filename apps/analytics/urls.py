from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('cancellations/', views.CancellationStatsListView.as_view(), name='cancellation_stats'),
    path('services/', views.ServiceStatsListView.as_view(), name='service_stats'),
]
