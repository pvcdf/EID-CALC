# conicas-rut/graphics/conic_plotter.py
from graphics.canvas_utils import CoordinateTransform, GridDrawer, ShapeDrawer

class ConicPlotter:
    """Grafica cónicas en forma canónica."""

    def __init__(self, canvas, theme):
        """
        Inicializa el plotter de cónicas.
        """
        self.canvas = canvas
        self.theme = theme

    def clear_plot(self):
        """Limpia todos los elementos dibujados excepto grid."""
        self.canvas.delete("conic", "foci", "vertices", "labels")

    def plot_ellipse(self, a, b, h, k, rotation=0):
        """
        Grafica una elipse en forma canónica.
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
        Grafica una hipérbola en forma canónica horizontal o vertical.
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
        Grafica una parábola en forma canónica vertical o horizontal.

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
        
        else:  # horizontal
            for i in range(num_points + 1):
                y_math = k - 4 * abs(p) + (i / num_points) * 8 * abs(p)
                x_math = h + (y_math - k) ** 2 / (4 * p)
                x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                if i > 0:
                    prev_y = k - 4 * abs(p) + ((i - 1) / num_points) * 8 * abs(p)
                    prev_x = h + (prev_y - k) ** 2 / (4 * p)
                    prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                    self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas, fill=self.theme.accent, width=2, tags="conic")

            # Foco y directriz
            ShapeDrawer.draw_point(self.canvas, transform, h + p, k, self.theme.yellow, size=5, label="F", theme=self.theme)
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=h - p, color=self.theme.yellow)

        # Vértice
        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.green, size=4, label="V", theme=self.theme)

    def plot_circle(self, radius, h, k):
        """
        Grafica una circunferencia en forma canónica

        """
        margin = 1
        transform = CoordinateTransform(
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            h - radius - margin, h + radius + margin,
            k - radius - margin, k + radius + margin
        )

        # Dibujar grilla y ejes
        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1, grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        # Graficar circunferencia usando aproximación con puntos
        num_points = 200
        import math
        points = []
        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * math.pi
            x_math = h + radius * math.cos(angle)
            y_math = k + radius * math.sin(angle)
            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
            if points:
                self.canvas.create_line(
                    points[-1][0], points[-1][1], x_canvas, y_canvas,
                    fill=self.theme.accent, width=2, tags="conic"
                )
            points.append((x_canvas, y_canvas))

        # Centro
        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.accent2, size=4, label="C", theme=self.theme)

        # Radio 
        x_math = h + radius
        y_math = k
        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
        origin_x, origin_y = transform.math_to_canvas(h, k)
        self.canvas.create_line(origin_x, origin_y, x_canvas, y_canvas, fill=self.theme.gray, width=1, dash=(2, 2), tags="conic")
        ShapeDrawer.draw_point(self.canvas, transform, x_math, y_math, self.theme.green, size=3, label="P", theme=self.theme)
