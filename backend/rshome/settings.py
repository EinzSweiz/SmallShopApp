
from pathlib import Path
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*f0@1d7kud%v*$9e__xw9x5-j9y5$71s4=d(=-#b-)8t^876ve'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #installed apps
    'mathfilters',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_email_verification',
    'django_google_fonts',
    'django_celery_beat',
    "django_celery_results",
    "django_htmx",
    'sorl.thumbnail',
    'rest_framework',
    'djoser',
    'drf_yasg',
    #my apps
    'shop',
    'cart',
    'account',
    'payment',
    'recommend',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'rshome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #custom context processor
                'shop.context_processors.categories',
                'cart.context_processors.cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'rshome.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USERNAME'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT', default=5432),
#     }
# }


#REDIS CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://bigcorp-redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
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

#Project Inside settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

#Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'rshome' / 'static',
    BASE_DIR / 'shop' / 'static',
    # BASE_DIR / 'shop' / 'static',
]
#Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

#SMTP

def email_verified_callback(user):
    user.is_active = True


# def password_change_callback(user, password):
#     user.set_password(password)


# Global Package Settings
EMAIL_FROM_ADDRESS = config('DEFAULT_FROM_EMAIL')  # mandatory
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8081/'
EMAIL_MULTI_USER = False

# Email Verification Settings (mandatory for email sending)
EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'email/mail_body.html'
EMAIL_MAIL_PLAIN = 'email/mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # one hour

# Email Verification Settings (mandatory for builtin view)
EMAIL_MAIL_PAGE_TEMPLATE = 'account/email_success_template.html'
EMAIL_MAIL_CALLBACK = email_verified_callback

# Password Recovery Settings (mandatory for email sending)
# EMAIL_PASSWORD_SUBJECT = 'Change your password {{ user.username }}'
# EMAIL_PASSWORD_HTML = 'password_body.html'
# EMAIL_PASSWORD_PLAIN = 'password_body.txt'
# EMAIL_PASSWORD_TOKEN_LIFE = 60 * 10  # 10 minutes

# Password Recovery Settings (mandatory for builtin view)
# EMAIL_PASSWORD_PAGE_TEMPLATE = 'password_changed_template.html'
# EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = 'password_change_template.html'
# EMAIL_PASSWORD_CALLBACK = password_change_callback

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
ADMIN_USER_EMAIL = config('ADMIN_USER_EMAIL')


#STRIPE
STRIPE_PUBLISH_KEY = config('STRIPE_PUBLISH_KEY', cast=str, default=None)
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', cast=str, default=None)
STRIPE_API_VERSION = config('STRIPE_API_VERSION')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', cast=str, default=None)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_AGE = 60 * 60 * 2

#Yookassa
YOOKASSA_SECRET_KEY=config('YOOKASSA_SECRET_KEY', cast=str, default=None)
YOOKASSA_SHOP_ID=config('YOOKASSA_SHOP_ID', cast=int, default=None)


#GOOGLE FONTS
GOOGLE_FONTS = ["Montserrat:wght@300,400", 'Roboto']

GOOGLE_FONTS_DIR = BASE_DIR / "static"


#Celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# CELERY_BEAT_SCHEDULE = {
#     "sample_task": {
#         "task": "core.tasks.sample_task",
#         "schedule": crontab(minute="*/1"),
#     },
# }


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'api.permissions.IsAdminOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'api.serializer.CustomerUserCreateSerializer'
    },
    'AUTH_HEADER_TYPES': ('JWT', ),
}
