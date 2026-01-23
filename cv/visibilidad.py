# cv/visibilidad.py - Utilidades para gestionar visibilidad de secciones

"""
Módulo para gestionar la visibilidad de secciones en la página del proyecto de vida.
Proporciona funciones auxiliares y template tags para filtrar datos.
"""

from .models import ConfiguracionVisibilidad, DatosPersonales

def obtener_configuracion_visibilidad(perfil_id=None):
    """
    Obtiene la configuración de visibilidad para un perfil.
    Si no existe, crea una por defecto.
    
    Args:
        perfil_id: ID del perfil. Si es None, usa el primer perfil activo.
    
    Returns:
        ConfiguracionVisibilidad object
    """
    try:
        if perfil_id:
            config = ConfiguracionVisibilidad.objects.get(perfil_id=perfil_id)
        else:
            config = ConfiguracionVisibilidad.objects.first()
        
        if not config:
            # Crear configuración por defecto para el primer perfil
            perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
            if perfil:
                config, _ = ConfiguracionVisibilidad.objects.get_or_create(
                    perfil=perfil
                )
        
        return config
    except ConfiguracionVisibilidad.DoesNotExist:
        return None

def obtener_datos_filtrados(perfil_id=None):
    """
    Obtiene todos los datos del perfil filtrados según la configuración de visibilidad.
    
    Args:
        perfil_id: ID del perfil
    
    Returns:
        Dict con todos los datos filtrados
    """
    config = obtener_configuracion_visibilidad(perfil_id)
    
    if not config:
        return {}
    
    datos = {}
    perfil = config.perfil
    
    # Datos personales
    if config.mostrar_datos_personales:
        datos['datos_personales'] = {
            'perfil': perfil,
            'mostrar_foto': config.mostrar_foto_perfil,
            'mostrar_contacto': config.mostrar_contacto,
            'mostrar_cv': config.mostrar_cv_descargable,
        }
    
    # Experiencia laboral
    if config.mostrar_experiencia_laboral:
        datos['experiencias'] = perfil.experiencias.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechafingestion')
    
    # Cursos
    if config.mostrar_cursos:
        datos['cursos'] = perfil.cursos.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechafin')
    
    # Reconocimientos
    if config.mostrar_reconocimientos:
        datos['reconocimientos'] = perfil.reconocimientos.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechareconocimiento')
    
    # Productos académicos
    if config.mostrar_productos_academicos:
        datos['productos_academicos'] = perfil.productos_academicos.filter(
            activarparaqueseveaenfront=True
        )
    
    # Productos laborales
    if config.mostrar_productos_laborales:
        datos['productos_laborales'] = perfil.productos_laborales.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechaproducto')
    
    # Venta garage
    if config.mostrar_venta_garage:
        datos['garage'] = perfil.garage.filter(
            activarparaqueseveaenfront=True
        )
    
    # Configuración
    datos['config'] = config
    
    return datos

def seccion_activa(config, nombre_seccion):
    """
    Verifica si una sección está activa en la configuración.
    
    Args:
        config: ConfiguracionVisibilidad object
        nombre_seccion: Nombre de la sección
    
    Returns:
        Boolean
    """
    secciones_activas = config.get_secciones_activas()
    return secciones_activas.get(nombre_seccion, False)

def obtener_resumen_visibilidad(perfil_id=None):
    """
    Obtiene un resumen de qué secciones están activas.
    
    Args:
        perfil_id: ID del perfil
    
    Returns:
        Dict con resumen
    """
    config = obtener_configuracion_visibilidad(perfil_id)
    
    if not config:
        return {
            'total': 0,
            'activas': 0,
            'porcentaje': 0,
            'secciones': {}
        }
    
    secciones = config.get_secciones_activas()
    total = len(secciones)
    activas = config.contar_secciones_activas()
    porcentaje = (activas / total * 100) if total > 0 else 0
    
    # Nombres amigables
    nombres_amigables = {
        'datos_personales': 'Datos Personales',
        'experiencia_laboral': 'Experiencia Laboral',
        'cursos': 'Cursos',
        'reconocimientos': 'Reconocimientos',
        'productos_academicos': 'Productos Académicos',
        'productos_laborales': 'Productos Laborales',
        'venta_garage': 'Venta Garage',
        'foto_perfil': 'Foto de Perfil',
        'contacto': 'Información de Contacto',
        'cv_descargable': 'CV Descargable',
    }
    
    secciones_detalle = {}
    for nombre, activa in secciones.items():
        secciones_detalle[nombre] = {
            'nombre': nombres_amigables.get(nombre, nombre),
            'activa': activa,
            'emoji': '✅' if activa else '❌'
        }
    
    return {
        'total': total,
        'activas': activas,
        'porcentaje': round(porcentaje, 1),
        'secciones': secciones_detalle
    }
