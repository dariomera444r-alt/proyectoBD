"""
WSGI config for config project.
"""

import os

# Aplicar parche de compatibilidad Python 3.14 ANTES de cualquier importación de Django
import config.python314_patch

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()