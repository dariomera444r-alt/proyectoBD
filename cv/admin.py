from django.contrib import admin
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos,
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'perfilactivo')
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    list_filter = ('perfilactivo',)

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion')
    search_fields = ('cargodesempenado', 'nombrempresa')
    list_filter = ('activarparaqueseveaenfront',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'fechainicio')
    search_fields = ('nombrecurso', 'entidadpatrocinadora')
    list_filter = ('activarparaqueseveaenfront',)

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'fechareconocimiento')
    search_fields = ('descripcionreconocimiento', 'tiporeconocimiento')
    list_filter = ('activarparaqueseveaenfront',)

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador')
    search_fields = ('nombrerecurso', 'clasificador')
    list_filter = ('activarparaqueseveaenfront',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto')
    search_fields = ('nombreproducto',)
    list_filter = ('activarparaqueseveaenfront',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'estadoproducto', 'valordelbien')
    search_fields = ('nombreproducto', 'estadoproducto')
    list_filter = ('activarparaqueseveaenfront',)