import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles/")

SECRET_KEY = 'django-insecure-4u)ln%rjah7-i)f1mxx)\
    8+h7s*m7h1yj6afzr5jnl)8^22d$57'

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


INTERNAL_IPS = ["127.0.0.1",]

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8080",]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOCALE_PATHS = ['movies/locale']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
}

if DEBUG:
    LOGGING.update({
        'handlers': {
            'debug-console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'filters': ['require_debug_true'],
                },
            },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['debug-console'],
                'propagate': False,
            }
        },
    })
