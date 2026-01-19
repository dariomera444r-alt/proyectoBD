from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def azure_file_url(obj, field_name: str):
    if not obj:
        return ""

    model_name = obj.__class__.__name__.lower()

    if model_name == "datospersonales":
        file_type = "perfil"
    elif model_name == "experiencialaboral":
        file_type = "experiencia"
    elif model_name == "cursosrealizados":
        file_type = "curso"
    elif model_name == "reconocimientos":
        file_type = "reconocimiento"
    else:
        return ""

    return reverse("serve_protected_file", args=[file_type, obj.pk, field_name])


@register.simple_tag
def azure_avatar_url(perfil):
    # ✅ Ya no usa /avatar/<id>/ para evitar tu 404
    if not perfil:
        return ""
    return reverse("serve_protected_file", args=["perfil", perfil.pk, "foto"])
