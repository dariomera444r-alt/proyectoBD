# cv/admin.py - VALIDACIÓN COMPLETA Y BLOQUEANTE EN TODAS LAS TABLAS
from django.contrib import admin
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.safestring import mark_safe
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos,
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage,
    ConfiguracionVisibilidad
)

# ==================== VALIDADORES REUTILIZABLES ====================
class FechaInputWidget(forms.DateInput):
    """Widget personalizado para campos de fecha con formato DD/MM/YYYY"""
    format = '%d/%m/%Y'
    input_type = 'text'
    
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs.update({
            'class': 'vDateField',
            'placeholder': 'DD/MM/YYYY',
            'style': 'color: #000 !important; background-color: #fff !important; border: 1px solid #999 !important; padding: 10px !important; font-size: 14px !important; font-weight: 500 !important;'
        })
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)

# ==================== ADMIN: DatosPersonales ====================
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'fechanacimiento')
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    list_filter = ('perfilactivo',)
    
    formfield_overrides = {
        models.DateField: {'widget': FechaInputWidget()},
    }
    
    class Media:
        css = {
            'all': ('admin/css/custom_fields.css',)
        }
    
    fieldsets = (
        ('Datos Básicos', {
            'fields': ('descripcionperfil', 'perfilactivo', 'nombres', 'apellidos', 'numerocedula')
        }),
        ('Fecha de Nacimiento - VALIDACIÓN BLOQUEANTE', {
            'fields': ('fechanacimiento',),
            'description': mark_safe(
                '<div style="background-color: #ffe6e6; border: 2px solid red; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>🚫 IMPORTANTE:</strong> La fecha no puede ser futura, y la edad mínima es 18 años.<br>'
                'Rango válido: últimos 120 años (máximo realista)<br>'
                'Formato: DD/MM/YYYY'
                '</div>'
            )
        }),
        ('Información Personal', {
            'fields': ('nacionalidad', 'lugarnacimiento', 'sexo', 'estadocivil', 'licenciaconducir')
        }),
        ('Contacto', {
            'fields': ('telefonoconvencional', 'telefonofijo', 'direcciontrabajo', 'direcciondomiciliaria')
        }),
        ('Otros', {
            'fields': ('sitioweb', 'foto', 'cv_pdf')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Bloquea el guardado si hay validaciones fallidas"""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            from django.contrib import messages
            for field, error in e.error_dict.items():
                for err_msg in error:
                    messages.error(request, f'{field}: {err_msg}')
            raise

# ==================== ADMIN: ExperienciaLaboral ====================
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'fechafingestion')
    search_fields = ('cargodesempenado', 'nombrempresa')
    list_filter = ('activarparaqueseveaenfront',)
    
    formfield_overrides = {
        models.DateField: {'widget': FechaInputWidget()},
    }
    
    class Media:
        css = {
            'all': ('admin/css/custom_fields.css',)
        }
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('nombrempresa', 'lugarempresa', 'emailempresa', 'sitiowebempresa')
        }),
        ('Cargo y Funciones', {
            'fields': ('cargodesempenado', 'descripcionfunciones')
        }),
        ('Fechas - VALIDACIÓN BLOQUEANTE', {
            'fields': ('fechainiciogestion', 'fechafingestion'),
            'description': mark_safe(
                '<div style="background-color: #ffe6e6; border: 2px solid red; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>🚫 IMPORTANTE:</strong> Ambas fechas NO pueden ser futuras.<br>'
                'La fecha de inicio DEBE ser anterior a la fecha de fin.<br>'
                'Duración máxima: 50 años.'
                '</div>'
            )
        }),
        ('Contacto Empresarial', {
            'fields': ('nombrecontactoempresarial', 'telefonocontactoempresarial')
        }),
        ('Otros', {
            'fields': ('idperfilconqueestaactivo', 'activarparaqueseveaenfront', 'rutacertificado')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Bloquea el guardado si hay validaciones fallidas"""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            from django.contrib import messages
            for field, error in e.error_dict.items():
                for err_msg in error:
                    messages.error(request, f'{field}: {err_msg}')
            raise

# ==================== ADMIN: Reconocimientos ====================
@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'fechareconocimiento')
    search_fields = ('descripcionreconocimiento', 'tiporeconocimiento')
    list_filter = ('activarparaqueseveaenfront',)
    
    formfield_overrides = {
        models.DateField: {'widget': FechaInputWidget()},
    }
    
    class Media:
        css = {
            'all': ('admin/css/custom_fields.css',)
        }
    
    fieldsets = (
        ('Información del Reconocimiento - VALIDACIÓN BLOQUEANTE', {
            'fields': ('tiporeconocimiento', 'descripcionreconocimiento', 'fechareconocimiento'),
            'description': mark_safe(
                '<div style="background-color: #ffe6e6; border: 2px solid red; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>🚫 IMPORTANTE:</strong> La fecha NO puede ser futura.<br>'
                'Año mínimo: 2000'
                '</div>'
            )
        }),
        ('Entidad Patrocinadora', {
            'fields': ('entidadpatrocinadora', 'nombrecontactoauspicia', 'telefonocontactoauspicia')
        }),
        ('Otros', {
            'fields': ('idperfilconqueestaactivo', 'activarparaqueseveaenfront', 'rutacertificado')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Bloquea el guardado si hay validaciones fallidas"""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            from django.contrib import messages
            for field, error in e.error_dict.items():
                for err_msg in error:
                    messages.error(request, f'{field}: {err_msg}')
            raise

# ==================== ADMIN: CursosRealizados ====================
@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'fechainicio', 'fechafin', 'totalhoras')
    search_fields = ('nombrecurso', 'entidadpatrocinadora')
    list_filter = ('activarparaqueseveaenfront',)
    
    formfield_overrides = {
        models.DateField: {'widget': FechaInputWidget()},
    }
    
    class Media:
        css = {
            'all': ('admin/css/custom_fields.css',)
        }
    
    fieldsets = (
        ('Información del Curso', {
            'fields': ('nombrecurso', 'descripcioncurso', 'entidadpatrocinadora', 'totalhoras'),
            'description': mark_safe(
                '<div style="background-color: #f0f7ff; border: 2px solid #2196F3; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>ℹ️ INFORMACIÓN:</strong><br>'
                'Las horas totales deben ser >= 1 hora. Se aceptan valores desde 1 en adelante.'
                '</div>'
            )
        }),
        ('Fechas - 🚫 VALIDACIÓN BLOQUEANTE ESTRICTA', {
            'fields': ('fechainicio', 'fechafin'),
            'description': mark_safe(
                '<div style="background-color: #ffe6e6; border: 2px solid red; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>🚫 VALIDACIÓN CRÍTICA:</strong><br>'
                '✗ NO se permiten fechas futuras (como mañana)<br>'
                '✗ fechainicio DEBE ser anterior a fechafin<br>'
                '✗ Duración máxima: 2 años<br>'
                '✗ Año mínimo: 2000<br>'
                '<br><strong>SI INCUMPLE ESTAS REGLAS, NO SE GUARDARÁ</strong>'
                '</div>'
            )
        }),
        ('Otros', {
            'fields': ('idperfilconqueestaactivo', 'activarparaqueseveaenfront', 'rutacertificado')
        }),
    )

    def save_model(self, request, obj, form, change):
        """🚫 BLOQUEANTE: Impide guardar si hay errores de validación"""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
            from django.contrib import messages
            messages.success(request, '✅ Curso guardado correctamente con todas las validaciones')
        except ValidationError as e:
            from django.contrib import messages
            messages.error(request, '🚫 ERROR: No se puede guardar. Verifique las fechas:')
            for field, error in e.error_dict.items():
                for err_msg in error:
                    messages.error(request, f'  ❌ {field}: {err_msg}')
            raise

# ==================== ADMIN: ProductosAcademicos ====================
@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador')
    search_fields = ('nombrerecurso', 'clasificador')
    list_filter = ('activarparaqueseveaenfront',)

# ==================== ADMIN: ProductosLaborales ====================
@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto')
    search_fields = ('nombreproducto',)
    list_filter = ('activarparaqueseveaenfront',)
    
    formfield_overrides = {
        models.DateField: {'widget': FechaInputWidget()},
    }
    
    class Media:
        css = {
            'all': ('admin/css/custom_fields.css',)
        }
    
    
    fieldsets = (
        ('Información del Producto - VALIDACIÓN BLOQUEANTE', {
            'fields': ('nombreproducto', 'descripcion', 'fechaproducto'),
            'description': mark_safe(
                '<div style="background-color: #ffe6e6; border: 2px solid red; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>🚫 IMPORTANTE:</strong> La fecha NO puede ser futura.<br>'
                'Año mínimo: 2000'
                '</div>'
            )
        }),
        ('Otros', {
            'fields': ('idperfilconqueestaactivo', 'activarparaqueseveaenfront')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Bloquea el guardado si hay validaciones fallidas"""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            from django.contrib import messages
            for field, error in e.error_dict.items():
                for err_msg in error:
                    messages.error(request, f'{field}: {err_msg}')
            raise

# ==================== ADMIN: VentaGarage ====================
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'estadoproducto', 'valordelbien')
    search_fields = ('nombreproducto', 'estadoproducto')
    list_filter = ('activarparaqueseveaenfront',)


# ==================== ADMIN: ConfiguracionVisibilidad ====================
@admin.register(ConfiguracionVisibilidad)
class ConfiguracionVisibilidadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'contar_secciones_activas', 'fecha_actualizacion')
    search_fields = ('perfil__nombres', 'perfil__apellidos')
    readonly_fields = ('fecha_actualizacion',)
    
    fieldsets = (
        ('Perfil', {
            'fields': ('perfil',)
        }),
        
        ('🎯 Secciones Principales', {
            'fields': (
                'mostrar_datos_personales',
                'mostrar_experiencia_laboral',
                'mostrar_cursos',
                'mostrar_reconocimientos',
                'mostrar_productos_academicos',
                'mostrar_productos_laborales',
                'mostrar_venta_garage',
            ),
            'description': mark_safe(
                '<div style="background-color: #e3f2fd; border: 2px solid #2196F3; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>✅ SELECCIONA QUÉ SECCIONES MOSTRAR</strong><br>'
                'Marca o desmarca los checkboxes para controlar qué información aparece en tu página de vida.'
                '</div>'
            )
        }),
        
        ('🎨 Elementos Adicionales', {
            'fields': (
                'mostrar_foto_perfil',
                'mostrar_contacto',
                'mostrar_cv_descargable',
            ),
            'description': mark_safe(
                '<div style="background-color: #f3e5f5; border: 2px solid #9c27b0; padding: 10px; border-radius: 5px; color: #000;">'
                '<strong>✨ ELEMENTOS VISUALES</strong><br>'
                'Controla elementos adicionales de tu perfil.'
                '</div>'
            )
        }),
        
        ('📅 Información del Sistema', {
            'fields': ('fecha_actualizacion',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Solo permitir editar perfil al crear, no al editar"""
        if obj:  # Si estamos editando un objeto existente
            return self.readonly_fields + ('perfil',)
        return self.readonly_fields
    
    def has_add_permission(self, request):
        """Limitar a una sola configuración por perfil"""
        # Contar cuántos objetos existen
        return ConfiguracionVisibilidad.objects.count() == 0
    
    def contar_secciones_activas(self, obj):
        """Mostrar cuántas secciones están activas"""
        count = obj.contar_secciones_activas()
        total = 10  # Total de opciones
        
        if count == total:
            color = 'green'
            emoji = '✅'
        elif count >= 7:
            color = 'blue'
            emoji = '✔️'
        elif count >= 5:
            color = 'orange'
            emoji = '⚠️'
        else:
            color = 'red'
            emoji = '⛔'
        
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">'
            f'{emoji} {count}/{total} secciones activas</span>'
        )
    
    contar_secciones_activas.short_description = 'Estado de Secciones'
    
    def save_model(self, request, obj, form, change):
        """Guardar y mostrar mensaje de confirmación"""
        super().save_model(request, obj, form, change)
        
        from django.contrib import messages
        activas = obj.contar_secciones_activas()
        messages.success(
            request, 
            f'✅ Configuración guardada. {activas} secciones activas.'
        )