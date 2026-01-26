# cv/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    DatosPersonales, 
    ExperienciaLaboral, 
    Reconocimientos, 
    CursosRealizados, 
    ProductosAcademicos, 
    ProductosLaborales, 
    VentaGarage
)

# ==================== FORMULARIO: DatosPersonales ====================
class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = "__all__"
        widgets = {
            'fechanacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_nacimiento = cleaned_data.get('fechanacimiento')
        hoy = timezone.now().date()
        
        if fecha_nacimiento:
            # No futura
            if fecha_nacimiento > hoy:
                self.add_error('fechanacimiento', '🚫 ERROR: La fecha de nacimiento no puede ser futura.')
            # Edad mínima (12 años)
            elif fecha_nacimiento.year < 1900:
                self.add_error('fechanacimiento', '🚫 ERROR: Año mínimo permitido: 1900.')
            else:
                edad_minima = hoy.replace(year=hoy.year - 12)
                if fecha_nacimiento > edad_minima:
                    self.add_error('fechanacimiento', '🚫 ERROR: La edad mínima debe ser 12 años.')
        
        return cleaned_data

# ==================== FORMULARIO: ExperienciaLaboral ====================
class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = "__all__"
        widgets = {
            'fechainiciogestion': forms.DateInput(attrs={'type': 'date'}),
            'fechafingestion': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fechainiciogestion')
        fecha_fin = cleaned_data.get('fechafingestion')
        hoy = timezone.now().date()
        
        # Validar fechas no futuras
        if fecha_inicio and fecha_inicio > hoy:
            self.add_error('fechainiciogestion', '🚫 ERROR: La fecha de inicio no puede ser futura.')
        
        if fecha_fin and fecha_fin > hoy:
            self.add_error('fechafingestion', '🚫 ERROR: La fecha de fin no puede ser futura.')
        
        # Validar orden de fechas (inicio < fin)
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                self.add_error('fechainiciogestion', '🚫 ERROR: La fecha de inicio debe ser anterior a la fecha de fin.')
                self.add_error('fechafingestion', '🚫 ERROR: La fecha de fin debe ser posterior a la fecha de inicio.')
            
            # Validar duración máxima (50 años)
            duracion_dias = (fecha_fin - fecha_inicio).days
            if duracion_dias > 365 * 50:
                self.add_error('fechafingestion', f'🚫 ERROR: Duración máxima permitida: 50 años (actual: {duracion_dias} días).')
        
        return cleaned_data

# ==================== FORMULARIO: Reconocimientos ====================
class ReconocimientosForm(forms.ModelForm):
    class Meta:
        model = Reconocimientos
        fields = "__all__"
        widgets = {
            'fechareconocimiento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_reconocimiento = cleaned_data.get('fechareconocimiento')
        hoy = timezone.now().date()
        
        if fecha_reconocimiento:
            # No futura
            if fecha_reconocimiento > hoy:
                self.add_error('fechareconocimiento', '🚫 ERROR: La fecha de reconocimiento no puede ser futura.')
            # Mínimo año 2000
            elif fecha_reconocimiento.year < 2000:
                self.add_error('fechareconocimiento', '🚫 ERROR: Año mínimo permitido: 2000.')
        
        return cleaned_data

# ==================== FORMULARIO: CursosRealizados ====================
class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        fields = "__all__"
        widgets = {
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fechainicio')
        fecha_fin = cleaned_data.get('fechafin')
        hoy = timezone.now().date()

        # 🚫 VALIDAR FECHAS NO FUTURAS
        if fecha_inicio and fecha_inicio > hoy:
            self.add_error('fechainicio', '🚫 ERROR: La fecha de inicio no puede ser futura.')

        if fecha_fin and fecha_fin > hoy:
            self.add_error('fechafin', '🚫 ERROR: La fecha de fin no puede ser futura.')

        # 🚫 VALIDAR QUE INICIO < FIN
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                self.add_error('fechainicio', '🚫 ERROR: La fecha de inicio debe ser anterior a la fecha de fin.')
                self.add_error('fechafin', '🚫 ERROR: La fecha de fin debe ser posterior a la fecha de inicio.')

            # Validar duración máxima (2 años para cursos)
            duracion_dias = (fecha_fin - fecha_inicio).days
            if duracion_dias > 730:  # 2 años
                self.add_error('fechafin', f'🚫 ERROR: Duración máxima para un curso: 2 años (actual: {duracion_dias} días).')

        return cleaned_data

# ==================== FORMULARIO: ProductosAcademicos ====================
class ProductosAcademicosForm(forms.ModelForm):
    class Meta:
        model = ProductosAcademicos
        fields = "__all__"

# ==================== FORMULARIO: ProductosLaborales ====================
class ProductosLaboralesForm(forms.ModelForm):
    class Meta:
        model = ProductosLaborales
        fields = "__all__"
        widgets = {
            'fechaproducto': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_producto = cleaned_data.get('fechaproducto')
        hoy = timezone.now().date()
        
        if fecha_producto:
            # No futura
            if fecha_producto > hoy:
                self.add_error('fechaproducto', '🚫 ERROR: La fecha del producto no puede ser futura.')
            # Mínimo año 2000
            elif fecha_producto.year < 2000:
                self.add_error('fechaproducto', '🚫 ERROR: Año mínimo permitido: 2000.')
        
        return cleaned_data

# ==================== FORMULARIO: VentaGarage ====================
class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        fields = ['nombreproducto', 'descripcion', 'estadoproducto', 'valordelbien', 'disponible', 'foto', 'foto2', 'foto3', 'activarparaqueseveaenfront']
        widgets = {
            'nombreproducto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto',
                'rows': 4
            }),
            'estadoproducto': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[
                ('', 'Seleccionar estado...'),
                ('Disponible', 'Disponible'),
                ('Vendido', 'Vendido'),
                ('Reservado', 'Reservado'),
            ]),
            'valordelbien': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.01',
                'step': '0.01',
                'min': '0.01'
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'foto2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'foto3': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'activarparaqueseveaenfront': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_valordelbien(self):
        """Validar que el valor sea mayor que 0"""
        valor = self.cleaned_data.get('valordelbien')
        if valor is not None and valor <= 0:
            raise forms.ValidationError('El precio debe ser mayor que 0.')
        return valor