# conicas-rut/ui/views/conic_view.py

from tkinter import Frame, Label, Entry, StringVar, Button, Toplevel, Listbox, Scrollbar
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
        self._correct_elements = {}  # Elementos correctos del core
        self._user_elements = {}  # Elementos ingresados por el usuario
        self._dropdown_window = None  # Ventana del dropdown
        self._dropdown_frame = None  # Frame del dropdown expandible
        self._dropdown_visible = False  # Estado del dropdown
        self._elements_card = None  # Referencia al card de elementos para insertar dropdown
        
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
        self._elements_card = CardFrame(self.left, self.theme, padx=12, pady=12)
        self._elements_card.pack(fill="x", pady=(10, 0))
        
        # Centro
        Label(self._elements_card, text="Centro:", bg=self.theme.card, fg=self.theme.fg,
              font=self.theme.fonts["label"]).pack(anchor="w", pady=(0, 2))
        centro_entry = Entry(self._elements_card, textvariable=self.centro_var, bg=self.theme.bg, fg=self.theme.fg,
              font=self.theme.fonts["label"], width=20)
        centro_entry.pack(anchor="w", pady=(0, 8))
        centro_entry.bind("<FocusIn>", lambda e: self._on_entry_focus())
        
        # Foco
        Label(self._elements_card, text="Foco:", bg=self.theme.card, fg=self.theme.fg,
              font=self.theme.fonts["label"]).pack(anchor="w", pady=(0, 2))
        foco_entry = Entry(self._elements_card, textvariable=self.foco_var, bg=self.theme.bg, fg=self.theme.fg,
              font=self.theme.fonts["label"], width=20)
        foco_entry.pack(anchor="w", pady=(0, 8))
        foco_entry.bind("<FocusIn>", lambda e: self._on_entry_focus())
        
        # Vértice
        Label(self._elements_card, text="Vértice:", bg=self.theme.card, fg=self.theme.fg,
              font=self.theme.fonts["label"]).pack(anchor="w", pady=(0, 2))
        vertice_entry = Entry(self._elements_card, textvariable=self.vertice_var, bg=self.theme.bg, fg=self.theme.fg,
              font=self.theme.fonts["label"], width=20)
        vertice_entry.pack(anchor="w")
        vertice_entry.bind("<FocusIn>", lambda e: self._on_entry_focus())
        
        # Botones
        buttons_frame = tk.Frame(self._elements_card, bg=self.theme.card)
        buttons_frame.pack(fill="x", pady=(16, 0))
        
        # Botón para mostrar respuesta (PRIMERO)
        self._show_answer_button = tk.Button(
            buttons_frame,
            text="✓ Mostrar respuesta",
            bg=self.theme.green,
            fg=self.theme.bg,
            font=self.theme.fonts["head"],
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            activebackground=self.theme.accent,
            activeforeground=self.theme.bg,
            command=self._mostrar_respuesta
        )
        self._show_answer_button.pack(anchor="center", padx=2, pady=(0, 8))
        
        # Botón para analizar elementos (SEGUNDO)
        self._analyze_button = tk.Button(
            buttons_frame,
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
        self._analyze_button.pack(anchor="center", padx=2)

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
        """Callback cuando cambia el valor de un elemento (en tiempo real)."""
        print(f"[DEBUG] _on_element_changed llamado para: {clave}")
        
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
        
        print(f"[DEBUG] Elementos parseados: {elementos}")
        
        # Guardar elementos del usuario
        self._user_elements = elementos
        
        # Dibujar en tiempo real
        if elementos:
            print(f"[DEBUG] Hay elementos para dibujar")
            if self._plotter_instance:
                print(f"[DEBUG] Usando plotter_instance")
                self._plotter_instance.draw_user_elements(elementos, self._active_transform)
            else:
                # Fallback: dibujar directamente en el canvas
                print(f"[DEBUG] Usando fallback canvas directo")
                self._draw_elements_on_canvas(elementos)
        else:
            # Limpiar si no hay elementos válidos
            print(f"[DEBUG] Sin elementos válidos, limpiando")
            if self._plotter_instance:
                self._plotter_instance.clear_user_elements()
            elif self._plotter:
                self._plotter.delete("user_input")
    
    def _on_entry_focus(self):
        """Limpia el gráfico cuando el usuario hace clic en un campo de entrada."""
        if self._plotter_instance:
            self._plotter_instance.clear_user_elements()
        elif self._plotter:
            self._plotter.delete("user_input")

    def _on_analyze_elements(self):
        """Abre/cierra un dropdown expandible con los elementos analizados."""
        if self._dropdown_visible:
            # Cerrar dropdown
            self._close_dropdown()
        else:
            # Abrir dropdown
            self._show_analysis_dropdown(self._user_elements)
    
    def _show_analysis_dropdown(self, elementos):
        """Muestra un dropdown expandible con lista scrollable de los elementos analizados."""
        # Si ya existe, cerrarlo primero
        if self._dropdown_frame:
            self._close_dropdown()
        
        # Crear frame dropdown
        self._dropdown_frame = tk.Frame(self._elements_card, bg=self.theme.bg, height=120)
        
        # Frame interior con padding
        dropdown_inner = tk.Frame(self._dropdown_frame, bg=self.theme.card)
        dropdown_inner.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Listbox con scroll
        listbox_frame = tk.Frame(dropdown_inner, bg=self.theme.card)
        listbox_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = Scrollbar(listbox_frame, bg=self.theme.border, activebackground=self.theme.accent)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox
        listbox = Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            bg=self.theme.bg,
            fg=self.theme.fg,
            font=self.theme.fonts["small"],
            bd=0,
            relief="flat",
            highlightthickness=0,
            height=5
        )
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Agregar elementos a la lista
        if elementos:
            for clave, coord in elementos.items():
                label_map = {"centro": "Centro", "foco": "Foco", "vertice": "Vértice"}
                display_name = label_map.get(clave, clave.title())
                display_value = self._format_coordinate(coord)
                listbox.insert("end", f"{display_name}: {display_value}")
        else:
            listbox.insert("end", "No hay elementos ingresados")
        
        # Insertar el frame en el card después del botón
        self._dropdown_frame.pack(fill="x", pady=(8, 0))
        self._dropdown_visible = True
        
        # Cambiar texto del botón
        self._analyze_button.config(text="▲ Cerrar elementos")
    
    def _close_dropdown(self):
        """Cierra el dropdown expandible."""
        if self._dropdown_frame:
            self._dropdown_frame.destroy()
            self._dropdown_frame = None
            self._dropdown_visible = False
            self._analyze_button.config(text="▼ Analizar elementos")

    def _draw_elements_on_canvas(self, elementos):
        """Dibuja elementos directamente en el canvas cuando no hay plotter_instance."""
        print(f"[DEBUG] _draw_elements_on_canvas llamado con: {elementos}")
        print(f"[DEBUG] self._plotter es: {self._plotter}")
        
        if not self._plotter:
            print("[DEBUG] ERROR: self._plotter es None")
            return
        
        # Limpiar elementos anteriores
        self._plotter.delete("user_input")
        
        # Colores para cada tipo de elemento
        colors = {
            "centro": self.theme.accent2,
            "foco": self.theme.yellow,
            "vertice": self.theme.green
        }
        
        # Obtenemos dimensiones del canvas
        try:
            canvas_width = self._plotter.winfo_width()
            canvas_height = self._plotter.winfo_height()
            print(f"[DEBUG] Canvas size: {canvas_width}x{canvas_height}")
        except Exception as e:
            print(f"[DEBUG] Error getting canvas size: {e}")
            return
        
        # Si canvas no está renderizado aún, esperar
        if canvas_width <= 50 or canvas_height <= 50:
            print(f"[DEBUG] Canvas muy pequeño, esperando... ({canvas_width}x{canvas_height})")
            self.after(100, lambda: self._draw_elements_on_canvas(elementos))
            return
        
        # Centro del canvas (donde está el origen de coordenadas matemáticas)
        x_centro = canvas_width / 2
        y_centro = canvas_height / 2
        print(f"[DEBUG] Centro del canvas: ({x_centro}, {y_centro})")
        
        # Escala: 40 píxeles = 1 unidad matemática
        escala = 40
        
        # Dibujar cada elemento
        for clave, coord in elementos.items():
            if coord and len(coord) == 2:
                x_math, y_math = coord
                
                # Convertir coordenadas matemáticas a píxeles del canvas
                x_canvas = x_centro + (x_math * escala)
                y_canvas = y_centro - (y_math * escala)  # Y invertido en canvas
                
                print(f"[DEBUG] Elemento {clave}: math({x_math},{y_math}) -> canvas({x_canvas},{y_canvas})")
                
                # Verificar que el punto esté dentro del canvas
                if not (0 <= x_canvas <= canvas_width and 0 <= y_canvas <= canvas_height):
                    print(f"[DEBUG] {clave} está FUERA del canvas")
                    continue
                
                color = colors.get(clave, self.theme.fg)
                radius = 5
                
                # Dibujar círculo
                print(f"[DEBUG] Dibujando círculo para {clave} en ({x_canvas}, {y_canvas}) con color {color}")
                self._plotter.create_oval(
                    x_canvas - radius, y_canvas - radius,
                    x_canvas + radius, y_canvas + radius,
                    fill=color, outline=color, tags="user_input", width=2
                )
                
                # Dibujar etiqueta
                label_map = {"centro": "C", "foco": "F", "vertice": "V"}
                label = label_map.get(clave, clave[0].upper())
                self._plotter.create_text(
                    x_canvas + 12, y_canvas - 12,
                    text=label, fill=color, font=("Arial", 11, "bold"),
                    tags="user_input"
                )
        
        # Forzar actualización del canvas
        self._plotter.update_idletasks()
        print("[DEBUG] Canvas actualizado")

    def _format_coordinate(self, coord):
        """Formatea una tupla (x, y) como 'x.xx,y.xx'."""
        if coord and len(coord) == 2:
            x, y = coord
            return f"{x:.2f},{y:.2f}"
        return ""

    def _mostrar_respuesta(self):
        """Muestra la respuesta correcta o dibuja los elementos actuales."""
        elementos_a_mostrar = {}
        
        # Si hay elementos correctos del core, usarlos
        if self._correct_elements:
            elementos_a_mostrar = self._correct_elements
        else:
            # Si no, usar los elementos ingresados por el usuario
            elementos_a_mostrar = self._user_elements
        
        if not elementos_a_mostrar:
            return
        
        # Llenar los campos con los valores
        if "center" in elementos_a_mostrar:
            self.centro_var.set(self._format_coordinate(elementos_a_mostrar["center"]))
        
        if "vertex" in elementos_a_mostrar:
            self.vertice_var.set(self._format_coordinate(elementos_a_mostrar["vertex"]))
        
        # También copiar "centro" si existe "center"
        if "center" in elementos_a_mostrar and "centro" not in elementos_a_mostrar:
            elementos_a_mostrar = {**elementos_a_mostrar, "centro": elementos_a_mostrar["center"]}
        
        # También copiar "vertice" si existe "vertex"
        if "vertex" in elementos_a_mostrar and "vertice" not in elementos_a_mostrar:
            elementos_a_mostrar = {**elementos_a_mostrar, "vertice": elementos_a_mostrar["vertex"]}
        
        # Limpiar y redibujar
        if self._plotter_instance:
            self._plotter_instance.clear_user_elements()
            self._plotter_instance.draw_user_elements(elementos_a_mostrar, self._active_transform)
        else:
            # Fallback: dibujar directamente en el canvas
            self._draw_elements_on_canvas(elementos_a_mostrar)

    def load_data(self, conic_type="ellipse", trans_data=None):
        """
        Carga datos de la cónica activa según su tipo.
        
        Args:
            conic_type: Tipo de cónica (ellipse, hyperbola, parabola)
            trans_data: Dict con datos transformados del core conteniendo "center", "vertex", etc.
        """
        print(f"[DEBUG] load_data llamado: conic_type={conic_type}, trans_data={trans_data}")
        
        # Guardar referencias del plotter y transform según el tipo de cónica
        self._plotter = self.graph_panel.canvas
        self._active_transform = conic_type
        
        print(f"[DEBUG] self._plotter asignado: {self._plotter}")
        print(f"[DEBUG] Canvas size en load_data: {self._plotter.winfo_width()}x{self._plotter.winfo_height()}")
        
        # Guardar elementos correctos del core
        self._correct_elements = {}
        if trans_data:
            if "center" in trans_data and trans_data["center"]:
                # Convertir a tupla si no lo es
                center = trans_data["center"]
                if isinstance(center, (tuple, list)) and len(center) == 2:
                    self._correct_elements["center"] = tuple(center)
            
            if "vertex" in trans_data and trans_data["vertex"]:
                # Convertir a tupla si no lo es
                vertex = trans_data["vertex"]
                if isinstance(vertex, (tuple, list)) and len(vertex) == 2:
                    self._correct_elements["vertex"] = tuple(vertex)
        
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