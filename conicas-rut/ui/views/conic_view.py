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
        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=1, minsize=500)
        self.columnconfigure(2, weight=0, minsize=300)
        self.rowconfigure(0, weight=1)

        self.left = PanelFrame(self, self.theme, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")
        SectionHeader(self.left, "Coeficientes generados", self.theme).pack(fill="x")
        self.coefficients_card = CardFrame(self.left, self.theme, padx=12, pady=12)
        self.coefficients_card.pack(fill="x", pady=(10, 0))

        self.center = PanelFrame(self, self.theme, padx=8, pady=8)
        self.center.grid(row=0, column=1, sticky="nsew")
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)
        self.graph_panel = GraphPanel(self.center, self.theme, title="Gráfico de cónica")
        self.graph_panel.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        self.right = PanelFrame(self, self.theme, padx=12, pady=12)
        self.right.grid(row=0, column=2, sticky="nsew")
        self.result_card = ResultSection(self.right, self.theme, "Pasos - Forma canónica")
        self.result_card.pack(fill="both", expand=True)
        self.step_container = StepContainer(self.result_card.body, self.theme)
        self.step_container.pack(fill="both", expand=True)

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
        if not coef_result["valid"]: return
        coef_data = coef_result["data"]
        
        for widget in self.coefficients_card.winfo_children():
            widget.destroy()
            
        Label(self.coefficients_card, text=f"A = {coef_data['A']:.2f}", bg=self.theme.card, fg=self.theme.fg, font=self.theme.fonts["mono"]).pack(anchor="w")
        Label(self.coefficients_card, text=f"B = {coef_data['B']:.2f}", bg=self.theme.card, fg=self.theme.fg, font=self.theme.fonts["mono"]).pack(anchor="w")
        Label(self.coefficients_card, text=f"C = {coef_data['C']}", bg=self.theme.card, fg=self.theme.fg, font=self.theme.fonts["mono"]).pack(anchor="w")
        Label(self.coefficients_card, text=f"D = {coef_data['D']}", bg=self.theme.card, fg=self.theme.fg, font=self.theme.fonts["mono"]).pack(anchor="w")
        Label(self.coefficients_card, text=f"E = {coef_data['E']}", bg=self.theme.card, fg=self.theme.fg, font=self.theme.fonts["mono"]).pack(anchor="w")

        class_result = classify_conic(coef_result)
        if not class_result["valid"]: return
        conic_type = class_result["conic_type"]

        transform_result = transform_conic(
            conic_type, 
            coef_data["A"], coef_data["B"], coef_data["C"], coef_data["D"], coef_data["E"]
        )
        if not transform_result["valid"]: return
        trans_data = transform_result["data"]

        pasos = []
        pasos.append({"title": "Construcción", "explanation": coef_result["explanation"], "equation": coef_data["equation_str"]})
        pasos.append({"title": "Clasificación", "explanation": class_result["explanation"], "result": class_result["data"]["conic_name_es"]})
        
        for p in transform_result.get("steps", []):
            pasos.append({"title": "Transformación", "explanation": p})
            
        pasos.append({"title": "Forma Canónica", "equation": trans_data["canonical_form"]})
        self.load_steps(pasos)

        self.graph_panel.canvas.delete("all")
        plotter = ConicPlotter(self.graph_panel.canvas, self.theme)
        
        if conic_type == "circle":
            plotter.plot_ellipse(trans_data["radius"], trans_data["radius"], trans_data["center"][0], trans_data["center"][1])
        elif conic_type == "ellipse":
            plotter.plot_ellipse(trans_data["a"], trans_data["b"], trans_data["center"][0], trans_data["center"][1])
        elif conic_type == "hyperbola":
            plotter.plot_hyperbola(trans_data["a"], trans_data["b"], trans_data["center"][0], trans_data["center"][1], trans_data["orientation"])
        elif conic_type == "parabola":
            plotter.plot_parabola(trans_data["p"], trans_data["vertex"][0], trans_data["vertex"][1], trans_data["orientation"])