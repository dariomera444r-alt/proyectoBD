#!/usr/bin/env bash
# build.sh
set -o errexit

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "📦 Colectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🗄️ Aplicando migraciones..."
python manage.py migrate --noinput --verbosity 2

echo "✅ Build completado!"