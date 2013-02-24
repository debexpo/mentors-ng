from os.path import abspath, dirname, join

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['mentors.debian.net']

ADMINS = (
    ('Nicolas Dandrimont', 'nicolas.dandrimont@crans.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# This goes to the "media" directory at the root of your git checkout
MEDIA_ROOT = abspath(join(dirname(abspath(__file__)), '../../media/'))

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# This goes to a "static" directory at the root of your git checkout
STATIC_ROOT = abspath(join(dirname(abspath(__file__)), '../../static/'))

# Make this unique, and don't share it with anybody.
# You can use python manage.py generate_secret_key to generate one
SECRET_KEY = ''

