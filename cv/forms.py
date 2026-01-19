from django import forms
from .models import Perfil, Proyecto, CursoRealizado

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = "__all__"


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = "__all__"


class CursoForm(forms.ModelForm):
    class Meta:
        model = CursoRealizado
        fields = "__all__"
