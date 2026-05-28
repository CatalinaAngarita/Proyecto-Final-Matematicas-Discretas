from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('create/', views.ServiceCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.ServiceUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.ServiceDeleteView.as_view(), name='delete'),
    path('categories/', views.ServiceCategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.ServiceCategoryCreateView.as_view(), name='category_create'),
    path('nail-types/', views.NailApplicationTypeListView.as_view(), name='nail_types_list'),
    path('nail-types/create/', views.NailApplicationTypeCreateView.as_view(), name='nail_types_create'),
]
