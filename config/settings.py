#config/settings.py
"""
Django settings for config project.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Hosts
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF
CSRF_TRUSTED_ORIGINS = []
csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if csrf_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins.split(",") if o.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "cv",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # ✅ permite templates globales
        "APP_DIRS": True,                  # ✅ permite templates dentro de apps (cv/templates/...)
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

# Static
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ============================
# MEDIA: Azure (si está listo) o Local (si no)
# ============================

AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME", "").strip()
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER", os.getenv("AZURE_CONTAINER_NAME", "media")).strip()

# Puede venir de dos formas:
# 1) AZURE_ACCOUNT_KEY = key real
# 2) AZURE_CONNECTION_STRING = connection string
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY", "").strip()
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING", "").strip()

def _extract_from_connection_string(cs: str):
    """
    Extrae AccountName y AccountKey desde un Connection String típico de Azure.
    """
    name = ""
    key = ""
    parts = [p.strip() for p in cs.split(";") if p.strip()]
    for p in parts:
        if p.lower().startswith("accountname="):
            name = p.split("=", 1)[1].strip()
        elif p.lower().startswith("accountkey="):
            key = p.split("=", 1)[1].strip()
    return name, key

# Si el usuario (como en tu .env actual) puso el connection string dentro de AZURE_ACCOUNT_KEY, lo detectamos:
if (not AZURE_CONNECTION_STRING) and AZURE_ACCOUNT_KEY.lower().startswith("defaultendpointsprotocol="):
    AZURE_CONNECTION_STRING = AZURE_ACCOUNT_KEY
    # y tratamos de extraer el key real para SAS
    extracted_name, extracted_key = _extract_from_connection_string(AZURE_CONNECTION_STRING)
    if not AZURE_ACCOUNT_NAME and extracted_name:
        AZURE_ACCOUNT_NAME = extracted_name
    if extracted_key:
        AZURE_ACCOUNT_KEY = extracted_key  # ahora sí queda solo la key real

# Si hay connection string pero faltan name/key, los extraemos
if AZURE_CONNECTION_STRING and (not AZURE_ACCOUNT_NAME or not AZURE_ACCOUNT_KEY):
    extracted_name, extracted_key = _extract_from_connection_string(AZURE_CONNECTION_STRING)
    if not AZURE_ACCOUNT_NAME and extracted_name:
        AZURE_ACCOUNT_NAME = extracted_name
    if not AZURE_ACCOUNT_KEY and extracted_key:
        AZURE_ACCOUNT_KEY = extracted_key

USE_AZURE_MEDIA = bool(AZURE_ACCOUNT_NAME and AZURE_CONTAINER and (AZURE_CONNECTION_STRING or AZURE_ACCOUNT_KEY))

# Media local (fallback)
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL_LOCAL = "/media/"

# Tu proyecto sirve media por views (proxy) cuando es Azure
MEDIA_URL_AZURE_PROXY = "/protected/media/"

if USE_AZURE_MEDIA:
    print(f"[OK] Azure habilitado. Cuenta: {AZURE_ACCOUNT_NAME} | Container: {AZURE_CONTAINER}")

    # Si no hay connection string, lo construimos con name/key
    if not AZURE_CONNECTION_STRING and AZURE_ACCOUNT_NAME and AZURE_ACCOUNT_KEY:
        AZURE_CONNECTION_STRING = (
            f"DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME};"
            f"AccountKey={AZURE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
        )

    AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
    AZURE_LOCATION = ""
    AZURE_OVERWRITE_FILES = False
    AZURE_URL_EXPIRATION_SECS = 3600

    MEDIA_URL = MEDIA_URL_AZURE_PROXY

    STORAGES = {
        "default": {
            "BACKEND": "cv.storage_backends.AzureMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    print("[WARN] Azure NO habilitado (faltan credenciales o container). Usando MEDIA local.")
    MEDIA_URL = MEDIA_URL_LOCAL

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": str(MEDIA_ROOT),
                "base_url": MEDIA_URL,
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security settings for production
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
