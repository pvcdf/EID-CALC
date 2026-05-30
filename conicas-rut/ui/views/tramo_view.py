from tkinter import Frame, Label
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.result_section import ResultSection
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
        self.columnconfigure(0, weight=0, minsize=260)   # izq: fijo 260px
        self.columnconfigure(1, weight=1, minsize=500)   # centro: elástico
        self.columnconfigure(2, weight=0, minsize=280)   # der: fijo 280px
        self.rowconfigure(0, weight=1)

        self.left = PanelFrame(self, self.theme, padx=14, pady=14)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(4, 2), pady=4)
        SectionHeader(self.left, "Función", self.theme).pack(fill="x", pady=(0, 12))
        self.summary = ResultSection(self.left, self.theme, "Resumen")
        self.summary.pack(fill="x", pady=(0, 12))
        self.summary.add_line("Se ha generado una función por tramos basada en el RUT ingresado.")
        self.summary.add_line("Los intervalos y valores se muestran en la tabla de la derecha.")

        self.step_container = StepContainer(self.left, self.theme)
        self.step_container.pack(fill="both", expand=True, pady=(8, 0))
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

        self.center = PanelFrame(self, self.theme, padx=10, pady=10)
        self.center.grid(row=0, column=1, sticky="nsew", padx=2, pady=4)
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)
        self.graph_panel = GraphPanel(self.center, self.theme, title="Gráfico")
        self.graph_panel.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self.right = PanelFrame(self, self.theme, padx=14, pady=14)
        self.right.grid(row=0, column=2, sticky="nsew", padx=(2, 4), pady=4)
        SectionHeader(self.right, "Tabla", self.theme).pack(fill="x", pady=(0, 12))
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

    def load_data(self, rut_data):
        self.graph_panel.canvas.delete("all")
        plotter = TramoPlotter(self.graph_panel.canvas, self.theme)
        data_interna = rut_data["data"]
        
        datos = CrearVariables(data_interna)
        analisis = AnalizarLimites(data_interna)
        tabla = CrearTablaValores(datos["a"], datos["funcion"])
        
        for widget in self.summary.body.winfo_children():
            widget.destroy()
            
        self.summary.add_line(f"Punto de análisis crítico: x = {datos['a']}")
        self.summary.add_line(f"Tipo detectado: Discontinuidad {datos['tipo_discontinuidad']}")
        self.summary.add_line(f"Motivo: {datos['explicacion']}")
        self.summary.add_line(f"Conclusión de límites: {analisis['tablas_aproximacion']['conclusion']}")

        pasos_formateados = []
        
        for i, paso in enumerate(datos["pasos_preliminares"]):
            pasos_formateados.append({
                "title": f"Paso {i+1}: Generación",
                "explanation": paso
            })
            
        pasos_formateados.append({
            "title": "Evaluación Preliminar",
            "explanation": analisis["explicacion_formal"]["preliminar"]
        })
        
        for i, dem in enumerate(analisis["explicacion_formal"]["demostracion"]):
            pasos_formateados.append({
                "title": f"Demostración {i+1}",
                "explanation": dem
            })
            
        self.load_steps(pasos_formateados)

        filas_tabla = []
        
        for fila in tabla["izquierda"]:
            y_val = f"{fila['y']:.4f}" if fila['y'] is not None else "Indef"
            filas_tabla.append((str(fila["x"]), y_val, "Izquierda"))
            
        for fila in tabla["derecha"]:
            y_val = f"{fila['y']:.4f}" if fila['y'] is not None else "Indef"
            filas_tabla.append((str(fila["x"]), y_val, "Derecha"))

        self.value_table.set_rows(filas_tabla)

        plotter = TramoPlotter(self.graph_panel.canvas, self.theme)
        plotter.clear_plot()

        tipo_disc = "removable"
        if datos["tipo_discontinuidad"] == "salto":
            tipo_disc = "jump"
        elif datos["tipo_discontinuidad"] == "infinita":
            tipo_disc = "infinite"

        tramo_info = [{
            "func": datos["funcion"],
            "x_min": datos["a"] - 5,
            "x_max": datos["a"] + 5,
            "discontinuity_type": tipo_disc
        }]

        plotter.plot_piecewise(
            tramo_info, 
            datos["a"] - 5, 
            datos["a"] + 5, 
            -20, 
            20
        )