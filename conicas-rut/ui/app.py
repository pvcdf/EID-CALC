"""
CónicasRUT — MAT1186
app.py: Punto de entrada de la aplicación.

Responsabilidades:
  - Crear la ventana principal
  - Mostrar la pantalla de ingreso de RUT
  - Navegar entre módulos (Cónicas / Funciones por Tramos)
  - Controlar el tema claro / oscuro

NO contiene: lógica matemática, validaciones, gráficos ni cálculos.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
import tkinter.font as tkfont


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

# Colores activos (se actualizan al cambiar tema)
C = dict(DARK)


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


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.F = _make_fonts()
        self.theme = "dark"   # tema inicial

        self.title("CónicasRUT — MAT1186")
        self.configure(bg=C["BG"])
        self.resizable(False, False)
        self._center_window(1200, 750)

        self.validated_rut = None
        self.pages     = {}
        self.tab_btns  = {}

        self._show_input_screen()

    # ── Utilidades ────────────────────────────────────────────────────────────
    def _center_window(self, width, height):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - width)  // 2
        y  = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _toggle_theme(self):
        """Alterna entre oscuro y claro, y reconstruye la pantalla actual."""
        global C
        if self.theme == "dark":
            self.theme = "light"
            C.update(LIGHT)
        else:
            self.theme = "dark"
            C.update(DARK)

        self.configure(bg=C["BG"])

        # Reconstruir la pantalla que está visible
        if self.validated_rut is None:
            self._show_input_screen()
        else:
            self._launch_main()

    def _theme_icon(self):
        """Luna = modo oscuro activo  /  Sol = modo claro activo."""
        return "☾" if self.theme == "dark" else "☀"

    # ── Pantalla de ingreso de RUT ────────────────────────────────────────────
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

        # Card
        input_card = tk.Frame(
            center, bg=C["CARD"],
            highlightbackground=C["BORDER"], highlightthickness=1
        )
        input_card.pack(ipadx=20, ipady=16)

        tk.Label(input_card, text="Ingresa tu RUT para comenzar",
                 bg=C["CARD"], fg=C["WHITE"],
                 font=self.F["label"]).pack(pady=(14, 8))

        entry_row = tk.Frame(input_card, bg=C["CARD"])
        entry_row.pack(padx=20, pady=(0, 6))

        self._rut_entry = tk.Entry(
            entry_row, bg=C["PANEL"], fg=C["WHITE"],
            insertbackground=C["WHITE"], font=self.F["mono"],
            bd=0, relief="flat", width=18, justify="center",
            highlightbackground=C["BORDER"], highlightthickness=1
        )
        self._rut_entry.pack(side="left", ipady=8, padx=(0, 8))
        self._rut_entry.insert(0, "Ej: 12345678-9")
        self._rut_entry.bind("<FocusIn>", self._clear_placeholder)
        self._rut_entry.bind("<Return>",  lambda e: self._on_analizar())

        tk.Button(
            entry_row, text="Analizar",
            bg=C["ACCENT"], fg=C["WHITE"], font=self.F["label"],
            bd=0, cursor="hand2", padx=14, pady=8,
            activebackground=C["ACCENT2"], activeforeground=C["BG"],
            command=self._on_analizar
        ).pack(side="left")

        self._status_var = tk.StringVar()
        tk.Label(
            input_card, textvariable=self._status_var,
            bg=C["CARD"], fg=C["RED"], font=self.F["small"]
        ).pack(pady=(4, 12))

    def _clear_placeholder(self, _event):
        if self._rut_entry.get().startswith("Ej:"):
            self._rut_entry.delete(0, "end")

    def _on_analizar(self):
        rut = self._rut_entry.get().strip()

        if not rut or rut.startswith("Ej:"):
            self._status_var.set("Por favor ingresa tu RUT.")
            return

        # ── Conectar con Gustavo (core/rut_validator.py) cuando esté listo ──
        # from core.rut_validator import validate_rut
        # result = validate_rut(rut)
        # if not result["valid"]:
        #     self._status_var.set(result["error"])
        #     return
        # self.validated_rut = result["rut_formatted"]
        # ─────────────────────────────────────────────────────────────────────

        if "-" not in rut:
            self._status_var.set("Formato inválido. Ejemplo: 12345678-9")
            return

        self.validated_rut = rut.upper()
        self._status_var.set("")
        self.after(200, self._launch_main)

    # ── Interfaz principal ────────────────────────────────────────────────────
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

        self.pages["conica"] = ConicView(container, self.validated_rut, self.F)
        self.pages["tramos"] = TramoView(container, self.validated_rut, self.F)

        for page in self.pages.values():
            page.place(x=0, y=0, relwidth=1, relheight=1)

        self._show_tab("conica")

    def _build_topbar(self, parent):
        bar = tk.Frame(parent, bg=C["PANEL"], height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # Logo izquierda
        logo = tk.Frame(bar, bg=C["PANEL"])
        logo.pack(side="left", padx=20, pady=10)
        tk.Label(logo, text="◈",         bg=C["PANEL"], fg=C["ACCENT"],
                 font=self.F["label"]).pack(side="left", padx=(0, 6))
        tk.Label(logo, text="CónicasRUT", bg=C["PANEL"], fg=C["WHITE"],
                 font=self.F["label"]).pack(side="left")
        tk.Label(logo, text=f"  ·  {self.validated_rut}",
                 bg=C["PANEL"], fg=C["GRAY"],
                 font=self.F["small"]).pack(side="left")

        # Botón de tema (esquina derecha)
        tk.Button(
            bar, text=self._theme_icon(),
            bg=C["PANEL"], fg=C["WHITE"], font=self.F["head"],
            bd=0, cursor="hand2",
            activebackground=C["PANEL"], activeforeground=C["ACCENT"],
            command=self._toggle_theme
        ).pack(side="right", padx=16)

        # Tabs
        tabs = tk.Frame(bar, bg=C["PANEL"])
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