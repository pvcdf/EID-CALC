"""
main.py - Módulo de inicialización y utilidades de la aplicación CónicasRUT.

Este módulo centraliza funciones de inicialización y configuración global
que son requeridas por la aplicación, tales como:
- Configuración del DPI en Windows
- Inicialización de temas y colores
- Configuración del path del proyecto
- Preparación del entorno

Para iniciar la aplicación, ejecutar: python ui/app.py o python -m ui.app
"""
import sys
import os


# ── Configuración del DPI en Windows ───────────────────────────────────────────
def setup_dpi_awareness():
    """
    Configura la conciencia de DPI en Windows para evitar el efecto "zoom"
    en pantallas de alta resolución.
    """
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass


# ── Configuración del path del proyecto ────────────────────────────────────────
def setup_project_path():
    """
    Agrega la ruta del proyecto al sys.path para permitir imports correctos.
    Se ejecuta automáticamente al importar este módulo.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


# ── Inicialización automática ──────────────────────────────────────────────────
# Se ejecutan automáticamente al importar el módulo
setup_dpi_awareness()
setup_project_path()

