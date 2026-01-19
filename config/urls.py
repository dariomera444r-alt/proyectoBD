from django.contrib import admin
from django.urls import path

from cv.views import hoja_vida, serve_protected_file, serve_avatar

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", hoja_vida, name="hoja_vida"),

    path("protected/<str:file_type>/<int:model_id>/<str:field_name>/", serve_protected_file, name="serve_protected_file"),
    path("avatar/<int:perfil_id>/", serve_avatar, name="serve_avatar"),
]
