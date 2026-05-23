
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

LIGHT = {
    "BG":      "#F7F7F8",
    "PANEL":   "#EFEFF2",
    "CARD":    "#E6E6EA",
    "ACCENT":  "#7B6FF0",
    "ACCENT2": "#534AB7",
    "GREEN":   "#059669",
    "RED":     "#DC2626",
    "YELLOW":  "#B45309",
    "WHITE":   "#0B0B0B",
    "GRAY":    "#6B6A85",
    "BORDER":  "#D1D1DB",
    "PLOT_BG": "#FFFFFF",
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
        self.name = name
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
        self.resizable(False, False)
        self._center_window(1600, 850)

        self.validated_rut = None
        self.pages = {}
        self.tab_btns = {}
        self._topbar = None
        self._mode_btn = None

        self._show_input_screen()

    # ── Utilidades ────────────────────────────────────────────────────────────
    # Centra la ventana principal en la pantalla.
    def _center_window(self, width, height):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - width)  // 2
        y  = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    # Cambia el tema oscuro/claro sin reiniciar la navegación principal.
    def _toggle_theme(self):
        """Alterna entre oscuro y claro, y actualiza solo el estilo visible."""
        global C
        if self.theme.name == "dark":
            self.theme.name = "light"
            C.update(LIGHT)
        else:
            self.theme.name = "dark"
            C.update(DARK)

        self.theme.update(C)
        self.configure(bg=C["BG"])

        if self.validated_rut is None:
            self._show_input_screen()
        else:
            self._refresh_main_theme()

    # Devuelve el icono del botón de modo según el tema activo.
    def _theme_icon(self):
        """Luna = modo oscuro activo  /  Sol = modo claro activo."""
        return "☾" if self.theme.name == "dark" else "☀"

    # ── Pantalla de ingreso de RUT ────────────────────────────────────────────
    # Construye la vista inicial donde el usuario ingresa su RUT.
    def _show_input_screen(self):
        if hasattr(self, "_root_frame"):
            self._root_frame.destroy()

        self._root_frame = tk.Frame(self, bg=C["BG"])
        self._root_frame.pack(fill="both", expand=True)

        # Botón de tema (esquina superior derecha)
        tk.Button(
            self._root_frame, text=self._theme_icon(),
            bg=C["BG"], fg=C["WHITE"], font=self.F["head"],
            bd=0, cursor="hand2", activebackground=C["BG"],
            activeforeground=C["ACCENT"], command=self._toggle_theme
        ).place(relx=1.0, x=-16, y=12, anchor="ne")

        # Contenido centrado
        center = tk.Frame(self._root_frame, bg=C["BG"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="◈", bg=C["BG"], fg=C["ACCENT"],
                 font=self.F["title"]).pack()
        tk.Label(center, text="CónicasRUT", bg=C["BG"], fg=C["WHITE"],
                 font=self.F["title"]).pack()
        tk.Label(center, text="MAT1186 — Ingeniería Civil en Informática",
                 bg=C["BG"], fg=C["GRAY"],
                 font=self.F["small"]).pack(pady=(2, 30))

        input_card = InputPanel(
            center,
            self.theme,
            title="Ingresa tu RUT para comenzar",
            button_text="Analizar",
            command=self._on_analizar,
            padx=0,
            pady=0,
        )
        input_card.pack(ipadx=20, ipady=16)

        self._rut_entry = input_card.entry
        self._input_card = input_card
        self._rut_entry.insert(0, "Ej: 12345678-9")
        self._rut_entry.bind("<FocusIn>", self._clear_placeholder)
        self._rut_entry.bind("<Return>", lambda e: self._on_analizar())

        self._status_var = tk.StringVar()
        self._input_card.status_label.configure(textvariable=self._status_var)

        vcmd = self.register(self._validate_rut_entry)
        self._rut_entry.configure(validate="key", validatecommand=(vcmd, "%P"))

    # Limpia el texto de ayuda cuando el campo RUT recibe foco.
    def _clear_placeholder(self, _event):
        if self._rut_entry.get().startswith("Ej:"):
            self._rut_entry.delete(0, "end")

    # Valida el ingreso del RUT en tiempo real para limitar el formato.
    def _validate_rut_entry(self, proposed):
        if proposed == "" or proposed.startswith("Ej:"):
            return True
        allowed = set("0123456789Kk-")
        if any(ch not in allowed for ch in proposed):
            return False
        if proposed.count("-") > 1:
            return False
        if "-" in proposed:
            tail = proposed.split("-", 1)[1]
            if len(tail) > 1:
                return False
        return True

    # Valida el RUT y avanza hacia la interfaz principal de resultados.
    def _on_analizar(self):
        rut = self._rut_entry.get().strip().upper()

        if not rut or rut.startswith("Ej:"):
            self._status_var.set("Por favor ingresa tu RUT.")
            return

        if rut.count("-") != 1:
            self._status_var.set("Formato inválido. Ejemplo: 12345678-9")
            return

        body, dv = rut.split("-", 1)
        if not body.isdigit() or len(dv) != 1 or not (dv.isdigit() or dv == "K"):
            self._status_var.set("Formato inválido. Debe tener un dígito verificador.")
            return

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

        # Botón de tema (esquina derecha)
        self._mode_btn = tk.Button(
            self._topbar, text=self._theme_icon(),
            bg=C["PANEL"], fg=C["WHITE"], font=self.F["head"],
            bd=0, cursor="hand2",
            activebackground=C["PANEL"], activeforeground=C["ACCENT"],
            command=self._toggle_theme
        )
        self._mode_btn.pack(side="right", padx=16)

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

    # Actualiza colores del tema en la pantalla principal sin reconstruir la ventana.
    def _refresh_main_theme(self):
        if hasattr(self, "_root_frame"):
            self._root_frame.configure(bg=C["BG"])
        if self._topbar is not None:
            self._topbar.configure(bg=C["PANEL"])
            self._apply_theme_to_frame(self._topbar, bg_color=C["PANEL"], fg_color=C["WHITE"])
        if self._mode_btn is not None:
            self._mode_btn.configure(
                text=self._theme_icon(),
                bg=C["PANEL"],
                fg=C["WHITE"],
                activebackground=C["PANEL"],
                activeforeground=C["ACCENT"],
            )
        for btn in self.tab_btns.values():
            btn.configure(bg=C["PANEL"], fg=C["GRAY"], activebackground=C["ACCENT"], activeforeground=C["WHITE"])
        for page in self.pages.values():
            try:
                page.update_theme(self.theme)
            except AttributeError:
                pass

    # Aplica los colores del tema a los widgets anidados de un frame.
    def _apply_theme_to_frame(self, frame, bg_color=None, fg_color=None):
        for widget in frame.winfo_children():
            try:
                widget.configure(bg=bg_color or widget.cget("bg"), fg=fg_color or widget.cget("fg"))
            except tk.TclError:
                pass
            if isinstance(widget, tk.Frame):
                self._apply_theme_to_frame(widget, bg_color, fg_color)

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