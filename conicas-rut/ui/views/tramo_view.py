# conicas-rut/ui/views/tramo_view.py
import re
import tkinter as tk
from tkinter import Frame, Label, Entry

from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.card import CardFrame
from ui.components.step_display import StepContainer

from core.tramo_function import CrearVariables
from core.limit_analyzer import AnalizarLimites
from core.value_table import CrearTablaValores
from graphics.tramo_plotter import TramoPlotter


class TramoView(Frame):

    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._datos    = None
        self._analisis = None
        self._build()

    def _build(self):
        t = self.theme
        self.configure(bg=t.bg)
        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=1, minsize=500)
        self.columnconfigure(2, weight=1, minsize=380)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_center()
        self._build_right()

    # ── Columna izquierda ─────────────────────────────────────────────────

    def _build_left(self):
        t = self.theme
        self.left = PanelFrame(self, t, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")

        SectionHeader(self.left, "Función por tramos", t).pack(fill="x")

        # Punto crítico
        info_card = CardFrame(self.left, t, padx=12, pady=10)
        info_card.pack(fill="x", pady=(10, 0))
        for i, (name, attr) in enumerate([("a", "_a_val"), ("Tipo", "_tipo_val")]):
            info_card.columnconfigure(i, weight=1)
            col = Frame(info_card, bg=t.card)
            col.grid(row=0, column=i, sticky="ew", padx=(0, 8) if i == 0 else 0)
            Label(col, text=name, bg=t.card, fg=t.gray,
                  font=t.fonts["mono_sm"], anchor="center").pack(fill="x")
            lbl = Label(col, text="—", bg=t.card, fg=t.accent2,
                        font=t.fonts["mono"], anchor="center")
            lbl.pack(fill="x")
            setattr(self, attr, lbl)

        # Expresión de la función
        expr_card = CardFrame(self.left, t, padx=12, pady=10)
        expr_card.pack(fill="x", pady=(10, 0))
        Label(expr_card, text="Definición", bg=t.card, fg=t.gray,
              font=t.fonts["small"]).pack(anchor="w")
        self._expr_f1 = Label(expr_card, text="—", bg=t.card, fg=t.fg,
                               font=t.fonts["mono_sm"], anchor="w")
        self._expr_f1.pack(anchor="w", pady=(4, 0))
        self._expr_f2 = Label(expr_card, text="", bg=t.card, fg=t.gray,
                               font=t.fonts["mono_sm"], anchor="w")
        self._expr_f2.pack(anchor="w")

        # Tipo de discontinuidad destacado
        cls_card = CardFrame(self.left, t, padx=12, pady=10)
        cls_card.pack(fill="x", pady=(10, 0))
        Label(cls_card, text="Clasificación", bg=t.card, fg=t.gray,
              font=t.fonts["small"]).pack(anchor="w")
        self._cls_label = Label(cls_card, text="—", bg=t.card,
                                 fg=t.accent, font=t.fonts["head"])
        self._cls_label.pack(anchor="w", pady=(4, 0))

        # Regla aplicada
        SectionHeader(self.left, "Regla aplicada", t).pack(
            fill="x", pady=(16, 0))
        rule_card = CardFrame(self.left, t, padx=12, pady=10)
        rule_card.pack(fill="x", pady=(6, 0))
        self._rule_label = Label(
            rule_card, text="—", bg=t.card, fg=t.gray,
            font=t.fonts["small"], wraplength=1, justify="left", anchor="w")
        self._rule_label.pack(fill="x")
        self._rule_label.bind("<Configure>", lambda e: self._rule_label.configure(wraplength=e.width - 4))

        # Pasos
        SectionHeader(self.left, "Pasos — Generación", t).pack(
            fill="x", pady=(16, 0))
        self.step_container = StepContainer(self.left, t)
        self.step_container.pack(fill="both", expand=True, pady=(6, 0))

    # ── Columna centro ──────────────────────────────────────────

    def _build_center(self):
        t = self.theme
        self.center = PanelFrame(self, t, padx=8, pady=8)
        self.center.grid(row=0, column=1, sticky="nsew")
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)
        self.graph_panel = GraphPanel(
            self.center, t, title="Gráfico de función por tramos")
        self.graph_panel.grid(
            row=0, column=0, sticky="nsew", padx=6, pady=6)

    # ── Columna derecha ───────────────────────────

    def _build_right(self):
        t = self.theme
        self.right = PanelFrame(self, t, padx=12, pady=12)
        self.right.grid(row=0, column=2, sticky="nsew")

        # ── Tabla de valores ──────────────────────────────────────────────
        SectionHeader(self.right, "Tabla de valores", t).pack(fill="x")

        tbl_card = CardFrame(self.right, t, padx=8, pady=6)
        tbl_card.pack(fill="x", pady=(8, 0))
        tbl_card.columnconfigure(0, weight=1)
        tbl_card.columnconfigure(1, weight=1)
        tbl_card.columnconfigure(2, weight=1, minsize=100)

        # Encabezado fijo
        for col_i, txt in enumerate(["x", "f(x)", "Lado"]):
            Label(tbl_card, text=txt, bg=t.card, fg=t.gray,
                font=t.fonts["mono_sm"], anchor="center").grid(
                row=0, column=col_i, sticky="ew", padx=4, pady=(0, 4))

        Frame(tbl_card, bg=t.border, height=1).grid(
            row=1, column=0, columnspan=3, sticky="ew")

        self._table_body = tbl_card  # el body ES la misma card
        self._table_body_start_row = 2  # las filas de datos empiezan en row=2

        # ── Análisis de límites───────────────────────────
        SectionHeader(self.right, "Análisis de límites", t).pack(
            fill="x", pady=(14, 0))

        self._entries = {}
        self._add_field("Límite izquierdo   lím(x→a⁻)", "lim_izq")
        self._add_field("Límite derecho     lím(x→a⁺)", "lim_der")
        self._add_field("Conclusión — existencia del límite", "concl_limite")
        self._add_field("Valor  f(a)", "f_a")

        SectionHeader(self.right, "Continuidad", t).pack(
            fill="x", pady=(12, 0))

        self._add_field("Conclusión — continuidad en x = a", "concl_cont")
        self._add_field("Tipo de discontinuidad", "tipo_disc")
        self._add_field("Justificación escrita", "justif", tall=True)

        # Botón revelar
        tk.Button(
            self.right,
            text="Verificar respuestas",
            bg=t.panel, fg=t.gray,
            font=t.fonts["small"],
            bd=0, cursor="hand2",
            padx=10, pady=6,
            relief="flat",
            highlightbackground=t.border,
            highlightthickness=1,
            activebackground=t.card,
            activeforeground=t.fg,
            command=self._reveal_answers,
        ).pack(fill="x", pady=(10, 0))

    def _add_field(self, label_text, key, tall=False):
        """Añade un campo Entry vacío con su label encima."""
        t = self.theme
        card = CardFrame(self.right, t, padx=10, pady=8)
        card.pack(fill="x", pady=(5, 0))
        Label(card, text=label_text, bg=t.card, fg=t.gray,
              font=t.fonts["small"], anchor="w").pack(anchor="w")
        entry = Entry(
            card,
            bg=t.panel, fg=t.fg,
            insertbackground=t.fg,
            font=t.fonts["mono_sm"],
            bd=0, relief="flat",
            highlightbackground=t.border,
            highlightthickness=1,
            state="normal",
        )
        entry.pack(fill="x", ipady=7 if tall else 4, pady=(3, 0))
        self._entries[key] = entry

    def load_data(self, rut_result: dict):
        rut_data = rut_result["data"]

        self._datos    = CrearVariables(rut_data)
        self._analisis = AnalizarLimites(rut_data)
        tabla          = CrearTablaValores(
            self._datos["a"], self._datos["funcion"])

        self._populate_left()
        self._populate_steps()
        self._populate_table(tabla)
        self.after(50, self._render_graph)

    # ── Poblar columna izquierda ──────────────────────────────────────────

    def _populate_left(self):
        d = self._datos
        tipo_map = {
            "removible": "Removible",
            "salto":     "Salto",
            "infinita":  "Infinita",
        }
        self._a_val.config(text=str(d["a"]))
        self._tipo_val.config(text=tipo_map.get(d["tipo_discontinuidad"], "—"))
        self._cls_label.config(
            text="Discontinuidad " + tipo_map.get(d["tipo_discontinuidad"], "—"))

        # Expresión: dos líneas si f1 ≠ f2
        if d["expr_f1"] != d["expr_f2"]:
            self._expr_f1.config(text=f"f(x) = {d['expr_f1']}")
            self._expr_f2.config(text=f"       {d['expr_f2']}")
        else:
            self._expr_f1.config(text=f"f(x) = {d['expr_f1']}")
            self._expr_f2.config(text="")

        texto = d["explicacion"]
        oraciones = [s.strip() for s in re.split(r'[.;]+', texto) if s.strip()]
        texto_lista = "\n• " + "\n• ".join(oraciones)
        self._rule_label.config(text=texto_lista)

    # ── Poblar pasos ──────────────────────────────────────────────────────

    def _populate_steps(self):
        d  = self._datos
        an = self._analisis
        pasos = []
        for i, texto in enumerate(d["pasos_preliminares"]):
            pasos.append({"title": f"Paso {i + 1}", "explanation": texto})
        for i, linea in enumerate(an["desarrollo_algebraico"]):
            pasos.append({"title": f"Desarrollo {i + 1}", "explanation": linea})
        self.step_container.set_steps(pasos)

    # ── Poblar tabla de valores ───────────────────────────────────────────

    def _populate_table(self, tabla):
        t = self.theme
        # Limpiar solo las filas de datos (desde row 2 en adelante)
        for w in self._table_body.winfo_children():
            if int(w.grid_info().get("row", 0)) >= 2:
                w.destroy()

        rows = (
            [(r, "◀ izq") for r in tabla["izquierda"]] +
            [(r, "der ▶") for r in tabla["derecha"]]
        )

        for idx, (row, lado) in enumerate(rows):
            actual_row = idx + 2  # offset por encabezado y separador

            if idx == len(tabla["izquierda"]):
                Frame(self._table_body, bg=t.border, height=1).grid(
                    row=actual_row, column=0, columnspan=3, sticky="ew")
                actual_row += 1

            bg      = t.card if idx % 2 == 0 else t.panel
            x_str   = f"{row['x']:.2f}"
            y_str   = f"{row['y']:.2f}" if row["y"] is not None else "Indef."
            y_color = t.accent2 if row["y"] is not None else "#F87171"

            for col_i, (txt, fg) in enumerate([
                (x_str, t.gray),
                (y_str, y_color),
                (lado,  t.gray),
            ]):
                Label(self._table_body, text=txt, bg=bg, fg=fg,
                    font=t.fonts["mono_sm"], anchor="center").grid(
                    row=actual_row, column=col_i, sticky="ew", padx=4, pady=2)

    # ── Renderizado del gráfico ───────────────────────────────────────────

    def _render_graph(self):
        if not self._datos:
            return

        canvas = self.graph_panel.canvas
        canvas.update_idletasks()
        if canvas.winfo_width() < 10:
            self.after(100, self._render_graph)
            return

        canvas.delete("all")
        self.graph_panel.clear_placeholder()
        t      = self.theme
        d      = self._datos
        a      = d["a"]
        tramos = d["funcion_tramos"]
        tipo   = d["tipo_discontinuidad"]

        x_min, x_max = a - 6, a + 6
        y_min, y_max = -15, 15

        plotter = TramoPlotter(canvas, t)
        plotter.plot_piecewise(tramos, x_min, x_max, y_min, y_max)

        from graphics.canvas_utils import CoordinateTransform, ShapeDrawer
        transform = CoordinateTransform(
            canvas.winfo_width(), canvas.winfo_height(),
            x_min, x_max, y_min, y_max,
        )
        red = "#F87171"

        if tipo == "removible":
            lim_val = self._analisis["lim_izquierdo"]
            if lim_val is not None:
                ShapeDrawer.draw_hole(canvas, transform, a, lim_val,
                                      color=red, size=6)

        elif tipo == "salto":
            lim_izq = self._analisis["lim_izquierdo"]
            lim_der = self._analisis["lim_derecho"]
            if lim_izq is not None:
                ShapeDrawer.draw_hole(canvas, transform, a, lim_izq,
                                      color=red, size=5)
            if lim_der is not None:
                ShapeDrawer.draw_point(canvas, transform, a, lim_der,
                                       color=t.accent2, size=5,
                                       label=f"f({a})", theme=t)

        elif tipo == "infinita":
            x_c, _ = transform.math_to_canvas(a, 0)
            canvas.create_line(
                x_c, 0, x_c, canvas.winfo_height(),
                fill=red, dash=(5, 4), width=2, tags="asymptote")
            canvas.create_text(
                x_c + 6, 16, text=f"x = {a}",
                fill=red, font=t.fonts["small"],
                anchor="w", tags="labels")

    # ── Revelar respuestas ────────────────────────────────────────────────

    def _reveal_answers(self):
        if not self._analisis:
            return
        an = self._analisis

        def _set(key, value):
            e = self._entries.get(key)
            if not e:
                return
            e.delete(0, "end")
            e.insert(0, str(value) if value is not None else "No definido")

        lim_izq = an["lim_izquierdo"]
        lim_der = an["lim_derecho"]
        _set("lim_izq",    lim_izq  if lim_izq is not None else "±∞")
        _set("lim_der",    lim_der  if lim_der is not None else "±∞")
        _set("concl_limite",  an["conclusion_limite"])
        _set("f_a",
             an["valor_en_punto"] if an["valor_en_punto"] is not None
             else "No definido")
        _set("concl_cont",    an["conclusion_continuidad"])
        _set("tipo_disc",     an["clasificacion_discontinuidad"])
        _set("justif",        an["justificacion"])

    # ── Tema ──────────────────────────────────────────────────────────────

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.bg)
        self.left.update_theme(theme)
        self.center.update_theme(theme)
        self.right.update_theme(theme)
        self.graph_panel.update_theme(theme)
        self.step_container.update_theme(theme)