# conicas-rut/ui/views/tramo_view.py

from tkinter import Frame, Label
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.result_section import ResultSection
from ui.components.value_table import ValueTable
from ui.components.step_display import StepContainer


class TramoView(Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=0, minsize=250)   # izq: fijo 250px
        self.columnconfigure(1, weight=1, minsize=500)   # centro: elástico
        self.columnconfigure(2, weight=0, minsize=280)   # der: fijo 280px
        self.rowconfigure(0, weight=1)

        self.left = PanelFrame(self, self.theme, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")
        SectionHeader(self.left, "Función generada", self.theme).pack(fill="x")
        self.summary = ResultSection(self.left, self.theme, "Resumen")
        self.summary.pack(fill="x", pady=(10, 0))
        self.summary.add_line("Se ha generado una función por tramos basada en el RUT ingresado.")
        self.summary.add_line("Los intervalos y valores se muestran en la tabla de la derecha.")

        self.step_container = StepContainer(self.left, self.theme)
        self.step_container.pack(fill="both", expand=True, pady=(10, 0))
        self.load_steps([
            {
                "title": "Paso 1: Definir intervalos",
                "explanation": "Cada tramo se define en un intervalo distinto y se escribe su expresión asociada.",
                "equation": "f(x) = 2x + 1  para x < 0",
                "result": "Primer tramo definido.",
                "observation": "Los pasos se muestran en una lista desplazable para grandes desarrollos.",
            },
            {
                "title": "Paso 2: Ajustar continuidad",
                "explanation": "Verificar que los valores en los extremos de los intervalos sean coherentes.",
                "result": "Continuidad visual mantenida.",
            },
        ])

        self.center = PanelFrame(self, self.theme, padx=8, pady=8)
        self.center.grid(row=0, column=1, sticky="nsew")
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)
        self.graph_panel = GraphPanel(self.center, self.theme, title="Gráfico por tramos")
        self.graph_panel.grid(row=0, column=0, sticky="nsew")

        self.right = PanelFrame(self, self.theme, padx=12, pady=12)
        self.right.grid(row=0, column=2, sticky="nsew")
        SectionHeader(self.right, "Tabla de valores", self.theme).pack(fill="x")
        self.value_table = ValueTable(self.right, self.theme, padx=6, pady=6)
        self.value_table.pack(fill="both", expand=True, pady=(10, 0))

    def load_steps(self, steps):
        self.step_container.set_steps(steps)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.bg)
        self.left.update_theme(theme)
        self.center.update_theme(theme)
        self.right.update_theme(theme)
        self.summary.update_theme(theme)
        self.step_container.update_theme(theme)
        self.graph_panel.update_theme(theme)
        self.value_table.update_theme(theme)