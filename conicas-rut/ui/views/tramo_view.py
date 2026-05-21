from tkinter import Frame, Label, Canvas
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.result_section import ResultSection
from ui.components.value_table import ValueTable
from ui.components.step_display import StepContainer


class TramoView(Frame):
    """Placeholder view for Funciones por Tramos section.

    Provides left summary, center graph placeholder and right value table placeholder.
    """

    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._build()

    def _build(self):
        self.columnconfigure(1, weight=1)

        left = PanelFrame(self, self.theme, padx=12, pady=12)
        left.grid(row=0, column=0, sticky="nsew")
        SectionHeader(left, "Función generada", self.theme).pack(fill="x")
        self.summary = ResultSection(left, self.theme, "Resumen")
        self.summary.pack(fill="x", pady=(10, 0))
        self.summary.add_line("Se ha generado una función por tramos basada en el RUT ingresado.")
        self.summary.add_line("Los intervalos y valores se muestran en la tabla de la derecha.")

        self.step_container = StepContainer(left, self.theme)
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

        center = PanelFrame(self, self.theme, padx=8, pady=8)
        center.grid(row=0, column=1, sticky="nsew")
        self.canvas = Canvas(center, bg=self.theme.plot, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_text(220, 140, text="[Gráfica - función por tramos]", fill=self.theme.gray)

        right = PanelFrame(self, self.theme, padx=12, pady=12)
        right.grid(row=0, column=2, sticky="nsew")
        SectionHeader(right, "Tabla de valores", self.theme).pack(fill="x")
        self.value_table = ValueTable(right, self.theme, padx=6, pady=6)
        self.value_table.pack(fill="both", expand=True, pady=(10, 0))

    def load_steps(self, steps):
        """Carga desde un módulo matemático la lista de pasos por tramos."""
        self.step_container.set_steps(steps)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.bg)
        for child in self.winfo_children():
            try:
                child.configure(bg=theme.panel)
            except Exception:
                pass
        self.canvas.configure(bg=theme.plot)
