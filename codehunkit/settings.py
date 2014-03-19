# Django settings for codehunkit project.

import socket
import os.path

DEV_MACS = ('Dev-Mac', 'Envy15', 'envy', 'trg-tech-farazm', 'faraz-VirtualBox', 'trg-tech-faraz', 'macbook-pro')


DEBUG = socket.gethostname() in DEV_MACS
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(__file__)

ADMINS = (
    # ('Faraz Masood Khan', 'faraz@codehunkit.com'),
)

MANAGERS = ADMINS

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'codehunkit',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'pguser',
            'PASSWORD': 'turboteen',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', #'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'codehunkit',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'chuser',
            'PASSWORD': 'WilliWonka',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.codehunkit.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Karachi'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '' if DEBUG else '/home/jeans/www/codehunkit.com/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = BASE_DIR if DEBUG else '/home/jeans/www/codehunkit.com/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2ixqylcela4rm8m)%_rexo@bg!!o5uq8pz)+glv+psi!8+#j!q'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'codehunkit.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'codehunkit.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'codehunkit.app',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)



SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Context processors
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request', 
    'codehunkit.app.context_processors.bootstrip',
)


INTERNAL_IPS = ('127.0.0.1',)

PAGE_SIZE = 20
MAX_COMMENT_LENGTH = 1000

# Email server settings
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@codehunkit.com'
EMAIL_HOST_PASSWORD = r'3q0piqx67st5'

# Modifying default django auth user
AUTH_USER_MODEL = 'app.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Facebook signup/login settings
if DEBUG:
    FB_APP_ID = '1432030800353700'
    FB_APP_SECRET = '8e9f18b2cc63edc4b22477ff7f164724'
else:
    FB_APP_ID = '1415643725356170'
    FB_APP_SECRET = 'be60188cf82b64a5bd17e6fb94af64eb'
    
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