from django.contrib import admin
from django.urls import path, include

from cv.views import hoja_vida, serve_protected_file, serve_avatar, print_preview_improved

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", hoja_vida, name="hoja_vida"),
    path("print-preview/", print_preview_improved, name="print_preview"),
    path("print-preview-improved/", print_preview_improved, name="print_preview_improved"),
    path("garage/", include("cv.urls")),

    path("protected/<str:file_type>/<int:model_id>/<str:field_name>/", serve_protected_file, name="serve_protected_file"),
    path("avatar/<int:perfil_id>/", serve_avatar, name="serve_avatar"),
]
