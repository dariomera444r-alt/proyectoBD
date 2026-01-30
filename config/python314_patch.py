"""
Parche de compatibilidad para Python 3.14 con Django 4.2.27
Este módulo debe importarse ANTES de cualquier importación de Django
Soluciona: AttributeError: 'super' object has no attribute 'dicts'
"""
import sys
import copy

_PATCH_APPLIED = False

def apply_patch():
    """Aplica el parche de compatibilidad para Python 3.14"""
    global _PATCH_APPLIED
    
    if _PATCH_APPLIED:
        return
    
    if sys.version_info >= (3, 14):
        # Intentar aplicar el parche inmediatamente si Django ya está cargado
        try:
            from django.template.context import BaseContext
            patch_basecontext(BaseContext)
        except (ImportError, AttributeError):
            # Si Django no está cargado aún, usar un import hook más seguro
            setup_import_hook()

def patch_basecontext(BaseContext):
    """Parchea BaseContext.__copy__ para Python 3.14"""
    global _PATCH_APPLIED
    
    if _PATCH_APPLIED:
        return
    
    # Verificar si ya está parcheado
    if hasattr(BaseContext.__copy__, '_python314_patched'):
        _PATCH_APPLIED = True
        return
    
    # Guardar el método original
    original_copy = BaseContext.__copy__
    
    def _patched_copy(self):
        """Parche para __copy__ compatible con Python 3.14"""
        # Crear una nueva instancia directamente sin usar copy(super())
        duplicate = self.__class__.__new__(self.__class__)
        # Copiar los dicts directamente
        if hasattr(self, 'dicts'):
            duplicate.dicts = self.dicts[:]
        # Copiar otros atributos si existen
        for key, value in self.__dict__.items():
            if key != 'dicts':
                try:
                    setattr(duplicate, key, copy.deepcopy(value))
                except (TypeError, ValueError, AttributeError):
                    try:
                        setattr(duplicate, key, value)
                    except (AttributeError, TypeError):
                        pass
        return duplicate
    
    # Marcar como parcheado
    _patched_copy._python314_patched = True
    
    # Aplicar el parche
    BaseContext.__copy__ = _patched_copy
    _PATCH_APPLIED = True

def setup_import_hook():
    """Configura un hook de importación para parchear cuando Django se carga"""
    import builtins
    original_import = builtins.__import__
    _hook_active = [True]  # Usar lista para evitar problemas de scope
    
    def patched_import(name, globals=None, locals=None, fromlist=(), level=0):
        """Hook de importación que parchea Django cuando se carga"""
        # Llamar al import original primero
        module = original_import(name, globals, locals, fromlist, level)
        
        # Solo parchear cuando se importa django.template.context y el hook está activo
        if _hook_active[0] and name == 'django.template.context':
            try:
                # Importar directamente sin usar el hook para evitar recursión
                import importlib
                context_module = importlib.import_module('django.template.context')
                BaseContext = getattr(context_module, 'BaseContext', None)
                if BaseContext:
                    patch_basecontext(BaseContext)
                    _hook_active[0] = False  # Desactivar el hook después de parchear
            except (ImportError, AttributeError):
                pass
        
        return module
    
    # Activar el hook y reemplazar __import__
    builtins.__import__ = patched_import

# Aplicar el parche inmediatamente al importar este módulo
apply_patch()
