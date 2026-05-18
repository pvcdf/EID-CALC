"""
MAT1186 — CónicasRUT
Interfaz visual principal - Replicación exacta de la maqueta
Flujo: Entrada RUT → Validación → Interfaz completa
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.rut_validator import validate_rut


# ─── PALETA DE COLORES ────────────────────────────────────────────────────────
DARK_THEME = {
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

LIGHT_THEME = {
    "BG": "#F7F7F8",
    "PANEL": "#EFEFF2",
    "CARD": "#E6E6EA",
    "ACCENT": "#7B6FF0",
    "ACCENT2": "#A78BFA",
    "GREEN": "#059669",
    "RED": "#DC2626",
    "YELLOW": "#B45309",
    # In light theme, main text should be dark for contrast
    "WHITE": "#0B0B0B",
    "GRAY": "#6B6A85",
    "BORDER": "#D1D1DB",
    "PLOT_BG": "#FFFFFF",
}

# Current active color names (module globals used by helpers)
BG = DARK_THEME["BG"]
PANEL = DARK_THEME["PANEL"]
CARD = DARK_THEME["CARD"]
ACCENT = DARK_THEME["ACCENT"]
ACCENT2 = DARK_THEME["ACCENT2"]
GREEN = DARK_THEME["GREEN"]
RED = DARK_THEME["RED"]
YELLOW = DARK_THEME["YELLOW"]
WHITE = DARK_THEME["WHITE"]
GRAY = DARK_THEME["GRAY"]
BORDER = DARK_THEME["BORDER"]
PLOT_BG = DARK_THEME["PLOT_BG"]


# ─── FUENTES ─────────────────────────────────────────────────────────────────
def setup_fonts():
    return {
        "title":   tkfont.Font(family="Courier New", size=18, weight="bold"),
        "head":    tkfont.Font(family="Courier New", size=13, weight="bold"),
        "label":   tkfont.Font(family="Courier New", size=10),
        "small":   tkfont.Font(family="Courier New", size=9),
        "mono":    tkfont.Font(family="Courier New", size=11),
        "mono_sm": tkfont.Font(family="Courier New", size=9),
        "big":     tkfont.Font(family="Courier New", size=22, weight="bold"),
    }


# ─── HELPERS UI ───────────────────────────────────────────────────────────────
def card(parent, **kw):
    return tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                    highlightthickness=1, **kw)

def section_title(parent, text, F):
    tk.Label(parent, text=text.upper(), bg=parent["bg"],
             fg=ACCENT2, font=F["small"], anchor="w").pack(
        fill="x", padx=4, pady=(14, 4))
    tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x", padx=4, pady=(0, 8))

def badge(parent, text, color=GREEN, bg=CARD):
    f = tk.Frame(parent, bg=bg)
    inner = tk.Frame(f, bg=color)
    inner.pack(padx=2, pady=2)
    tk.Label(inner, text=f"  {text}  ", bg=color, fg=BG,
             font=tkfont.Font(family="Courier New", size=9, weight="bold")).pack()
    return f

def metric_card(parent, title, value, sub="", F=None):
    c = card(parent)
    c.pack_propagate(False)
    c.configure(height=100)
    tk.Label(c, text=title, bg=CARD, fg=GRAY,
             font=F["small"], anchor="w").pack(fill="x", padx=12, pady=(10, 2))
    tk.Label(c, text=value, bg=CARD, fg=ACCENT2,
             font=F["head"], anchor="w").pack(fill="x", padx=12)
    if sub:
        tk.Label(c, text=sub, bg=CARD, fg=GRAY,
                 font=F["small"], anchor="w").pack(fill="x", padx=12, pady=(0, 8))
    else:
        tk.Frame(c, bg=CARD, height=8).pack()
    return c


def _derive_demo_from_rut(rut_formatted: str) -> dict:
    """Deriva valores demo a partir del RUT formateado.
    Esto permite que la segunda interfaz cambie según el RUT ingresado.
    """
    # Extraer solo dígitos del RUT
    import re
    digits = re.sub(r"\D", "", rut_formatted or "")
    if not digits:
        digits = "12345678"

    # Use slices and sums to produce deterministic demo values
    def g(i, length=2):
        return int(digits[i:i+length]) if i + length <= len(digits) else int(digits[-2:])

    A = round((g(0) % 9) + 0.5, 2)
    B = round((g(2) % 7) + 0.2, 2)
    C = - (g(4) % 20)
    D = - (g(5) % 18)
    E = (g(6) % 12)

    tipo = "Elipse" if A > B else "Hipérbola"

    demo = {
        "rut": rut_formatted,
        "valido": True,
        "A": f"{A}",
        "B": f"{B}",
        "C": f"{C}",
        "D": f"{D}",
        "E": f"{E}",
        "tipo": tipo,
        "ecuacion": f"{A}x² + {B}y² {C:+}x {D:+}y + {E} = 0",
        "canonica": "(x−h)² / a  +  (y−k)² / b  =  1",
        "centro": "(h , k)",
        "focos": "(h ± c , k)",
        "vertices": "(...)",
        "pasos_gen_can": ["1. Agrupar términos...", "2. Completar cuadrados..."] ,
        "pasos_can_gen": ["1. Expandir...", "2. Reagrupar..."],
    }
    return demo


# ═══════════════════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CónicasRUT — MAT1186")
        self.geometry("1200x750")
        self.minsize(1100, 680)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.F = setup_fonts()
        self.current_page = None
        self.rut_digit_entries = []
        self.rut_dv_entry = None
        self.current_theme = "dark"
        self.validated_rut = None

        # Detect Windows theme preference (safe fallback to dark)
        try:
            self.current_theme = self._detect_windows_theme()
        except Exception:
            self.current_theme = "dark"
        self._apply_theme(self.current_theme)

        self._show_input_screen()

    def _detect_windows_theme(self):
        """Detecta preferencia de tema en Windows (AppsUseLightTheme).
        Devuelve 'light' o 'dark'."""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if val == 1 else "dark"
        except Exception:
            return "dark"

    def _apply_theme(self, theme_name):
        """Apply theme colors by updating module-level color globals and reconfiguring window bg."""
        global BG, PANEL, CARD, ACCENT, ACCENT2, GREEN, RED, YELLOW, WHITE, GRAY, BORDER, PLOT_BG
        palette = LIGHT_THEME if theme_name == "light" else DARK_THEME
        BG = palette["BG"]
        PANEL = palette["PANEL"]
        CARD = palette["CARD"]
        ACCENT = palette["ACCENT"]
        ACCENT2 = palette["ACCENT2"]
        GREEN = palette["GREEN"]
        RED = palette["RED"]
        YELLOW = palette["YELLOW"]
        WHITE = palette["WHITE"]
        GRAY = palette["GRAY"]
        BORDER = palette["BORDER"]
        PLOT_BG = palette["PLOT_BG"]
        self.configure(bg=BG)

    def _show_input_screen(self):
        """Pantalla inicial: entrada de RUT"""
        if self.current_page:
            self.current_page.destroy()
        
        self.current_page = tk.Frame(self, bg=BG)
        self.current_page.pack(fill="both", expand=True)
        
        # Centro vertical
        center = tk.Frame(self.current_page, bg=BG)
        center.place(relx=0.55, rely=0.5, anchor="center")
        
        # Logo
        logo_frame = tk.Frame(center, bg=BG)
        logo_frame.pack(pady=(0, 40))
        tk.Label(logo_frame, text="◈", bg=BG, fg=ACCENT, font=self.F["title"]).pack()
        tk.Label(logo_frame, text="CónicasRUT", bg=BG, fg=WHITE, font=self.F["title"]).pack()
        tk.Label(logo_frame, text="MAT1186", bg=BG, fg=GRAY, font=self.F["label"]).pack()
        
        # Card de entrada
        input_card = card(center)
        # Make the input card larger and prevent it shrinking
        input_card.configure(width=820, height=240)
        input_card.pack(padx=40, pady=20)
        input_card.pack_propagate(False)
        
        tk.Label(input_card, text="Ingresa tu RUT", bg=CARD, fg=WHITE,
                 font=self.F["head"]).pack(padx=24, pady=(14, 10))
        
        entry_frame = tk.Frame(input_card, bg=CARD)
        entry_frame.pack(padx=24, pady=(6, 6), fill="x")
        
        self._create_rut_boxes(entry_frame)
        self.rut_digit_entries[0].focus_set()
        
        # RUT status badge (válido/no válido)
        status_badge_frame = tk.Frame(input_card, bg=CARD)
        status_badge_frame.pack(padx=24, pady=(6, 4))
        self.rut_status_badge = tk.Label(status_badge_frame, text="• RUT no validado", 
                                          bg=CARD, fg=GRAY, font=self.F["label"], anchor="w")
        self.rut_status_badge.pack(fill="x")
        
        # Requirement checklist (3 puntos) - live feedback
        req_frame = tk.Frame(input_card, bg=CARD)
        req_frame.pack(fill="x", padx=24, pady=(4, 6))
        self.req_rows = []
        req_texts = [
            "7 u 8 dígitos antes del guion (completos)",
            "Si tiene 7 dígitos, primera casilla vacía",
            "DV presente (0-9 o K)"
        ]
        for txt in req_texts:
            row = tk.Frame(req_frame, bg=CARD)
            row.pack(fill="x", pady=2)
            icon = tk.Label(row, text="•", bg=CARD, fg=GRAY, font=self.F["label"], width=2)
            icon.pack(side="left")
            lbl = tk.Label(row, text=txt, bg=CARD, fg=GRAY, font=self.F["small"], anchor="w")
            lbl.pack(side="left", fill="x")
            self.req_rows.append((icon, lbl))
        
        # Make button larger
        btn_frame = tk.Frame(input_card, bg=CARD)
        btn_frame.pack(padx=20, pady=(8, 18), fill="x")
        
        btn = tk.Button(btn_frame, text="Analizar", bg=ACCENT, fg=WHITE,
                        font=self.F["label"], bd=0, cursor="hand2",
                        activebackground=ACCENT2, activeforeground=BG,
                        command=self._validate_and_show)
        btn.pack(ipady=10, ipadx=28)
        
        status_frame = tk.Frame(input_card, bg=CARD)
        status_frame.pack(padx=20, pady=(0, 12), fill="x")
        self.status_label = tk.Label(status_frame, text="", bg=CARD, fg=RED, font=self.F["small"])
        self.status_label.pack()
        self.on_input_screen = True
        # initial check
        self._update_requirements_status()

    def _validate_and_show(self):
        """Validar RUT y mostrar interfaz completa"""
        rut, error = self._get_rut_from_boxes()
        if error:
            self.status_label.config(text=error, fg=RED)
            return
        
        validation = validate_rut(rut)
        if not validation["valid"]:
            self.status_label.config(text=validation["error"], fg=RED)
            return
        
        self.validated_rut = validation["rut_formatted"]
        self.status_label.config(text=f"✓ RUT válido: {self.validated_rut}", fg=GREEN)
        self.after(600, self._show_main_interface)

    def _restrict_digit(self, event, is_dv=False):
        widget = event.widget
        value = widget.get().upper()
        if is_dv:
            if not value:
                return
            if len(value) > 1:
                value = value[0]
            if value not in "0123456789K":
                widget.delete(0, "end")
                return
            widget.delete(0, "end")
            widget.insert(0, value)
            return
        if not value:
            widget.delete(0, "end")
            return
        if len(value) > 1:
            value = value[0]
        if not value.isdigit():
            widget.delete(0, "end")
            return
        widget.delete(0, "end")
        widget.insert(0, value)

    def _focus_next_rut_digit(self, event, index):
        if len(event.widget.get()) == 1:
            if index + 1 < len(self.rut_digit_entries):
                self.rut_digit_entries[index + 1].focus_set()
            else:
                self.rut_dv_entry.focus_set()

    def _update_requirements_status(self):
        """Actualizar la lista de requisitos en tiempo real según el contenido de las casillas."""
        if not hasattr(self, 'req_rows'):
            return
        digits = [e.get().strip() for e in self.rut_digit_entries]
        dv = self.rut_dv_entry.get().strip().upper() if self.rut_dv_entry else ""
        group1 = digits[:2]
        group2 = digits[2:5]
        group3 = digits[5:8]
        filled_digits = [d for d in digits if d != ""]
        total_filled = len(filled_digits)
        middle_filled = all(d != "" for d in group2 + group3)

        # Req 1: 7 u 8 dígitos antes del guion y middle groups completos
        req1_ok = middle_filled and (total_filled == 7 or total_filled == 8)
        # Req 2: si tiene 7 dígitos, primera casilla vacía
        if total_filled == 7:
            req2_ok = (group1[0] == "" and group1[1] != "")
        elif total_filled == 8:
            req2_ok = (group1[0] != "" and group1[1] != "")
        else:
            req2_ok = False
        # Req 3: DV presente y correcto formato (sin verificar checksum)
        req3_ok = bool(dv) and (dv.isdigit() or dv == "K")

        reqs = [req1_ok, req2_ok, req3_ok]
        messages = [
            "Completa 7 u 8 dígitos antes del guion",
            "Primera casilla debe quedar vacía para RUTs de 7 dígitos",
            "Ingresa DV (0-9 o K)"
        ]

        first_error = None
        for i, (ok, (icon, lbl)) in enumerate(zip(reqs, self.req_rows)):
            if ok:
                icon.config(text="✓", fg=GREEN)
                lbl.config(fg=GREEN)
            else:
                # determine neutral vs error
                related_filled = False
                if i == 0:
                    related_filled = total_filled > 0
                elif i == 1:
                    related_filled = (group1[0] != "" or group1[1] != "")
                else:
                    related_filled = bool(dv)
                if related_filled:
                    icon.config(text="✖", fg=RED)
                    lbl.config(fg=RED)
                    if first_error is None:
                        first_error = messages[i]
                else:
                    icon.config(text="•", fg=GRAY)
                    lbl.config(fg=GRAY)
        if first_error:
            self.status_label.config(text=first_error, fg=RED)
        else:
            self.status_label.config(text="", fg=GREEN)

    def _get_rut_from_boxes(self):
        digits = [entry.get().strip() for entry in self.rut_digit_entries]
        dv = self.rut_dv_entry.get().strip().upper()

        if not any(digits):
            return None, "Por favor completa el RUT"
        if not dv:
            return None, "Por favor ingresa el dígito verificador"
        if not (dv.isdigit() or dv == "K"):
            return None, "DV debe ser un número o K"

        group1 = digits[:2]
        group2 = digits[2:5]
        group3 = digits[5:8]

        if any(d == "" for d in group2 + group3):
            return None, "Completa todas las casillas del RUT"
        if group1[0] == "" and group1[1] == "":
            return None, "Completa la primera casilla del RUT"
        if group1[0] != "" and group1[1] == "":
            return None, "Para un RUT de 7 dígitos deja vacía la primera casilla"

        if group1[0] != "" and group1[1] != "":
            rut_digits = group1 + group2 + group3
            if len(rut_digits) != 8:
                return None, "El RUT debe tener 8 dígitos antes del guion"
        else:
            rut_digits = [group1[1]] + group2 + group3
            if len(rut_digits) != 7:
                return None, "El RUT debe tener 7 dígitos antes del guion"

        if not all(d.isdigit() for d in rut_digits):
            return None, "Los dígitos del RUT deben ser números"

        rut_number = "".join(rut_digits)
        if len(rut_number) == 8:
            formatted = f"{rut_number[:2]}.{rut_number[2:5]}.{rut_number[5:]}-{dv}"
        else:
            formatted = f"{rut_number[:1]}.{rut_number[1:4]}.{rut_number[4:]}-{dv}"
        return formatted, None

    def _create_rut_boxes(self, parent):
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", padx=10, pady=(0, 4))
        # Center the row
        row_wrapper = tk.Frame(parent, bg=CARD)
        row_wrapper.pack(fill="x", padx=10, pady=(0, 4))
        row = tk.Frame(row_wrapper, bg=CARD)
        row.pack(anchor="center")

        self.rut_digit_entries = []
        group_sizes = [2, 3, 3]
        for group_index, size in enumerate(group_sizes):
            for i in range(size):
                entry = tk.Entry(row, bg=PANEL, fg=WHITE, insertbackground=WHITE,
                                 font=self.F["mono"], bd=0, relief="flat",
                                 width=3, justify="center")
                entry.pack(side="left", ipadx=6, ipady=8)
                idx = len(self.rut_digit_entries)
                entry.bind("<KeyRelease>", lambda ev, idx=idx: self._on_rut_digit(ev, idx))
                entry.bind("<KeyPress>", lambda ev, idx=idx: self._on_rut_keypress(ev, idx))
                self.rut_digit_entries.append(entry)
            if group_index < len(group_sizes) - 1:
                tk.Label(row, text=".", bg=CARD, fg=GRAY, font=self.F["head"]).pack(side="left", padx=6)

        hyphen = tk.Label(row, text="-", bg=CARD, fg=GRAY, font=self.F["head"])
        hyphen.pack(side="left", padx=6)

        self.rut_dv_entry = tk.Entry(row, bg=PANEL, fg=WHITE, insertbackground=WHITE,
                         font=self.F["mono"], bd=0, relief="flat",
                         width=3, justify="center")
        self.rut_dv_entry.pack(side="left", ipadx=6, ipady=8)
        self.rut_dv_entry.bind("<KeyRelease>", lambda ev: self._on_rut_dv(ev))
        self.rut_dv_entry.bind("<KeyPress>", lambda ev: self._on_rut_dv_keypress(ev))
        self.rut_dv_entry.bind("<Return>", lambda ev: self._validate_and_show())
        # update requirements and validation badge when boxes are created
        try:
            self._update_requirements_status()
            self._update_rut_validation_badge()
        except Exception:
            pass

    def _on_rut_digit(self, event, index):
        self._restrict_digit(event, is_dv=False)
        self._focus_next_rut_digit(event, index)
        try:
            self._update_requirements_status()
            self._update_rut_validation_badge()
        except Exception:
            pass

    def _on_rut_keypress(self, event, index):
        key = event.keysym
        w = event.widget
        if key == "BackSpace":
            if w.get():
                w.delete(0, "end")
            else:
                if index > 0:
                    prev = self.rut_digit_entries[index - 1]
                    prev.delete(0, "end")
                    prev.focus_set()
        elif key == "Delete":
            if w.get():
                w.delete(0, "end")
            else:
                if index + 1 < len(self.rut_digit_entries):
                    nxt = self.rut_digit_entries[index + 1]
                    nxt.delete(0, "end")
                    nxt.focus_set()
                else:
                    self.rut_dv_entry.delete(0, "end")
                    self.rut_dv_entry.focus_set()
        elif key == "Left":
            if index > 0:
                self.rut_digit_entries[index - 1].focus_set()
        elif key == "Right":
            if index + 1 < len(self.rut_digit_entries):
                self.rut_digit_entries[index + 1].focus_set()
            else:
                self.rut_dv_entry.focus_set()

    def _on_rut_dv_keypress(self, event):
        key = event.keysym
        if key == "BackSpace":
            if self.rut_dv_entry.get():
                self.rut_dv_entry.delete(0, "end")
            else:
                # move focus to last digit
                if self.rut_digit_entries:
                    last = self.rut_digit_entries[-1]
                    last.delete(0, "end")
                    last.focus_set()
        elif key == "Delete":
            self.rut_dv_entry.delete(0, "end")
        elif key == "Left":
            if self.rut_digit_entries:
                self.rut_digit_entries[-1].focus_set()

    def _on_rut_dv(self, event):
        self._restrict_digit(event, is_dv=True)
        try:
            self._update_requirements_status()
            self._update_rut_validation_badge()
        except Exception:
            pass

    def _show_main_interface(self):
        """Mostrar la interfaz principal con navegación y contenido"""
        if self.current_page:
            self.current_page.destroy()
        
        self.current_page = tk.Frame(self, bg=BG)
        self.current_page.pack(fill="both", expand=True)
        
        self._topbar(self.current_page)
        
        # Contenedor de pestañas
        self.tab_frame = tk.Frame(self.current_page, bg=BG)
        self.tab_frame.pack(fill="both", expand=True)
        
        # Crear páginas
        self.pages = {}
        for name, Cls in [("conica", PageConica), ("tramos", PageTramos)]:
            p = Cls(self.tab_frame, self.F)
            p.place(x=0, y=0, relwidth=1, relheight=1)
            # provide validated RUT to pages for updating graphs/calculations
            try:
                p.rut = self.validated_rut
                if hasattr(p, 'update_with_rut'):
                    p.update_with_rut(self.validated_rut)
            except Exception:
                pass
            self.pages[name] = p
        
        self._show("conica")
        self.on_input_screen = False

    def _toggle_theme(self):
        """Alterna entre tema claro/oscuro y vuelve a renderizar la vista actual."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme(self.current_theme)
        # update icon
        if hasattr(self, 'theme_btn'):
            icon = "☀" if self.current_theme == "light" else "☾"
            self.theme_btn.config(text=icon)
        # re-render current page to apply new colors
        if getattr(self, 'on_input_screen', False):
            self._show_input_screen()
        else:
            self._show_main_interface()

    def _topbar(self, parent):
        """Barra superior con logo y navegación"""
        bar = tk.Frame(parent, bg=PANEL, height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        # Theme toggle (right)
        right = tk.Frame(bar, bg=PANEL)
        right.pack(side="right", padx=12)
        # icon: sun for light, moon for dark
        icon = "☀" if self.current_theme == "light" else "☾"
        self.theme_btn = tk.Button(right, text=icon, bg=PANEL, fg=WHITE,
                       font=self.F["head"], bd=0, cursor="hand2",
                       activebackground=PANEL, activeforeground=ACCENT,
                       command=self._toggle_theme)
        self.theme_btn.pack(padx=6, pady=6)
        
        # Logo
        logo = tk.Frame(bar, bg=PANEL)
        logo.pack(side="left", padx=20, pady=10)
        tk.Label(logo, text="◈", bg=PANEL, fg=ACCENT, font=self.F["head"]).pack(side="left", padx=(0, 6))
        tk.Label(logo, text="CónicasRUT", bg=PANEL, fg=WHITE, font=self.F["head"]).pack(side="left")
        tk.Label(logo, text=" · MAT1186", bg=PANEL, fg=GRAY, font=self.F["label"]).pack(side="left")
        
        # Tabs
        tab_wrap = tk.Frame(bar, bg=PANEL)
        tab_wrap.pack(side="right", padx=20, pady=10)
        
        self.tab_btns = {}
        for key, label in [("conica", "⬡  Secciones Cónicas"), ("tramos", "∿  Funciones por Tramos")]:
            b = tk.Button(tab_wrap, text=label, bg=PANEL, fg=GRAY,
                         font=self.F["small"], bd=0, cursor="hand2",
                         command=lambda k=key: self._show(k))
            b.pack(side="left", padx=(0, 10))
            self.tab_btns[key] = b

    def _show(self, name):
        """Cambiar entre páginas y actualizar estilo de tabs"""
        for k, b in self.tab_btns.items():
            if k == name:
                b.config(bg=ACCENT, fg=WHITE)
            else:
                b.config(bg=PANEL, fg=GRAY)
        self.pages[name].lift()


# ═══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 1 — SECCIONES CÓNICAS
# ═══════════════════════════════════════════════════════════════════════════════
class PageConica(tk.Frame):
    def __init__(self, parent, F):
        super().__init__(parent, bg=BG)
        self.F = F
        # Datos demo (en futuro vendrán del core)
        self.demo = {
            "rut":        "12.345.678-9",
            "valido":     True,
            "A":  "1.44",
            "B":  "0.78",
            "C":  "-11",
            "D":  "-15",
            "E":  "9",
            "tipo":       "Elipse",
            "ecuacion":   "1.44x² + 0.78y² − 11x − 15y + 9 = 0",
            "canonica":   "(x−3.8)² / 6.9  +  (y−9.6)² / 12.8  =  1",
            "centro":     "(3.8 , 9.6)",
            "focos":      "(3.8 ± 2.5 , 9.6)",
            "vertices":   "(1.2 , 9.6)  y  (6.4 , 9.6)",
            "pasos_gen_can": [
                "1. Agrupar términos en x e y:",
                "   1.44(x² − 7.64x) + 0.78(y² − 19.2y) = −9",
                "2. Completar cuadrado en x:",
                "   1.44(x − 3.8)² − 20.8",
                "3. Completar cuadrado en y:",
                "   0.78(y − 9.6)² − 71.9",
                "4. Despejar e igualar a 1:",
                "   (x−3.8)²/6.9 + (y−9.6)²/12.8 = 1  ✓",
            ],
            "pasos_can_gen": [
                "1. Expandir (x−3.8)² = x² − 7.6x + 14.44",
                "2. Expandir (y−9.6)² = y² − 19.2y + 92.16",
                "3. Multiplicar por A=1.44 y B=0.78",
                "4. Reagrupar todos los términos:",
                "   1.44x² + 0.78y² − 11x − 15y + 9 = 0  ✓",
            ],
        }
        self._build()

    def update_with_rut(self, rut_formatted: str):
        """Re-genera la vista usando datos derivados del RUT."""
        try:
            self.demo = _derive_demo_from_rut(rut_formatted)
            # Rebuild UI to reflect new demo data
            for ch in self.winfo_children():
                ch.destroy()
            self._build()
        except Exception:
            pass

    def _build(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=16, pady=12)
        
        # layout: sidebar izq | contenido der
        left = tk.Frame(root, bg=BG, width=290)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        
        right = tk.Frame(root, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(14, 0))
        
        self._sidebar(left)
        self._content(right)

    def _sidebar(self, parent):
        """Panel izquierdo: RUT, coeficientes, ecuaciones"""
        
        # RUT
        section_title(parent, "Ingresa tu RUT", self.F)
        rut_card = card(parent)
        rut_card.pack(fill="x", padx=2, pady=2)
        
        tk.Label(rut_card, text="RUT", bg=CARD, fg=GRAY,
                 font=self.F["small"], anchor="w").pack(fill="x", padx=12, pady=(10, 2))
        
        entry_row = tk.Frame(rut_card, bg=CARD)
        entry_row.pack(fill="x", padx=10, pady=(0, 4))
        
        self.rut_var = tk.StringVar(value=self.demo["rut"])
        e = tk.Entry(entry_row, textvariable=self.rut_var, bg=PANEL,
                     fg=WHITE, insertbackground=WHITE,
                     font=self.F["mono"], bd=0, relief="flat",
                     highlightbackground=BORDER, highlightthickness=1)
        e.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        
        btn = tk.Button(entry_row, text="Analizar", bg=ACCENT, fg=WHITE,
                        font=self.F["small"], bd=0, cursor="hand2",
                        activebackground=ACCENT2, activeforeground=BG,
                        padx=10, pady=6)
        btn.pack(side="left")
        
        badge_row = tk.Frame(rut_card, bg=CARD)
        badge_row.pack(fill="x", padx=10, pady=(4, 10))
        badge(badge_row, "✓  RUT válido", GREEN, CARD).pack(side="left", padx=(0, 6))
        badge(badge_row, self.demo["tipo"], ACCENT, CARD).pack(side="left")
        
        # Coeficientes
        section_title(parent, "Coeficientes generados", self.F)
        coef_card = card(parent)
        coef_card.pack(fill="x", padx=2, pady=2)
        
        grid = tk.Frame(coef_card, bg=CARD)
        grid.pack(fill="x", padx=10, pady=10)
        for letra, val in [
            ("A", self.demo["A"]), ("B", self.demo["B"]), ("C", self.demo["C"]),
            ("D", self.demo["D"]), ("E", self.demo["E"])
        ]:
            col = tk.Frame(grid, bg=CARD)
            col.pack(side="left", expand=True)
            tk.Label(col, text=letra, bg=CARD, fg=GRAY, font=self.F["small"]).pack()
            tk.Label(col, text=val, bg=CARD, fg=ACCENT2, font=self.F["head"]).pack()
        
        # Ecuación general
        section_title(parent, "Ecuación general", self.F)
        eq_card = card(parent)
        eq_card.pack(fill="x", padx=2, pady=2)
        tk.Label(eq_card, text=self.demo["ecuacion"], bg=CARD, fg=WHITE,
                 font=self.F["small"], wraplength=250, justify="center").pack(padx=10, pady=12)
        
        # Forma canónica
        section_title(parent, "Forma canónica", self.F)
        can_card = card(parent)
        can_card.pack(fill="x", padx=2, pady=2)
        tk.Label(can_card, text=self.demo["canonica"], bg=CARD, fg=ACCENT2,
                 font=self.F["small"], wraplength=250, justify="center").pack(padx=10, pady=12)

    def _content(self, parent):
        """Panel derecho: métricas, gráfico y pasos"""
        
        # Métricas
        metrics = tk.Frame(parent, bg=BG)
        metrics.pack(fill="x", pady=(0, 10))
        
        for i, (tit, val, sub) in enumerate([
            ("Tipo de cónica", self.demo["tipo"], "A y B mismo signo, A ≠ B"),
            ("Centro", self.demo["centro"], "completando el cuadrado"),
            ("Focos", self.demo["focos"], "c² = a² − b²"),
            ("Vértices", self.demo["vertices"], "sobre el eje mayor"),
        ]):
            m = metric_card(metrics, tit, val, sub, self.F)
            m.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 8, 0))
        
        # Fila inferior
        bottom = tk.Frame(parent, bg=BG)
        bottom.pack(fill="both", expand=True)
        
        self._plot(bottom)
        self._steps(bottom)

    def _plot(self, parent):
        """Área de gráfico"""
        frame = card(parent)
        frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(frame, text="Gráfico — Plano Cartesiano", bg=CARD,
                 fg=WHITE, font=self.F["label"], anchor="w").pack(
            fill="x", padx=14, pady=(10, 0))
        
        self.canvas_plot = tk.Canvas(frame, bg=PLOT_BG, bd=0, highlightthickness=0)
        self.canvas_plot.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas_plot.bind("<Configure>", lambda e: self._draw_plot())

    def _draw_plot(self):
        """Dibujar gráfico con elipse, focos y vértices"""
        c = self.canvas_plot
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 10 or h < 10:
            return
        
        cx, cy = w // 2, h // 2
        scale = min(w, h) // 10
        
        # Grid
        for i in range(-10, 11):
            c.create_line(cx + i * scale, 0, cx + i * scale, h, fill=BORDER, width=0.5)
            c.create_line(0, cy + i * scale, w, cy + i * scale, fill=BORDER, width=0.5)
        
        # Ejes
        c.create_line(0, cy, w, cy, fill=GRAY, width=1)
        c.create_line(cx, 0, cx, h, fill=GRAY, width=1)
        c.create_text(w - 12, cy - 10, text="x", fill=GRAY, font=self.F["small"])
        c.create_text(cx + 10, 12, text="y", fill=GRAY, font=self.F["small"])
        
        # Ticks
        for i in range(-8, 9):
            if i != 0:
                c.create_line(cx + i * scale - 2, cy - 2, cx + i * scale + 2, cy + 2, fill=GRAY, width=0.5)
                c.create_line(cx - 2, cy + i * scale - 2, cx + 2, cy + i * scale + 2, fill=GRAY, width=0.5)
                c.create_text(cx + i * scale, cy + 14, text=str(i), fill=GRAY, font=self.F["small"])
                c.create_text(cx - 14, cy + i * scale, text=str(-i), fill=GRAY, font=self.F["small"])
        
        # Elipse demo (parameters derived from demo data if available)
        try:
            A = float(self.demo.get("A", 1.0))
            B = float(self.demo.get("B", 1.0))
            D = float(self.demo.get("D", 0.0))
            E = float(self.demo.get("E", 0.0))
        except Exception:
            A, B, D, E = 1.0, 1.0, 0.0, 0.0

        # center offset influenced by D/E
        ox = cx - int(scale * (0.5 + (D % 3) * 0.1))
        oy = cy + int(scale * (0.3 + (E % 3) * 0.1))
        # radii influenced by A/B
        ra = max(10, int(scale * (1.8 + A * 0.6)))
        rb = max(8, int(scale * (1.2 + B * 0.5)))

        # Sombra
        c.create_oval(ox - ra + 4, oy - rb + 4, ox + ra + 4, oy + rb + 4,
                      outline="", fill="#2E1D60", width=0)
        # Elipse
        fill_col = "#1C1545" if BG == DARK_THEME["BG"] else "#EDE7FF"
        c.create_oval(ox - ra, oy - rb, ox + ra, oy + rb,
                      outline=ACCENT, fill=fill_col, width=2)

        # Centro
        c.create_oval(ox - 5, oy - 5, ox + 5, oy + 5, fill=ACCENT, outline="")
        c.create_text(ox + 12, oy - 12, text="C", fill=ACCENT2, font=self.F["small"])

        # Focos
        c_dist = int(scale * (1.4 + (A - B) * 0.2))
        for fx, label_text in [(ox - c_dist, "F₂"), (ox + c_dist, "F₁")]:
            c.create_oval(fx - 4, oy - 4, fx + 4, oy + 4, fill=YELLOW, outline="")
            c.create_text(fx, oy - 14, text=label_text, fill=YELLOW, font=self.F["small"])

        # Vértices
        for vx, label_text in [(ox - ra, "V₁"), (ox + ra, "V₂")]:
            c.create_oval(vx - 4, oy - 4, vx + 4, oy + 4, fill=GREEN, outline="")
            c.create_text(vx, oy + 14, text=label_text, fill=GREEN, font=self.F["small"])
        
        # Leyenda
        items = [("━", ACCENT, "Elipse"),
                 ("●", ACCENT2, "Centro"),
                 ("●", YELLOW, "Focos"),
                 ("●", GREEN, "Vértices")]
        lx, ly = 10, h - 30
        for sym, col, txt in reversed(items):
            c.create_text(lx, ly, text=sym, fill=col, font=self.F["label"], anchor="w")
            c.create_text(lx + 20, ly, text=txt, fill=col, font=self.F["small"], anchor="w")
            ly -= 18

    def _steps(self, parent):
        """Tabs con pasos de transformación"""
        frame = card(parent)
        frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        nb = ttk.Notebook(frame)
        nb.pack(fill="both", expand=True, padx=8, pady=8)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=CARD, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL, foreground=GRAY,
                        font=("Courier New", 9), padding=[10, 4])
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", WHITE)])
        
        for title, pasos in [
            ("General → Canónica", self.demo["pasos_gen_can"]),
            ("Canónica → General", self.demo["pasos_can_gen"]),
        ]:
            tab = tk.Frame(nb, bg=CARD)
            nb.add(tab, text=title)
            
            text_frame = tk.Frame(tab, bg=CARD)
            text_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            for paso in pasos:
                tk.Label(text_frame, text=paso, bg=CARD, fg=WHITE if paso.startswith(("1", "2", "3", "4")) else ACCENT2,
                         font=self.F["mono_sm"], justify="left", anchor="w").pack(
                    fill="x", pady=2)


