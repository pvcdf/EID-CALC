import sys
import os

# Importar funciones de inicialización desde main.py
# Esto configura DPI awareness y el path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main  # noqa: F401

import tkinter as tk
import tkinter.font as tkfont
from ui.components.input_panel import InputPanel


# ── Temas ─────────────────────────────────────────────────────────────────────
DARK = {
    "BG":      "#0F0E17",
    "PANEL":   "#1A1928",
    "CARD":    "#222136",
    "ACCENT":  "#7B6FF0",
    "ACCENT2": "#A78BFA",
    "GREEN":   "#34D399",
    "RED":     "#F87171",
    "YELLOW":  "#FBBF24",
    "WHITE":   "#F4F3FF",
    "GRAY":    "#6B6A85",
    "BORDER":  "#2E2D47",
    "PLOT_BG": "#13121F",
}

# Colores activos
C = dict(DARK)


# Crea las fuentes utilizadas por la interfaz.
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


# Estado de colores y fuentes que define el tema actual de la aplicación.
class ThemeState:
    def __init__(self, colors, fonts, name="dark"):
        self.name = "dark"  # Siempre modo oscuro
        self.fonts = fonts
        self.update(colors)

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


# Ventana principal de la aplicación y control de la navegación entre pantallas.
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.F = _make_fonts()
        self.theme = ThemeState(C, self.F, name="dark")

        self.title("CónicasRUT — MAT1186")
        self.configure(bg=C["BG"])
        self.resizable(True, True)
        self._maximize_window()

        self.validated_rut = None
        self.pages = {}
        self.tab_btns = {}
        self._topbar = None
        self._is_maximized = True

        self._show_input_screen()
        self._monitor_window_state()

    # ── Utilidades ────────────────────────────────────────────────────────────
    # Maximiza la ventana conservando la barra de título del SO.
    def _maximize_window(self):
        if sys.platform == "win32":
            self.state("zoomed")
        else:
            self.attributes("-zoomed", True)

    # Monitorea cambios en el estado de la ventana (maximizado → restaurado).
    def _monitor_window_state(self):
        """Verifica si la ventana salió del estado maximizado y aplica tamaño normal."""
        try:
            current_state = self.state()
            if self._is_maximized and current_state != "zoomed":
                # La ventana fue restaurada/minimizada
                self._is_maximized = False
                self._set_normal_size()
            elif not self._is_maximized and current_state == "zoomed":
                # La ventana fue maximizada nuevamente
                self._is_maximized = True
        except Exception:
            pass
        
        # Continuar monitoreando cada 500ms
        self.after(500, self._monitor_window_state)

    # Establece un tamaño normal para la ventana (después de minimizar/restaurar).
    def _set_normal_size(self):
        """Aplica un tamaño visible cuando la ventana sale de maximizado."""
        if sys.platform == "win32":
            self.state("normal")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Tamaño: 60% del ancho y alto de la pantalla, centrado
        new_width = int(screen_width * 0.6)
        new_height = int(screen_height * 0.6)
        x_pos = (screen_width - new_width) // 2
        y_pos = (screen_height - new_height) // 2
        
        self.geometry(f"{new_width}x{new_height}+{x_pos}+{y_pos}")

    # Cambia el tema oscuro/claro sin reiniciar la navegación principal.
    def _toggle_theme(self):
        """Método removido - solo modo oscuro disponible."""
        pass

    # Devuelve el icono del botón de modo según el tema activo.
    def _theme_icon(self):
        """Método removido - solo modo oscuro disponible."""
        return ""

    # ── Pantalla de ingreso de RUT ────────────────────────────────────────────
    # Construye la vista inicial donde el usuario ingresa su RUT.
    def _show_input_screen(self):
        if hasattr(self, "_root_frame"):
            self._root_frame.destroy()

        self._root_frame = tk.Frame(self, bg=C["BG"])
        self._root_frame.pack(fill="both", expand=True)

        # Contenedor centrado horizontalmente en la pantalla
        center = tk.Frame(self._root_frame, bg=C["BG"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="◈", bg=C["BG"], fg=C["ACCENT"],
                 font=self.F["title"]).pack(anchor="center")
        tk.Label(center, text="CónicasRUT", bg=C["BG"], fg=C["WHITE"],
                 font=self.F["title"]).pack(anchor="center")
        tk.Label(center, text="MAT1186 — Ingeniería Civil en Informática",
                 bg=C["BG"], fg=C["GRAY"],
                 font=self.F["small"]).pack(anchor="center", pady=(2, 30))

        input_card = InputPanel(
            center,
            self.theme,
            title="Ingresa tu RUT para comenzar",
            button_text="Analizar",
            command=self._on_analizar,
            padx=0,
            pady=0,
        )
        input_card.pack(anchor="center", ipadx=0, ipady=0)

        self._rut_entry = input_card.entry
        self._input_card = input_card
        self._rut_entry.insert(0, "Ej: 12345678-9")
        self._rut_entry.bind("<FocusIn>", self._clear_placeholder)
        self._rut_entry.bind("<Return>", lambda e: self._on_analizar())

        self._status_var = tk.StringVar()
        self._input_card.status_label.configure(textvariable=self._status_var)

    # Limpia el texto de ayuda cuando el campo RUT recibe foco.
    def _clear_placeholder(self, _event):
        if self._rut_entry.get().startswith("Ej:"):
            self._rut_entry.delete(0, "end")

    # Obtiene el RUT del campo de entrada y avanza hacia la interfaz principal.
    def _on_analizar(self):
        rut = self._rut_entry.get().strip().upper()
        self.validated_rut = rut
        self._status_var.set("")
        self.after(200, self._launch_main)

    # ── Interfaz principal ────────────────────────────────────────────────────
    # Crea la interfaz principal con pestañas y vistas secundarias.
    def _launch_main(self):
        from ui.views.conic_view import ConicView
        from ui.views.tramo_view import TramoView

        if hasattr(self, "_root_frame"):
            self._root_frame.destroy()

        self._root_frame = tk.Frame(self, bg=C["BG"])
        self._root_frame.pack(fill="both", expand=True)

        self._build_topbar(self._root_frame)

        container = tk.Frame(self._root_frame, bg=C["BG"])
        container.pack(fill="both", expand=True)

        self.pages["conica"] = ConicView(container, self.theme)
        self.pages["tramos"] = TramoView(container, self.theme)

        for page in self.pages.values():
            page.place(x=0, y=0, relwidth=1, relheight=1)

        self._show_tab("conica")

    # Construye la barra superior con logo, RUT y navegación entre secciones.
    def _build_topbar(self, parent):
        self._topbar = tk.Frame(parent, bg=C["PANEL"], height=56)
        self._topbar.pack(fill="x")
        self._topbar.pack_propagate(False)

        # Logo izquierda
        logo = tk.Frame(self._topbar, bg=C["PANEL"])
        logo.pack(side="left", padx=20, pady=10)
        tk.Label(logo, text="◈", bg=C["PANEL"], fg=C["ACCENT"],
                 font=self.F["label"]).pack(side="left", padx=(0, 6))
        tk.Label(logo, text="CónicasRUT", bg=C["PANEL"], fg=C["WHITE"],
                 font=self.F["label"]).pack(side="left")
        tk.Label(logo, text=f"  ·  {self.validated_rut}",
                 bg=C["PANEL"], fg=C["GRAY"],
                 font=self.F["small"]).pack(side="left")

        # Tabs
        tabs = tk.Frame(self._topbar, bg=C["PANEL"])
        tabs.pack(side="right", padx=(0, 4))

        self.tab_btns = {}
        for key, label in [
            ("conica", "⬡  Secciones Cónicas"),
            ("tramos", "∿  Funciones por Tramos"),
        ]:
            btn = tk.Button(
                tabs, text=label,
                bg=C["PANEL"], fg=C["GRAY"],
                font=self.F["small"], bd=0, cursor="hand2",
                padx=14, pady=14,
                activebackground=C["ACCENT"], activeforeground=C["WHITE"],
                command=lambda k=key: self._show_tab(k)
            )
            btn.pack(side="left")
            self.tab_btns[key] = btn

    # Cambia la vista activa entre pestañas y actualiza el estilo del tab seleccionado.
    def _show_tab(self, name: str):
        for key, btn in self.tab_btns.items():
            if key == name:
                btn.config(bg=C["ACCENT"], fg=C["WHITE"])
            else:
                btn.config(bg=C["PANEL"],  fg=C["GRAY"])
        self.pages[name].lift()


# ── Punto de entrada ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()