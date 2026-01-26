# cv/models.py
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# ==================== VALIDADORES REUTILIZABLES ====================
def validar_no_fecha_futura(value):
    """🚫 BLOQUEANTE: Valida que la fecha NO sea futura"""
    if value and value > timezone.now().date():
        raise ValidationError("🚫 ERROR: No se permiten fechas futuras.")
    return value


def validar_fecha_inicio_anterior_fin(fecha_inicio, fecha_fin):
    """🚫 BLOQUEANTE: Valida que fecha_inicio < fecha_fin"""
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise ValidationError(
            "🚫 ERROR: La fecha de inicio ({}) debe ser anterior a la fecha de fin ({})".format(
                fecha_inicio, fecha_fin
            )
        )
    return True


def validar_horas_no_negativas(value):
    """🚫 BLOQUEANTE: Valida que las horas sean >= 1"""
    if value is not None and value < 1:
        raise ValidationError("🚫 ERROR: Las horas deben ser >= 1 hora.")
    return value


# ==================== MODELO: DatosPersonales ====================
class DatosPersonales(models.Model):
    idperfil = models.AutoField(primary_key=True)
    descripcionperfil = models.CharField(max_length=50, blank=True, null=True)
    perfilactivo = models.IntegerField(default=1)

    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)

    nacionalidad = models.CharField(max_length=20, blank=True, null=True)
    lugarnacimiento = models.CharField(max_length=60, blank=True, null=True)
    fechanacimiento = models.DateField(
        blank=True,
        null=True,
        validators=[validar_no_fecha_futura],
    )

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

    def clean(self):
        """🚫 VALIDACIÓN BLOQUEANTE"""
        super().clean()
        errores = {}
        hoy = timezone.now().date()

        if self.fechanacimiento:
            if self.fechanacimiento > hoy:
                errores["fechanacimiento"] = (
                    "🚫 ERROR: La fecha de nacimiento no puede ser futura."
                )
            elif self.fechanacimiento.year < 1900:
                errores["fechanacimiento"] = (
                    "🚫 ERROR: Año mínimo permitido: 1900."
                )
            else:
                edad_minima = hoy.replace(year=hoy.year - 12)
                if self.fechanacimiento > edad_minima:
                    errores["fechanacimiento"] = (
                        "🚫 ERROR: La edad mínima debe ser 12 años."
                    )

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        """Fuerza la validación antes de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Datos personales"
        verbose_name_plural = "Datos personales"


# ==================== MODELO: ExperienciaLaboral ====================
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

    fechainiciogestion = models.DateField(
        blank=True,
        null=True,
        validators=[validar_no_fecha_futura],
    )
    fechafingestion = models.DateField(
        blank=True,
        null=True,
        validators=[validar_no_fecha_futura],
    )

    descripcionfunciones = models.CharField(max_length=100, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    rutacertificado = models.FileField(
        upload_to="experiencia/certificados/", blank=True, null=True
    )

    def clean(self):
        """🚫 VALIDACIÓN BLOQUEANTE"""
        super().clean()
        errores = {}
        hoy = timezone.now().date()

        if self.fechainiciogestion and self.fechainiciogestion > hoy:
            errores["fechainiciogestion"] = (
                "🚫 ERROR: La fecha de inicio no puede ser futura."
            )

        if self.fechafingestion and self.fechafingestion > hoy:
            errores["fechafingestion"] = (
                "🚫 ERROR: La fecha de fin no puede ser futura."
            )

        if self.fechainiciogestion and self.fechafingestion:
            if self.fechainiciogestion > self.fechafingestion:
                errores["fechainiciogestion"] = (
                    "🚫 ERROR: La fecha de inicio debe ser anterior a la fecha de fin."
                )
                errores["fechafingestion"] = (
                    "🚫 ERROR: La fecha de fin debe ser posterior a la fecha de inicio."
                )

            duracion_dias = (self.fechafingestion - self.fechainiciogestion).days
            if duracion_dias > 365 * 50:
                errores["fechafingestion"] = (
                    "🚫 ERROR: Duración máxima permitida: 50 años "
                    f"(actual: {duracion_dias} días)."
                )

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        """Fuerza la validación antes de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cargodesempenado or ''} - {self.nombrempresa or ''}".strip()


