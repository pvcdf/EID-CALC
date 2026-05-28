# conicas-rut/ui/theme.py

import tkinter.font as tkfont


# ── Paleta de colores ─────────────────────────────────────────────────────────
COLORS = {
    "BG": "#0F0E17",
    "PANEL": "#1A1928",
    "CARD": "#222136",
    "ACCENT": "#7B6FF0",
    "ACCENT2": "#A78BFA",
    "GREEN": "#34D399",
    "RED": "#F87171",
    "YELLOW": "#FBBF24",
    "WHITE": "#F4F3FF",
    "GRAY": "#6B6A85",
    "BORDER": "#2E2D47",
    "PLOT_BG": "#13121F",
}


# ── Fuentes ──────────────────────────────────────────────────────────────────
# Se crean después de iniciar tkinter para evitar errores.
def _make_fonts():
    return {
        "title": tkfont.Font(
            family="Courier New",
            size=18,
            weight="bold"
        ),

        "head": tkfont.Font(
            family="Courier New",
            size=13,
            weight="bold"
        ),

        "label": tkfont.Font(
            family="Courier New",
            size=10
        ),

        "small": tkfont.Font(
            family="Courier New",
            size=9
        ),

        "mono": tkfont.Font(
            family="Courier New",
            size=11
        ),

        "mono_sm": tkfont.Font(
            family="Courier New",
            size=9
        ),

        "big": tkfont.Font(
            family="Courier New",
            size=22,
            weight="bold"
        ),
    }


# Cache global de fuentes
FONTS = None


def get_fonts():
    """
    Retorna el diccionario de fuentes.
    Debe llamarse después de crear tk.Tk().
    """
    global FONTS

    if FONTS is None:
        FONTS = _make_fonts()

    return FONTS


# ── Estado del tema ──────────────────────────────────────────────────────────
class ThemeState:
    """
    Contenedor del estado visual actual de la aplicación.
    """

    def __init__(self, colors=None, fonts=None, name="dark"):
        self.name = name
        self.fonts = fonts or get_fonts()

        self.update(colors or COLORS)

    def update(self, colors):
        self.bg = colors["BG"]
        self.panel = colors["PANEL"]
        self.card = colors["CARD"]

        self.accent = colors["ACCENT"]
        self.accent2 = colors["ACCENT2"]

        self.green = colors["GREEN"]
        self.red = colors["RED"]
        self.yellow = colors["YELLOW"]

        self.fg = colors["WHITE"]
        self.gray = colors["GRAY"]

        self.border = colors["BORDER"]
        self.plot = colors["PLOT_BG"]
