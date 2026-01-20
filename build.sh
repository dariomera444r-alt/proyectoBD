#!/usr/bin/env bash
# build.sh
set -o errexit

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "📦 Colectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🗄️ Verificando migraciones pendientes..."
python manage.py showmigrations

echo "🗄️ Aplicando migraciones..."
python manage.py migrate --noinput

echo "✅ Build completado!"