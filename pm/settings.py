from pathlib import Path

from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-==!jg4=unmolv!hrp1ztlb-$z!mw%l^_9)jbi0=o9hpyn6c5u%'

DEBUG = True

ALLOWED_HOSTS = ['4211-51-210-61-210.eu.ngrok.io', '127.0.0.1']

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'account.apps.AccountConfig',
    'product.apps.ProductConfig',
    'order.apps.OrderConfig',
    'blog.apps.BlogConfig',
    'ticket.apps.TicketConfig',
    'api.apps.ApiConfig',
    # third_apps
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'django_q',
    'crispy_forms',
    'azbankgateways',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pm.urls'
AUTH_USER_MODEL = 'account.User'
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
            ],
        },
    },
]

WSGI_APPLICATION = 'pm.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'ck/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full'
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1']

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nimajavangt@gmail.com'
EMAIL_HOST_PASSWORD = 'unpjqtrtqmzwgshk'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# CELERY STUFF
BROKER_URL = 'redis://192.168.121.27:6379'
CELERY_RESULT_BACKEND = 'redis://192.168.121.27:6379'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_SERIALIZER = 'json'

# Django-q config
Q_CLUSTER = {
    'name': 'pm',
    'workers': 1,
    'recycle': 500,
    'timeout': 60,
    'compress': False,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'orm': 'default',
}

AZ_IRANIAN_BANK_GATEWAYS = {
    'GATEWAYS': {
        'BMI': {
            'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
            'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
            'SECRET_KEY': '<YOUR SECRET CODE>',
        },
        'SEP': {
            'MERCHANT_CODE': 'zpTeufRA-K9BHVv',
            'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
        },
        'ZARINPAL': {
            'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
            'SANDBOX': 0,  # 0 disable, 1 active
        },
        'IDPAY': {
            'MERCHANT_CODE': '6a7f99eb-7c20-4412-a972-6dfb7cd253a4',
            'METHOD': 'POST',  # GET or POST
            'X_SANDBOX': 1,  # 0 disable, 1 active
        },
        'ZIBAL': {
            'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
        },
        'BAHAMTA': {
            'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
        },
        'MELLAT': {
            'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
            'USERNAME': '<YOUR USERNAME>',
            'PASSWORD': '<YOUR PASSWORD>',
        },
    },
    'IS_SAMPLE_FORM_ENABLE': True,  # اختیاری و پیش فرض غیر فعال است
    'DEFAULT': 'SEP',
    'CURRENCY': 'IRR',  # اختیاری
    'TRACKING_CODE_QUERY_PARAM': 'tc',  # اختیاری
    'TRACKING_CODE_LENGTH': 16,  # اختیاری
    'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',  # اختیاری
    'BANK_PRIORITIES': [
        'SEP',
        'BMI',
        # and so on ...
    ],  # اختیاری
}
