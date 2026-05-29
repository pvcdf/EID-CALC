<<<<<<< HEAD
﻿# conicas-rut/ui/app.py
=======
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main  # noqa: F401

import tkinter as tk

from ui.components.input_panel import InputPanel
from core.rut_validator import validate_rut
from ui.theme import COLORS, ThemeState, get_fonts


# ── Aplicación principal ─────────────────────────────────────────────────────
class App(tk.Tk):
    """
    Ventana principal y controlador de navegación.
    """
    def __init__(self):
        super().__init__()
        # Tema visual
        self.theme = ThemeState(COLORS, get_fonts())
        self.F = self.theme.fonts
        # Configuración ventana
        self.title("CónicasRUT — MAT1186")
<<<<<<< HEAD
        self.configure(bg=self.theme.bg)
        self.resizable(True, True)
        self._maximize_window()
        # Estado
=======
        self.configure(bg=C["BG"])
        self.resizable(False, False)
        self._center_window(1800, 850)

>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))
        self.validated_rut = None
        self.pages = {}
        self.tab_btns = {}
        self._topbar = None
        self._is_maximized = True
        # Inicio
        self._show_input_screen()
        self._monitor_window_state()

<<<<<<< HEAD
    # ── Utilidades ──────────────────────────────────────────────────────────
    def _maximize_window(self):
        """
        Maximiza la ventana conservando la barra del sistema.
        """
        if sys.platform == "win32":
            self.state("zoomed")
        else:
            self.attributes("-zoomed", True)
=======
    # ── Utilidades ────────────────────────────────────────────────────────────
    # Centra la ventana principal en la pantalla.
    def _center_window(self, width, height):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - width)  // 2
        y  = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))

    def _monitor_window_state(self):
        """
        Detecta restauración/minimización de la ventana.
        """
        try:
            current_state = self.state()
            if self._is_maximized and current_state != "zoomed":
                self._is_maximized = False
                self._set_normal_size()
            elif not self._is_maximized and current_state == "zoomed":
                self._is_maximized = True
        except Exception:
            pass
        self.after(500, self._monitor_window_state)

    def _set_normal_size(self):
        """
        Aplica tamaño visible al restaurar ventana.
        """
        if sys.platform == "win32":
            self.state("normal")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        new_width = int(screen_width * 0.6)
        new_height = int(screen_height * 0.6)
        x_pos = (screen_width - new_width) // 2
        y_pos = (screen_height - new_height) // 2
        self.geometry(
            f"{new_width}x{new_height}+{x_pos}+{y_pos}"
        )

    # ── Pantalla inicial ────────────────────────────────────────────────────
    def _show_input_screen(self):
        if hasattr(self, "_root_frame"):
            self._root_frame.destroy()
        self._root_frame = tk.Frame(
            self,
            bg=self.theme.bg
        )
        self._root_frame.pack(fill="both", expand=True)
<<<<<<< HEAD
        # Contenedor centrado
        center = tk.Frame(
            self._root_frame,
            bg=self.theme.bg
        )
        center.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        tk.Label(
            center,
            text="◈",
            bg=self.theme.bg,
            fg=self.theme.accent,
            font=self.F["title"]
        ).pack(anchor="center")
        tk.Label(
            center,
            text="CónicasRUT",
            bg=self.theme.bg,
            fg=self.theme.fg,
            font=self.F["title"]
        ).pack(anchor="center")
        tk.Label(
            center,
            text="MAT1186 — Ingeniería Civil en Informática",
            bg=self.theme.bg,
            fg=self.theme.gray,
            font=self.F["small"]
        ).pack(anchor="center", pady=(2, 30))
=======

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

>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))
        input_card = InputPanel(
            center,
            self.theme,
            title="Ingresa tu RUT para comenzar",
            button_text="Analizar",
            command=self._on_analizar,
            padx=0,
            pady=0,
        )
<<<<<<< HEAD
        input_card.pack(
            anchor="center",
            ipadx=0,
            ipady=0
        )
=======
        input_card.pack(ipadx=20, ipady=16)
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))

        self._rut_entry = input_card.entry
        self._input_card = input_card
        self._rut_entry.insert(0, "Ej: 12345678-9")
<<<<<<< HEAD
        self._rut_entry.bind(
            "<FocusIn>",
            self._clear_placeholder
        )
        self._rut_entry.bind(
            "<Return>",
            lambda e: self._on_analizar()
        )
=======
        self._rut_entry.bind("<FocusIn>", self._clear_placeholder)
        self._rut_entry.bind("<KeyRelease>", self._on_rut_keyrelease)
        self._rut_entry.bind("<Return>", lambda e: self._on_analizar())

