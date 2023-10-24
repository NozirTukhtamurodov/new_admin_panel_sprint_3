from config.components.base import DEBUG


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies.apps.MoviesConfig',
    'corsheaders'
]
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    INSTALLED_APPS.append('django_extensions')
