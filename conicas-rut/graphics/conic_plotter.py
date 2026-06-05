"""
Funciones para la graficación de cónicas (elipses, hipérbolas, parábolas).

Proporciona métodos para renderizar cónicas en su forma canónica,
mostrando focos, vértices y otros elementos especiales.
"""

from graphics.canvas_utils import CoordinateTransform, GridDrawer, ShapeDrawer

class ConicPlotter:
    """Grafica cónicas en forma canónica."""

    def __init__(self, canvas, theme):
        """
        Inicializa el plotter de cónicas.

        Args:
            canvas: Canvas de tkinter donde se dibujará
            theme: Objeto de tema con colores y fuentes
        """
        self.canvas = canvas
        self.theme = theme

    def clear_plot(self):
        """Limpia todos los elementos dibujados excepto grid."""
        self.canvas.delete("conic", "foci", "vertices", "labels")

    def plot_ellipse(self, a, b, h, k, rotation=0):
        """
        Grafica una elipse en forma canónica (x-h)²/a² + (y-k)²/b² = 1.

        Args:
            a: Semi-eje mayor (o semieje en dirección X)
            b: Semi-eje menor (o semieje en dirección Y)
            h: Traslación horizontal del centro
            k: Traslación vertical del centro
            rotation: Ángulo de rotación en grados (futuro)
        """
        # Configurar transformada de coordenadas
        margin = 2
        transform = CoordinateTransform(
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            h - a - margin, h + a + margin,
            k - b - margin, k + b + margin
        )

        # Dibujar grilla y ejes
        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1, grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        # Graficar elipse usando aproximación con puntos
        num_points = 200
        points = []
        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * 3.14159
            x_math = h + a * __import__("math").cos(angle)
            y_math = k + b * __import__("math").sin(angle)
            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
            if points:
                self.canvas.create_line(
                    points[-1][0], points[-1][1], x_canvas, y_canvas,
                    fill=self.theme.accent, width=2, tags="conic"
                )
            points.append((x_canvas, y_canvas))

        # Dibujar focos
        c = __import__("math").sqrt(abs(a**2 - b**2))
        if a > b:
            focus1 = (h - c, k)
            focus2 = (h + c, k)
        else:
            focus1 = (h, k - c)
            focus2 = (h, k + c)

        ShapeDrawer.draw_point(self.canvas, transform, focus1[0], focus1[1], self.theme.yellow, size=5, label="F₁", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, focus2[0], focus2[1], self.theme.yellow, size=5, label="F₂", theme=self.theme)

        # Dibujar vértices
        ShapeDrawer.draw_point(self.canvas, transform, h - a, k, self.theme.green, size=4, label="V₁", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, h + a, k, self.theme.green, size=4, label="V₂", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, h, k - b, self.theme.green, size=4, label="V₃", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, h, k + b, self.theme.green, size=4, label="V₄", theme=self.theme)

        # Centro
        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.accent2, size=3, label="C", theme=self.theme)

    def plot_hyperbola(self, a, b, h, k, orientation="horizontal"):
        """
        Grafica una hipérbola en forma canónica.
        (x-h)²/a² - (y-k)²/b² = 1 (horizontal) o (y-k)²/a² - (x-h)²/b² = 1 (vertical).

        Args:
            a: Semi-eje transversal
            b: Semi-eje conjugado
            h: Traslación horizontal del centro
            k: Traslación vertical del centro
            orientation: "horizontal" o "vertical"
        """
        margin = 2
        transform = CoordinateTransform(
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            h - a - margin, h + a + margin,
            k - b - margin, k + b + margin
        )

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1, grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        # Dibujar asíntotas
        if orientation == "horizontal":
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=h + a)
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=h - a)
        else:
            ShapeDrawer.draw_asymptote(self.canvas, transform, y_math=k + b)
            ShapeDrawer.draw_asymptote(self.canvas, transform, y_math=k - b)

        # Graficar ramas de la hipérbola
        num_points = 150
        import math

        if orientation == "horizontal":
            # Rama derecha
            for y_offset in range(-int(b * 3), int(b * 3)):
                y_math = k + y_offset * 0.1
                if abs(y_math - k) < b * 3:
                    x_math = h + a * math.sqrt(1 + ((y_math - k) / b) ** 2)
                    x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                    if y_offset > -int(b * 3):
                        prev_y = k + (y_offset - 1) * 0.1
                        prev_x = h + a * math.sqrt(1 + ((prev_y - k) / b) ** 2)
                        prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                        self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas, fill=self.theme.accent, width=2, tags="conic")

            # Rama izquierda
            for y_offset in range(-int(b * 3), int(b * 3)):
                y_math = k + y_offset * 0.1
                if abs(y_math - k) < b * 3:
                    x_math = h - a * math.sqrt(1 + ((y_math - k) / b) ** 2)
                    x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                    if y_offset > -int(b * 3):
                        prev_y = k + (y_offset - 1) * 0.1
                        prev_x = h - a * math.sqrt(1 + ((prev_y - k) / b) ** 2)
                        prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                        self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas, fill=self.theme.accent, width=2, tags="conic")

            # Focos
            c = math.sqrt(a**2 + b**2)
            ShapeDrawer.draw_point(self.canvas, transform, h - c, k, self.theme.yellow, size=5, label="F₁", theme=self.theme)
            ShapeDrawer.draw_point(self.canvas, transform, h + c, k, self.theme.yellow, size=5, label="F₂", theme=self.theme)

            # Vértices
            ShapeDrawer.draw_point(self.canvas, transform, h - a, k, self.theme.green, size=4, label="V₁", theme=self.theme)
            ShapeDrawer.draw_point(self.canvas, transform, h + a, k, self.theme.green, size=4, label="V₂", theme=self.theme)

        # Centro
        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.accent2, size=3, label="C", theme=self.theme)

    def plot_parabola(self, p, h, k, orientation="vertical"):
        """
        Grafica una parábola en forma canónica.
        (x-h)² = 4p(y-k) (vertical) o (y-k)² = 4p(x-h) (horizontal).

        Args:
            p: Distancia focal
            h: Traslación horizontal del vértice
            k: Traslación vertical del vértice
            orientation: "vertical" u "horizontal"
        """
        margin = 2
        if orientation == "vertical":
            transform = CoordinateTransform(
                self.canvas.winfo_width(), self.canvas.winfo_height(),
                h - 4 * abs(p) - margin, h + 4 * abs(p) + margin,
                k - 2 * abs(p) - margin, k + 4 * abs(p) + margin
            )
        else:
            transform = CoordinateTransform(
                self.canvas.winfo_width(), self.canvas.winfo_height(),
                h - 4 * abs(p) - margin, h + 4 * abs(p) + margin,
                k - 2 * abs(p) - margin, k + 2 * abs(p) + margin
            )

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1, grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        # Graficar parábola
        num_points = 200
        import math

        if orientation == "vertical":
            for i in range(num_points + 1):
                x_math = h - 4 * abs(p) + (i / num_points) * 8 * abs(p)
                y_math = k + (x_math - h) ** 2 / (4 * p)
                x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                if i > 0:
                    prev_x = h - 4 * abs(p) + ((i - 1) / num_points) * 8 * abs(p)
                    prev_y = k + (prev_x - h) ** 2 / (4 * p)
                    prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                    self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas, fill=self.theme.accent, width=2, tags="conic")

            # Foco y directriz
            ShapeDrawer.draw_point(self.canvas, transform, h, k + p, self.theme.yellow, size=5, label="F", theme=self.theme)
            ShapeDrawer.draw_asymptote(self.canvas, transform, y_math=k - p, color=self.theme.yellow)

        # Vértice
        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.green, size=4, label="V", theme=self.theme)

    def clear_user_elements(self):
        """Limpia todos los elementos de entrada del usuario."""
        self.canvas.delete("user_input")

    def draw_user_elements(self, elements, transform):
        """
        Dibuja elementos ingresados por el usuario (centro, foco, vértice).
        
        Args:
            elements: Dict con claves 'centro', 'foco', 'vertice' y tuplas (x, y) como valores
            transform: CoordinateTransform para convertir coordenadas matemáticas a canvas
        """
        import math
        
        # Primero limpiar elementos anteriores
        self.canvas.delete("user_input")
        
        # Colores para cada tipo de elemento
        colors = {
            "centro": self.theme.accent2,  # Acento 2 (podría ser blanco/neutro)
            "foco": self.theme.yellow,
            "vertice": self.theme.green
        }
        
        # Dibujar cada elemento
        for clave, coord in elements.items():
            if coord and len(coord) == 2:
                x_math, y_math = coord
                x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                color = colors.get(clave, self.theme.fg)
                
                # Dibujar círculo pequeño
                radius = 4
                self.canvas.create_oval(
                    x_canvas - radius, y_canvas - radius,
                    x_canvas + radius, y_canvas + radius,
                    fill=color, outline=color, tags="user_input"
                )
                
                # Dibujar etiqueta
                label_map = {"centro": "C", "foco": "F", "vertice": "V"}
                label = label_map.get(clave, clave[0].upper())
                self.canvas.create_text(
                    x_canvas + 8, y_canvas - 8,
                    text=label, fill=color, font=("Arial", 9, "bold"),
                    tags="user_input"
                )
