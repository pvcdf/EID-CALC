# conicas-rut/main.py

"""
Módulo de inicialización global de CónicasRUT.

Responsabilidades:
- Configurar DPI awareness en Windows.
- Asegurar que la raíz del proyecto esté en sys.path.
"""

import os
import sys


def setup_dpi_awareness():
    """
    Configura la conciencia de DPI en Windows.

    Esto ayuda a evitar que Tkinter se vea borroso o escalado incorrectamente
    en pantallas con alta resolución.
    """
    if sys.platform != "win32":
        return

    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)

    except Exception:
        pass


def setup_project_path():
    """
    Agrega la raíz del proyecto al sys.path para permitir imports absolutos.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))

    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def initialize_environment():
    """
    Ejecuta la configuración global necesaria para la aplicación.
    """
    setup_dpi_awareness()
    setup_project_path()


initialize_environment()