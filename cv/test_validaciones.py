# cv/test_validaciones.py - Script para probar las validaciones

"""
Este script prueba que las validaciones de fecha funcionan correctamente.
Úsalo con: python manage.py shell < cv/test_validaciones.py
"""

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import (
    DatosPersonales, CursosRealizados, ExperienciaLaboral, 
    Reconocimientos, ProductosLaborales
)

def test_fechas_futuras():
    """Prueba que NO se pueden guardar fechas futuras"""
    
    print("\n" + "="*60)
    print("🧪 PRUEBA 1: Bloqueo de fechas futuras")
    print("="*60)
    
    # Crear perfil de prueba
    perfil = DatosPersonales(
        nombres="Test",
        apellidos="Usuario",
        numerocedula="1234567890",
    )
    perfil.save()
    print("✅ Perfil creado")
    
    # Intentar guardar curso con fecha futura
    mañana = timezone.now().date() + timedelta(days=1)
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Futuro",
        fechainicio=mañana,
        fechafin=mañana + timedelta(days=1)
    )
    
    try:
        curso.save()
        print("❌ FALLO: Se guardó un curso con fecha futura (DEBE FALLAR)")
        return False
    except ValidationError as e:
        print(f"✅ ÉXITO: ValidationError capturado")
        print(f"   Errores: {e.error_dict}")
        return True

def test_fecha_inicio_mayor_fin():
    """Prueba que fechainicio NO puede ser mayor a fechafin"""
    
    print("\n" + "="*60)
    print("🧪 PRUEBA 2: Validación fechainicio < fechafin")
    print("="*60)
    
    perfil = DatosPersonales.objects.first()
    
    # Fechas válidas pero en orden incorrecto
    fecha1 = timezone.now().date() - timedelta(days=100)
    fecha2 = timezone.now().date() - timedelta(days=200)  # fecha2 < fecha1
    
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Invertido",
        fechainicio=fecha1,
        fechafin=fecha2
    )
    
    try:
        curso.save()
        print("❌ FALLO: Se guardó con fechainicio > fechafin (DEBE FALLAR)")
        return False
    except ValidationError as e:
        print(f"✅ ÉXITO: ValidationError capturado")
        print(f"   Errores: {e.error_dict}")
        return True

def test_fechas_validas():
    """Prueba que SÍ se guarden fechas válidas"""
    
    print("\n" + "="*60)
    print("🧪 PRUEBA 3: Fechas válidas DEBEN guardarse")
    print("="*60)
    
    perfil = DatosPersonales.objects.first()
    
    fecha1 = timezone.now().date() - timedelta(days=100)
    fecha2 = timezone.now().date() - timedelta(days=10)
    
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Válido",
        fechainicio=fecha1,
        fechafin=fecha2
    )
    
    try:
        curso.save()
        print("✅ ÉXITO: Curso guardado correctamente")
        print(f"   ID: {curso.idcursorealizado}")
        print(f"   Inicio: {curso.fechainicio}")
        print(f"   Fin: {curso.fechafin}")
        return True
    except ValidationError as e:
        print(f"❌ FALLO: No se guardó un curso válido")
        print(f"   Errores: {e.error_dict}")
        return False

def test_duracion_maxima():
    """Prueba que la duración máxima es de 2 años"""
    
    print("\n" + "="*60)
    print("🧪 PRUEBA 4: Duración máxima para cursos (2 años)")
    print("="*60)
    
    perfil = DatosPersonales.objects.first()
    
    fecha1 = timezone.now().date() - timedelta(days=365*3)  # 3 años atrás
    fecha2 = timezone.now().date() - timedelta(days=365)  # 1 año atrás
    
    curso = CursosRealizados(
        idperfilconqueestaactivo=perfil,
        nombrecurso="Curso Muy Largo",
        fechainicio=fecha1,
        fechafin=fecha2
    )
    
    try:
        curso.save()
        print("❌ FALLO: Se guardó un curso de más de 2 años (DEBE FALLAR)")
        return False
    except ValidationError as e:
        print(f"✅ ÉXITO: ValidationError capturado")
        print(f"   Errores: {e.error_dict}")
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
    
    print("\n" + "="*60)
    print("📊 RESULTADOS FINALES")
    print("="*60)
    
    for prueba, resultado in resultados.items():
        estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
        print(f"{estado}: {prueba}")
    
    total = len(resultados)
    exitosas = sum(resultados.values())
    
    print(f"\nTotal: {exitosas}/{total} pruebas pasadas")
    
    if exitosas == total:
        print("\n🎉 TODAS LAS VALIDACIONES FUNCIONAN CORRECTAMENTE 🎉")
    else:
        print(f"\n⚠️  {total - exitosas} pruebas fallaron")

if __name__ == "__main__":
    main()
