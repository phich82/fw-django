from .base import *  # NOQA
import sys
import logging.config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]["OPTIONS"].update({"debug": True})

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if "celery" in sys.argv[0]:
    DEBUG = False

# Less strict password authentication and validation
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

# Django Debug Toolbar
INSTALLED_APPS += ("debug_toolbar",)

# Additional middleware introduced by debug toolbar
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Show emails to console in DEBUG mode
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True

# Allow internal IPs for debugging
INTERNAL_IPS = ["127.0.0.1", "0.0.0.1"]

# Show Debug Toolbar from docker
if DEBUG:
   import socket
   hostname, _, ips =socket.gethostbyname_ex(socket.gethostname())
   INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]

# Log everything to the logs directory at the top
# LOGFILE_ROOT = BASE_DIR.parent / "logs"
LOGFILE_ROOT = BASE_DIR / "logs"

if not os.path.exists(LOGFILE_ROOT):
    os.makedirs(LOGFILE_ROOT, exist_ok=True)

# Reset logging
# (see http://www.caktusgroup.com/blog/2015/01/27/Django-Logging-Configuration-logging_config-default-settings-logger/)

LOGGING_CONFIG = None
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%m/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "django_log_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(LOGFILE_ROOT / "django.log"),
            "formatter": "verbose",
        },
        "proj_log_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(LOGFILE_ROOT / "project.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django_log_file"],
            "propagate": True,
            "level": "DEBUG",
        },
        "project": {"handlers": ["proj_log_file"], "level": "DEBUG"},
    },
}

logging.config.dictConfig(LOGGING)
