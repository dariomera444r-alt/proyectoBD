# GUÍA DE PRUEBAS Y VALIDACIÓN

## ¿Qué se ha cambiado?

Se ha implementado un sistema **BLOQUEANTE** de validación de fechas en 3 niveles:

1. **Modelos (models.py)** - Validación de negocio
2. **Formularios (forms.py)** - Validación de formularios
3. **Admin (admin.py)** - Validación en panel de administración

## Validaciones implementadas:

### ✅ Fechas futuras bloqueadas
- **NO se puede ingresar mañana ni cualquier fecha futura**
- Se valida en todas las tablas con campos de fecha

### ✅ fechainicio debe ser menor a fechafin
- Si ambas fechas existen, `fechainicio < fechafin`
- Si no se cumple, **NO SE GUARDA**

### ✅ Duración máxima por tabla
- **CursosRealizados**: Máximo 2 años (730 días)
- **ExperienciaLaboral**: Máximo 50 años
- Otros campos: Sin límite de duración (solo validar relación)

---

## Cómo probar en el panel Admin

### Opción 1: Probar manualmente

1. Ir a `http://localhost:8000/admin/`
2. Iniciar sesión
3. Hacer clic en **"Cursos realizados"**
4. Hacer clic en **"Agregar curso realizado"**
5. Llenar los campos:
   - **Nombre del curso**: "Test Course"
   - **Fecha de inicio**: Seleccionar **MAÑANA** (24/01/2026)
   - **Fecha de fin**: Seleccionar cualquier fecha
6. Hacer clic en **"Guardar"**

**Resultado esperado:**
```
ERROR: La fecha de inicio no puede ser futura
```

---

### Opción 2: Ejecutar script de pruebas

```bash
# Ir al directorio del proyecto
cd c:\Users\Alexon\Downloads\project-hv\project-hv

# Ejecutar pruebas
python manage.py shell < cv/test_validaciones.py
```

**Resultado esperado:**
```
✅ ÉXITO: Bloqueo de fechas futuras
✅ ÉXITO: Validación fechainicio < fechafin
✅ ÉXITO: Fechas válidas guardan
✅ ÉXITO: Duración máxima
```

---

## Casos de prueba

### ❌ Caso 1: Fecha futura (FALLA)
```python
fechainicio = 24/01/2026  # ← MAÑANA
fechafin = 25/01/2026

# Resultado: ERROR - No se guarda
```

### ❌ Caso 2: fechainicio > fechafin (FALLA)
```python
fechainicio = 01/01/2020
fechafin = 31/12/2019  # ← Anterior a inicio

# Resultado: ERROR - No se guarda
```

### ❌ Caso 3: Duración > 2 años en cursos (FALLA)
```python
fechainicio = 01/01/2020
fechafin = 01/01/2023  # ← 3 años después

# Resultado: ERROR - No se guarda (en CursosRealizados)
```

### ✅ Caso 4: Fechas válidas (PASA)
```python
fechainicio = 01/01/2025
fechafin = 01/12/2025  # ← 11 meses (válido)

# Resultado: ÉXITO - Se guarda
```

---

## Tablas y su validación

### 📅 **DatosPersonales**
- Campo: `fechanacimiento`
- Validaciones:
  - ❌ No puede ser futura
  - ❌ Edad mínima: 12 años
  - ❌ Año mínimo: 1900

### 📅 **ExperienciaLaboral**
- Campos: `fechainiciogestion`, `fechafingestion`
- Validaciones:
  - ❌ Ninguna puede ser futura
  - ❌ inicio < fin
  - ❌ Duración máxima: 50 años

### 📅 **Reconocimientos**
- Campo: `fechareconocimiento`
- Validaciones:
  - ❌ No puede ser futura
  - ❌ Año mínimo: 2000

### 📅 **CursosRealizados** (CRÍTICO)
- Campos: `fechainicio`, `fechafin`
- Validaciones:
  - ❌ Ninguna puede ser futura **← PUNTO CRÍTICO**
  - ❌ inicio < fin
  - ❌ Duración máxima: 2 años (730 días)
  - ❌ Año mínimo: 2000

### 📅 **ProductosLaborales**
- Campo: `fechaproducto`
- Validaciones:
  - ❌ No puede ser futura
  - ❌ Año mínimo: 2000

---

## Flujo de validación (3 niveles)

```
Usuario intenta guardar
         ↓
    [1] FORM (forms.py)
    Valida en el navegador
         ↓
    ❌ Si hay error → Muestra error
    ✅ Si es OK → Continúa
         ↓
    [2] MODEL (models.py)
    Ejecuta clean() automáticamente
         ↓
    ❌ Si hay error → Lanza ValidationError
    ✅ Si es OK → Continúa
         ↓
    [3] ADMIN (admin.py)
    Ejecuta full_clean() en save_model()
         ↓
    ❌ Si hay error → Muestra error en admin
    ✅ Si es OK → GUARDA ✅
```

---

## Mensajes de error

Todos los errores incluyen el emoji 🚫 para identificarlos rápidamente:

```
🚫 ERROR: La fecha de inicio no puede ser futura.
🚫 ERROR: La fecha de inicio debe ser anterior a la fecha de fin.
🚫 ERROR: Duración máxima para un curso: 2 años.
🚫 ERROR: Año mínimo permitido: 2000.
```

---

## Archivos modificados

- ✅ `cv/models.py` - Modelos con validaciones
- ✅ `cv/forms.py` - Formularios con validaciones
- ✅ `cv/admin.py` - Admin con bloqueo en save_model()
- 📄 `cv/VALIDACIONES_FECHAS_RESUMEN.md` - Documentación completa
- 🧪 `cv/test_validaciones.py` - Script de pruebas

---

## FAQ

**P: ¿Se puede by-pass la validación?**
R: No. Se valida en 3 niveles (form → model → admin), es imposible evitar.

**P: ¿Qué sucede si intento guardar una fecha futura?**
R: Recibe error 🚫 y NO se guarda.

**P: ¿Funciona en formularios también?**
R: Sí. La validación funciona en:
   - Formularios webs (forms.py)
   - Panel admin (admin.py)
   - API (si las usas)

**P: ¿Qué significa "fecha futura"?**
R: Cualquier fecha igual o posterior a la de mañana (> hoy).

---

## Resumen

✅ **Bloqueante**: Imposible guardar fechas futuras
✅ **Completo**: Validado en 3 niveles
✅ **Claro**: Mensajes de error con 🚫
✅ **Probado**: Script de pruebas incluido

Ahora **NO se puede ingresar fechas como la de mañana** en ninguna tabla.
