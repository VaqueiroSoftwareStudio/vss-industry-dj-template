"""
Django settings for {{ project_name }} project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

RUNNING_PROD_SERVER = True if os.getenv("SETTINGS_MODE", "") == "prod" else False


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "{{ secret_key }}"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if RUNNING_PROD_SERVER else True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    # VSS Industry Dependencies
    "maintenance_mode",
    # VSS Dependencies
    "django_quill",
    # VSS Apps
    "vss",
    "vss.apps.dashboard",
    "vss.apps.accounts",
    "vss.apps.blog",
    "vss.apps.components",
    "vss.apps.data",
    # VSS Industry
    "vss_industry",
    "vss_industry.apps",
    "vss_industry.apps.catalog",
    "vss_industry.apps.components",
    "vss_industry.apps.data",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "vss.middleware.DisableClientSideCachingMiddleware",
    # NOTE: Maintenance mode must be last.
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
]

ROOT_URLCONF = "{{ project_name }}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
                "vss.context_processors.vss",
                "vss_industry.context_processors.vss_industry",
            ],
        },
    },
]

WSGI_APPLICATION = "{{ project_name }}.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if RUNNING_PROD_SERVER:
    DEBUG_PROPAGATE_EXCEPTIONS = True
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "<< DATABASE_NAME >>",
            "USER": "<< DATABASE_USER >>",
            "PASSWORD": "<< DATABASE_PASS >>",
            "HOST": "<< DATABASE_HOST >>",
            "PORT": 3306,
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
            "TEST": {
                "CHARSET": "utf8mb4",
                "COLLATION": "utf8mb4_unicode_ci",
            },
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = "es"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ("es", _("Español")),
    ("en", _("Inglés")),
]

# NOTE: Must be a list or tuple
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.dirname(BASE_DIR) + "/public/static/"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.dirname(BASE_DIR) + "/public/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

# Email
DEFAULT_FROM_EMAIL = "<< SITE_EMAIL_ADDRESS >>"  # SiteName <web@example.com>
EMAIL_HOST = "<< SITE_EMAIL_HOST >>"  # mail.example.com
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = "<< SITE_EMAIL_PASS >>"
EMAIL_HOST_USER = "<< SITE_EMAIL_ADDRESS >>"
EMAIL_SUBJECT_PREFIX = ""
EMAIL_USE_TLS = True
SERVER_EMAIL = "<< SITE_SERVER_MAIL >>"  # web@example.com

if not RUNNING_PROD_SERVER:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# X_FRAME_OPTIONS
X_FRAME_OPTIONS = "SAMEORIGIN"

XS_SHARING_ALLOWED_METHODS = ["POST", "GET", "OPTIONS", "PUT", "DELETE"]

# SSL
if RUNNING_PROD_SERVER:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    }
}

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# Auth
AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
LOGIN_URL = "/accounts/login/"

QUILL_CONFIGS = {
    "default": {
        "theme": "snow",
        "modules": {
            "syntax": True,
            "toolbar": [
                [{"header": []}],
                [
                    "bold",
                    "italic",
                    "underline",
                    "strike",
                    "blockquote",
                ],
                [
                    {"list": "ordered"},
                    {"list": "bullet"},
                ],
                [{"align": []}],
                ["link", "image", "video"],
                ["code-block"],
                ["clean"],
            ],
        },
        # quill-image-compress
        "imageCompressor": {
            "quality": 0.8,
            "maxWidth": 2000,
            "maxHeight": 2000,
            "imageType": "image/jpeg",
            "debug": False,
            "suppressErrorLogging": True,
        },
        # quill-resize
        "resize": {
            "showSize": True,
            "locale": {},
        },
    }
}

# Requisitos para VSS Studio

VSS_DASHBOARD_REGISTRY = [
    {
        "group_name": _("Blog"),
        "admin_data": [
            "vss.apps.blog.vss_admin.ArticleAdmin",
            "vss.apps.blog.vss_admin.CategoryAdmin",
            "vss.apps.blog.vss_admin.ArticleCommentAdmin",
        ],
    },
    {
        "group_name": _("Catálogo"),
        "admin_data": [
            "vss_industry.apps.catalog.vss_admin.ProductCategoryAdmin",
            "vss_industry.apps.catalog.vss_admin.ProductAdmin",
        ],
    },
    {
        "group_name": _("Marketing"),
        "admin_data": [
            "vss_industry.apps.components.vss_admin.BannerAdmin",
            "vss_industry.apps.components.vss_admin.FeatureAdmin",
            "vss.apps.components.vss_admin.FAQAdmin",
            "vss_industry.apps.components.vss_admin.GalleryImageAdmin",
            "vss.apps.components.vss_admin.TestimonialAdmin",
        ],
    },
]


VSS_DASHBOARD_SETTINGS = [
    {
        "group_name": _("Contacto"),
        "admin_data": [
            "vss.apps.data.vss_admin.SiteSocialNetworkAdmin",
            "vss_industry.apps.data.vss_admin.SiteContactDataAdmin",
            "vss_industry.apps.data.vss_admin.LocationAdmin",
        ],
    },
    {
        "group_name": _("Empresa"),
        "admin_data": [
            "vss_industry.apps.data.vss_admin.SiteAboutAdmin",
            "vss_industry.apps.components.vss_admin.TimelineEventAdmin",
            "vss.apps.components.vss_admin.TextPageAdmin",
        ],
    },
    {
        "group_name": _("Sitio Web"),
        "admin_data": [
            "vss.apps.data.vss_admin.SiteBrandingDataAdmin",
            "vss_industry.apps.data.vss_admin.SiteSEOAdmin",
            "vss.apps.data.vss_admin.SiteGoogleServicesAdmin",
            "vss.apps.data.vss_admin.SiteSnippetsAdmin",
        ],
    },
    {
        "group_name": _("Dashboard"),
        "admin_data": [
            "vss.apps.accounts.vss_admin.UserAdmin",
        ],
    },
]


VSS_DASHBOARD_INDEX = {
    # Muestra un enlace a model.create.view si:
    #     vssadmin.enable_create = True
    #     vssadmin.sitedata_model != True
    "quick_links": [
        "vss.apps.blog.vss_admin.ArticleAdmin",
        "vss_industry.apps.components.vss_admin.BannerAdmin",
        "vss_industry.apps.catalog.vss_admin.ProductAdmin",
        "vss.apps.accounts.vss_admin.UserAdmin",
    ],
    # Muestra los 5 elementos mas recientes en una lista
    "quick_view": [
        "vss.apps.blog.vss_admin.ArticleCommentAdmin",
    ],
}

# NOTE: Necesitamos este setting en django 4.0+ para que el popup de PayPal funcione correctamente.
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25MB

VSS_PROJECT_TIME_ZONE = "America/Mexico_City"

VSS_DASHBOARD_BANNER = "vss_industry/img/vss_banner.png"

# NOTE: Maintenance_Mode requiere la instalacion de django-maintenance-mode

# NOTE: Para activar/desactivar el modo de mantenimiento
# hay que entrar como superusuario a las urls:
# - /maintenance-mode/on/
# - /maintenance-mode/off/

# MAINTENANCE_MODE = True
MAINTENANCE_MODE_IGNORE_AUTHENTICATED_USER = True
MAINTENANCE_MODE_IGNORE_URLS = (
    r"^/media/",
    r"^/static/",
    r"^/accounts/",
    r"^/es/accounts/",
    r"^/en/accounts/",
    r"^/maintenance-mode/off/",
    r"^/es/maintenance-mode/off/",
    r"^/en/maintenance-mode/off/",
    r"^/maintenance-mode/on/",
    r"^/es/maintenance-mode/on/",
    r"^/en/maintenance-mode/on/",
)

# NOTE: Esto nos permite evitar que django mande emails de error 503 en
# modo mantenimiento.
LOGGING = {
    "version": 1,
    "filters": {
        "require_not_maintenance_mode_503": {
            "()": "maintenance_mode.logging.RequireNotMaintenanceMode503",
        },
    },
}

VSS_BLOG_ARTICLE_COVER_SIZE = [1980, 1980]
VSS_COMPONENTS_BANNER_IMAGE = [1980, 1980]
VSS_FILLED_TESTIMONIAL_STAR = '<i class="bx bxs-star text-warning"></i>'
VSS_EMPTY_TESTIMONIAL_STAR = '<i class="bx bx-star text-muted opacity-75"></i>'
