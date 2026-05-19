import tkinter.font as tkfont


# ── Colores ───────────────────────────────────────────────────────────────────
COLORS = {
    "BG":       "#0F0E17",   # fondo principal
    "PANEL":    "#1A1928",   # topbar y paneles laterales
    "CARD":     "#222136",   # cards internas
    "ACCENT":   "#7B6FF0",   # morado principal (botones activos, tabs)
    "ACCENT2":  "#A78BFA",   # morado claro (valores, highlights)
    "GREEN":    "#34D399",   # válido, tramo izquierdo
    "RED":      "#F87171",   # error, discontinuidad
    "YELLOW":   "#FBBF24",   # focos, tramo derecho
    "WHITE":    "#F4F3FF",   # texto principal
    "GRAY":     "#6B6A85",   # texto secundario
    "BORDER":   "#2E2D47",   # bordes de cards
    "PLOT_BG":  "#13121F",   # fondo del canvas de gráficos
}


# ── Fuentes ───────────────────────────────────────────────────────────────────
# Se inicializan como funciones para evitar errores si tkinter no está listo
def _make_fonts():
    return {
        "title":   tkfont.Font(family="Courier New", size=18, weight="bold"),
        "head":    tkfont.Font(family="Courier New", size=13, weight="bold"),
        "label":   tkfont.Font(family="Courier New", size=10),
        "small":   tkfont.Font(family="Courier New", size=9),
        "mono":    tkfont.Font(family="Courier New", size=11),
        "mono_sm": tkfont.Font(family="Courier New", size=9),
        "big":     tkfont.Font(family="Courier New", size=22, weight="bold"),
    }


# FONTS se carga la primera vez que se importa (tkinter ya debe estar iniciado)
FONTS = None


def get_fonts():
    """Retorna el diccionario de fuentes. Llama esto después de crear tk.Tk()."""
    global FONTS
    if FONTS is None:
        FONTS = _make_fonts()
    return FONTS