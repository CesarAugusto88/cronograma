import os

from decouple import config

from dj_database_url import parse as dburl

from django.conf.locale.pt_BR import formats as br_formats
br_formats.DATE_FORMAT = 'd/m/Y'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Adicionando IP da maquina 192.168.X.X para acessar em rede interna
# na porta 8080 -> python manage.py runserver 192.168.X.X:8080
ALLOWED_HOSTS = [
    'confidence.devsys.com.br', 'www.confidence.devsys.com.br',
    '127.0.0.1', 'localhost', '192.168.X.X']

INTERNAL_IPS = ['127.0.0.1']

ADMINS = [('Cesar', 'cesar@devsys.com.br')]

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'debug_toolbar',
    # my apps
    'apps.confidencechronograms',
    'apps.account',
    "crispy_forms",
    'bootstrapform',
    'auditlog',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # comentar qndo der erro - produção proibido
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Debug Toolbar
    # '/debug_toolbar.middleware.DebugToolbarMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'confidencechronogram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'confidencechronogram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_FORMAT = 'd/m/Y'

# DATE_INPUT_FORMATS = (
#     '%d/%m/%Y',
# )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_TMP = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/cronogramaconfiavel/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Configurations e-mail
# EMAIL_HOST = 'http://mail.devsys.com.br'
# EMAIL_PORT =
# EMAIL_HOST_USER = config('MY_EMAIL')
# EMAIL_HOST_PASSWORD = config('SECRET_EMAIL')
# EMAIL_USE_TLS = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.devsys.com.br'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cesar@devsys.com.br'
EMAIL_HOST_PASSWORD = config('SECRET_EMAIL')
