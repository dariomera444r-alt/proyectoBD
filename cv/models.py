# cv/models.py
from django.db import models

class DatosPersonales(models.Model):
    idperfil = models.AutoField(primary_key=True)
    descripcionperfil = models.CharField(max_length=50, blank=True, null=True)
    perfilactivo = models.IntegerField(default=1)

    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)

    nacionalidad = models.CharField(max_length=20, blank=True, null=True)
    lugarnacimiento = models.CharField(max_length=60, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)

    numerocedula = models.CharField(max_length=10, unique=True)

    sexo = models.CharField(max_length=1, blank=True, null=True)
    estadocivil = models.CharField(max_length=50, blank=True, null=True)

    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)

    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)

    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50, blank=True, null=True)

    sitioweb = models.CharField(max_length=60, blank=True, null=True)

    foto = models.ImageField(upload_to="perfil/foto/", blank=True, null=True)
    cv_pdf = models.FileField(upload_to="perfil/cv/", blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Datos personales"
        verbose_name_plural = "Datos personales"

class ExperienciaLaboral(models.Model):
    idexperiencilaboral = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="experiencias"
    )

    cargodesempenado = models.CharField(max_length=100, blank=True, null=True)
    nombrempresa = models.CharField(max_length=50, blank=True, null=True)
    lugarempresa = models.CharField(max_length=50, blank=True, null=True)
    emailempresa = models.CharField(max_length=100, blank=True, null=True)
    sitiowebempresa = models.CharField(max_length=100, blank=True, null=True)

    nombrecontactoempresarial = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoempresarial = models.CharField(max_length=60, blank=True, null=True)

    fechainiciogestion = models.DateField(blank=True, null=True)
    fechafingestion = models.DateField(blank=True, null=True)

    descripcionfunciones = models.CharField(max_length=100, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    rutacertificado = models.FileField(upload_to="experiencia/certificados/", blank=True, null=True)

    def __str__(self):
        return f"{self.cargodesempenado or ''} - {self.nombrempresa or ''}".strip()

class Reconocimientos(models.Model):
    idreconocimiento = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="reconocimientos"
    )

    tiporeconocimiento = models.CharField(max_length=50, blank=True, null=True)
    descripcionreconocimiento = models.CharField(max_length=100, blank=True, null=True)
    fechareconocimiento = models.DateField(blank=True, null=True)

    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    rutacertificado = models.FileField(upload_to="reconocimientos/evidencias/", blank=True, null=True)

    def __str__(self):
        return self.descripcionreconocimiento or "Reconocimiento"

class CursosRealizados(models.Model):
    idcursorealizado = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="cursos"
    )

    nombrecurso = models.CharField(max_length=100)
    descripcioncurso = models.CharField(max_length=100, blank=True, null=True)

    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)

    totalhoras = models.IntegerField(blank=True, null=True)

    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    rutacertificado = models.FileField(upload_to="cursos/certificados/", blank=True, null=True)

    def __str__(self):
        return self.nombrecurso

class ProductosAcademicos(models.Model):
    idproductoacademico = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="productos_academicos"
    )

    nombrerecurso = models.CharField(max_length=100, blank=True, null=True)
    clasificador = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombrerecurso or "Producto académico"

class ProductosLaborales(models.Model):
    idproductoslaborales = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="productos_laborales"
    )

    nombreproducto = models.CharField(max_length=100, blank=True, null=True)
    fechaproducto = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreproducto or "Producto laboral"

class VentaGarage(models.Model):
    idventagarage = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="garage"
    )

    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    valordelbien = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreproducto