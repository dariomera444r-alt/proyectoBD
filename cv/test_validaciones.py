from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from cv.models import DatosPersonales, CursosRealizados

def get_perfil():
    """Obtiene el primer perfil activo para las pruebas"""
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if not perfil:
        # Fallback si no hay activo, intenta obtener cualquiera
        perfil = DatosPersonales.objects.first()
    return perfil

def test_fechas_futuras():
    perfil = get_perfil()
    if not perfil:
        print("⚠️ No se encontró perfil para realizar la prueba.")
        return False
    
    # Fecha mañana (Futura)
    fecha_futura = timezone.now().date() + timedelta(days=1)
    
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Futuro Test",
        fechainicio=fecha_futura,
        fechafin=fecha_futura + timedelta(days=5)
    )
    
    try:
        curso.full_clean() # Forzar validación explícita
        curso.save()
        print("❌ FALLO: Se guardó un curso con fecha futura (Debería haber fallado)")
        curso.delete()
        return False
    except ValidationError as e:
        print(f"✅ ÉXITO: Validación de fecha futura capturada correctamente: {e}")
        return True

def test_fecha_inicio_mayor_fin():
    perfil = get_perfil()
    if not perfil: return False
    
    hoy = timezone.now().date()
    ayer = hoy - timedelta(days=1)
    
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Incoherente Test",
        fechainicio=hoy,     # Inicio: Hoy
        fechafin=ayer        # Fin: Ayer (Error)
    )
    
    try:
        curso.full_clean()
        curso.save()
        print("❌ FALLO: Se guardó inicio > fin (Debería haber fallado)")
        curso.delete()
        return False
    except ValidationError as e:
        print(f"✅ ÉXITO: Validación inicio > fin capturada correctamente: {e}")
        return True

def test_fechas_validas():
    perfil = get_perfil()
    if not perfil: return False
    
    hoy = timezone.now().date()
    hace_mes = hoy - timedelta(days=30)
    
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Válido Test",
        fechainicio=hace_mes,
        fechafin=hoy
    )
    
    try:
        curso.full_clean()
        curso.save()
        print("✅ ÉXITO: Curso válido guardado correctamente")
        curso.delete() # Limpieza
        return True
    except ValidationError as e:
        print(f"❌ FALLO: Error inesperado al guardar curso válido: {e}")
        return False

def test_duracion_maxima():
    perfil = get_perfil()
    if not perfil: return False
    
    hoy = timezone.now().date()
    hace_3_anos = hoy - timedelta(days=365*3)
    
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Muy Largo Test",
        fechainicio=hace_3_anos,
        fechafin=hoy
    )
    
    try:
        curso.full_clean()
        curso.save()
        print("❌ FALLO: Se guardó un curso de más de 2 años (DEBE FALLAR)")
        # Nota: Si esta prueba falla, es porque falta el validador de duración en models.py
        curso.delete()
        return False
    except ValidationError as e:
        print(f"✅ ÉXITO: ValidationError capturado")
        print(f"   Errores: {e.error_dict}")
        print(f"✅ ÉXITO: ValidationError capturado (Duración máxima)")
        return True

def main():
    """Ejecutar todas las pruebas"""
    
    print("\n\n")
    print("🧪"*30)
    print("SUITE DE PRUEBAS: VALIDACIÓN DE FECHAS")
    print("🧪"*30)
    
    resultados = {
        "Fechas futuras bloqueadas": test_fechas_futuras(),
        "fechainicio < fechafin": test_fecha_inicio_mayor_fin(),
        "Fechas válidas guardan": test_fechas_validas(),
        "Duración máxima": test_duracion_maxima(),
    }

    print("\nRESULTADOS:")
    for prueba, paso in resultados.items():
        print(f"{prueba}: {'✅ PASÓ' if paso else '❌ FALLÓ'}")


if __name__ == "__main__":
    main()