# cv/templatetags/visibilidad_tags.py - Template tags para controlar visibilidad

"""
Template tags para verificar visibilidad de secciones en templates.

Uso en templates:
    {% load visibilidad_tags %}
    
    {% if seccion_activa 'cursos' %}
        <!-- Mostrar cursos -->
    {% endif %}
"""

from django import template
from ..visibilidad import obtener_configuracion_visibilidad, seccion_activa

register = template.Library()

@register.filter
def es_seccion_activa(config, nombre_seccion):
    """
    Verifica si una sección está activa.
    Uso: {{ config|es_seccion_activa:"cursos" }}
    """
    if not config:
        return False
    return seccion_activa(config, nombre_seccion)

@register.simple_tag
def obtener_config_visibilidad(perfil_id=None):
    """
    Obtiene la configuración de visibilidad.
    Uso: {% obtener_config_visibilidad as config %}
    """
    return obtener_configuracion_visibilidad(perfil_id)

@register.simple_tag
def mostrar_datos_personales(config):
    """Verifica si mostrar datos personales"""
    return config.mostrar_datos_personales if config else False

@register.simple_tag
def mostrar_experiencia(config):
    """Verifica si mostrar experiencia laboral"""
    return config.mostrar_experiencia_laboral if config else False

@register.simple_tag
def mostrar_cursos(config):
    """Verifica si mostrar cursos"""
    return config.mostrar_cursos if config else False

@register.simple_tag
def mostrar_reconocimientos(config):
    """Verifica si mostrar reconocimientos"""
    return config.mostrar_reconocimientos if config else False

@register.simple_tag
def mostrar_productos_academicos(config):
    """Verifica si mostrar productos académicos"""
    return config.mostrar_productos_academicos if config else False

@register.simple_tag
def mostrar_productos_laborales(config):
    """Verifica si mostrar productos laborales"""
    return config.mostrar_productos_laborales if config else False

@register.simple_tag
def mostrar_venta_garage(config):
    """Verifica si mostrar venta garage"""
    return config.mostrar_venta_garage if config else False

@register.simple_tag
def mostrar_foto_perfil(config):
    """Verifica si mostrar foto de perfil"""
    return config.mostrar_foto_perfil if config else False

@register.simple_tag
def mostrar_contacto(config):
    """Verifica si mostrar información de contacto"""
    return config.mostrar_contacto if config else False

@register.simple_tag
def mostrar_cv_descargable(config):
    """Verifica si mostrar CV descargable"""
    return config.mostrar_cv_descargable if config else False

@register.simple_tag
def contar_secciones_activas(config):
    """Cuenta cuántas secciones están activas"""
    if not config:
        return 0
    return config.contar_secciones_activas()
