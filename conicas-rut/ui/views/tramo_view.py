# conicas-rut/ui/views/tramo_view.py

import tkinter as tk

from core.limites.limit_analyzer import AnalizarLimites
from core.limites.limit_elements import (
    build_limit_answer_values,
    build_limit_generation_steps,
    build_rule_bullets,
    build_value_table_rows,
    format_value,
)
from core.limites.tramo_function import CrearVariables
from graphics.limites.limit_elements_plotter import LimitElementsPlotter
from graphics.limites.tramo_plotter import TramoPlotter
from ui.components.card import CardFrame
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.limit_element_inputs import LimitElementsInput
from ui.components.panel import PanelFrame
from ui.components.step_display import StepContainer


class TramoView(tk.Frame):
    """Vista para mostrar función por tramos, límites laterales y continuidad."""

    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._datos = None
        self._analisis = None
        self._build()

    # ── Construcción UI ────────────────────────────────────────────────────

    def _build(self):
        """Construye la distribución principal de la vista."""
        t = self.theme
        self.configure(bg=t.bg)

        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=1, minsize=500)
        self.columnconfigure(2, weight=1, minsize=380)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_center()
        self._build_right()

    def _build_left(self):
        """Construye el panel izquierdo con definición, regla aplicada y pasos."""
        t = self.theme
        self.left = PanelFrame(self, t, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")

        SectionHeader(self.left, "Función por tramos", t).pack(fill="x")
        self._build_info_card()
        self._build_expression_card()

        SectionHeader(self.left, "Regla aplicada", t).pack(fill="x", pady=(16, 0))
        self._build_rule_card()

        SectionHeader(self.left, "Pasos — Generación", t).pack(fill="x", pady=(16, 0))
        self.step_container = StepContainer(self.left, t)
        self.step_container.pack(fill="both", expand=True, pady=(6, 0))

    def _build_info_card(self):
        """Construye la tarjeta con el punto crítico y el tipo de discontinuidad."""
        t = self.theme
        card = CardFrame(self.left, t, padx=12, pady=10)
        card.pack(fill="x", pady=(10, 0))
        self._info_labels = {}

        for i, (title, key) in enumerate([("a", "a"), ("Tipo", "tipo")]):
            card.columnconfigure(i, weight=1)

            col = tk.Frame(card, bg=t.card)
            col.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=(0, 8) if i == 0 else 0,
            )

            self._label(
                col,
                title,
                t.card,
                t.gray,
                t.fonts["mono_sm"],
                anchor="center",
            ).pack(fill="x")

            lbl = self._label(
                col,
                "—",
                t.card,
                t.accent2,
                t.fonts["mono"],
                anchor="center",
            )
            lbl.pack(fill="x")

            self._info_labels[key] = lbl

    def _build_expression_card(self):
        """Construye la tarjeta con la definición de la función."""
        t = self.theme
        card = CardFrame(self.left, t, padx=12, pady=10)
        card.pack(fill="x", pady=(10, 0))

        self._label(
            card,
            "Definición",
            t.card,
            t.gray,
            t.fonts["small"],
        ).pack(anchor="w")

        self._expr_f1 = self._label(
            card,
            "—",
            t.card,
            t.fg,
            t.fonts["mono_sm"],
            anchor="w",
            justify="left",
            wraplength=1,
        )

        self._expr_f2 = self._label(
            card,
            "",
            t.card,
            t.gray,
            t.fonts["mono_sm"],
            anchor="w",
            justify="left",
            wraplength=1,
        )

        self._expr_f1.pack(fill="x", pady=(4, 0))
        self._expr_f2.pack(fill="x")

        self._expr_f1.bind(
            "<Configure>",
            lambda e: self._expr_f1.configure(wraplength=max(e.width - 4, 40)),
        )
        self._expr_f2.bind(
            "<Configure>",
            lambda e: self._expr_f2.configure(wraplength=max(e.width - 4, 40)),
        )

    def _build_rule_card(self):
        """Construye la tarjeta que resume la regla aplicada desde el RUT."""
        t = self.theme
        card = CardFrame(self.left, t, padx=12, pady=10)
        card.pack(fill="x", pady=(6, 0))

        self._rule_label = self._label(
            card,
            "—",
            t.card,
            t.gray,
            t.fonts["small"],
            anchor="w",
            justify="left",
            wraplength=1,
        )
        self._rule_label.pack(fill="x")
        self._rule_label.bind(
            "<Configure>",
            lambda e: self._rule_label.configure(wraplength=max(e.width - 4, 40)),
        )

    def _build_center(self):
        """Construye el panel central con el gráfico de la función."""
        t = self.theme
        self.center = PanelFrame(self, t, padx=8, pady=8)
        self.center.grid(row=0, column=1, sticky="nsew")
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)

        self.graph_panel = GraphPanel(self.center, t, title="Gráfico de función por tramos")
        self.graph_panel.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.graph_panel.set_resize_callback(self._render_graph)

    def _build_right(self):
        """Construye el panel derecho con tabla de valores y respuestas."""
        t = self.theme
        self.right = PanelFrame(self, t, padx=12, pady=12)
        self.right.grid(row=0, column=2, sticky="nsew")

        SectionHeader(self.right, "Tabla de valores", t).pack(fill="x")
        self._build_table()

        self.answers_input = LimitElementsInput(self.right, t)
        self.answers_input.pack(fill="x")

        self._build_answer_buttons()

    def _build_table(self):
        """Construye la estructura base de la tabla de valores."""
        t = self.theme
        self._table_card = CardFrame(self.right, t, padx=8, pady=6)
        self._table_card.pack(fill="x", pady=(8, 0))

        for col in range(3):
            self._table_card.columnconfigure(col, weight=1)

        for col, text in enumerate(["x", "f(x)", "Lado"]):
            self._label(
                self._table_card,
                text,
                t.card,
                t.gray,
                t.fonts["mono_sm"],
                anchor="center",
            ).grid(row=0, column=col, sticky="ew", padx=4, pady=(0, 4))

        tk.Frame(
            self._table_card,
            bg=t.border,
            height=1,
        ).grid(row=1, column=0, columnspan=3, sticky="ew")

    def _build_answer_buttons(self):
        """Construye botones para revelar y limpiar respuestas."""
        t = self.theme
        row = tk.Frame(self.right, bg=t.panel)
        row.pack(fill="x", pady=(10, 0))

        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=1)

        self._button(row, "Verificar respuestas", self._reveal_answers).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 4),
        )

        self._button(row, "Limpiar", self.answers_input.clear_values).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(4, 0),
        )

    # ── Carga de datos ─────────────────────────────────────────────────────

    def load_data(self, rut_result: dict):
        """Genera la función por tramos, analiza límites y actualiza la vista."""
        self._datos = CrearVariables(rut_result)
        self._analisis = AnalizarLimites(rut_result)

        self._populate_left()
        self._populate_steps()
        self._populate_table()

        self.answers_input.clear_values()
        self.after(50, self._render_graph)

    def _populate_left(self):
        """Rellena datos principales del panel izquierdo."""
        d = self._datos
        tipo_map = {
            "removible": "Removible",
            "salto": "Salto",
            "infinita": "Infinita",
        }

        self._info_labels["a"].config(text=str(d["a"]))
        self._info_labels["tipo"].config(
            text=tipo_map.get(d["tipo_discontinuidad"], "—")
        )

        self._expr_f1.config(text=f"f(x) = {d['expr_f1']}")
        self._expr_f2.config(
            text=f"       {d['expr_f2']}" if d["expr_f1"] != d["expr_f2"] else ""
        )
        self._rule_label.config(text=build_rule_bullets(d.get("explicacion", "")))

    def _populate_steps(self):
        """Carga pasos de generación y desarrollo algebraico."""
        steps = build_limit_generation_steps(self._datos, self._analisis)
        self.step_container.set_steps(self._steps_without_direct_results(steps))

    def _populate_table(self):
        """Rellena la tabla de aproximación lateral."""
        t = self.theme

        for widget in self._table_card.winfo_children():
            if int(widget.grid_info().get("row", 0)) >= 2:
                widget.destroy()

        current_row = 2

        for item in build_value_table_rows(self._analisis):
            if item.get("separator_before"):
                tk.Frame(
                    self._table_card,
                    bg=t.border,
                    height=1,
                ).grid(
                    row=current_row,
                    column=0,
                    columnspan=3,
                    sticky="ew",
                    pady=(2, 2),
                )
                current_row += 1

            bg = t.card if current_row % 2 == 0 else t.panel
            y_text = format_value(item["y"], undefined="Indef.")
            y_color = t.accent2 if item["y"] is not None else t.red

            values = [
                (format_value(item["x"]), t.gray),
                (y_text, y_color),
                (item["lado"], t.gray),
            ]

            for col, (text, color) in enumerate(values):
                self._label(
                    self._table_card,
                    text,
                    bg,
                    color,
                    t.fonts["mono_sm"],
                    anchor="center",
                ).grid(row=current_row, column=col, sticky="ew", padx=4, pady=2)

            current_row += 1

    # ── Gráfico ────────────────────────────────────────────────────────────

    def _render_graph(self):
        """Grafica la función por tramos y los elementos de discontinuidad."""
        if not self._datos:
            return

        canvas = self.graph_panel.canvas
        canvas.update_idletasks()

        if canvas.winfo_width() < 10:
            self.after(100, self._render_graph)
            return

        d = self._datos
        a = d["a"]

        self.graph_panel.clear_graph()

        plotter = TramoPlotter(canvas, self.theme)
        transform = plotter.plot_piecewise(
            d["funcion_tramos"],
            a - 6,
            a + 6,
            -15,
            15,
        )

        if transform:
            LimitElementsPlotter(canvas, self.theme).plot_from_analysis(
                d,
                self._analisis,
                transform,
            )

    # ── Respuestas ─────────────────────────────────────────────────────────

    def _reveal_answers(self):
        """Muestra los resultados correctos del análisis de límites."""
        if not self._analisis:
            return

        self.answers_input.set_values(build_limit_answer_values(self._analisis))

    # ── Helpers y tema ─────────────────────────────────────────────────────

    def _label(self, parent, text, bg, fg, font, **kwargs):
        """Crea una etiqueta estándar de la vista."""
        return tk.Label(parent, text=text, bg=bg, fg=fg, font=font, **kwargs)

    def _button(self, parent, text, command):
        """Crea un botón estándar de la vista."""
        t = self.theme

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=t.panel,
            fg=t.gray,
            font=t.fonts["small"],
            bd=0,
            cursor="hand2",
            padx=10,
            pady=6,
            relief="flat",
            highlightbackground=t.border,
            highlightthickness=1,
            activebackground=t.card,
            activeforeground=t.fg,
        )

    def _steps_without_direct_results(self, steps: list) -> list:
        """
        Las respuestas finales siguen disponibles solo en el botón
        'Verificar respuestas'.
        """
        cleaned = []

        for step in steps:
            if isinstance(step, dict):
                new_step = dict(step)
                new_step.pop("result", None)
                cleaned.append(new_step)
            else:
                cleaned.append(step)

        return cleaned

    def update_theme(self, theme):
        """Actualiza referencias de tema en la vista y sus componentes."""
        self.theme = theme
        self.configure(bg=theme.bg)

        for panel in [
            self.left,
            self.center,
            self.right,
            self.graph_panel,
            self.step_container,
            self.answers_input,
        ]:
            panel.update_theme(theme)