# ==================== MODELO: Reconocimientos ====================
class Reconocimientos(models.Model):
    idreconocimiento = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="reconocimientos"
    )

    tiporeconocimiento = models.CharField(max_length=50, blank=True, null=True)
    descripcionreconocimiento = models.CharField(max_length=100, blank=True, null=True)
    fechareconocimiento = models.DateField(
        blank=True,
        null=True,
        validators=[validar_no_fecha_futura],
    )

    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    rutacertificado = models.FileField(
        upload_to="reconocimientos/evidencias/", blank=True, null=True
    )

    def clean(self):
        """🚫 VALIDACIÓN BLOQUEANTE"""
        super().clean()
        errores = {}
        hoy = timezone.now().date()

        if self.fechareconocimiento:
            if self.fechareconocimiento > hoy:
                errores["fechareconocimiento"] = (
                    "🚫 ERROR: La fecha de reconocimiento no puede ser futura."
                )
            elif self.fechareconocimiento.year < 2000:
                errores["fechareconocimiento"] = "🚫 ERROR: Año mínimo permitido: 2000."

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        """Fuerza la validación antes de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descripcionreconocimiento or "Reconocimiento"


# ==================== MODELO: CursosRealizados ====================
class CursosRealizados(models.Model):
    idcursorealizado = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="cursos"
    )

    nombrecurso = models.CharField(max_length=100)
    descripcioncurso = models.CharField(max_length=100, blank=True, null=True)

    fechainicio = models.DateField(
        blank=True,
        null=True,
        validators=[validar_no_fecha_futura],
    )
    fechafin = models.DateField(
        blank=True,
        null=True,
        validators=[validar_no_fecha_futura],
    )

    totalhoras = models.IntegerField(
        blank=True, null=True, validators=[validar_horas_no_negativas]
    )

    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    rutacertificado = models.FileField(
        upload_to="cursos/certificados/", blank=True, null=True
    )

    def clean(self):
        """🚫 VALIDACIÓN BLOQUEANTE - IMPIDE GUARDAR CURSOS CON FECHAS INVÁLIDAS"""
        super().clean()
        errores = {}
        hoy = timezone.now().date()

        if self.totalhoras is not None and self.totalhoras < 1:
            errores["totalhoras"] = "🚫 ERROR: Las horas deben ser >= 1 hora."

        if self.fechainicio:
            if self.fechainicio > hoy:
                errores["fechainicio"] = (
                    "🚫 ERROR: La fecha de inicio no puede ser futura."
                )
            elif self.fechainicio.year < 2000:
                errores["fechainicio"] = "🚫 ERROR: Año mínimo permitido: 2000."

        if self.fechafin:
            if self.fechafin > hoy:
                errores["fechafin"] = "🚫 ERROR: La fecha de fin no puede ser futura."
            elif self.fechafin.year < 2000:
                errores["fechafin"] = "🚫 ERROR: Año mínimo permitido: 2000."

        if self.fechainicio and self.fechafin:
            if self.fechainicio > self.fechafin:
                errores["fechainicio"] = (
                    "🚫 ERROR: La fecha de inicio debe ser anterior a la fecha de fin."
                )
                errores["fechafin"] = (
                    "🚫 ERROR: La fecha de fin debe ser posterior a la fecha de inicio."
                )

            duracion_dias = (self.fechafin - self.fechainicio).days
            if duracion_dias > 730:
                errores["fechafin"] = (
                    "🚫 ERROR: Duración máxima para un curso: 2 años "
                    f"(actual: {duracion_dias} días)."
                )

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        """Fuerza la validación antes de guardar - IMPIDE GUARDAR SI HAY ERRORES"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombrecurso


# ==================== MODELO: ProductosAcademicos ====================
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


