#!/usr/bin/env bash
# build.sh
set -o errexit

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "📦 Colectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🗄️ Aplicando migraciones..."
python manage.py migrate --noinput --verbosity 2

echo "🔐 Creando superusuario..."
python manage.py shell <<END
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('✅ Superusuario creado exitosamente')
else:
    print('⚠️ El superusuario ya existe')
END

echo "✅ Build completado!"