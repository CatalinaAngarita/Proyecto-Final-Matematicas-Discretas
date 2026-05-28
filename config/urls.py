from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.public.urls')),
    path('dashboard/', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('clients/', include('apps.clients.urls')),
    path('services/', include('apps.services.urls')),
    path('specialists/', include('apps.specialists.urls')),
    path('schedules/', include('apps.schedules.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
