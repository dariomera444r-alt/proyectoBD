from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def azure_file_url(obj, field_name):
    if not obj or not getattr(obj, field_name, None):
        return ''
    
    model_name = obj.__class__.__name__.lower()
    if 'experiencia' in model_name:
        file_type = 'experiencia'
    elif 'curso' in model_name:
        file_type = 'curso'
    elif 'reconocimiento' in model_name:
        file_type = 'reconocimiento'
    elif 'datospersonales' in model_name:
        file_type = 'perfil'
    else:
        return ''
    
    return reverse('serve_protected_file', args=[file_type, obj.pk, field_name])

@register.simple_tag
def azure_avatar_url(perfil):
    if not perfil or not perfil.idperfil:
        return '/static/img/default-avatar.png'
    
    return reverse('serve_avatar', args=[perfil.idperfil])