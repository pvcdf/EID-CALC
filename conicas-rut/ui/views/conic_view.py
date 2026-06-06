from tkinter import Frame, Label
from ui.components.card import CardFrame
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.result_section import ResultSection
from ui.components.step_display import StepContainer

from core.coef_builder import build_coefficients
from core.conic_classifier import classify_conic
from core.transforms.canonical_transform import transform_conic
from graphics.conic_plotter import ConicPlotter

class ConicView(Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=0, minsize=260)
        self.columnconfigure(1, weight=1, minsize=500)
        self.columnconfigure(2, weight=0, minsize=300)
        self.rowconfigure(0, weight=1)

        self.left = PanelFrame(self, self.theme, padx=14, pady=14)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(4, 2), pady=4)
        SectionHeader(self.left, "Coeficientes", self.theme).pack(fill="x", pady=(0, 12))
        self.coefficients_card = CardFrame(self.left, self.theme, padx=10, pady=10)
        self.coefficients_card.pack(fill="x", pady=(0, 12))

        self.center = PanelFrame(self, self.theme, padx=10, pady=10)
        self.center.grid(row=0, column=1, sticky="nsew", padx=2, pady=4)
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)
        self.graph_panel = GraphPanel(self.center, self.theme, title="Gráfico")
        self.graph_panel.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self.right = PanelFrame(self, self.theme, padx=14, pady=14)
        self.right.grid(row=0, column=2, sticky="nsew", padx=(2, 4), pady=4)
        self.result_card = ResultSection(self.right, self.theme, "Pasos")
        self.result_card.pack(fill="both", expand=True)
        self.step_container = StepContainer(self.result_card.body, self.theme)
        self.step_container.pack(fill="both", expand=True, padx=2, pady=2)

    def load_steps(self, steps):
        self.step_container.set_steps(steps)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.bg)
        self.left.update_theme(theme)
        self.center.update_theme(theme)
        self.right.update_theme(theme)
        self.result_card.update_theme(theme)
        self.step_container.update_theme(theme)
        self.graph_panel.update_theme(theme)

    def load_data(self, rut_data):
            coef_result = build_coefficients(rut_data)
            
            if not coef_result["valid"]:
                self.load_steps([{"title": "Error", "explanation": coef_result.get("error", "Error desconocido")}])
                return
                
            coef_data = coef_result["data"]
            
            for widget in self.coefficients_card.winfo_children():
                widget.destroy()
            
            coef_labels = [
                ("A", coef_data['A']),
                ("B", coef_data['B']),
                ("C", coef_data['C']),
                ("D", coef_data['D']),
                ("E", coef_data['E'])
            ]
            
            for i, (name, value) in enumerate(coef_labels):
                color = self.theme.accent if i % 2 == 0 else self.theme.accent2
                Label(self.coefficients_card, text=f"{name} = {value:.2f}" if isinstance(value, float) else f"{name} = {value}", 
                    bg=self.theme.card, fg=color, font=self.theme.fonts["mono"]).pack(anchor="w", pady=4, padx=4)

            class_result = classify_conic(coef_result)
            
            if not class_result["valid"]:
                self.load_steps([{"title": "Error de Clasificación", "explanation": class_result.get("error", "")}])
                return
                
            conic_type = class_result["conic_type"]

            transform_result = transform_conic(
                conic_type, 
                coef_data["A"], coef_data["B"], coef_data["C"], coef_data["D"], coef_data["E"]
            )
            
            pasos = []
            pasos.append({"title": "Construcción", "explanation": coef_result["explanation"], "equation": coef_data["equation_str"]})
            pasos.append({"title": "Clasificación", "explanation": class_result["explanation"], "result": class_result["data"]["conic_name_es"]})
            
            if not transform_result["valid"]:
                pasos.append({"title": "Singularidad Matemática", "explanation": transform_result.get("error", ""), "observation": "Cálculo abortado para evitar división por cero o raíces imaginarias."})
                self.load_steps(pasos)
                self.graph_panel.canvas.delete("all")
                return
                
            trans_data = transform_result["data"]

            for p in transform_result.get("steps", []):
                pasos.append({"title": "Transformación", "explanation": p})
                
            pasos.append({"title": "Forma Canónica", "equation": trans_data["canonical_form"]})
            self.load_steps(pasos)

            self.current_plot_data = trans_data
            self.current_conic_type = conic_type

            self.graph_panel.canvas.bind("<Configure>", self._on_canvas_resize)
            
            self.redraw_plot()

    def _on_canvas_resize(self, event):
        if event.width > 10 and hasattr(self, 'current_plot_data'):
            self.redraw_plot()

    def redraw_plot(self):
        self.graph_panel.canvas.delete("all")
        plotter = ConicPlotter(self.graph_panel.canvas, self.theme)
            
        conic_type = self.current_conic_type
        trans_data = self.current_plot_data

        if conic_type == "circle":
            plotter.plot_circle(trans_data["radius"], trans_data["center"][0], trans_data["center"][1])
        elif conic_type == "ellipse":
            plotter.plot_ellipse(trans_data["a"], trans_data["b"], trans_data["center"][0], trans_data["center"][1])
        elif conic_type == "hyperbola":
            plotter.plot_hyperbola(trans_data["a"], trans_data["b"], trans_data["center"][0], trans_data["center"][1], trans_data["orientation"])
        elif conic_type == "parabola":
            plotter.plot_parabola(trans_data["p"], trans_data["vertex"][0], trans_data["vertex"][1], trans_data["orientation"])