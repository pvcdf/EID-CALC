# conicas-rut/ui/views/conic_view.py

from tkinter import Frame, Label, Entry, StringVar, Button
from ui.components.card import CardFrame
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.result_section import ResultSection
from ui.components.step_display import StepContainer
import tkinter as tk


class ConicView(Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._plotter = None  # Canvas del graph_panel
        self._plotter_instance = None  # Instancia de ConicPlotter si se proporciona
        self._active_transform = None
        
        # StringVars para elementos editables
        self.centro_var = StringVar()
        self.foco_var = StringVar()
        self.vertice_var = StringVar()
        
        # Agregar trace a los StringVars
        self.centro_var.trace_add("write", lambda *args: self._on_element_changed("centro"))
        self.foco_var.trace_add("write", lambda *args: self._on_element_changed("foco"))
        self.vertice_var.trace_add("write", lambda *args: self._on_element_changed("vertice"))
        
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=0, minsize=250)   # izq: reducido de 380 → 250
        self.columnconfigure(1, weight=1, minsize=500)   # centro: elástico, antes weight=0
        self.columnconfigure(2, weight=0, minsize=300)   # der: fijo 300px (antes se cortaba)
        self.rowconfigure(0, weight=1)

        self.left = PanelFrame(self, self.theme, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")
        SectionHeader(self.left, "Coeficientes generados", self.theme).pack(fill="x")
        coefficients_card = CardFrame(self.left, self.theme, padx=12, pady=12)
        coefficients_card.pack(fill="x", pady=(10, 0))
        Label(coefficients_card, text="A  B  C  D  E", bg=self.theme.card, fg=self.theme.gray,
              font=self.theme.fonts["mono"]).pack(anchor="w")
        
        # Panel de elementos editables
        SectionHeader(self.left, "Elementos (x,y o x, y)", self.theme).pack(fill="x", pady=(15, 0))
        elements_card = CardFrame(self.left, self.theme, padx=12, pady=12)
        elements_card.pack(fill="x", pady=(10, 0))
        
        # Centro
        Label(elements_card, text="Centro:", bg=self.theme.card, fg=self.theme.fg,
              font=self.theme.fonts["label"]).pack(anchor="w", pady=(0, 2))
        Entry(elements_card, textvariable=self.centro_var, bg=self.theme.bg, fg=self.theme.fg,
              font=self.theme.fonts["label"], width=20).pack(anchor="w", pady=(0, 8))
        
        # Foco
        Label(elements_card, text="Foco:", bg=self.theme.card, fg=self.theme.fg,
              font=self.theme.fonts["label"]).pack(anchor="w", pady=(0, 2))
        Entry(elements_card, textvariable=self.foco_var, bg=self.theme.bg, fg=self.theme.fg,
              font=self.theme.fonts["label"], width=20).pack(anchor="w", pady=(0, 8))
        
        # Vértice
        Label(elements_card, text="Vértice:", bg=self.theme.card, fg=self.theme.fg,
              font=self.theme.fonts["label"]).pack(anchor="w", pady=(0, 2))
        Entry(elements_card, textvariable=self.vertice_var, bg=self.theme.bg, fg=self.theme.fg,
              font=self.theme.fonts["label"], width=20).pack(anchor="w")
        
        # Botón para analizar elementos
        self._analyze_button = tk.Button(
            elements_card,
            text="▼ Analizar elementos",
            bg=self.theme.accent,
            fg=self.theme.bg,
            font=self.theme.fonts["head"],
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            activebackground=self.theme.accent2,
            activeforeground=self.theme.bg,
            command=self._on_analyze_elements
        )
        self._analyze_button.pack(anchor="center", pady=(16, 0), padx=2)

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
        self.step_container.set_steps(steps)

    def _parse_coordinate(self, text):
        """Parsea texto como 'x,y' o '(x,y)' y retorna tupla (x, y) o None si es inválido."""
        if not text or not text.strip():
            return None
        
        # Limpiar espacios y paréntesis
        text = text.strip().replace("(", "").replace(")", "").strip()
        
        try:
            parts = text.split(",")
            if len(parts) != 2:
                return None
            x = float(parts[0].strip())
            y = float(parts[1].strip())
            return (x, y)
        except (ValueError, AttributeError):
            return None

    def _on_element_changed(self, clave):
        """Callback cuando cambia el valor de un elemento (centro, foco, vértice)."""
        # Solo procesar si tenemos un plotter real (no solo el canvas)
        if not hasattr(self, '_plotter_instance') or not self._plotter_instance:
            return
        
        # Obtener los valores actuales
        elementos = {}
        
        centro = self._parse_coordinate(self.centro_var.get())
        if centro:
            elementos["centro"] = centro
        
        foco = self._parse_coordinate(self.foco_var.get())
        if foco:
            elementos["foco"] = foco
        
        vertice = self._parse_coordinate(self.vertice_var.get())
        if vertice:
            elementos["vertice"] = vertice
        
        if elementos:
            self._plotter_instance.draw_user_elements(elementos, self._active_transform)
        else:
            self._plotter_instance.clear_user_elements()

    def _on_analyze_elements(self):
        """Callback cuando el usuario presiona el botón de analizar elementos."""
        # Obtener los valores actuales
        elementos = {}
        
        centro = self._parse_coordinate(self.centro_var.get())
        if centro:
            elementos["centro"] = centro
        
        foco = self._parse_coordinate(self.foco_var.get())
        if foco:
            elementos["foco"] = foco
        
        vertice = self._parse_coordinate(self.vertice_var.get())
        if vertice:
            elementos["vertice"] = vertice
        
        # Dibujar si hay elementos válidos
        if elementos:
            if self._plotter_instance:
                self._plotter_instance.draw_user_elements(elementos, self._active_transform)
            else:
                # Fallback: intentar dibujar directamente en el canvas
                self._draw_elements_on_canvas(elementos)
    
    def _draw_elements_on_canvas(self, elementos):
        """Dibuja elementos directamente en el canvas cuando no hay plotter_instance."""
        if not self._plotter:
            return
        
        # Limpiar elementos anteriores
        self._plotter.delete("user_input")
        
        # Colores para cada tipo de elemento
        colors = {
            "centro": self.theme.accent2,
            "foco": self.theme.yellow,
            "vertice": self.theme.green
        }
        
        # Dibujar cada elemento
        for clave, coord in elementos.items():
            if coord and len(coord) == 2:
                x_math, y_math = coord
                # Para el canvas directo, usar coordenadas relativas simples
                # Esto es un fallback básico
                canvas_width = self._plotter.winfo_width()
                canvas_height = self._plotter.winfo_height()
                
                # Escala simple (asumiendo rango -5 a 5)
                x_canvas = (canvas_width / 2) + (x_math * canvas_width / 10)
                y_canvas = (canvas_height / 2) - (y_math * canvas_height / 10)
                
                color = colors.get(clave, self.theme.fg)
                radius = 5
                
                # Dibujar círculo
                self._plotter.create_oval(
                    x_canvas - radius, y_canvas - radius,
                    x_canvas + radius, y_canvas + radius,
                    fill=color, outline=color, tags="user_input"
                )
                
                # Dibujar etiqueta
                label_map = {"centro": "C", "foco": "F", "vertice": "V"}
                label = label_map.get(clave, clave[0].upper())
                self._plotter.create_text(
                    x_canvas + 10, y_canvas - 10,
                    text=label, fill=color, font=("Arial", 10, "bold"),
                    tags="user_input"
                )

    def load_data(self, conic_type="ellipse"):
        """Carga datos de la cónica activa según su tipo."""
        # Guardar referencias del plotter y transform según el tipo de cónica
        self._plotter = self.graph_panel.canvas
        self._active_transform = conic_type
        
        # Limpiar los campos de entrada
        self.centro_var.set("")
        self.foco_var.set("")
        self.vertice_var.set("")
        
        # Limpiar elementos previos del usuario
        if self._plotter_instance:
            self._plotter_instance.clear_user_elements()
        else:
            # Si no hay plotter_instance, limpiar manualmente
            if self._plotter:
                self._plotter.delete("user_input")
    
    def set_plotter(self, plotter_instance):
        """Asigna una instancia de ConicPlotter para dibujar elementos."""
        self._plotter_instance = plotter_instance

    def load_conic(self, coefficients: dict):
        self.graph_panel.canvas.delete("graphgrid")
        self.graph_panel.canvas.create_text(200, 120, text=f"Coef: {coefficients}", fill=self.theme.fg)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.bg)
        self.left.update_theme(theme)
        self.center.update_theme(theme)
        self.right.update_theme(theme)
        self.result_card.update_theme(theme)
        self.step_container.update_theme(theme)
        self.graph_panel.update_theme(theme)