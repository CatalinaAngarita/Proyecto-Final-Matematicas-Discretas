from pathlib import Path
from decouple import config, Csv
import os

# ---------------------------------------------------------------------------
# BASE DIR
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------------------
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ---------------------------------------------------------------------------
# APPS
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'django_extensions',
    'django_filters',
    'widget_tweaks',
]

LOCAL_APPS = [
    'apps.public',
    'apps.core',
    'apps.accounts',
    'apps.clients',
    'apps.services',
    'apps.specialists',
    'apps.schedules',
    'apps.appointments',
    'apps.notifications',
    'apps.analytics',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ---------------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ---------------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.app_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

# ---------------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# ---------------------------------------------------------------------------
# MEDIA FILES
# ---------------------------------------------------------------------------
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------------------------------
# DEFAULT AUTO FIELD
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# CRISPY FORMS
# ---------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ---------------------------------------------------------------------------
# UNFOLD (Admin Theme)
# ---------------------------------------------------------------------------
UNFOLD = {
    # -----------------------------------------------------------------------
    # BRANDING
    # -----------------------------------------------------------------------
    'SITE_TITLE': 'Diana Nails',
    'SITE_HEADER': 'Diana Nails',
    'SITE_SUBHEADER': 'Smart Booking System',
    'SITE_URL': '/',
    'SITE_ICON': lambda request: None,
    'SITE_LOGO': lambda request: None,
    'SHOW_VIEW_ON_SITE': False,
    'STYLES': [
        'css/admin.css',
    ],

    # -----------------------------------------------------------------------
    # COLORS & DESIGN
    # -----------------------------------------------------------------------
    'COLORS': {
        'primary': {
            '50': '250 245 255',
            '100': '243 232 255',
            '200': '233 213 255',
            '300': '216 180 254',
            '400': '192 132 252',
            '500': '168 85 247',
            '600': '147 51 234',
            '700': '126 34 206',
            '800': '107 33 168',
            '900': '88 28 135',
        },
    },

    # -----------------------------------------------------------------------
    # LAYOUT
    # -----------------------------------------------------------------------
    'LAYOUT': {
        'sidebar': {
            'collapsed': False,
        },
    },

    # -----------------------------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------------------------
    'SIDEBAR': {
        'show_search': False,
        'show_all_applications': False,
        'navigation': [

            # -----------------------------------------------------------------
            # DASHBOARD
            # -----------------------------------------------------------------
            {
                'title': 'Dashboard',
                'separator': True,
                'items': [
                    {
                        'title': 'Inicio',
                        'icon': 'space_dashboard',
                        'link': '/admin/',
                    },
                ],
            },

            # -----------------------------------------------------------------
            # GESTIÓN
            # -----------------------------------------------------------------
            {
                'title': 'Gestión',
                'icon': 'apps',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Citas',
                        'icon': 'calendar_month',
                        'link': '/admin/appointments/appointment/',
                    },
                    {
                        'title': 'Clientas',
                        'icon': 'groups',
                        'link': '/admin/clients/client/',
                    },
                    {
                        'title': 'Especialistas',
                        'icon': 'badge',
                        'link': '/admin/specialists/specialist/',
                    },
                    {
                        'title': 'Servicios',
                        'icon': 'spa',
                        'link': '/admin/services/service/',
                    },
                    {
                        'title': 'Categorías',
                        'icon': 'category',
                        'link': '/admin/services/servicecategory/',
                    },
                    {
                        'title': 'Tipos de uñas',
                        'icon': 'back_hand',
                        'link': '/admin/services/nailapplicationtype/',
                    },
                ],
            },

            # -----------------------------------------------------------------
            # HORARIOS
            # -----------------------------------------------------------------
            {
                'title': 'Horarios',
                'icon': 'schedule',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Horarios laborales',
                        'icon': 'work_history',
                        'link': '/admin/schedules/workschedule/',
                    },
                    {
                        'title': 'Descansos',
                        'icon': 'coffee',
                        'link': '/admin/schedules/breakschedule/',
                    },
                    {
                        'title': 'Días libres',
                        'icon': 'event_busy',
                        'link': '/admin/schedules/dayoff/',
                    },
                ],
            },

            # -----------------------------------------------------------------
            # ANALÍTICAS
            # -----------------------------------------------------------------
            {
                'title': 'Analíticas',
                'icon': 'insights',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Cancelaciones',
                        'icon': 'cancel',
                        'link': '/admin/analytics/cancellationstat/',
                    },
                    {
                        'title': 'Servicios',
                        'icon': 'trending_up',
                        'link': '/admin/analytics/servicestat/',
                    },
                ],
            },

            # -----------------------------------------------------------------
            # NOTIFICACIONES
            # -----------------------------------------------------------------
            {
                'title': 'Notificaciones',
                'icon': 'campaign',
                'collapsible': True,
                'items': [
                    {
                        'title': 'WhatsApp',
                        'icon': 'notifications_active',
                        'link': '/admin/notifications/notificationlog/',
                    },
                ],
            },

            # -----------------------------------------------------------------
            # AUTENTICACIÓN
            # -----------------------------------------------------------------
            {
                'title': 'Administración',
                'icon': 'admin_panel_settings',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Usuarios',
                        'icon': 'person',
                        'link': '/admin/auth/user/',
                    },
                    {
                        'title': 'Roles y grupos',
                        'icon': 'group',
                        'link': '/admin/auth/group/',
                    },
                ],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# NOTIFICATIONS
# ---------------------------------------------------------------------------
NOTIFICATION_REMINDER_HOURS = config('NOTIFICATION_REMINDER_HOURS', default='24,2', cast=Csv(int))
