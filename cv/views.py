from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, FileResponse, JsonResponse
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


def print_preview_improved(request):
    """Vista mejorada para la vista previa de impresión"""
    try:
        # Obtener perfil con manejo seguro
        perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
        
        # Obtener configuración de visibilidad
        from .visibilidad import obtener_configuracion_visibilidad
        config = obtener_configuracion_visibilidad(perfil.idperfil) if perfil else None
        
        # Obtener configuraciones desde URL
        sections_config = {
            "datos_personales": request.GET.get("datos-personales", "1") == "1",
            "experiencia": request.GET.get("experiencia", "1") == "1",
            "cursos": request.GET.get("cursos", "1") == "1",
            "reconocimientos": request.GET.get("reconocimientos", "1") == "1",
            "productos_academicos": request.GET.get("productos-academicos", "1") == "1",
            "productos_laborales": request.GET.get("productos-laborales", "1") == "1",
            "venta_garage": request.GET.get("venta-garage", "1") == "1",
        }
        
        # Obtener los modelos con manejo seguro
        context_data = {}
        
        if perfil and config:
            try:
                context_data["experiencias"] = ExperienciaLaboral.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechafingestion')
            except Exception as e:
                print(f"Error cargando experiencias: {e}")
                context_data["experiencias"] = []

            try:
                context_data["cursos"] = CursosRealizados.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechafin')
            except Exception as e:
                print(f"Error cargando cursos: {e}")
                context_data["cursos"] = []

            try:
                context_data["reconocimientos"] = Reconocimientos.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechareconocimiento')
            except Exception as e:
                print(f"Error cargando reconocimientos: {e}")
                context_data["reconocimientos"] = []

            try:
                context_data["prod_acad"] = ProductosAcademicos.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                )
            except Exception as e:
                print(f"Error cargando productos académicos: {e}")
                context_data["prod_acad"] = []

            try:
                context_data["prod_lab"] = ProductosLaborales.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechaproducto')
            except Exception as e:
                print(f"Error cargando productos laborales: {e}")
                context_data["prod_lab"] = []

            try:
                context_data["garage"] = VentaGarage.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-idventagarage')
            except Exception as e:
                print(f"Error cargando garage: {e}")
                context_data["garage"] = []
        else:
            # Si no hay perfil o config, datos vacíos
            context_data = {
                "experiencias": [],
                "cursos": [],
                "reconocimientos": [],
                "prod_acad": [],
                "prod_lab": [],
                "garage": [],
            }

        context = {
            "perfil": perfil,
            "config": config,
            **context_data,
            "sections_config": sections_config,
        }

        return render(request, "hoja_vida_print_improved.html", context)

    except Exception as e:
        print(f"Error en print_preview: {e}")
        return render(request, "hoja_vida_print_improved.html", {
            "perfil": None,
            "config": None,
            "experiencias": [],
            "cursos": [],
            "reconocimientos": [],
            "prod_acad": [],
            "prod_lab": [],
            "garage": [],
            "sections_config": {
                "datos_personales": False,
                "experiencia": False,
                "cursos": False,
                "reconocimientos": False,
                "productos_academicos": False,
                "productos_laborales": False,
                "vista_garage": False,
            }
        })

def hoja_vida(request):
    """Vista original para hoja de vida"""
    try:
        # Obtener perfil con manejo seguro
        perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
        
        # Obtener configuración de visibilidad
        from .visibilidad import obtener_configuracion_visibilidad
        config = obtener_configuracion_visibilidad(perfil.idperfil) if perfil else None
        
        # Obtener los modelos con manejo seguro de errores
        context_data = {}

        if perfil and config:
            # Experiencias
            try:
                context_data["experiencias"] = ExperienciaLaboral.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechafingestion')
            except Exception as e:
                print(f"Error cargando experiencias: {e}")
                context_data["experiencias"] = []

            # Cursos
            try:
                context_data["cursos"] = CursosRealizados.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechafin')
            except Exception as e:
                print(f"Error cargando cursos: {e}")
                context_data["cursos"] = []

            # Reconocimientos
            try:
                context_data["reconocimientos"] = Reconocimientos.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechareconocimiento')
            except Exception as e:
                print(f"Error cargando reconocimientos: {e}")
                context_data["reconocimientos"] = []

            # Productos Académicos
            try:
                context_data["prod_acad"] = ProductosAcademicos.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                )
            except Exception as e:
                print(f"Error cargando productos académicos: {e}")
                context_data["prod_acad"] = []

            # Productos Laborales
            try:
                context_data["prod_lab"] = ProductosLaborales.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-fechaproducto')
            except Exception as e:
                print(f"Error cargando productos laborales: {e}")
                context_data["prod_lab"] = []

            # Garage
            try:
                context_data["garage"] = VentaGarage.objects.filter(
                    idperfilconqueestaactivo=perfil,
                    activarparaqueseveaenfront=True
                ).order_by('-idventagarage')
            except Exception as e:
                print(f"Error cargando garage: {e}")
                context_data["garage"] = []

        context = {
            "perfil": perfil,
            "config": config,
            **context_data,
        }

        return render(request, "hoja_vida_print.html", context)

    except Exception as e:
        print(f"Error general en hoja_vida: {e}")
        return render(request, "hoja_vida_print.html", {
            "perfil": None,
            "config": None,
            "experiencias": [],
            "cursos": [],
            "reconocimientos": [],
            "prod_acad": [],
            "prod_lab": [],
            "garage": [],
        })


def hoja_vida(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

    # Verificar si es vista previa o descarga
    is_preview = request.GET.get('preview') == '1'
    is_download = request.GET.get('download') == '1'

    # Obtener configuraciones de secciones desde URL o usar valores por defecto
    sections_config = {
        "datos_personales": request.GET.get("datos-personales", "1") == "1",
        "experiencia": request.GET.get("experiencia", "1") == "1",
        "cursos": request.GET.get("cursos", "1") == "1",
        "reconocimientos": request.GET.get("reconocimientos", "1") == "1",
        "productos_academicos": request.GET.get("productos-academicos", "1") == "1",
        "productos_laborales": request.GET.get("productos-laborales", "1") == "1",
        "venta_garage": request.GET.get("venta-garage", "1") == "1",
    }

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
        "is_preview": is_preview,
        "is_download": is_download,
        "sections_config": sections_config,
    }

    # Si es descarga, forzar impresión automática
    if is_download:
        response = render(request, "hoja_vida_cv.html", context)
        response['Content-Type'] = 'text/html'
        response['Content-Disposition'] = f'attachment; filename="CV_{perfil.nombres}_{perfil.apellidos}.html"' if perfil else 'attachment; filename="CV.html"'
        return response

    # ✅ tu HTML real
    return render(request, "hoja_vida_cv.html", context)


def garage(request):
    """Vista para la página de venta garage"""
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        raise Http404("Perfil no encontrado")
    
    productos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-idventagarage')
    
    context = {
        "perfil": perfil,
        "garage": productos,
    }
    
    return render(request, "garage.html", context)


def serve_protected_file(request, file_type, model_id, field_name):
    model_map = {
        "perfil": DatosPersonales,
        "experiencia": ExperienciaLaboral,
        "curso": CursosRealizados,
        "reconocimiento": Reconocimientos,
        "garage": VentaGarage,
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
        
        # No cachear archivos de garage para permitir actualizaciones de fotos
        if file_type == "garage":
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
        else:
            response["Cache-Control"] = "public, max-age=3600"
        
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