>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))
        self._status_var = tk.StringVar()
        self._input_card.status_label.configure(
            textvariable=self._status_var
        )

<<<<<<< HEAD
=======
        vcmd = self.register(self._validate_rut_entry)
        self._rut_entry.configure(validate="key", validatecommand=(vcmd, "%P"))

    # Limpia el texto de ayuda cuando el campo RUT recibe foco.
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))
    def _clear_placeholder(self, _event):

        if self._rut_entry.get().startswith("Ej:"):
            self._rut_entry.delete(0, "end")

<<<<<<< HEAD
    def _on_analizar(self):
=======
    def _on_rut_keyrelease(self, _event):
        value = self._rut_entry.get()
        if value.isdigit() and len(value) == 8:
            self._rut_entry.insert("end", "-")

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
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))

        rut = self._rut_entry.get().strip()
        if not rut or rut.startswith("Ej:"):
            self._status_var.set(
                "Ingrese un RUT válido."
            )
            return

        result = validate_rut(rut)
        if not result["valid"]:
            self._status_var.set(
                result["error"]
            )
            return

        self.validated_rut = result
        self._status_var.set("RUT válido.")
        self.after(200, self._show_validation_steps)

    def _show_validation_steps(self):
        from ui.views.validation_view import ValidationView

        if hasattr(self, "_root_frame"):
            self._root_frame.destroy()

        self._root_frame = ValidationView(
            self,
            theme=self.theme,
            rut_result=self.validated_rut,
            on_continue=self._launch_main,
        )
        self._root_frame.pack(fill="both", expand=True)
        
    # ── Interfaz principal ──────────────────────────────────────────────────
    def _launch_main(self):

        from ui.views.conic_view import ConicView
        from ui.views.tramo_view import TramoView

        if hasattr(self, "_root_frame"):
            self._root_frame.destroy()
        self._root_frame = tk.Frame(
            self,
            bg=self.theme.bg
        )
        self._root_frame.pack(
            fill="both",
            expand=True
        )
        self._build_topbar(self._root_frame)
        container = tk.Frame(
            self._root_frame,
            bg=self.theme.bg
        )
        container.pack(
            fill="both",
            expand=True
        )
        self.pages["conica"] = ConicView(
            container,
            self.theme
        )
        self.pages["tramos"] = TramoView(
            container,
            self.theme
        )
        for page in self.pages.values():
            page.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )
        self._show_tab("conica")

    # ── Barra superior ──────────────────────────────────────────────────────
    def _build_topbar(self, parent):

        self._topbar = tk.Frame(parent, bg=self.theme.panel, height=56)
        self._topbar.pack(fill="x")
        self._topbar.pack_propagate(False)

        # Logo
        logo = tk.Frame( self._topbar, bg=self.theme.panel)
        logo.pack( side="left", padx=20, pady=10)
        tk.Label( logo, text="◈", bg=self.theme.panel, fg=self.theme.accent, font=self.F["label"] 
        ).pack(side="left", padx=(0, 6))

        tk.Label( logo, text="CónicasRUT", bg=self.theme.panel, fg=self.theme.fg, font=self.F["label"]
        ).pack(side="left")

        tk.Label( logo, text=f"  ·  {self.validated_rut['data']['clean_rut']}", bg=self.theme.panel, fg=self.theme.gray, font=self.F["small"]
        ).pack(side="left")

        # Tabs
        tabs = tk.Frame(self._topbar, bg=self.theme.panel)
        tabs.pack(side="right", padx=(0, 4))
        self.tab_btns = {}

        for key, label in [
            ("conica", "⬡  Secciones Cónicas"),
            ("tramos", "∿  Funciones por Tramos"),
        ]:

            btn = tk.Button(tabs, text=label, bg=self.theme.panel, fg=self.theme.gray,
                font=self.F["small"], bd=0, cursor="hand2", padx=14, pady=14,
                activebackground=self.theme.accent,
                activeforeground=self.theme.fg,
                command=lambda k=key: self._show_tab(k))
            btn.pack(side="left")
            self.tab_btns[key] = btn

    # ── Navegación ──────────────────────────────────────────────────────────
    def _show_tab(self, name: str):

        for key, btn in self.tab_btns.items():
            if key == name:
                btn.config(bg=self.theme.accent, fg=self.theme.fg)

            else:
                btn.config(bg=self.theme.panel, fg=self.theme.gray)
        self.pages[name].lift()

# ── Entrada ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()

