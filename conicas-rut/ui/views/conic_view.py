from tkinter import Frame, Label
from ui.components.card import CardFrame
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.result_section import ResultSection
from ui.components.step_display import StepContainer


class ConicView(Frame):
    """Placeholder view for Cónicas section.

    This creates three columns: left (coefficients/equations), center (graph),
    right (steps / canonical form). Methods are provided to update theme and
    to receive future data for plotting.
    """

    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=0, minsize=380)
        self.columnconfigure(1, weight=0, minsize=900)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self.left = PanelFrame(self, self.theme, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")
        SectionHeader(self.left, "Coeficientes generados", self.theme).pack(fill="x")
        coefficients_card = CardFrame(self.left, self.theme, padx=12, pady=12)
        coefficients_card.pack(fill="x", pady=(10, 0))
        Label(coefficients_card, text="A  B  C  D  E", bg=self.theme.card, fg=self.theme.gray,
              font=self.theme.fonts["mono"]).pack(anchor="w")

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
        self.load_steps([
            {
                "title": "Paso 1: Simplificar términos",
                "explanation": "Agrupamos los términos cuadrados y lineales para preparar la forma canónica.",
                "equation": "Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0",
                "result": "Expresión reordenada",
                "observation": "Este paso es solo visual; aún no se realizan cálculos.",
            },
            {
                "title": "Paso 2: Identificar constantes",
                "explanation": "Separamos los valores independientes y preparamos la traslación.",
                "result": "Constantes listadas para construir la cónica.",
            },
        ])

    def load_steps(self, steps):
        """Carga dinámicamente una lista de pasos matemáticos."""
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

    # Placeholder for future data integration
    def load_conic(self, coefficients: dict):
        self.graph_panel.canvas.delete("graphgrid")
        self.graph_panel.canvas.create_text(200, 120, text=f"Coef: {coefficients}", fill=self.theme.fg)
