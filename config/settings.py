# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Maximum upload size (5MB)
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Allowed image types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']

# Image sizes configuration
IMAGE_SIZES = {
    'thumbnail': (100, 100),
    'medium': (300, 300),
    'large': (800, 800)
}

# Image quality settings
IMAGE_QUALITY = {
    'thumbnail': 75,
    'medium': 85,
    'large': 90
} 