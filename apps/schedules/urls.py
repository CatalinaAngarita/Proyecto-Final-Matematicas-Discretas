from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('work/', views.WorkScheduleListView.as_view(), name='work_list'),
    path('work/create/', views.WorkScheduleCreateView.as_view(), name='work_create'),
    path('work/<uuid:pk>/edit/', views.WorkScheduleUpdateView.as_view(), name='work_update'),
    path('work/<uuid:pk>/delete/', views.WorkScheduleDeleteView.as_view(), name='work_delete'),
    path('breaks/', views.BreakScheduleListView.as_view(), name='break_list'),
    path('breaks/create/', views.BreakScheduleCreateView.as_view(), name='break_create'),
    path('days-off/', views.DayOffListView.as_view(), name='day_off_list'),
    path('days-off/create/', views.DayOffCreateView.as_view(), name='day_off_create'),
]