# ═══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 2 — FUNCIONES POR TRAMOS
# ═══════════════════════════════════════════════════════════════════════════════
class PageTramos(tk.Frame):
    def __init__(self, parent, F):
        super().__init__(parent, bg=BG)
        self.F = F
        self.demo_tramo = {
            "caso":     "Discontinuidad removible  (d₈ = 8, múltiplo de 3)",
            "funcion":  ["f(x) = (x−3)(x+1) / (x−3)   si x < 3",
                         "f(x) = x + 4                  si x ≥ 3"],
            "lim_izq":  "lím x→3⁻  f(x) = 3 + 1 = 4",
            "lim_der":  "lím x→3⁺  f(x) = 3 + 4 = 7",
            "tabla": [
                ("x", "f(x)"),
                ("2.000", "3.000"),
                ("2.900", "3.900"),
                ("2.990", "3.990"),
                ("2.999", "3.999"),
                ("—", "—"),
                ("3.001", "7.001"),
                ("3.010", "7.010"),
                ("3.100", "7.100"),
                ("4.000", "8.000"),
            ],
            "conclusion": "Límite NO existe (límites laterales distintos)\nDiscontinuidad de SALTO en x = 3",
        }
        self._build()

    def update_with_rut(self, rut_formatted: str):
        """Update demo_tramo based on provided RUT and rebuild UI."""
        try:
            # For demo purposes, change the case string based on last digit
            import re
            digits = re.sub(r"\D", "", rut_formatted or "")
            last = int(digits[-1]) if digits else 0
            if last % 3 == 0:
                caso = "Discontinuidad removible"
            elif last % 2 == 0:
                caso = "Continuidad"
            else:
                caso = "Discontinuidad de salto"
            self.demo_tramo["caso"] = f"{caso}  (d = {last})"
            self.demo_tramo["last_digit"] = last
            for ch in self.winfo_children():
                ch.destroy()
            self._build()
        except Exception:
            pass

    def _build(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=16, pady=12)
        
        left = tk.Frame(root, bg=BG, width=290)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        
        right = tk.Frame(root, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(14, 0))
        
        self._sidebar(left)
        self._content(right)

    def _sidebar(self, parent):
        """Panel izquierdo para funciones por tramos"""
        section_title(parent, "Función generada", self.F)
        
        c1 = card(parent)
        c1.pack(fill="x", padx=2, pady=2)
        tk.Label(c1, text="Caso seleccionado:", bg=CARD, fg=GRAY,
                 font=self.F["small"], anchor="w").pack(
            fill="x", padx=12, pady=(10, 2))
        tk.Label(c1, text=self.demo_tramo["caso"], bg=CARD, fg=YELLOW,
                 font=self.F["small"], wraplength=250,
                 justify="left", anchor="w").pack(
            fill="x", padx=12, pady=(0, 10))
        
        section_title(parent, "Definición f(x)", self.F)
        c2 = card(parent)
        c2.pack(fill="x", padx=2, pady=2)
        for line in self.demo_tramo["funcion"]:
            tk.Label(c2, text=line, bg=CARD, fg=ACCENT2,
                     font=self.F["mono_sm"], anchor="w").pack(
                fill="x", padx=12, pady=2)
        tk.Frame(c2, bg=CARD, height=8).pack()
        
        section_title(parent, "Límites laterales", self.F)
        c3 = card(parent)
        c3.pack(fill="x", padx=2, pady=2)
        tk.Label(c3, text=self.demo_tramo["lim_izq"], bg=CARD, fg=GREEN,
                 font=self.F["small"], anchor="w").pack(
            fill="x", padx=12, pady=(10, 4))
        tk.Label(c3, text=self.demo_tramo["lim_der"], bg=CARD, fg=YELLOW,
                 font=self.F["small"], anchor="w").pack(
            fill="x", padx=12, pady=(0, 10))
        
        section_title(parent, "Conclusión", self.F)
        c4 = card(parent)
        c4.pack(fill="x", padx=2, pady=2)
        tk.Label(c4, text=self.demo_tramo["conclusion"], bg=CARD, fg=RED,
                 font=self.F["small"], wraplength=250,
                 justify="left", anchor="w").pack(
            fill="x", padx=12, pady=10)

    def _content(self, parent):
        """Panel derecho: gráfico y tabla"""
        top = tk.Frame(parent, bg=BG)
        top.pack(fill="both", expand=True)
        
        self._plot_tramo(top)
        self._tabla_defensa(top)

    def _plot_tramo(self, parent):
        """Gráfico de funciones por tramos"""
        frame = card(parent)
        frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(frame, text="Gráfico — Función por tramos", bg=CARD,
                 fg=WHITE, font=self.F["label"], anchor="w").pack(
            fill="x", padx=14, pady=(10, 0))
        
        self.cv_tramo = tk.Canvas(frame, bg=PLOT_BG, bd=0, highlightthickness=0)
        self.cv_tramo.pack(fill="both", expand=True, padx=10, pady=10)
        self.cv_tramo.bind("<Configure>", lambda e: self._draw_tramo())

    def _draw_tramo(self):
        """Dibujar gráfico de función por tramos con discontinuidad"""
        c = self.cv_tramo
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 10 or h < 10:
            return
        
        xmin, xmax = -3, 10
        ymin, ymax = -2, 14
        last = self.demo_tramo.get('last_digit', 3)
        a = 3 + (last % 4)
        
        def px(x_val):
            return int((x_val - xmin) / (xmax - xmin) * w)
        def py(y_val):
            return int(h - (y_val - ymin) / (ymax - ymin) * h)
        
        # Grid
        for i in range(xmin, xmax + 1):
            c.create_line(px(i), 0, px(i), h, fill=BORDER, width=0.5)
        for j in range(ymin, ymax + 1):
            c.create_line(0, py(j), w, py(j), fill=BORDER, width=0.5)
        
        # Ejes
        c.create_line(px(0), 0, px(0), h, fill=GRAY, width=1)
        c.create_line(0, py(0), w, py(0), fill=GRAY, width=1)
        
        # Etiquetas eje x
        for i in range(xmin, xmax + 1, 2):
            c.create_text(px(i), py(0) + 14, text=str(i), fill=GRAY, font=self.F["small"])
        
        # Asíntota vertical
        c.create_line(px(a), 0, px(a), h, fill=RED, dash=(6, 4), width=1)
        c.create_text(px(a) + 10, 14, text=f"x={a}", fill=RED, font=self.F["small"])
        
        # Tramo izquierdo: f(x) = x+1 (x < 3)
        pts = []
        for i in range(300):
            x = xmin + (i / 300) * (a - xmin)
            y = x + 1
            if ymin <= y <= ymax:
                pts.append((px(x), py(y)))
        if len(pts) >= 4:
            c.create_line(*pts, fill=GREEN, width=2)
        
        # Punto hueco en x=3, y=4
        hx, hy = px(a), py(a + 1)
        c.create_oval(hx - 5, hy - 5, hx + 5, hy + 5,
                      outline=GREEN, fill=PLOT_BG, width=2)
        
        # Tramo derecho: f(x) = x+4 (x >= 3)
        pts2 = []
        for i in range(300):
            x = a + (i / 300) * (xmax - a)
            y = x + 4
            if ymin <= y <= ymax:
                pts2.append((px(x), py(y)))
        if len(pts2) >= 4:
            c.create_line(*pts2, fill=YELLOW, width=2)
        
        # Punto sólido en x=3, y=7
        sx, sy = px(a), py(a + 4)
        c.create_oval(sx - 5, sy - 5, sx + 5, sy + 5, fill=YELLOW, outline="")
        
        # Leyenda
        items = [("━", GREEN, "x < 3  →  x+1"),
                 ("━", YELLOW, "x ≥ 3  →  x+4"),
                 ("○", GREEN, "punto hueco"),
                 ("●", YELLOW, "punto definido"),
                 ("┅", RED, "x = 3  (discontinuidad)")]
        lx, ly = 10, h - 20
        for sym, col, txt in reversed(items):
            c.create_text(lx, ly, text=sym, fill=col, font=self.F["label"], anchor="w")
            c.create_text(lx + 20, ly, text=txt, fill=col, font=self.F["small"], anchor="w")
            ly -= 18

    def _tabla_defensa(self, parent):
        """Panel derecho: tabla y campos de defensa"""
        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        # Tabla
        frame_t = card(right)
        frame_t.pack(fill="x")
        tk.Label(frame_t, text="Tabla de valores cercanos a x = 3", bg=CARD,
                 fg=WHITE, font=self.F["label"], anchor="w").pack(
            fill="x", padx=14, pady=(10, 4))
        
        tbl = tk.Frame(frame_t, bg=CARD)
        tbl.pack(fill="x", padx=10, pady=(0, 10))
        for r, (x_val, fx_val) in enumerate(self.demo_tramo["tabla"]):
            row = tk.Frame(tbl, bg=CARD)
            row.pack(fill="x", pady=2)
            
            color = WHITE if r == 0 else (GRAY if x_val == "—" else ACCENT2)
            tk.Label(row, text=x_val, bg=CARD, fg=color, font=self.F["mono_sm"],
                     width=8, anchor="e").pack(side="left")
            tk.Label(row, text=fx_val, bg=CARD, fg=color, font=self.F["mono_sm"],
                     width=8, anchor="e").pack(side="left", padx=(20, 0))
        
        # Campos defensa
        frame_d = card(right)
        frame_d.pack(fill="both", expand=True, pady=(10, 0))
        
        tk.Label(frame_d, text="⬡  Campos para defensa oral  (completar manualmente)",
                 bg=CARD, fg=ACCENT2, font=self.F["label"], anchor="w").pack(
            fill="x", padx=14, pady=(10, 6))
        
        fields_container = tk.Frame(frame_d, bg=CARD)
        fields_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        for label_text in [
            "Límite por la izquierda  →  lím x→3⁻ f(x) =",
            "Límite por la derecha    →  lím x→3⁺ f(x) =",
            "¿Existe el límite?",
            "Valor de f(3)",
            "¿Es continua en x=3?",
            "Tipo de discontinuidad",
            "Justificación escrita:",
        ]:
            row = tk.Frame(fields_container, bg=CARD)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label_text, bg=CARD, fg=GRAY, font=self.F["small"],
                     anchor="w").pack(side="left", fill="x", expand=True)
            tk.Entry(row, bg=PANEL, fg=ACCENT2, insertbackground=ACCENT2,
                     font=self.F["mono_sm"], bd=0, relief="flat",
                     highlightbackground=BORDER, highlightthickness=1).pack(
                side="right", fill="x", expand=True, padx=(10, 0))


def run():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    run()
