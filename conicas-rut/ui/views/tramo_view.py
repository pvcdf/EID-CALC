from tkinter import Frame
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.value_table import ValueTable
from ui.components.step_display import StepContainer
from core.tramo_function import CrearVariables
from core.limit_analyzer import AnalizarLimites
from core.value_table import CrearTablaValores
from graphics.tramo_plotter import TramoPlotter

class TramoView(Frame):
    
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=0, minsize=320)
        self.columnconfigure(1, weight=1, minsize=500)
        self.columnconfigure(2, weight=0, minsize=300)
        self.rowconfigure(0, weight=1)

        self.left = PanelFrame(self, self.theme, padx=14, pady=14)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(4, 2), pady=4)
        SectionHeader(self.left, "Análisis Formal", self.theme).pack(fill="x", pady=(0, 12))
        
        self.step_container = StepContainer(self.left, self.theme)
        self.step_container.pack(fill="both", expand=True, pady=(8, 0))

        self.center = PanelFrame(self, self.theme, padx=10, pady=10)
        self.center.grid(row=0, column=1, sticky="nsew", padx=2, pady=4)
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)
        self.graph_panel = GraphPanel(self.center, self.theme, title="Gráfico")
        self.graph_panel.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self.right = PanelFrame(self, self.theme, padx=14, pady=14)
        self.right.grid(row=0, column=2, sticky="nsew", padx=(2, 4), pady=4)
        SectionHeader(self.right, "Aproximación Numérica", self.theme).pack(fill="x", pady=(0, 12))
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
        self.step_container.update_theme(theme)
        self.graph_panel.update_theme(theme)
        self.value_table.update_theme(theme)

    def load_data(self, rut_data):
        self.graph_panel.canvas.delete("all")
        
        rut_str = rut_data["data"]["clean_rut"]
        
        datos = CrearVariables(rut_str)
        analisis = AnalizarLimites(rut_str)
        tabla = CrearTablaValores(datos["a"], datos["funcion"])
        
        pasos_formateados = []
        
        pasos_formateados.append({
            "title": f"Punto Crítico: x = {datos['a']}",
            "explanation": f"Se evalúa una discontinuidad de tipo {datos['tipo_discontinuidad']}.\n{datos['explicacion']}",
            "result": analisis['tablas_aproximacion']['conclusion']
        })

        for i, paso in enumerate(datos["pasos_preliminares"]):
            if i > 0:
                pasos_formateados.append({"title": f"Generación: Fase {i}", "explanation": paso})
            
        pasos_formateados.append({
            "title": "Estructura Algebraica", 
            "explanation": analisis["explicacion_formal"]["preliminar"]
        })
        
        for i, dem in enumerate(analisis["explicacion_formal"]["demostracion"]):
            pasos_formateados.append({"title": f"Demostración {i+1}", "explanation": dem})
            
        self.load_steps(pasos_formateados)

        filas_tabla = []
        for fila in tabla["izquierda"]:
            y_val = f"{fila['y']:.4f}" if fila['y'] is not None else "Indef"
            filas_tabla.append((str(fila["x"]), y_val, "Izquierda"))
            
        for fila in tabla["derecha"]:
            y_val = f"{fila['y']:.4f}" if fila['y'] is not None else "Indef"
            filas_tabla.append((str(fila["x"]), y_val, "Derecha"))

        self.value_table.set_rows(filas_tabla)

        tipo_disc = "removable"
        if datos["tipo_discontinuidad"] == "salto":
            tipo_disc = "jump"
        elif datos["tipo_discontinuidad"] == "infinita":
            tipo_disc = "infinite"

        self.tramo_info = [{
            "func": datos["funcion"],
            "x_min": datos["a"] - 5,
            "x_max": datos["a"] + 5,
            "discontinuity_type": tipo_disc
        }]
        
        self.x_center = datos["a"]

        self.graph_panel.canvas.bind("<Configure>", self._on_canvas_resize)
        self.redraw_plot()

    def _on_canvas_resize(self, event):
        if event.width > 10 and hasattr(self, 'tramo_info'):
            self.redraw_plot()

    def redraw_plot(self):
        self.graph_panel.canvas.delete("all")
        plotter = TramoPlotter(self.graph_panel.canvas, self.theme)

        plotter.plot_piecewise(
            self.tramo_info, 
            self.x_center - 5, 
            self.x_center + 5, 
            -20, 
            20
        )