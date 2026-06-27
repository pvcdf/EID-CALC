# conicas-rut/ui/views/conic_view.py

import re
import tkinter as tk

from core.conicas.conic_elements import build_conic_elements, get_ellipse_orientation
from core.conicas.conic_pipeline import run_pipeline
from graphics.conicas.conic_elements_plotter import ConicElementsPlotter
from graphics.conicas.conic_plotter import ConicPlotter
from ui.components.card import CardFrame
from ui.components.conic_element_inputs import ConicElementsInput
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.step_display import StepContainer


class ConicView(tk.Frame):
    """Vista principal para mostrar coeficientes, forma canónica, gráfica y elementos de cónicas."""

    def __init__(self, master, theme, pipeline: dict = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self.pipeline = pipeline or {}
        self._conic_type = None
        self._active_tab = "general_canonical"
        self._elements_visible = False
        self._attempt_data = None
        self._attempt_error = None

        self._build()

        if pipeline and pipeline.get("valid"):
            self._load_pipeline(pipeline)

    # ── Construcción UI ────────────────────────────────────────────────────

    def _build(self):
        """Construye la distribución principal de la vista."""
        t = self.theme
        self.configure(bg=t.bg)

        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=1, minsize=500)
        self.columnconfigure(2, weight=0, minsize=330)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_center()
        self._build_right()

    def _build_left(self):
        """Construye el panel izquierdo con coeficientes, ecuación general y pasos."""
        t = self.theme
        self.left = PanelFrame(self, t, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")

        SectionHeader(self.left, "Coeficientes generados", t).pack(fill="x")
        self._build_coefficients_card()
        self._build_equation_card()
        self._build_type_card()

        SectionHeader(self.left, "Pasos — Coeficientes", t).pack(fill="x", pady=(16, 0))
        self.coef_steps = StepContainer(self.left, t)
        self.coef_steps.pack(fill="both", expand=True, pady=(6, 0))

    def _build_coefficients_card(self):
        """Construye la tarjeta que muestra A, B, C, D y E."""
        t = self.theme
        card = CardFrame(self.left, t, padx=12, pady=10)
        card.pack(fill="x", pady=(10, 0))
        self._coef_labels = {}

        for i, name in enumerate(["A", "B", "C", "D", "E"]):
            card.columnconfigure(i, weight=1)

            col = tk.Frame(card, bg=t.card)
            col.grid(row=0, column=i, sticky="ew")

            self._label(
                col,
                name,
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

            self._coef_labels[name] = lbl

    def _build_equation_card(self):
        """Construye la tarjeta de ecuación general."""
        t = self.theme
        card = CardFrame(self.left, t, padx=12, pady=10)
        card.pack(fill="x", pady=(10, 0))

        self._label(
            card,
            "Ecuación general",
            t.card,
            t.gray,
            t.fonts["small"],
        ).pack(anchor="w")

        self._eq_label = self._label(
            card,
            "—",
            t.card,
            t.fg,
            t.fonts["mono_sm"],
            anchor="w",
            justify="left",
            wraplength=1,
        )
        self._eq_label.pack(fill="x", pady=(4, 0))
        self._eq_label.bind(
            "<Configure>",
            lambda e: self._eq_label.configure(wraplength=max(e.width - 4, 40)),
        )

    def _build_type_card(self):
        """Construye la tarjeta que muestra el tipo de cónica."""
        t = self.theme
        card = CardFrame(self.left, t, padx=12, pady=10)
        card.pack(fill="x", pady=(10, 0))

        self._label(
            card,
            "Tipo de cónica",
            t.card,
            t.gray,
            t.fonts["small"],
        ).pack(anchor="w")

        self._type_label = self._label(
            card,
            "—",
            t.card,
            t.accent,
            t.fonts["head"],
        )
        self._type_label.pack(anchor="w", pady=(4, 0))

    def _build_center(self):
        """Construye el panel central con el canvas de la gráfica."""
        t = self.theme
        self.center = PanelFrame(self, t, padx=8, pady=8)
        self.center.grid(row=0, column=1, sticky="nsew")
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)

        self.graph_panel = GraphPanel(self.center, t, title="Gráfico de cónica")
        self.graph_panel.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.graph_panel.set_resize_callback(self._render_graph)

    def _build_right(self):
        """Construye el panel derecho con forma canónica, elementos y pasos."""
        t = self.theme
        self.right = PanelFrame(self, t, padx=12, pady=12)
        self.right.grid(row=0, column=2, sticky="nsew")

        SectionHeader(self.right, "Forma canónica", t).pack(fill="x")
        self._build_canonical_card()

        self.elements_input = ConicElementsInput(self.right, t)
        self.elements_input.pack(fill="x", pady=(10, 0))

        self._build_element_buttons()
        self._build_tab_switcher()

        self._steps_frame = tk.Frame(self.right, bg=t.panel)
        self._steps_frame.pack(fill="both", expand=True, pady=(6, 0))
        self._steps_frame.rowconfigure(0, weight=1)
        self._steps_frame.columnconfigure(0, weight=1)

        self.canon_steps = StepContainer(self._steps_frame, t)
        self.general_steps = StepContainer(self._steps_frame, t)

        self.canon_steps.grid(row=0, column=0, sticky="nsew")
        self.general_steps.grid(row=0, column=0, sticky="nsew")

        self._show_tab("general_canonical")

    def _build_canonical_card(self):
        """Construye la tarjeta que muestra la forma canónica."""
        t = self.theme
        card = CardFrame(self.right, t, padx=12, pady=10)
        card.pack(fill="x", pady=(10, 0))

        self._label(
            card,
            "Ecuación canónica",
            t.card,
            t.gray,
            t.fonts["small"],
        ).pack(anchor="w")

        self._canonical_label = self._label(
            card,
            "—",
            t.card,
            t.accent2,
            t.fonts["mono_sm"],
            anchor="w",
            justify="left",
            wraplength=1,
        )
        self._canonical_label.pack(fill="x", pady=(4, 0))
        self._canonical_label.bind(
            "<Configure>",
            lambda e: self._canonical_label.configure(wraplength=max(e.width - 4, 40)),
        )

    def _build_element_buttons(self):
        """Construye botones para revelar, graficar intento y limpiar elementos."""
        t = self.theme
        row = tk.Frame(self.right, bg=t.panel)
        row.pack(fill="x", pady=(6, 0))

        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=1)
        row.columnconfigure(2, weight=1)

        self._button(row, "Mostrar elementos", self._reveal_elements).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 4),
        )

        self._button(row, "Graficar intento", self._plot_attempt).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=4,
        )

        self._button(row, "Limpiar", self._clear_elements).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(4, 0),
        )

    def _build_tab_switcher(self):
        """Construye pestañas para alternar entre pasos de transformación."""
        t = self.theme
        switcher = tk.Frame(self.right, bg=t.panel)
        switcher.pack(fill="x", pady=(12, 0))

        tk.Frame(switcher, bg=t.border, height=1).pack(fill="x")

        tabs_row = tk.Frame(switcher, bg=t.panel)
        tabs_row.pack(fill="x")
        self._tab_btns = {}

        for key, text in [
            ("general_canonical", "General → Canónica"),
            ("canonical_general", "Canónica → General"),
        ]:
            btn = self._button(
                tabs_row,
                text,
                lambda k=key: self._show_tab(k),
                padx=10,
                pady=6,
            )
            btn.pack(side="left", fill="x", expand=True)
            self._tab_btns[key] = btn

        tk.Frame(switcher, bg=t.border, height=1).pack(fill="x")

    # ── Carga de datos ─────────────────────────────────────────────────────

    def load_data(self, rut_result: dict):
        """Carga datos desde un RUT validado o desde un pipeline ya calculado."""
        if self.pipeline and self.pipeline.get("valid"):
            self._load_pipeline(self.pipeline)
            return

        self.pipeline = run_pipeline(rut_result)

        if self.pipeline.get("valid"):
            self._load_pipeline(self.pipeline)
        else:
            self._show_generic_error(self.pipeline.get("error", "Error desconocido."))

    def _load_pipeline(self, pipeline: dict):
        """Carga en la vista los resultados del pipeline de cónicas."""
        coefs = pipeline["coefs"]["data"]
        classifier = pipeline["classifier"]
        transform = pipeline.get("transform", {})
        transform_data = transform.get("data", {})

        self._conic_type = classifier["conic_type"]
        self._elements_visible = False

        for name in ["A", "B", "C", "D", "E"]:
            self._coef_labels[name].config(text=self._fmt(coefs[name]))

        self._eq_label.config(text=coefs.get("equation_str", "—"))
        self._type_label.config(text=classifier["data"].get("conic_name_es", "—"))
        self._canonical_label.config(text=transform_data.get("canonical_form", "—"))

        self.coef_steps.set_steps(pipeline["coefs"].get("steps", []))
        self.canon_steps.set_steps(self._steps_without_direct_results(transform.get("steps", [])))
        self.general_steps.set_steps(
            self._steps_without_direct_results((pipeline.get("to_general") or {}).get("steps", []))
        )

        if transform.get("valid"):
            self.elements_input.set_conic_type(self._conic_type)
            self._attempt_data = None
            self._attempt_error = None
            self.after(50, self._render_graph)
            return

        if transform_data.get("imaginary"):
            self.elements_input.show_message("Sin elementos reales\n(cónica imaginaria)")
            self.after(
                50,
                lambda: self._show_imaginary_notice(self._conic_type, transform_data),
            )
            return

        self.elements_input.show_message("No se pudieron calcular elementos.")
        self.after(
            50,
            lambda: self._show_generic_error(
                transform.get("error", "No se pudo transformar la cónica.")
            ),
        )

    # ── Gráfico ────────────────────────────────────────────────────────────

    def _render_graph(self):
        """Renderiza la curva real, los elementos reales y el intento del usuario."""
        canvas = self.graph_panel.canvas
        canvas.update_idletasks()

        if canvas.winfo_width() < 10:
            self.after(100, self._render_graph)
            return

        self.graph_panel.clear_graph()

        plotter = ConicPlotter(canvas, self.theme)
        actual_transform = None

        if self.pipeline and self.pipeline.get("valid"):
            transform = self.pipeline.get("transform", {})

            if transform.get("valid"):
                actual_transform = self._plot_curve(plotter, transform["data"])

        attempt_transform = None

        if self._attempt_data is not None:
            attempt_transform = self._plot_attempt_curve(plotter, self._attempt_data)

        if actual_transform and self._elements_visible:
            ConicElementsPlotter(canvas, self.theme).plot_from_transform(
                self._conic_type,
                self.pipeline["transform"]["data"],
                actual_transform,
            )

        if attempt_transform:
            ConicElementsPlotter(canvas, self.theme).plot_attempt_elements(
                self._conic_type,
                self._attempt_data,
                attempt_transform,
            )

        elif self._attempt_error:
            canvas.create_text(
                canvas.winfo_width() / 2,
                canvas.winfo_height() - 24,
                text=self._attempt_error,
                fill=self.theme.red,
                font=self.theme.fonts["small"],
                tags="labels",
                anchor="s",
                justify="center",
            )

    def _plot_curve(self, plotter: ConicPlotter, data: dict):
        """Grafica la curva real según el tipo de cónica."""
        ct = self._conic_type

        if ct == "circle":
            return plotter.plot_circle(
                radius=data["radius"],
                h=data["center"][0],
                k=data["center"][1],
            )

        if ct == "ellipse":
            return plotter.plot_ellipse(
                a=data["a"],
                b=data["b"],
                h=data["center"][0],
                k=data["center"][1],
                major_axis=get_ellipse_orientation(data),
            )

        if ct == "hyperbola":
            return plotter.plot_hyperbola(
                a=data["a"],
                b=data["b"],
                h=data["center"][0],
                k=data["center"][1],
                orientation=data.get("orientation", "horizontal"),
            )

        if ct == "parabola":
            return plotter.plot_parabola(
                p=data["p"],
                h=data["vertex"][0],
                k=data["vertex"][1],
                orientation=data.get("orientation", "vertical"),
            )

        return None

    def _plot_attempt_curve(self, plotter: ConicPlotter, data: dict):
        """Grafica con línea segmentada los valores ingresados por el usuario."""
        ct = self._conic_type
        clear_flag = not (self.pipeline and self.pipeline.get("valid"))

        if ct == "circle":
            return plotter.plot_circle(
                radius=data["radius"],
                h=data["center"][0],
                k=data["center"][1],
                clear=clear_flag,
                dash=(4, 4),
                tag="attempt",
            )

        if ct == "ellipse":
            return plotter.plot_ellipse(
                a=data["a"],
                b=data["b"],
                h=data["center"][0],
                k=data["center"][1],
                major_axis=data.get("orientation", "horizontal"),
                clear=clear_flag,
                dash=(4, 4),
                tag="attempt",
            )

        if ct == "hyperbola":
            return plotter.plot_hyperbola(
                a=data["a"],
                b=data["b"],
                h=data["center"][0],
                k=data["center"][1],
                orientation=data.get("orientation", "horizontal"),
                clear=clear_flag,
                dash=(4, 4),
                tag="attempt",
            )

        if ct == "parabola":
            return plotter.plot_parabola(
                p=data["p"],
                h=data["vertex"][0],
                k=data["vertex"][1],
                orientation=data.get("orientation", "vertical"),
                clear=clear_flag,
                dash=(4, 4),
                tag="attempt",
            )

        return None

    # ── Intento de elementos ingresados ────────────────────────────────────

    def _plot_attempt(self):
        """Lee los campos manuales y grafica un intento de cónica."""
        if not self._conic_type:
            return

        values = self.elements_input.get_values()
        self._attempt_data, self._attempt_error = self._build_attempt_data(values)
        self._render_graph()

    def _build_attempt_data(self, values: dict):
        """Convierte los campos escritos por el usuario en datos graficables."""
        conic_type = self._conic_type

        if conic_type == "circle":
            center = self._parse_point(values.get("centro", ""))
            radius = self._parse_number(values.get("radio", ""))

            if center is None:
                return None, "Centro inválido. Usa formato (x, y)."

            if radius is None:
                return None, "Radio inválido. Ingresa un número."

            return {"center": center, "radius": radius}, None

        if conic_type in ("ellipse", "hyperbola"):
            center = self._parse_point(values.get("centro", ""))
            a = self._parse_number(values.get("a", ""))
            b = self._parse_number(values.get("b", ""))
            orientation = self._parse_orientation(values.get("orientacion", ""))

            if center is None:
                return None, "Centro inválido. Usa formato (x, y)."

            if a is None or b is None:
                return None, "a o b inválidos. Ingresa números válidos."

            return {
                "center": center,
                "a": a,
                "b": b,
                "orientation": orientation,
            }, None

        if conic_type == "parabola":
            vertex = self._parse_point(values.get("vertice", ""))
            orientation = self._parse_orientation(values.get("orientacion", ""))

            if vertex is None:
                return None, "Vértice inválido. Usa formato (x, y)."

            p = None
            focus = self._parse_point(values.get("foco", ""))
            directrix_value = self._parse_directrix(
                values.get("directriz", ""),
                orientation,
            )

            if focus is not None:
                if orientation == "vertical":
                    p = focus[1] - vertex[1]
                else:
                    p = focus[0] - vertex[0]

            elif directrix_value is not None:
                if orientation == "vertical":
                    p = vertex[1] - directrix_value
                else:
                    p = vertex[0] - directrix_value

            if p is None:
                return None, "No se pudo obtener p. Ingresa foco o directriz válidos."

            if p == 0:
                return None, "p no puede ser 0 para graficar la parábola."

            return {
                "vertex": vertex,
                "p": p,
                "orientation": orientation,
            }, None

        return None, "Tipo de cónica desconocido."

    # ── Parsers de entrada manual ──────────────────────────────────────────

    def _parse_number(self, text: str):
        """Convierte texto a número decimal."""
        if not isinstance(text, str):
            return None

        value = text.strip()

        if not value:
            return None

        try:
            return float(value)
        except ValueError:
            return None

    def _parse_point(self, text: str):
        """Convierte texto con formato (x, y) a una tupla numérica."""
        if not isinstance(text, str):
            return None

        value = text.strip()

        if not value:
            return None

        match = re.match(
            r"^\s*\(?\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*,\s*"
            r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*\)?\s*$",
            value,
        )

        if not match:
            return None

        try:
            x = float(match.group(1))
            y = float(match.group(2))

            return (x, y)

        except ValueError:
            return None

    def _parse_orientation(self, text: str):
        """Interpreta orientación horizontal o vertical desde texto."""
        if not isinstance(text, str):
            return "horizontal"

        value = text.strip().lower()

        if value.startswith("vert") or value == "v":
            return "vertical"

        if value.startswith("horiz") or value == "h":
            return "horizontal"

        return "horizontal"

    def _parse_directrix(self, text: str, orientation: str):
        """Lee una directriz con formato x = n o y = n según la orientación."""
        if not isinstance(text, str):
            return None

        value = text.strip().lower()

        if not value:
            return None

        pattern = r"^(x|y)\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)$"
        match = re.match(pattern, value)

        if not match:
            return None

        axis = match.group(1)
        number = float(match.group(2))

        if orientation == "vertical" and axis != "y":
            return None

        if orientation == "horizontal" and axis != "x":
            return None

        return number

    # ── Mensajes de gráfico ────────────────────────────────────────────────

    def _show_imaginary_notice(self, conic_type: str, transform_data: dict):
        """Muestra aviso cuando la cónica no tiene puntos reales."""
        t = self.theme

        self.graph_panel.clear_graph()

        canvas = self.graph_panel.canvas
        canvas.update_idletasks()

        w = max(canvas.winfo_width(), 500)
        h_mid = max(canvas.winfo_height(), 400) // 2

        title = {
            "circle": "Circunferencia imaginaria",
            "ellipse": "Elipse imaginaria",
        }.get(conic_type, "Cónica imaginaria")

        canvas.create_text(
            w // 2,
            h_mid - 30,
            text=title,
            fill=t.accent,
            font=t.fonts["head"],
            justify="center",
        )

        canvas.create_text(
            w // 2,
            h_mid + 10,
            text="Esta ecuación no tiene puntos reales.",
            fill=t.fg,
            font=t.fonts["small"],
            justify="center",
        )

        detail = self._imaginary_detail(conic_type, transform_data)

        if detail:
            canvas.create_text(
                w // 2,
                h_mid + 42,
                text=detail,
                fill=t.gray,
                font=t.fonts["mono_sm"],
                justify="center",
            )

    def _imaginary_detail(self, conic_type: str, data: dict) -> str:
        """Genera detalle matemático breve para cónicas imaginarias."""
        if conic_type == "circle" and data.get("radius_squared") is not None:
            return f"r² = {data['radius_squared']} < 0  →  sin radio real"

        if conic_type == "ellipse":
            a2 = data.get("a2", data.get("x_radius_squared"))
            b2 = data.get("b2", data.get("y_radius_squared"))

            if a2 is not None and b2 is not None:
                return f"Denominadores: {a2}, {b2}  →  sin puntos reales"

        return ""

    def _show_generic_error(self, message: str):
        """Muestra un error genérico dentro del canvas."""
        t = self.theme

        self.graph_panel.clear_graph()

        canvas = self.graph_panel.canvas
        canvas.update_idletasks()

        w = max(canvas.winfo_width(), 500)
        h_mid = max(canvas.winfo_height(), 400) // 2

        canvas.create_text(
            w // 2,
            h_mid,
            text=f"No se pudo graficar:\n{message}",
            fill=t.gray,
            font=t.fonts["small"],
            justify="center",
        )

    # ── Elementos reales ───────────────────────────────────────────────────

    def _reveal_elements(self):
        """Muestra en campos y gráfico los elementos reales de la cónica."""
        transform = self.pipeline.get("transform", {})

        if not transform.get("valid"):
            return

        result = build_conic_elements(self._conic_type, transform["data"])

        if not result["valid"]:
            self.elements_input.show_message(result["reason"])
            return

        self.elements_input.set_values(result["values"])
        self._elements_visible = True
        self._render_graph()

    def _clear_elements(self):
        """Limpia campos, elementos reales e intento del usuario."""
        self.elements_input.clear_values()
        self._elements_visible = False
        self._attempt_data = None
        self._attempt_error = None
        self._render_graph()

    # ── Tabs, helpers y tema ───────────────────────────────────────────────

    def _show_tab(self, tab: str):
        """Alterna entre pasos General→Canónica y Canónica→General."""
        t = self.theme
        self._active_tab = tab

        for key, btn in self._tab_btns.items():
            btn.config(
                bg=t.card if key == tab else t.panel,
                fg=t.accent if key == tab else t.gray,
            )

        if tab == "general_canonical":
            self.canon_steps.lift()
        else:
            self.general_steps.lift()

    def _label(self, parent, text, bg, fg, font, **kwargs):
        """Crea una etiqueta estándar de la vista."""
        return tk.Label(parent, text=text, bg=bg, fg=fg, font=font, **kwargs)

    def _button(self, parent, text, command, padx=10, pady=5):
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
            padx=padx,
            pady=pady,
            relief="flat",
            highlightbackground=t.border,
            highlightthickness=1,
            activebackground=t.card,
            activeforeground=t.fg,
        )

    def _steps_without_direct_results(self, steps: list) -> list:
        """
        Mantiene título, explicación y ecuación para que se vea el desarrollo,
        pero evita revelar la respuesta directa en verde.
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

    def _fmt(self, value):
        """Formatea valores numéricos para mostrarlos en etiquetas."""
        if isinstance(value, float):
            if value == int(value):
                return str(int(value))

            return f"{value:.2f}"

        return str(value)

    def update_theme(self, theme):
        """Actualiza referencias de tema en la vista y sus componentes."""
        self.theme = theme
        self.configure(bg=theme.bg)

        for panel in [
            self.left,
            self.center,
            self.right,
            self.graph_panel,
            self.elements_input,
            self.coef_steps,
            self.canon_steps,
            self.general_steps,
        ]:
            panel.update_theme(theme)