# ==================== MODELO: ProductosLaborales ====================
class ProductosLaborales(models.Model):
    idproductoslaborales = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="productos_laborales"
    )

    nombreproducto = models.CharField(max_length=100, blank=True, null=True)
    fechaproducto = models.DateField(
        blank=True,
        null=True,
        validators=[validar_no_fecha_futura],
    )
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def clean(self):
        """🚫 VALIDACIÓN BLOQUEANTE"""
        super().clean()
        errores = {}
        hoy = timezone.now().date()

        if self.fechaproducto:
            if self.fechaproducto > hoy:
                errores["fechaproducto"] = (
                    "🚫 ERROR: La fecha del producto no puede ser futura."
                )
            elif self.fechaproducto.year < 2000:
                errores["fechaproducto"] = "🚫 ERROR: Año mínimo permitido: 2000."

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        """Fuerza la validación antes de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombreproducto or "Producto laboral"


# ==================== MODELO: VentaGarage ====================
class VentaGarage(models.Model):
    idventagarage = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="garage"
    )

    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    valordelbien = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    disponible = models.BooleanField(default=True, verbose_name="Disponible")

    foto = models.ImageField(upload_to="garage/productos/", blank=True, null=True)
    foto2 = models.ImageField(upload_to="garage/productos/", blank=True, null=True)
    foto3 = models.ImageField(upload_to="garage/productos/", blank=True, null=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Producto en Venta"
        verbose_name_plural = "Productos en Venta"
        ordering = ["-idventagarage"]

    def get_fotos(self):
        """Retorna lista de fotos disponibles"""
        fotos = []
        if self.foto:
            fotos.append(("foto", self.foto))
        if self.foto2:
            fotos.append(("foto2", self.foto2))
        if self.foto3:
            fotos.append(("foto3", self.foto3))
        return fotos

    def __str__(self):
        return self.nombreproducto


# ==================== MODELO: ConfiguracionVisibilidad ====================
class ConfiguracionVisibilidad(models.Model):
    """
    Modelo para controlar qué secciones se muestran en la página del proyecto de vida
    """

    perfil = models.OneToOneField(
        "DatosPersonales",
        on_delete=models.CASCADE,
        related_name="configuracion_visibilidad",
        verbose_name="Perfil",
    )

    mostrar_datos_personales = models.BooleanField(
        default=True, verbose_name="Mostrar Datos Personales"
    )
    mostrar_experiencia_laboral = models.BooleanField(
        default=True, verbose_name="Mostrar Experiencia Laboral"
    )
    mostrar_cursos = models.BooleanField(
        default=True, verbose_name="Mostrar Cursos Realizados"
    )
    mostrar_reconocimientos = models.BooleanField(
        default=True, verbose_name="Mostrar Reconocimientos"
    )
    mostrar_productos_academicos = models.BooleanField(
        default=True, verbose_name="Mostrar Productos Académicos"
    )
    mostrar_productos_laborales = models.BooleanField(
        default=True, verbose_name="Mostrar Productos Laborales"
    )
    mostrar_venta_garage = models.BooleanField(
        default=False, verbose_name="Mostrar Venta Garage"
    )

    mostrar_foto_perfil = models.BooleanField(
        default=True, verbose_name="Mostrar Foto de Perfil"
    )
    mostrar_contacto = models.BooleanField(
        default=True, verbose_name="Mostrar Información de Contacto"
    )
    mostrar_cv_descargable = models.BooleanField(
        default=True, verbose_name="Mostrar CV Descargable"
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True, verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Configuración de Visibilidad"
        verbose_name_plural = "Configuración de Visibilidad"

    def __str__(self):
        return f"Configuración de {self.perfil.nombres} {self.perfil.apellidos}"

    def get_secciones_activas(self):
        """Retorna un diccionario con las secciones activas"""
        return {
            "datos_personales": self.mostrar_datos_personales,
            "experiencia_laboral": self.mostrar_experiencia_laboral,
            "cursos": self.mostrar_cursos,
            "reconocimientos": self.mostrar_reconocimientos,
            "productos_academicos": self.mostrar_productos_academicos,
            "productos_laborales": self.mostrar_productos_laborales,
            "venta_garage": self.mostrar_venta_garage,
            "foto_perfil": self.mostrar_foto_perfil,
            "contacto": self.mostrar_contacto,
            "cv_descargable": self.mostrar_cv_descargable,
        }

    def contar_secciones_activas(self):
        """Retorna la cantidad de secciones activas"""
        return sum(1 for v in self.get_secciones_activas().values() if v)
