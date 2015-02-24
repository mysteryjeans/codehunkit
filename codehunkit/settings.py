# Django settings for codehunkit project.

import os.path

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['CODEHUNKIT_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DB_NAME' not in os.environ

TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)

ADMINS = (
    ('Faraz Masood Khan', 'faraz@fanaticlab.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.app.rootplugin.com', 'codehunkit.rootplugin.com']

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'codehunkit',
            'USER': 'codehunkit',
            'PASSWORD': 'codehunkit',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ['DB_PORT'],
        }
    }

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'codehunkit.app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'codehunkit.urls'

WSGI_APPLICATION = 'codehunkit.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Context processors
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'codehunkit.app.context_processors.bootstrip',
)


PAGE_SIZE = 20
MAX_COMMENT_LENGTH = 1000

# Email server settings
EMAIL_HOST = os.environ['CODEHUNKIT_EMAIL_HOST']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ['CODEHUNKIT_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['CODEHUNKIT_EMAIL_HOST_PASSWORD']
MAX_COMMENT_LEGNTH = 1000

# Modifying default django auth user
AUTH_USER_MODEL = 'app.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Facebook signup/login settings
FB_APP_ID = os.environ['CODEHUNKIT_FB_APP_ID']
FB_APP_SECRET = os.environ['CODEHUNKIT_FB_APP_SECRET']

FB_ACCESS_TOKEN = 'https://graph.facebook.com/oauth/access_token'
FB_AUTH_URL = 'https://www.facebook.com/dialog/oauth'
FB_GRAPH_ME = 'https://graph.facebook.com/me'
FB_GRAPH_FRIENDS = 'https://graph.facebook.com/me/friends'

# CSS and Javascript less & compressor settings
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

INSTALLED_APPS += (
    'pipeline',
)

PIPELINE_CSS = {
    'style': {
        'source_filenames': (
          'app/css/style.less',
        ),
        'output_filename': 'app/css/style.css',
    },
    'base': {
        'source_filenames': (
          'app/css/base.less',
        ),
        'output_filename': 'app/css/base.css',
    },
    'social': {
        'source_filenames': (
          'app/css/social.less',
        ),
        'output_filename': 'app/css/social.css',
    },
    'public': {
        'source_filenames': (
          'app/css/public.less',
        ),
        'output_filename': 'app/css/public.css',
    },
    'submit_snippet': {
        'source_filenames': (
          'app/lib/select2/select2.less',
        ),
        'output_filename': 'app/css/submit_snippet.css',
    },
}

PIPELINE_JS = {
    'stats': {
        'source_filenames': (
          'app/lib/histats.js',
          'app/lib/google-analytics.js',
        ),
        'output_filename': 'app/lib/stats.js',
    },
    'base': {
        'source_filenames': (
          'app/lib/jquery-ajax.js',
          'app/lib/votes-utils.js',
          'app/lib/utils.js',
        ),
        'output_filename': 'app/lib/base.js',
    },
    'social_base': {
        'source_filenames': (
          'app/lib/jquery-ui-1.10.4.js',
          'app/lib/jquery.slimscroll.min.js',
        ),
        'output_filename': 'app/lib/social_base.js',
    },
    'submit_snippet': {
        'source_filenames': (
          'app/lib/select2/select2.js',
        ),
        'output_filename': 'app/lib/submit_snippet.js',
    }
}

PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
)

PIPELINE_DISABLE_WRAPPER = True
