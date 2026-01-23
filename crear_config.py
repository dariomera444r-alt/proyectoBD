import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from cv.models import DatosPersonales, ConfiguracionVisibilidad

# Obtener el perfil activo
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

if perfil:
    # Crear o obtener la configuración
    config, creado = ConfiguracionVisibilidad.objects.get_or_create(perfil=perfil)
    
    if creado:
        print(f"✅ Configuración creada para: {perfil.nombres} {perfil.apellidos}")
    else:
        print(f"✅ Configuración ya existe para: {perfil.nombres} {perfil.apellidos}")
    
    print(f"Secciones activas: {config.contar_secciones_activas()}/10")
else:
    print("❌ No hay perfil activo")
