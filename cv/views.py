from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from django.views.decorators.cache import cache_control
from django.conf import settings

from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    CursosRealizados,
    Reconocimientos,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage,
)
from .storage_backends import AzureFileProxy

import mimetypes
import os


def hoja_vida(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

    context = {
        "perfil": perfil,
        "experiencias": ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=perfil,
            activarparaqueseveaenfront=True
        ) if perfil else [],
        "cursos": CursosRealizados.objects.filter(
            idperfilconqueestaactivo=perfil,
            activarparaqueseveaenfront=True
        ) if perfil else [],
        "reconocimientos": Reconocimientos.objects.filter(
            idperfilconqueestaactivo=perfil,
            activarparaqueseveaenfront=True
        ) if perfil else [],
        "prod_acad": ProductosAcademicos.objects.filter(
            idperfilconqueestaactivo=perfil,
            activarparaqueseveaenfront=True
        ) if perfil else [],
        "prod_lab": ProductosLaborales.objects.filter(
            idperfilconqueestaactivo=perfil,
            activarparaqueseveaenfront=True
        ) if perfil else [],
        "garage": VentaGarage.objects.filter(
            idperfilconqueestaactivo=perfil,
            activarparaqueseveaenfront=True
        ) if perfil else [],
    }

    # ✅ tu HTML real
    return render(request, "hoja_vida_cv.html", context)


@cache_control(max_age=3600)
def serve_protected_file(request, file_type, model_id, field_name):
    model_map = {
        "perfil": DatosPersonales,
        "experiencia": ExperienciaLaboral,
        "curso": CursosRealizados,
        "reconocimiento": Reconocimientos,
    }

    if file_type not in model_map:
        raise Http404("Tipo de archivo no válido")

    model_class = model_map[file_type]
    obj = get_object_or_404(model_class, pk=model_id)

    file_field = getattr(obj, field_name, None)
    if not file_field:
        raise Http404("Campo de archivo no existe")

    # Intenta .name y si no, intenta .url
    blob_ref = getattr(file_field, "name", "") or ""
    if not blob_ref:
        blob_ref = getattr(file_field, "url", "") or ""

    if not blob_ref:
        raise Http404("Archivo no asociado al registro")

    try:
        content, blob_properties = AzureFileProxy.download_blob(blob_ref)

        content_type = getattr(blob_properties.content_settings, "content_type", None)
        if not content_type:
            filename_guess = os.path.basename(str(blob_ref))
            content_type, _ = mimetypes.guess_type(filename_guess)
            if not content_type:
                content_type = "application/octet-stream"

        # filename final
        filename = os.path.basename(str(blob_ref).replace("\\", "/").split("?")[0])

        force_download = request.GET.get("download") == "1"
        inline_ok = content_type in ["application/pdf", "image/jpeg", "image/png", "image/gif"]

        response = HttpResponse(content, content_type=content_type)

        if force_download:
            disposition = "attachment"
        else:
            disposition = "inline" if inline_ok else "attachment"

        response["Content-Disposition"] = f'{disposition}; filename="{filename}"'
        return response

    except FileNotFoundError:
        raise Http404("Archivo no encontrado en el almacenamiento")
    except Exception as e:
        raise Http404(f"Error al obtener el archivo: {str(e)}")



@cache_control(max_age=86400)
def serve_avatar(request, perfil_id):
    perfil = get_object_or_404(DatosPersonales, pk=perfil_id)

    if not perfil.foto or not getattr(perfil.foto, "name", ""):
        default_image_path = os.path.join(settings.BASE_DIR, "static", "img", "default-avatar.png")
        if os.path.exists(default_image_path):
            return FileResponse(open(default_image_path, "rb"), content_type="image/png")
        raise Http404("No hay foto disponible")

    blob_name = perfil.foto.name

    try:
        content, blob_properties = AzureFileProxy.download_blob(blob_name)
        content_type = getattr(blob_properties.content_settings, "content_type", None) or "image/jpeg"

        response = HttpResponse(content, content_type=content_type)
        response["Content-Disposition"] = f'inline; filename="{os.path.basename(blob_name)}"'
        response["Cache-Control"] = "public, max-age=86400"
        return response

    except Exception:
        default_image_path = os.path.join(settings.BASE_DIR, "static", "img", "default-avatar.png")
        if os.path.exists(default_image_path):
            return FileResponse(open(default_image_path, "rb"), content_type="image/png")
        raise Http404("Error al cargar la imagen")

