"""
MAT1186 — CónicasRUT
Interfaz visual principal - Replicación exacta de la maqueta
Flujo: Entrada RUT → Validación → Interfaz completa
"""

import math
import re
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


def _normalize_rut_digits(rut_formatted: str) -> str:
    digits = re.sub(r"\D", "", rut_formatted or "")
    return digits if digits else "1234567"


def _signed(value: float, precision: int = 2) -> str:
    return f"+{abs(value):.{precision}f}" if value >= 0 else f"-{abs(value):.{precision}f}"


def _signed_int(value: int) -> str:
    return f"+{abs(value)}" if value >= 0 else f"-{abs(value)}"


def _derive_demo_from_rut(rut_formatted: str) -> dict:
    digits = _normalize_rut_digits(rut_formatted)
    digits = digits[:8].ljust(8, "0")
    values = [int(d) for d in digits]

    A = 1.2 + (values[0] % 4) + (values[1] * 0.05)
    B = 0.8 + (values[1] % 4) + (values[2] * 0.04)
    if values[2] % 2:
        B = -B

    C = -((values[3] % 10) + 1) * (1 + (values[4] % 2))
    D = -((values[4] % 9) + 1) * (1 + (values[5] % 2))
    E = (values[5] % 10) - 4 + (values[6] % 3)
    if values[7] % 2:
        E += 2

    h = -C / (2 * A)
    k = -D / (2 * B)
    constant = -E + A * h * h + B * k * k
    if abs(constant) < 0.5:
        constant = 1.2 if constant >= 0 else -1.2
    if A * B > 0 and constant < 0:
        constant = abs(constant) + 2.5

    tipo = "Elipse" if A * B > 0 else "Hipérbola"
    sign_x = "-" if h >= 0 else "+"
    sign_y = "-" if k >= 0 else "+"

    a2 = abs(constant / A)
    b2 = abs(constant / B)
    a = math.sqrt(max(a2, 0.1))
    b = math.sqrt(max(b2, 0.1))
    c_val = math.sqrt(abs(a * a - b * b)) if tipo == "Elipse" else math.sqrt(a * a + b * b)

    if tipo == "Elipse":
        canonica = (
            f"(x {sign_x} {abs(h):.2f})² / {a2:.2f} + "
            f"(y {sign_y} {abs(k):.2f})² / {b2:.2f} = 1"
        )
        if a2 >= b2:
            vertices = f"({h:.2f} ± {a:.2f}, {k:.2f})"
            focos = f"({h:.2f} ± {c_val:.2f}, {k:.2f})"
        else:
            vertices = f"({h:.2f}, {k:.2f} ± {a:.2f})"
            focos = f"({h:.2f}, {k:.2f} ± {c_val:.2f})"
    else:
        if A > 0:
            canonica = (
                f"(x {sign_x} {abs(h):.2f})² / {a2:.2f} - "
                f"(y {sign_y} {abs(k):.2f})² / {b2:.2f} = 1"
            )
            vertices = f"({h:.2f} ± {a:.2f}, {k:.2f})"
            focos = f"({h:.2f} ± {c_val:.2f}, {k:.2f})"
        else:
            canonica = (
                f"(y {sign_y} {abs(k):.2f})² / {a2:.2f} - "
                f"(x {sign_x} {abs(h):.2f})² / {b2:.2f} = 1"
            )
            vertices = f"({h:.2f}, {k:.2f} ± {a:.2f})"
            focos = f"({h:.2f}, {k:.2f} ± {c_val:.2f})"

    if tipo == "Elipse":
        centro = f"({h:.2f} , {k:.2f})"
    else:
        centro = f"({h:.2f} , {k:.2f})"

    demo = {
        "rut": rut_formatted or "12.345.678-9",
        "valido": True,
        "A": f"{A:.2f}",
        "B": f"{B:.2f}",
        "C": f"{C}",
        "D": f"{D}",
        "E": f"{E}",
        "tipo": tipo,
        "ecuacion": f"{A:.2f}x² {_signed(B)}y² {_signed_int(C)}x {_signed_int(D)}y {_signed_int(E)} = 0",
        "canonica": canonica,
        "centro": centro,
        "focos": focos,
        "vertices": vertices,
        "pasos_gen_can": [
            f"1. Agrupar términos: {A:.2f}x² {_signed_int(C)}x {_signed(B)}y² {_signed_int(D)}y = {-E:.2f}",
            f"2. Completar cuadrados en x e y para obtener centro {centro}",
            f"3. Despejar el lado derecho: {constant:.2f}",
            f"4. Normalizar y escribir forma canónica",
        ],
        "pasos_gen_can_details": [
            "Para comenzar, aislamos los términos en x e y y mantenemos todos los constantes a la derecha. Esto permite formar los cuadrados perfectos.",
            "Luego completamos el cuadrado en x e y añadiendo y restando los mismos valores dentro de cada grupo para obtener las expresiones (x−h)² y (y−k)².",
            "Después, desplazamos la constante resultante al lado derecho de la ecuación para que la expresión quede igualada a un número.",
            "Finalmente dividimos por ese número para convertir la ecuación en la forma canónica estándar y organizar los denominadores.",
        ],
        "pasos_can_gen": [
            f"1. Expandir (x {sign_x} {abs(h):.2f})² y (y {sign_y} {abs(k):.2f})²",
            f"2. Multiplicar por A={A:.2f} y B={B:.2f}",
            f"3. Reagrupar términos para regresar a {A:.2f}x² {_signed(B)}y² {_signed_int(C)}x {_signed_int(D)}y {_signed_int(E)} = 0",
            f"4. Verificar que la ecuación general coincida con la forma original",
        ],
        "pasos_can_gen_details": [
            "Expandimos cada binomio cuadrado usando la fórmula (x±h)² = x² ± 2hx + h² y hacemos lo mismo con la variable y.",
            "Multiplicamos el resultado por A y B para obtener los coeficientes correctos del polinomio y conservar la forma original.",
            "Sumamos todos los términos semejantes y simplificamos, de modo que los términos en x², y², x y y vuelvan a formar la ecuación general.",
            "Verificamos que el resultado coincida con la ecuación original, revisando signos y constante para asegurar la equivalencia.",
        ],
        "center_x": h,
        "center_y": k,
        "a2": a2,
        "b2": b2,
        "a": a,
        "b": b,
    }
    return demo


