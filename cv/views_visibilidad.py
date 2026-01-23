# cv/views_visibilidad.py - Vistas de ejemplo para usar visibilidad

"""
Vistas de ejemplo para mostrar cómo usar el sistema de visibilidad.
Puedes adaptar estas vistas a tu aplicación.
"""

from django.shortcuts import render, get_object_or_404
from .models import DatosPersonales, ConfiguracionVisibilidad
from .visibilidad import obtener_datos_filtrados, obtener_resumen_visibilidad

def proyecto_vida_completo(request, perfil_id=None):
    """
    Vista que muestra el proyecto de vida completo filtrando por visibilidad.
    
    URL: /cv/proyecto-vida/ o /cv/proyecto-vida/<int:perfil_id>/
    """
    
    if perfil_id:
        perfil = get_object_or_404(DatosPersonales, idperfil=perfil_id)
    else:
        # Obtener el primer perfil activo
        perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
        if not perfil:
            return render(request, 'cv/error.html', {
                'error': 'No hay perfiles activos'
            })
    
    # Obtener configuración
    try:
        config = ConfiguracionVisibilidad.objects.get(perfil=perfil)
    except ConfiguracionVisibilidad.DoesNotExist:
        # Si no existe configuración, crearla con valores por defecto
        config = ConfiguracionVisibilidad.objects.create(perfil=perfil)
    
    # Obtener datos filtrados
    datos = obtener_datos_filtrados(perfil.idperfil)
    
    # Obtener resumen
    resumen = obtener_resumen_visibilidad(perfil.idperfil)
    
    contexto = {
        'perfil': perfil,
        'config': config,
        'datos': datos,
        'resumen': resumen,
    }
    
    return render(request, 'cv/proyecto_vida.html', contexto)

def panel_control_visibilidad(request):
    """
    Vista para mostrar un panel de control de visibilidad.
    Permite ver y modificar qué secciones están activas.
    
    URL: /cv/control-visibilidad/
    """
    
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        return render(request, 'cv/error.html', {
            'error': 'No hay perfiles activos'
        })
    
    try:
        config = ConfiguracionVisibilidad.objects.get(perfil=perfil)
    except ConfiguracionVisibilidad.DoesNotExist:
        config = ConfiguracionVisibilidad.objects.create(perfil=perfil)
    
    resumen = obtener_resumen_visibilidad(perfil.idperfil)
    
    contexto = {
        'perfil': perfil,
        'config': config,
        'resumen': resumen,
    }
    
    return render(request, 'cv/panel_control_visibilidad.html', contexto)

def api_obtener_secciones_activas(request, perfil_id=None):
    """
    API que retorna un JSON con las secciones activas.
    
    URL: /api/cv/secciones-activas/ o /api/cv/secciones-activas/<int:perfil_id>/
    
    Response:
    {
        "perfil_id": 1,
        "secciones": {
            "datos_personales": true,
            "experiencia_laboral": true,
            "cursos": true,
            ...
        },
        "total_activas": 8,
        "total": 10
    }
    """
    from django.http import JsonResponse
    
    if perfil_id:
        perfil = get_object_or_404(DatosPersonales, idperfil=perfil_id)
    else:
        perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)
    
    try:
        config = ConfiguracionVisibilidad.objects.get(perfil=perfil)
    except ConfiguracionVisibilidad.DoesNotExist:
        config = ConfiguracionVisibilidad.objects.create(perfil=perfil)
    
    secciones = config.get_secciones_activas()
    
    return JsonResponse({
        'perfil_id': perfil.idperfil,
        'perfil_nombre': f"{perfil.nombres} {perfil.apellidos}",
        'secciones': secciones,
        'total_activas': config.contar_secciones_activas(),
        'total': len(secciones),
    })

def api_actualizar_visibilidad(request, perfil_id=None):
    """
    API para actualizar la visibilidad desde JavaScript.
    
    URL: /api/cv/actualizar-visibilidad/ (POST)
    
    Body:
    {
        "seccion": "cursos",
        "valor": false
    }
    """
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    import json
    
    if not request.method == 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if perfil_id:
        perfil = get_object_or_404(DatosPersonales, idperfil=perfil_id)
    else:
        perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)
    
    try:
        config = ConfiguracionVisibilidad.objects.get(perfil=perfil)
    except ConfiguracionVisibilidad.DoesNotExist:
        config = ConfiguracionVisibilidad.objects.create(perfil=perfil)
    
    try:
        data = json.loads(request.body)
        seccion = data.get('seccion')
        valor = data.get('valor')
        
        # Mapear nombre de sección al campo del modelo
        campo_map = {
            'datos_personales': 'mostrar_datos_personales',
            'experiencia_laboral': 'mostrar_experiencia_laboral',
            'cursos': 'mostrar_cursos',
            'reconocimientos': 'mostrar_reconocimientos',
            'productos_academicos': 'mostrar_productos_academicos',
            'productos_laborales': 'mostrar_productos_laborales',
            'venta_garage': 'mostrar_venta_garage',
            'foto_perfil': 'mostrar_foto_perfil',
            'contacto': 'mostrar_contacto',
            'cv_descargable': 'mostrar_cv_descargable',
        }
        
        if seccion not in campo_map:
            return JsonResponse({'error': 'Sección no válida'}, status=400)
        
        # Actualizar el campo
        setattr(config, campo_map[seccion], valor)
        config.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Sección {seccion} actualizada a {valor}',
            'secciones_activas': config.contar_secciones_activas(),
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
