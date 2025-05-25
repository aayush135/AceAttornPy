import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
        "https://aceattornlegalsolutions.com",
            "https://www.aceattornlegalsolutions.com"]
# Application definition
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    
    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
    'compressor',
    'meta',
    'taggit',
    'django_prometheus',
    
    # Local apps
    'core.apps.CoreConfig',
    'blog.apps.BlogConfig',
    'dashboard.apps.DashboardConfig',
    'analytics.apps.AnalyticsConfig',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'analytics.middleware.AnalyticsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'aceattorn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'aceattorn.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Site ID and Domain Settings
SITE_ID = 1
SITE_DOMAIN = 'aceattornlegalsolutions.com'
SITE_NAME = 'AceAttorn Legal Solutions'

# Django Meta
META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = SITE_DOMAIN
META_SITE_NAME = SITE_NAME

# Static files (CSS, JavaScript, Images)
# Static files (CSS, JavaScript, Images)
# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static'),
#]

# Django Compressor settings
COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
COMPRESS_OUTPUT_DIR = 'CACHE'
COMPRESS_STORAGE = 'compressor.storage.CompressorFileStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# Remove or comment out this line
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Use the default storage instead

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

# Django Meta
META_SITE_PROTOCOL = 'https'
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_DEFAULT_KEYWORDS = ['legal', 'law firm', 'intellectual property', 'contract management']

# Site ID
SITE_ID = 1

# Compress
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]

# Email Settings with Gmail OAuth2
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info@aceattornlegalsolutions.com'
GOOGLE_OAUTH2_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'credentials.json')
DEFAULT_FROM_EMAIL = 'AceAttorn Legal Solutions <info@aceattornlegalsolutions.com>'
ADMIN_EMAIL = 'nikita@aceattornlegalsolutions.com'

# Admin Interface Theme Settings
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

# Redis Configuration
REDIS_HOST = 'redis'  # Use 'redis' if running in Docker
REDIS_PORT = 6379  # Match the external port in docker-compose.yml
REDIS_DB = 0

# Admin Interface Customization
ADMIN_INTERFACE_THEME_SETTINGS = {
    'theme': 'default',
    'css_header_background_color': '#2c3e50',
    'css_header_text_color': '#ffffff',
    'css_header_link_color': '#ffffff',
    'css_header_link_hover_color': '#f1c40f',
    'css_module_background_color': '#ecf0f1',
    'css_module_text_color': '#2c3e50',
    'css_module_link_color': '#2980b9',
    'css_module_link_hover_color': '#3498db',
    'css_module_rounded_corners': True,
    'css_generic_link_color': '#2980b9',
    'css_generic_link_hover_color': '#3498db',
    'css_save_button_background_color': '#27ae60',
    'css_save_button_background_hover_color': '#2ecc71',
    'css_save_button_text_color': '#ffffff',
    'css_delete_button_background_color': '#c0392b',
    'css_delete_button_background_hover_color': '#e74c3c',
    'css_delete_button_text_color': '#ffffff',
    'list_filter_dropdown': True,
    'related_modal_active': True,
    'related_modal_background_color': '#000000',
    'related_modal_background_opacity': '0.8',
    'related_modal_rounded_corners': True,
    'logo': True,
    'logo_color': '#ffffff',
    'title': 'AceAttorn Legal Solutions',
    'welcome_sign': 'Welcome to AceAttorn Admin',
    'copyright': 'AceAttorn Legal Solutions 2025',
}

# Login settings
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/analytics/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Prometheus settings
PROMETHEUS_PORT = int(os.environ.get('PROMETHEUS_PORT', 9091))

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