def _derive_tramo_from_rut(rut_formatted: str) -> dict:
    digits = _normalize_rut_digits(rut_formatted)
    digits = digits[:7].rjust(7, "0")
    values = [int(d) for d in digits]

    x_cut = 2 + (values[0] % 5)
    m1 = 1 + (values[1] % 4)
    b1 = -3 + (values[2] % 6)
    m2 = m1 + (1 if values[3] % 2 == 0 else -1)
    b2 = b1 + (values[4] % 5 - 2)

    left_fn = lambda x: m1 * x + b1
    right_fn = lambda x: m2 * x + b2
    left_limit = left_fn(x_cut)
    right_limit = right_fn(x_cut)
    case_code = values[5] % 3

    if case_code == 1:
        # Continuidad: hacer coincidir ambos tramos en x_cut
        b2 = left_limit - m2 * x_cut
        right_fn = lambda x: m2 * x + b2
        right_limit = right_fn(x_cut)
        conclusion = f"Límite existe y coincide en x = {x_cut}. Función continua."
        defined_at_cut = True
        conclusion_type = "Continuidad"
    elif case_code == 0:
        # Discontinuidad removible: límites iguales, punto no definido
        b2 = left_limit - m2 * x_cut
        right_fn = lambda x: m2 * x + b2
        right_limit = right_fn(x_cut)
        conclusion = (
            f"Límite existe ({left_limit:.3f}) pero x = {x_cut} no está definido. "
            "Discontinuidad removible."
        )
        defined_at_cut = False
        conclusion_type = "Discontinuidad removible"
    else:
        conclusion = (
            f"Límite NO existe ({left_limit:.3f} ≠ {right_limit:.3f}). "
            "Discontinuidad de salto."
        )
        defined_at_cut = True
        conclusion_type = "Discontinuidad de salto"

    lines = [
        f"f(x) = {m1}x {_signed_int(b1)}  si x < {x_cut}",
        f"f(x) = {m2}x {_signed_int(b2)}  si x ≥ {x_cut}",
    ]

    x_values = [x_cut - 1, x_cut - 0.1, x_cut - 0.01, x_cut - 0.001, None,
                x_cut + 0.001, x_cut + 0.01, x_cut + 0.1, x_cut + 1]
    table = []
    for x in x_values:
        if x is None:
            table.append(("—", "—"))
            continue
        y = left_fn(x) if x < x_cut else right_fn(x)
        table.append((f"{x:.3f}", f"{y:.3f}"))

    lim_izq_str = f"lím x→{x_cut}⁻ f(x) = {left_limit:.3f}"
    lim_der_str = f"lím x→{x_cut}⁺ f(x) = {right_limit:.3f}"
    f_c = f"f({x_cut}) = {right_limit:.3f}" if defined_at_cut else f"f({x_cut}) no está definido"

    return {
        "caso": f"{conclusion_type}  (x = {x_cut})",
        "funcion": lines,
        "lim_izq": lim_izq_str,
        "lim_der": lim_der_str,
        "f_c": f_c,
        "tabla": table,
        "conclusion": conclusion,
        "x_cut": x_cut,
        "left_slope": m1,
        "left_intercept": b1,
        "right_slope": m2,
        "right_intercept": b2,
        "defined_at_cut": defined_at_cut,
        "left_value": left_limit,
        "right_value": right_limit,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CónicasRUT — MAT1186")

        # Tamaño de la ventana
        window_width = 1850
        window_height = 850

        # Obtener tamaño de pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular posición centrada
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Aplicar tamaño + posición
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Tamaño mínimo permitido
        self.minsize(1400, 780)

        # Configuración general
        self.configure(bg=BG)
        self.resizable(False, False)

        self.F = setup_fonts()
        self.current_page = None
        self.rut_digit_entries = []
        self.rut_dv_entry = None
        self.current_theme = "dark"
        self.validated_rut = None

        # Detectar tema de Windows
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

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )

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
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo
        logo_frame = tk.Frame(center, bg=BG)
        logo_frame.pack(pady=(0, 40))
        tk.Label(logo_frame, text="◈", bg=BG, fg=ACCENT, font=self.F["title"]).pack()
        tk.Label(logo_frame, text="CónicasRUT", bg=BG, fg=WHITE, font=self.F["title"]).pack()
        tk.Label(logo_frame, text="MAT1186", bg=BG, fg=GRAY, font=self.F["label"]).pack()
        
        # Card de entrada
        input_card = card(center)
        # Make the input card larger and prevent it shrinking
        input_card.configure(width=1100, height=340)
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
        btn_frame.pack(padx=20, pady=(8, 8), fill="x")
        
        btn = tk.Button(btn_frame, text="Analizar", bg=ACCENT, fg=WHITE,
                        font=self.F["label"], bd=0, cursor="hand2",
                        activebackground=ACCENT2, activeforeground=BG,
                        command=self._validate_and_show)
        btn.pack(ipady=12, ipadx=30)
        
        verify_frame = tk.Frame(input_card, bg=CARD)
        verify_frame.pack(padx=20, pady=(4, 12), fill="x")
        verify_btn = tk.Button(verify_frame, text="Verificar", bg=PANEL, fg=WHITE,
                               font=self.F["label"], bd=0, cursor="hand2",
                               activebackground=ACCENT2, activeforeground=BG,
                               command=self._verify_rut)
        verify_btn.pack(ipady=10, ipadx=26)
        
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
            self.rut_status_badge.config(text="✖ RUT no válido", fg=RED)
            return

        self.validated_rut = validation["rut_formatted"]
        self.status_label.config(text=f"✓ RUT válido: {self.validated_rut}", fg=GREEN)
        self.rut_status_badge.config(text=f"✓ RUT válido: {self.validated_rut}", fg=GREEN)
        self.after(600, self._show_main_interface)

    def _verify_rut(self):
        rut, error = self._get_rut_from_boxes()
        if error:
            self.status_label.config(text=error, fg=RED)
            self.rut_status_badge.config(text="✖ RUT no válido", fg=RED)
            return

        validation = validate_rut(rut)
        if not validation["valid"]:
            self.status_label.config(text=validation["error"], fg=RED)
            self.rut_status_badge.config(text="✖ RUT no válido", fg=RED)
            return

        self.status_label.config(text=f"✓ RUT válido: {validation['rut_formatted']}", fg=GREEN)
        self.rut_status_badge.config(text=f"✓ RUT válido: {validation['rut_formatted']}", fg=GREEN)

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

    def _update_rut_validation_badge(self):
        if not hasattr(self, 'rut_status_badge'):
            return
        rut, error = self._get_rut_from_boxes()
        if rut and not error:
            validation = validate_rut(rut)
            if validation["valid"]:
                self.rut_status_badge.config(text=f"✓ RUT válido: {validation['rut_formatted']}", fg=GREEN)
                self.status_label.config(text="", fg=GREEN)
            else:
                self.rut_status_badge.config(text="✖ RUT no válido", fg=RED)
                self.status_label.config(text=validation.get("error", "RUT inválido"), fg=RED)
        else:
            self.rut_status_badge.config(text="• RUT no validado", fg=GRAY)

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
        self.demo = _derive_demo_from_rut("12.345.678-9")
        self.rut_error = tk.StringVar(value="")
        self._build()

    def update_with_rut(self, rut_formatted: str):
        """Re-genera la vista usando datos derivados del RUT."""
        try:
            self.demo = _derive_demo_from_rut(rut_formatted)
            self.rut_var.set(self.demo["rut"])
            self.rut_error.set("")
            for ch in self.winfo_children():
                ch.destroy()
            self._build()
        except Exception:
            pass

    def _analyze_rut(self):
        rut = self.rut_var.get().strip()
        rut = self._clean_page_rut(rut)
        self.rut_var.set(rut)
        result = validate_rut(rut)
        if not result["valid"]:
            self.rut_error.set(result.get("error", "RUT inválido"))
            self.rut_error_label.config(fg=RED)
            return
        self.rut_error.set(f"✓ RUT válido: {result['rut_formatted']}")
        self.rut_error_label.config(fg=GREEN)
        self.update_with_rut(result["rut_formatted"])

    def _clean_page_rut(self, text: str) -> str:
        text = text.strip().upper()
        text = re.sub(r"[^0-9K-]", "", text)
        parts = text.split("-")
        main = parts[0] if parts else ""
        dv = parts[1] if len(parts) > 1 else ""
        main = re.sub(r"\D", "", main)[:8]
        dv = dv[:1].upper()
        if dv and dv not in "0123456789K":
            dv = ""
        if dv:
            return f"{main}-{dv}"
        return main

    def _sanitize_page_rut_input(self):
        cleaned = self._clean_page_rut(self.rut_var.get())
        if cleaned != self.rut_var.get():
            self.rut_var.set(cleaned)

    def _build(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=16, pady=12)
        
        # layout: sidebar izq | contenido der
        left = tk.Frame(root, bg=BG, width=340)
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
        e.bind("<Return>", lambda ev: self._analyze_rut())
        e.bind("<KeyRelease>", lambda ev: self._sanitize_page_rut_input())

        btn = tk.Button(entry_row, text="Analizar", bg=ACCENT, fg=WHITE,
                        font=self.F["small"], bd=0, cursor="hand2",
                        activebackground=ACCENT2, activeforeground=BG,
                        padx=10, pady=6, command=self._analyze_rut)
        btn.pack(side="left")
        
        self.rut_error_label = tk.Label(rut_card, textvariable=self.rut_error, bg=CARD,
                                        fg=GREEN, font=self.F["small"], anchor="w")
        self.rut_error_label.pack(fill="x", padx=12, pady=(4, 6))
        
        badge_row = tk.Frame(rut_card, bg=CARD)
        badge_row.pack(fill="x", padx=10, pady=(0, 10))
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
        """Dibujar gráfico con la cónica generada desde el RUT."""
        c = self.canvas_plot
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 10 or h < 10:
            return

        # Grid and axes
        padding = 20
        for i in range(-10, 11):
            x = padding + (w - 2 * padding) * (i + 10) / 20
            y = padding + (h - 2 * padding) * (i + 10) / 20
            c.create_line(x, padding, x, h - padding, fill=BORDER, width=0.5)
            c.create_line(padding, y, w - padding, y, fill=BORDER, width=0.5)

        c.create_line(padding, h // 2, w - padding, h // 2, fill=GRAY, width=1)
        c.create_line(w // 2, padding, w // 2, h - padding, fill=GRAY, width=1)
        c.create_text(w - padding, h // 2 - 12, text="x", fill=GRAY, font=self.F["small"])
        c.create_text(w // 2 + 12, padding + 4, text="y", fill=GRAY, font=self.F["small"])

        try:
            A = float(self.demo.get("A", 1.0))
            B = float(self.demo.get("B", 1.0))
            C = float(self.demo.get("C", 0.0))
            D = float(self.demo.get("D", 0.0))
            E = float(self.demo.get("E", 0.0))
        except Exception:
            A, B, C, D, E = 1.0, 1.0, 0.0, 0.0, 0.0

        hcen = -C / (2 * A)
        kcen = -D / (2 * B)
        constant = -E + A * hcen * hcen + B * kcen * kcen
        if abs(constant) < 0.5:
            constant = 1.2

        a2 = abs(constant / A)
        b2 = abs(constant / B)
        a = math.sqrt(max(a2, 0.1))
        b = math.sqrt(max(b2, 0.1))

        x_min = hcen - max(6, a * 1.8)
        x_max = hcen + max(6, a * 1.8)
        y_min = kcen - max(4, b * 1.8)
        y_max = kcen + max(4, b * 1.8)

        def px(value):
            return int(padding + (value - x_min) / (x_max - x_min) * (w - 2 * padding))

        def py(value):
            return int(h - padding - (value - y_min) / (y_max - y_min) * (h - 2 * padding))

        conic_type = self.demo.get("tipo", "Elipse")
        coords = []
        if conic_type == "Elipse":
            for deg in range(0, 361, 4):
                theta = math.radians(deg)
                x = hcen + a * math.cos(theta)
                y = kcen + b * math.sin(theta)
                coords.extend([px(x), py(y)])
            if len(coords) > 4:
                c.create_line(coords, fill=ACCENT, width=2, smooth=True)
        else:
            if A > 0:
                for branch in (-1, 1):
                    pts = []
                    for t in [i * 0.15 + 0.5 for i in range(40)]:
                        x = hcen + branch * a * math.cosh(t)
                        y = kcen + b * math.sinh(t)
                        if x_min <= x <= x_max and y_min <= y <= y_max:
                            pts.extend([px(x), py(y)])
                    if len(pts) > 4:
                        c.create_line(pts, fill=ACCENT, width=2, smooth=True)
            else:
                for branch in (-1, 1):
                    pts = []
                    for t in [i * 0.15 + 0.5 for i in range(40)]:
                        x = hcen + b * math.sinh(t)
                        y = kcen + branch * a * math.cosh(t)
                        if x_min <= x <= x_max and y_min <= y <= y_max:
                            pts.extend([px(x), py(y)])
                    if len(pts) > 4:
                        c.create_line(pts, fill=ACCENT, width=2, smooth=True)

        # Centro
        c.create_oval(px(hcen) - 4, py(kcen) - 4, px(hcen) + 4, py(kcen) + 4,
                      fill=ACCENT, outline="")
        c.create_text(px(hcen) + 12, py(kcen) - 12, text="C", fill=ACCENT2, font=self.F["small"])

        if conic_type == "Elipse":
            c_val = math.sqrt(abs(a * a - b * b))
            if a2 >= b2:
                foci = [(hcen - c_val, kcen), (hcen + c_val, kcen)]
                vertices = [(hcen - a, kcen), (hcen + a, kcen)]
            else:
                foci = [(hcen, kcen - c_val), (hcen, kcen + c_val)]
                vertices = [(hcen, kcen - a), (hcen, kcen + a)]
        else:
            c_val = math.sqrt(a * a + b * b)
            if A > 0:
                foci = [(hcen - c_val, kcen), (hcen + c_val, kcen)]
                vertices = [(hcen - a, kcen), (hcen + a, kcen)]
            else:
                foci = [(hcen, kcen - c_val), (hcen, kcen + c_val)]
                vertices = [(hcen, kcen - a), (hcen, kcen + a)]

        for fx, fy in foci:
            c.create_oval(px(fx) - 4, py(fy) - 4, px(fx) + 4, py(fy) + 4,
                          fill=YELLOW, outline="")
            c.create_text(px(fx), py(fy) - 12, text="F", fill=YELLOW, font=self.F["small"])

        for vx, vy in vertices:
            c.create_oval(px(vx) - 4, py(vy) - 4, px(vx) + 4, py(vy) + 4,
                          fill=GREEN, outline="")
            c.create_text(px(vx), py(vy) + 12, text="V", fill=GREEN, font=self.F["small"])

        # Leyenda
        items = [("━", ACCENT, conic_type),
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
        
        for title, pasos, details in [
            ("General → Canónica", self.demo["pasos_gen_can"], self.demo["pasos_gen_can_details"]),
            ("Canónica → General", self.demo["pasos_can_gen"], self.demo["pasos_can_gen_details"]),
        ]:
            tab = tk.Frame(nb, bg=CARD)
            nb.add(tab, text=title)

            scroll_canvas = tk.Canvas(tab, bg=CARD, bd=0, highlightthickness=0)
            scrollbar = tk.Scrollbar(tab, orient="vertical", command=scroll_canvas.yview)
            scroll_canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            scroll_canvas.pack(side="left", fill="both", expand=True)

            inner = tk.Frame(scroll_canvas, bg=CARD)
            scroll_canvas.create_window((0, 0), window=inner, anchor="nw")

            def _on_frame_config(event, canvas=scroll_canvas):
                canvas.configure(scrollregion=canvas.bbox("all"))

            inner.bind("<Configure>", _on_frame_config)

            for paso, detail in zip(pasos, details):
                row = tk.Frame(inner, bg=CARD, highlightbackground=ACCENT, highlightthickness=1)
                row.pack(fill="x", pady=6, padx=6)

                header = tk.Frame(row, bg=CARD)
                header.pack(fill="x", padx=8, pady=8)
                tk.Label(header, text=paso, bg=CARD, fg=WHITE,
                         font=self.F["mono_sm"], justify="left", anchor="w").pack(side="left", fill="x", expand=True)

                toggle_btn = tk.Button(header, text="▾ Desarrollo del paso", bg=PANEL,
                                       fg=WHITE, font=self.F["small"], bd=0, cursor="hand2",
                                       activebackground=ACCENT2, activeforeground=BG)
                toggle_btn.pack(side="right")

                detail_frame = tk.Frame(row, bg=PANEL)
                detail_label = tk.Label(detail_frame, text=detail, bg=PANEL, fg=WHITE,
                                        font=self.F["mono_sm"], justify="left", anchor="w",
                                        wraplength=760)
                detail_label.pack(fill="x", padx=10, pady=10)
                detail_frame.pack_forget()

                def _toggle(frame=detail_frame):
                    if frame.winfo_ismapped():
                        frame.pack_forget()
                    else:
                        frame.pack(fill="x", padx=8, pady=(0, 8))

                toggle_btn.config(command=_toggle)


# ═══════════════════════════════════════════════════════════════════════════════
#  PÁGINA 2 — FUNCIONES POR TRAMOS
# ═══════════════════════════════════════════════════════════════════════════════
class PageTramos(tk.Frame):
    def __init__(self, parent, F):
        super().__init__(parent, bg=BG)
        self.F = F
        self.demo_tramo = _derive_tramo_from_rut("12.345.678-9")
        self._build()

    def update_with_rut(self, rut_formatted: str):
        """Update demo_tramo based on provided RUT and rebuild UI."""
        try:
            self.demo_tramo = _derive_tramo_from_rut(rut_formatted)
            for ch in self.winfo_children():
                ch.destroy()
            self._build()
        except Exception:
            pass

    def _build(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=16, pady=12)
        
        left = tk.Frame(root, bg=BG, width=340)
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

        x_cut = self.demo_tramo.get("x_cut", 3)
        m1 = self.demo_tramo.get("left_slope", 1)
        b1 = self.demo_tramo.get("left_intercept", 1)
        m2 = self.demo_tramo.get("right_slope", 2)
        b2 = self.demo_tramo.get("right_intercept", 4)
        left_value = self.demo_tramo.get("left_value", 0)
        right_value = self.demo_tramo.get("right_value", 0)
        defined_at_cut = self.demo_tramo.get("defined_at_cut", True)

        padding = 30
        x_min = x_cut - 5
        x_max = x_cut + 7
        y_values = [m1 * x_min + b1, m1 * (x_cut - 0.5) + b1,
                    m2 * (x_cut + 0.5) + b2, m2 * x_max + b2,
                    left_value, right_value]
        y_min = min(y_values) - 3
        y_max = max(y_values) + 3

        def px(x_val):
            return int(padding + (x_val - x_min) / (x_max - x_min) * (w - 2 * padding))

        def py(y_val):
            return int(h - padding - (y_val - y_min) / (y_max - y_min) * (h - 2 * padding))

        # Grid
        for i in range(int(x_min), int(x_max) + 1):
            c.create_line(px(i), 0, px(i), h, fill=BORDER, width=0.5)
        for j in range(int(math.floor(y_min)), int(math.ceil(y_max)) + 1):
            c.create_line(0, py(j), w, py(j), fill=BORDER, width=0.5)

        # Ejes
        c.create_line(px(0), 0, px(0), h, fill=GRAY, width=1)
        c.create_line(0, py(0), w, py(0), fill=GRAY, width=1)

        for i in range(int(x_min), int(x_max) + 1, 2):
            c.create_text(px(i), py(0) + 14, text=str(i), fill=GRAY, font=self.F["small"])

        c.create_line(px(x_cut), 0, px(x_cut), h, fill=RED, dash=(6, 4), width=1)
        c.create_text(px(x_cut) + 10, padding + 12, text=f"x={x_cut}", fill=RED, font=self.F["small"])

        # Left branch
        left_pts = []
        for i in range(200):
            x = x_min + (x_cut - x_min) * i / 199
            y = m1 * x + b1
            if y_min <= y <= y_max:
                left_pts.extend([px(x), py(y)])
        if len(left_pts) > 4:
            c.create_line(left_pts, fill=GREEN, width=2, smooth=True)

        # Right branch
        right_pts = []
        for i in range(200):
            x = x_cut + (x_max - x_cut) * i / 199
            y = m2 * x + b2
            if y_min <= y <= y_max:
                right_pts.extend([px(x), py(y)])
        if len(right_pts) > 4:
            c.create_line(right_pts, fill=YELLOW, width=2, smooth=True)

        # Points at x_cut
        open_y = left_value
        solid_y = right_value if defined_at_cut else None
        c.create_oval(px(x_cut) - 5, py(open_y) - 5, px(x_cut) + 5, py(open_y) + 5,
                      outline=GREEN, fill=PLOT_BG, width=2)
        if defined_at_cut:
            c.create_oval(px(x_cut) - 5, py(solid_y) - 5, px(x_cut) + 5, py(solid_y) + 5,
                          fill=YELLOW, outline="")

        items = [("━", GREEN, f"x < {x_cut}  →  {m1}x {_signed_int(int(b1))}"),
                 ("━", YELLOW, f"x ≥ {x_cut}  →  {m2}x {_signed_int(int(b2))}"),
                 ("○", GREEN, "punto hueco" if not defined_at_cut else "límite izquierdo"),
                 ("●", YELLOW, "punto definido" if defined_at_cut else "límite derecho"),
                 ("┅", RED, f"x = {x_cut}  (discontinuidad)")]
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
        x_cut = self.demo_tramo.get("x_cut", 3)
        tk.Label(frame_t, text=f"Tabla de valores cercanos a x = {x_cut}", bg=CARD,
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
