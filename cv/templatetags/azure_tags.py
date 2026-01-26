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
    elif model_name == "ventagarage":
        file_type = "garage"
    else:
        return ""

    return reverse("serve_protected_file", args=[file_type, obj.pk, field_name])


@register.simple_tag
def azure_avatar_url(perfil):
    # ✅ Ya no usa /avatar/<id>/ para evitar tu 404
    if not perfil:
        return ""
    return reverse("serve_protected_file", args=["perfil", perfil.pk, "foto"])


@register.simple_tag
def tiene_archivo(obj, field_name: str):
    """
    Verifica si un objeto tiene un archivo cargado en el campo especificado.
    Retorna True si existe el archivo, False en caso contrario.
    """
    if not obj:
        return False
    
    try:
        field = getattr(obj, field_name, None)
        if not field:
            return False

        if isinstance(field, str):
            return bool(field.strip())

        name = getattr(field, "name", "") or ""
        if name:
            return True

        try:
            url = getattr(field, "url", "") or ""
        except Exception:
            url = ""

        return bool(url)
    except Exception:
        return False
