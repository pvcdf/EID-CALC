# conicas-rut/ui/views/conic_view.py

import tkinter as tk
from tkinter import Frame, Label, Entry, StringVar, Canvas, Scrollbar
from ui.components.card import CardFrame
from ui.components.graph_panel import GraphPanel
from ui.components.header import SectionHeader
from ui.components.panel import PanelFrame
from ui.components.step_display import StepContainer

from core.coef_builder import build_coefficients
from core.conic_classifier import classify_conic
from core.transforms.canonical_transform import transform_conic
from graphics.conic_plotter import ConicPlotter
from graphics.canvas_utils import CoordinateTransform

class ConicView(Frame):
    def __init__(self, master, theme, pipeline: dict = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self.pipeline = pipeline or {}
        self._active_tab = "general_canonical"  # tab activo del switcher
        self._conic_type = None
        self._plotter = None
        self._active_transform = None
        self._correct_elements = {}
        
        self._build()
        if pipeline and pipeline.get("valid"):
            self._load_pipeline(pipeline)

    # ── Layout ────────────────────────────────────────────────────────────

    def _build(self):
        t = self.theme
        self.configure(bg=t.bg)
        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=1, minsize=500)
        self.columnconfigure(2, weight=0, minsize=310)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_center()
        self._build_right()

    # ── Columna izquierda ─────────────────────────────────────────────────

    def _build_left(self):
        t = self.theme
        self.left = PanelFrame(self, t, padx=12, pady=12)
        self.left.grid(row=0, column=0, sticky="nsew")
        
        SectionHeader(self.left, "Coeficientes generados", t).pack(fill="x")

        # Tabla A B C D E
        coef_card = CardFrame(self.left, t, padx=12, pady=10)
        coef_card.pack(fill="x", pady=(10, 0))
        self._coef_labels = {}
        for i, name in enumerate(["A", "B", "C", "D", "E"]):
            col = Frame(coef_card, bg=t.card)
            col.grid(row=0, column=i, sticky="ew")
            coef_card.columnconfigure(i, weight=1)
            Label(col, text=name, bg=t.card, fg=t.gray,
                  font=t.fonts["mono_sm"], anchor="center").pack(fill="x")
            lbl = Label(col, text="—", bg=t.card, fg=t.accent2,
                        font=t.fonts["mono"], anchor="center")
            lbl.pack(fill="x")
            self._coef_labels[name] = lbl

        # Ecuación general
        eq_card = CardFrame(self.left, t, padx=12, pady=10)
        eq_card.pack(fill="x", pady=(10, 0))
        Label(eq_card, text="Ecuación general", bg=t.card, fg=t.gray,
              font=t.fonts["small"]).pack(anchor="w")
        self._eq_label = Label(eq_card, text="—", bg=t.card, fg=t.fg,
                               font=t.fonts["mono_sm"],
                               wraplength=200, justify="left")
        self._eq_label.pack(anchor="w", pady=(4, 0))

        # Tipo de cónica
        cls_card = CardFrame(self.left, t, padx=12, pady=10)
        cls_card.pack(fill="x", pady=(10, 0))
        Label(cls_card, text="Tipo de cónica", bg=t.card, fg=t.gray,
              font=t.fonts["small"]).pack(anchor="w")
        self._type_label = Label(cls_card, text="—", bg=t.card,
                                  fg=t.accent, font=t.fonts["head"])
        self._type_label.pack(anchor="w", pady=(4, 0))

        # Pasos coeficientes
        SectionHeader(self.left, "Pasos — Coeficientes", t).pack(
            fill="x", pady=(16, 0))
        self.coef_steps = StepContainer(self.left, t)
        self.coef_steps.pack(fill="both", expand=True, pady=(6, 0))

    # ── Columna centro ────────────────────────────────────────────────────

    def _build_center(self):
        t = self.theme
        self.center = PanelFrame(self, t, padx=8, pady=8)
        self.center.grid(row=0, column=1, sticky="nsew")
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)
        self.graph_panel = GraphPanel(self.center, t, title="Gráfico de cónica")
        self.graph_panel.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    # ── Columna derecha ───────────────────────────────────────────────────

    def _build_right(self):
        t = self.theme
        self.right = PanelFrame(self, t, padx=12, pady=12)
        self.right.grid(row=0, column=2, sticky="nsew")

        SectionHeader(self.right, "Forma canónica", t).pack(fill="x")

        # Ecuación canónica
        can_card = CardFrame(self.right, t, padx=12, pady=10)
        can_card.pack(fill="x", pady=(10, 0))
        Label(can_card, text="Ecuación canónica", bg=t.card, fg=t.gray,
              font=t.fonts["small"]).pack(anchor="w")
        self._canonical_label = Label(can_card, text="—", bg=t.card,
                                       fg=t.accent2, font=t.fonts["mono_sm"],
                                       wraplength=270, justify="left")
        self._canonical_label.pack(anchor="w", pady=(4, 0))

        # Elementos vacíos (Entry para defensa oral)
        self._elements_card = CardFrame(self.right, t, padx=12, pady=10)
        self._elements_card.pack(fill="x", pady=(10, 0))
        Label(self._elements_card, text="Elementos", bg=t.card, fg=t.gray,
              font=t.fonts["small"]).pack(anchor="w", pady=(0, 6))
        self._elements_frame = Frame(self._elements_card, bg=t.card)
        self._elements_frame.pack(fill="x")

        # Botones para actualizar gráfico y mostrar respuesta
        btn_frame = Frame(self._elements_card, bg=t.card)
        btn_frame.pack(fill="x", pady=(8, 0))
        
        tk.Button(
            btn_frame,
            text="Actualizar gráfico",
            bg=t.card, fg=t.accent2,
            font=t.fonts["small"],
            bd=0, cursor="hand2",
            relief="flat",
            activebackground=t.panel,
            activeforeground=t.accent,
            command=self._actualizar_grafico,
        ).pack(side="left", fill="both", expand=True, padx=(0, 4))
        
        self._mostrar_respuesta_btn = tk.Button(
            btn_frame,
            text="Mostrar respuesta",
            bg=t.card, fg=t.accent,
            font=t.fonts["small"],
            bd=0, cursor="hand2",
            relief="flat",
            activebackground=t.panel,
            activeforeground=t.accent2,
            command=self._mostrar_respuesta,
            state="disabled",
        )
        self._mostrar_respuesta_btn.pack(side="left", fill="both", expand=True)

        # Tab switcher General↔Canónica
        self._build_tab_switcher(self.right)

        # Contenedor de pasos (ambas vistas comparten el mismo slot)
        self._steps_frame = Frame(self.right, bg=t.panel)
        self._steps_frame.pack(fill="both", expand=True, pady=(6, 0))
        self._steps_frame.rowconfigure(0, weight=1)
        self._steps_frame.columnconfigure(0, weight=1)

        self.canon_steps = StepContainer(self._steps_frame, t)
        self.canon_steps.grid(row=0, column=0, sticky="nsew")

        self.general_steps = StepContainer(self._steps_frame, t)
        self.general_steps.grid(row=0, column=0, sticky="nsew")

        # Mostrar tab inicial
        self._show_tab("general_canonical")

    def _build_tab_switcher(self, parent):
        t = self.theme

        switcher = Frame(parent, bg=t.panel)
        switcher.pack(fill="x", pady=(12, 0))

        # Línea separadora arriba
        Frame(switcher, bg=t.border, height=1).pack(fill="x")

        tabs_row = Frame(switcher, bg=t.panel)
        tabs_row.pack(fill="x")

        self._tab_btns = {}
        for key, label in [
            ("general_canonical", "General → Canónica"),
            ("canonical_general", "Canónica → General"),
        ]:
            btn = tk.Button(
                tabs_row, text=label,
                bg=t.panel, fg=t.gray,
                font=t.fonts["small"],
                bd=0, cursor="hand2",
                padx=10, pady=6,
                relief="flat",
                activebackground=t.card,
                activeforeground=t.fg,
                command=lambda k=key: self._show_tab(k),
            )
            btn.pack(side="left", fill="x", expand=True)
            self._tab_btns[key] = btn

        # Línea separadora abajo
        Frame(switcher, bg=t.border, height=1).pack(fill="x")

    def _show_tab(self, tab: str):
        t = self.theme
        self._active_tab = tab
        for key, btn in self._tab_btns.items():
            if key == tab:
                btn.config(bg=t.card, fg=t.accent,
                           font=t.fonts["small"])
            else:
                btn.config(bg=t.panel, fg=t.gray,
                           font=t.fonts["small"])

        if tab == "general_canonical":
            self.canon_steps.lift()
        else:
            self.general_steps.lift()

    # ── Cargar datos del pipeline ─────────────────────────────────────────

    def _load_pipeline(self, pipeline: dict):
        coefs      = pipeline["coefs"]["data"]
        classifier = pipeline["classifier"]
        transform  = pipeline["transform"]["data"]
        self._conic_type = classifier["conic_type"]

        def _fmt(val):
            if isinstance(val, float) and val == int(val):
                return str(int(val))
            return f"{val:.2f}" if isinstance(val, float) else str(val)

        self._coef_labels["A"].config(text=_fmt(coefs["A"]))
        self._coef_labels["B"].config(text=_fmt(coefs["B"]))
        self._coef_labels["C"].config(text=str(coefs["C"]))
        self._coef_labels["D"].config(text=str(coefs["D"]))
        self._coef_labels["E"].config(text=str(coefs["E"]))

        self._eq_label.config(text=coefs.get("equation_str", "—"))
        self._type_label.config(
            text=classifier["data"].get("conic_name_es", "—"))
        self._canonical_label.config(
            text=transform.get("canonical_form", "—"))

        # Guardar plotter y transform activo
        self._load_data_internals(transform)
        
        self._populate_elements(self._conic_type)
        self.coef_steps.set_steps(pipeline["coefs"]["steps"])
        self.canon_steps.set_steps(pipeline["transform"]["steps"])
        self.general_steps.set_steps(
            pipeline["to_general"]["steps"]
        )

    # ── Elementos vacíos (Entry) ──────────────────────────────────────────

    def _populate_elements(self, conic_type: str):
        t = self.theme
        frame = self._elements_frame
        for child in frame.winfo_children():
            child.destroy()

        self._element_entries = {}

        # Campos por tipo de cónica
        fields = {
            "circle":    [("Centro", "centro"), ("Radio", "radio")],
            "ellipse":   [("Centro", "centro"),  ("c",        "c"),
                          ("a",      "a"),        ("Orientación", "orientacion"),
                          ("b",      "b")],
            "hyperbola": [("Centro", "centro"),  ("c",        "c"),
                          ("a",      "a"),        ("Orientación", "orientacion"),
                          ("b",      "b")],
            "parabola":  [("Vértice", "vertice"), ("p",       "p"),
                          ("Directriz", "directriz"), ("Orientación", "orientacion")],
        }.get(conic_type, [])

        # Grid de 2 columnas
        for i, (label_text, key) in enumerate(fields):
            col = i % 2
            row = i // 2

            cell = Frame(frame, bg=t.card)
            cell.grid(row=row, column=col, sticky="ew",
                      padx=(0, 8) if col == 0 else 0, pady=3)
            frame.columnconfigure(col, weight=1)

            Label(cell, text=label_text, bg=t.card, fg=t.gray,
                  font=t.fonts["small"], anchor="w").pack(anchor="w")

            entry = Entry(
                cell,
                bg=t.panel,
                fg=t.fg,
                insertbackground=t.fg,
                font=t.fonts["mono_sm"],
                bd=0,
                relief="flat",
                highlightbackground=t.border,
                highlightthickness=1,
            )
            entry.pack(fill="x", ipady=4)
            self._element_entries[key] = entry

    # ── Helpers ───────────────────────────────────────────────────────────

    def _strings_to_steps(self, raw: list[str]) -> list[dict]:
        steps = []
        current_title = None
        current_lines = []
        for line in raw:
            line = line.strip()
            if not line:
                if current_title:
                    steps.append({
                        "title": current_title,
                        "explanation": " ".join(current_lines) or None,
                    })
                    current_title = None
                    current_lines = []
                continue
            if line.startswith("PASO") or line.startswith("[Regla"):
                if current_title:
                    steps.append({
                        "title": current_title,
                        "explanation": " ".join(current_lines) or None,
                    })
                current_title = line.rstrip(" ══")
                current_lines = []
            elif current_title is None:
                current_title = line
            else:
                current_lines.append(line)
        if current_title:
            steps.append({
                "title": current_title,
                "explanation": " ".join(current_lines) or None,
            })
        return steps


    def load_data(self, rut_result: dict):
        if self.pipeline and self.pipeline.get("valid"):
            # No renderizar la cónica aquí - esperar a que el usuario presione botones
            return

        # Fallback: construir pipeline desde rut_result
        from core.conic_pipeline import run_pipeline
        self.pipeline = run_pipeline(rut_result)
        if self.pipeline.get("valid"):
            self._load_pipeline(self.pipeline)
            # No renderizar la cónica aquí - esperar a que el usuario presione botones

    # ── Renderizado del gráfico ───────────────────────────────────────────

    def _render_graph(self):
        """Dibuja la cónica en el GraphPanel usando ConicPlotter."""
        if not self.pipeline or not self.pipeline.get("valid"):
            return

        canvas = self.graph_panel.canvas
        canvas.delete("all")
        self.graph_panel.clear_placeholder()

        # Forzar que el canvas tenga dimensiones reales
        canvas.update_idletasks()
        if canvas.winfo_width() < 10:
            self.after(100, self._render_graph)
            return

        td = self.pipeline["transform"]["data"]
        ct = self._conic_type

        plotter = ConicPlotter(canvas, self.theme)
        self._plotter = plotter

        try:
            if ct == "circle":
                plotter.plot_circle(
                    radius=td["radius"],
                    h=td["center"][0],
                    k=td["center"][1],
                )

            elif ct == "ellipse":
                if td["a2"] >= td["b2"]:
                    plotter.plot_ellipse(
                        a=td["a"], b=td["b"],
                        h=td["center"][0], k=td["center"][1],
                    )
                else:
                    plotter.plot_ellipse(
                        a=td["b"], b=td["a"],
                        h=td["center"][0], k=td["center"][1],
                    )

            elif ct == "hyperbola":
                plotter.plot_hyperbola(
                    a=td["a"], b=td["b"],
                    h=td["center"][0], k=td["center"][1],
                    orientation=td.get("orientation", "horizontal"),
                )

            elif ct == "parabola":
                plotter.plot_parabola(
                    p=td["p"],
                    h=td["vertex"][0],
                    k=td["vertex"][1],
                    orientation=td.get("orientation", "vertical"),
                )

        except Exception as e:
            canvas.create_text(
                canvas.winfo_width() // 2,
                canvas.winfo_height() // 2,
                text=f"Error al graficar:\n{e}",
                fill=self.theme.gray,
                font=self.theme.fonts["small"],
                justify="center",
            )

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

    def _actualizar_grafico(self):
        """Actualiza el gráfico con los valores ingresados en los inputs."""
        if not self.pipeline or not self.pipeline.get("valid"):
            return
        
        # Limpiar canvas
        canvas = self.graph_panel.canvas
        canvas.delete("all")
        self.graph_panel.clear_placeholder()
        
        # Forzar que el canvas tenga dimensiones reales
        canvas.update_idletasks()
        if canvas.winfo_width() < 10:
            self.after(100, self._actualizar_grafico)
            return
        
        ct = self._conic_type
        
        # Leer los valores de los inputs
        elementos = {}
        
        for key, entry in self._element_entries.items():
            value = entry.get().strip()
            if not value:
                continue
            
            try:
                # Si es una coordenada (centro o vértice)
                if key in ["centro", "vertice"]:
                    coord = self._parse_coordinate(value)
                    if coord:
                        display_key = "Centro" if key == "centro" else "Vértice"
                        elementos[display_key] = coord
            except Exception:
                pass
        
        # Si no hay elementos válidos, mostrar mensaje
        if not elementos:
            canvas.create_text(
                canvas.winfo_width() // 2,
                canvas.winfo_height() // 2,
                text="Ingresa valores de forma correcta en los campos de entrada",
                fill=self.theme.gray,
                font=self.theme.fonts["small"],
                justify="center",
            )
            return
        
        # Crear transform para el canvas
        td = self.pipeline["transform"]["data"]
        try:
            # Obtener límites según el tipo de cónica
            if ct == "circle":
                r = td.get("radius", 1)
                h, k = td.get("center", (0, 0))
                margin = 1
                x_min, x_max = h - r - margin, h + r + margin
                y_min, y_max = k - r - margin, k + r + margin
            elif ct in ["ellipse", "hyperbola"]:
                a = td.get("a", 1)
                b = td.get("b", 1)
                h, k = td.get("center", (0, 0))
                margin = 2
                x_min, x_max = h - a - margin, h + a + margin
                y_min, y_max = k - b - margin, k + b + margin
            elif ct == "parabola":
                p = td.get("p", 1)
                h, k = td.get("vertex", (0, 0))
                margin = 2
                x_min, x_max = h - 4*abs(p) - margin, h + 4*abs(p) + margin
                y_min, y_max = k - 2*abs(p) - margin, k + 4*abs(p) + margin
            else:
                return
            
            from graphics.canvas_utils import CoordinateTransform, GridDrawer
            transform = CoordinateTransform(
                canvas.winfo_width(), canvas.winfo_height(),
                x_min, x_max, y_min, y_max
            )
            
            # Dibujar grilla y ejes
            GridDrawer.draw_grid(canvas, transform, grid_spacing=1, 
                                grid_color=self.theme.border, 
                                axis_color=self.theme.gray)
            GridDrawer.draw_axis_labels(canvas, transform, self.theme, spacing=1)
            
            # Dibujar los elementos ingresados por el usuario
            plotter = ConicPlotter(canvas, self.theme)
            plotter.draw_user_elements(elementos, transform)
            
        except Exception as e:
            print(f"Error al actualizar gráfico: {e}")

    def _mostrar_respuesta(self):
        """Rellena los campos con los elementos correctos y dibuja la cónica completa."""
        if not self.pipeline or not self.pipeline.get("valid"):
            return
        
        # Limpiar canvas
        canvas = self.graph_panel.canvas
        canvas.delete("all")
        self.graph_panel.clear_placeholder()
        
        # Renderizar la cónica completa con todos sus elementos
        self._render_graph()
        
        # Rellenar campos con valores correctos
        td = self.pipeline["transform"]["data"]
        ct = self._conic_type
        
        def fmt(n):
            return str(round(n, 2))
        
        def fmt_coord(pair):
            return f"{round(pair[0], 2)},{round(pair[1], 2)}"
        
        # Mapear valores correctos a los campos de la derecha
        for key, entry in self._element_entries.items():
            entry.delete(0, "end")
            
            if ct == "circle":
                if key == "centro":
                    entry.insert(0, fmt_coord(td["center"]))
                elif key == "radio":
                    entry.insert(0, fmt(td["radius"]))
            
            elif ct == "ellipse":
                if key == "centro":
                    entry.insert(0, fmt_coord(td["center"]))
                elif key == "a":
                    entry.insert(0, fmt(td["a"]))
                elif key == "b":
                    entry.insert(0, fmt(td["b"]))
                elif key == "c":
                    entry.insert(0, fmt(td["c"]))
                elif key == "orientacion":
                    entry.insert(0, "horizontal" if td["a2"] > td["b2"] else "vertical")
            
            elif ct == "hyperbola":
                if key == "centro":
                    entry.insert(0, fmt_coord(td["center"]))
                elif key == "a":
                    entry.insert(0, fmt(td["a"]))
                elif key == "b":
                    entry.insert(0, fmt(td["b"]))
                elif key == "c":
                    entry.insert(0, fmt(td["c"]))
                elif key == "orientacion":
                    entry.insert(0, td.get("orientation", "—"))
            
            elif ct == "parabola":
                if key == "vertice":
                    entry.insert(0, fmt_coord(td["vertex"]))
                elif key == "p":
                    entry.insert(0, fmt(td["p"]))
                elif key == "orientacion":
                    entry.insert(0, td.get("orientation", "—"))

    def _update_mostrar_respuesta_btn(self):
        """Actualiza el estado del botón 'Mostrar respuesta' según los datos disponibles."""
        if not hasattr(self, '_mostrar_respuesta_btn'):
            return
        
        # Verificar si hay elementos correctos del core disponibles
        has_correct_elements = bool(self._correct_elements)
        
        # Activar botón si hay elementos correctos
        if has_correct_elements:
            self._mostrar_respuesta_btn.config(state="normal")
        else:
            self._mostrar_respuesta_btn.config(state="disabled")

    def _load_data_internals(self, transform):
        """Carga referencias internas del transform y crea CoordinateTransform."""
        # Guardar elementos correctos del core
        self._correct_elements = {}
        if "center" in transform and transform["center"]:
            center = transform["center"]
            if isinstance(center, (tuple, list)) and len(center) == 2:
                self._correct_elements["Center"] = tuple(center)
        if "vertex" in transform and transform["vertex"]:
            vertex = transform["vertex"]
            if isinstance(vertex, (tuple, list)) and len(vertex) == 2:
                self._correct_elements["Vertex"] = tuple(vertex)
        
        # Actualizar estado del botón después de cargar elementos correctos
        self._update_mostrar_respuesta_btn()
        
        # Crear transform para coordenadas
        try:
            # Obtener límites según el tipo de cónica
            if self._conic_type == "circle":
                r = transform.get("radius", 1)
                h, k = transform.get("center", (0, 0))
                margin = 1
                x_min, x_max = h - r - margin, h + r + margin
                y_min, y_max = k - r - margin, k + r + margin
            elif self._conic_type in ["ellipse", "hyperbola"]:
                a = transform.get("a", 1)
                b = transform.get("b", 1)
                h, k = transform.get("center", (0, 0))
                margin = 2
                x_min, x_max = h - a - margin, h + a + margin
                y_min, y_max = k - b - margin, k + b + margin
            elif self._conic_type == "parabola":
                p = transform.get("p", 1)
                h, k = transform.get("vertex", (0, 0))
                margin = 2
                x_min, x_max = h - 4*abs(p) - margin, h + 4*abs(p) + margin
                y_min, y_max = k - 2*abs(p) - margin, k + 4*abs(p) + margin
            else:
                return
            
            # El canvas debe tener dimensiones para crear el transform
            self.after(50, lambda: self._create_transform_when_ready(x_min, x_max, y_min, y_max))
        except Exception:
            pass

    def _create_transform_when_ready(self, x_min, x_max, y_min, y_max):
        """Crea el CoordinateTransform cuando el canvas está listo."""
        canvas = self.graph_panel.canvas
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        
        if w > 10 and h > 10:
            self._active_transform = CoordinateTransform(w, h, x_min, x_max, y_min, y_max)
        else:
            # Reintentar si el canvas no está listo
            self.after(100, lambda: self._create_transform_when_ready(x_min, x_max, y_min, y_max))

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.bg)
        self.left.update_theme(theme)
        self.center.update_theme(theme)
        self.right.update_theme(theme)
        self.graph_panel.update_theme(theme)
        self.coef_steps.update_theme(theme)
        self.canon_steps.update_theme(theme)
        self.general_steps.update_theme(theme)
