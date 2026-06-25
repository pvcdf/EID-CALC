# conicas-rut/graphics/conic_plotter.py

"""
Funciones para la graficación de cónicas (elipses, hipérbolas, parábolas).
Proporciona métodos para renderizar cónicas en su forma canónica,
mostrando focos, vértices y otros elementos especiales.
"""

from graphics.canvas_utils import CoordinateTransform, GridDrawer, ShapeDrawer

# ── Constante ─────────────────────────────────────────────────────────────────
_PI = 3.141592653589793

def _sin(x: float) -> float:
    """Seno via serie de Taylor."""
    x = x % (2 * _PI)
    if x > _PI:
        x -= 2 * _PI
    return x - x**3/6 + x**5/120 - x**7/5040 + x**9/362880


def _cos(x: float) -> float:
    """Coseno via identidad cos(x) = sin(x + π/2)."""
    return _sin(x + _PI / 2)


def _sqrt(n: float) -> float:
    """Raíz cuadrada via método de Newton-Raphson."""
    if n <= 0:
        return 0.0
    x = n
    for _ in range(50):
        x = (x + n / x) / 2
    return x


# ── Plotter ───────────────────────────────────────────────────────────────────

class ConicPlotter:
    def __init__(self, canvas, theme):
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
        margin = 2
        transform = CoordinateTransform(
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            h - a - margin, h + a + margin,
            k - b - margin, k + b + margin
        )

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1,
                             grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        # Graficar elipse parametricamente
        num_points = 200
        points = []
        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * _PI
            x_math = h + a * _cos(angle)
            y_math = k + b * _sin(angle)
            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
            if points:
                self.canvas.create_line(
                    points[-1][0], points[-1][1], x_canvas, y_canvas,
                    fill=self.theme.accent, width=2, tags="conic"
                )
            points.append((x_canvas, y_canvas))

        # Focos
        c = _sqrt(abs(a**2 - b**2))
        if a > b:
            focus1 = (h - c, k)
            focus2 = (h + c, k)
        else:
            focus1 = (h, k - c)
            focus2 = (h, k + c)

        ShapeDrawer.draw_point(self.canvas, transform, focus1[0], focus1[1],
                               self.theme.yellow, size=5, label="F₁", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, focus2[0], focus2[1],
                               self.theme.yellow, size=5, label="F₂", theme=self.theme)

        # Vértices
        ShapeDrawer.draw_point(self.canvas, transform, h - a, k,
                               self.theme.green, size=4, label="V₁", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, h + a, k,
                               self.theme.green, size=4, label="V₂", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, h, k - b,
                               self.theme.green, size=4, label="V₃", theme=self.theme)
        ShapeDrawer.draw_point(self.canvas, transform, h, k + b,
                               self.theme.green, size=4, label="V₄", theme=self.theme)

        # Centro
        ShapeDrawer.draw_point(self.canvas, transform, h, k,
                               self.theme.accent2, size=3, label="C", theme=self.theme)

    def plot_hyperbola(self, a, b, h, k, orientation="horizontal"):
        """
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

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1,
                             grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        # Asíntotas
        if orientation == "horizontal":
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=h + a)
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=h - a)
        else:
            ShapeDrawer.draw_asymptote(self.canvas, transform, y_math=k + b)
            ShapeDrawer.draw_asymptote(self.canvas, transform, y_math=k - b)

        # Ramas de la hipérbola
        num_points = 150

        if orientation == "horizontal":
            for y_offset in range(-int(b * 3), int(b * 3)):
                y_math = k + y_offset * 0.1
                if abs(y_math - k) < b * 3:
                    x_math = h + a * _sqrt(1 + ((y_math - k) / b) ** 2)
                    x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                    if y_offset > -int(b * 3):
                        prev_y = k + (y_offset - 1) * 0.1
                        prev_x = h + a * _sqrt(1 + ((prev_y - k) / b) ** 2)
                        prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                        self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas,
                                                fill=self.theme.accent, width=2, tags="conic")

            for y_offset in range(-int(b * 3), int(b * 3)):
                y_math = k + y_offset * 0.1
                if abs(y_math - k) < b * 3:
                    x_math = h - a * _sqrt(1 + ((y_math - k) / b) ** 2)
                    x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                    if y_offset > -int(b * 3):
                        prev_y = k + (y_offset - 1) * 0.1
                        prev_x = h - a * _sqrt(1 + ((prev_y - k) / b) ** 2)
                        prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                        self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas,
                                                fill=self.theme.accent, width=2, tags="conic")

            # Focos
            c = _sqrt(a**2 + b**2)
            ShapeDrawer.draw_point(self.canvas, transform, h - c, k,
                                   self.theme.yellow, size=5, label="F₁", theme=self.theme)
            ShapeDrawer.draw_point(self.canvas, transform, h + c, k,
                                   self.theme.yellow, size=5, label="F₂", theme=self.theme)

            # Vértices
            ShapeDrawer.draw_point(self.canvas, transform, h - a, k,
                                   self.theme.green, size=4, label="V₁", theme=self.theme)
            ShapeDrawer.draw_point(self.canvas, transform, h + a, k,
                                   self.theme.green, size=4, label="V₂", theme=self.theme)

        else:  # vertical
            for x_offset in range(-int(a * 3), int(a * 3)):
                x_math = h + x_offset * 0.1
                if abs(x_math - h) < a * 3:
                    y_math = k + b * _sqrt(1 + ((x_math - h) / a) ** 2)
                    x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                    if x_offset > -int(a * 3):
                        prev_x = h + (x_offset - 1) * 0.1
                        prev_y = k + b * _sqrt(1 + ((prev_x - h) / a) ** 2)
                        prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                        self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas,
                                                fill=self.theme.accent, width=2, tags="conic")

            for x_offset in range(-int(a * 3), int(a * 3)):
                x_math = h + x_offset * 0.1
                if abs(x_math - h) < a * 3:
                    y_math = k - b * _sqrt(1 + ((x_math - h) / a) ** 2)
                    x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                    if x_offset > -int(a * 3):
                        prev_x = h + (x_offset - 1) * 0.1
                        prev_y = k - b * _sqrt(1 + ((prev_x - h) / a) ** 2)
                        prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                        self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas,
                                                fill=self.theme.accent, width=2, tags="conic")

            # Focos
            c = _sqrt(a**2 + b**2)
            ShapeDrawer.draw_point(self.canvas, transform, h, k - c,
                                   self.theme.yellow, size=5, label="F₁", theme=self.theme)
            ShapeDrawer.draw_point(self.canvas, transform, h, k + c,
                                   self.theme.yellow, size=5, label="F₂", theme=self.theme)

            # Vértices
            ShapeDrawer.draw_point(self.canvas, transform, h, k - b,
                                   self.theme.green, size=4, label="V₁", theme=self.theme)
            ShapeDrawer.draw_point(self.canvas, transform, h, k + b,
                                   self.theme.green, size=4, label="V₂", theme=self.theme)

        # Centro
        ShapeDrawer.draw_point(self.canvas, transform, h, k,
                               self.theme.accent2, size=3, label="C", theme=self.theme)

    def plot_parabola(self, p, h, k, orientation="vertical"):
        """
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

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1,
                             grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        num_points = 200

        if orientation == "vertical":
            for i in range(num_points + 1):
                x_math = h - 4 * abs(p) + (i / num_points) * 8 * abs(p)
                y_math = k + (x_math - h) ** 2 / (4 * p)
                x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                if i > 0:
                    prev_x = h - 4 * abs(p) + ((i - 1) / num_points) * 8 * abs(p)
                    prev_y = k + (prev_x - h) ** 2 / (4 * p)
                    prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                    self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas,
                                            fill=self.theme.accent, width=2, tags="conic")

            # Foco y directriz
            ShapeDrawer.draw_point(self.canvas, transform, h, k + p,
                                   self.theme.yellow, size=5, label="F", theme=self.theme)
            ShapeDrawer.draw_asymptote(self.canvas, transform, y_math=k - p,
                                       color=self.theme.yellow)

        else:  # horizontal
            for i in range(num_points + 1):
                y_math = k - 4 * abs(p) + (i / num_points) * 8 * abs(p)
                x_math = h + (y_math - k) ** 2 / (4 * p)
                x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                if i > 0:
                    prev_y = k - 4 * abs(p) + ((i - 1) / num_points) * 8 * abs(p)
                    prev_x = h + (prev_y - k) ** 2 / (4 * p)
                    prev_x_c, prev_y_c = transform.math_to_canvas(prev_x, prev_y)
                    self.canvas.create_line(prev_x_c, prev_y_c, x_canvas, y_canvas,
                                            fill=self.theme.accent, width=2, tags="conic")

            # Foco y directriz
            ShapeDrawer.draw_point(self.canvas, transform, h + p, k,
                                   self.theme.yellow, size=5, label="F", theme=self.theme)
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=h - p,
                                       color=self.theme.yellow)

        # Vértice
        ShapeDrawer.draw_point(self.canvas, transform, h, k,
                               self.theme.green, size=4, label="V", theme=self.theme)

    def plot_circle(self, radius, h, k):
        """
        Args:
            radius: Radio de la circunferencia
            h: Traslación horizontal del centro
            k: Traslación vertical del centro
        """
        margin = 1
        transform = CoordinateTransform(
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            h - radius - margin, h + radius + margin,
            k - radius - margin, k + radius + margin
        )

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1,
                             grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=1)

        # Graficar circunferencia parametricamente
        num_points = 200
        points = []
        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * _PI
            x_math = h + radius * _cos(angle)
            y_math = k + radius * _sin(angle)
            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
            if points:
                self.canvas.create_line(
                    points[-1][0], points[-1][1], x_canvas, y_canvas,
                    fill=self.theme.accent, width=2, tags="conic"
                )
            points.append((x_canvas, y_canvas))

        # Centro
        ShapeDrawer.draw_point(self.canvas, transform, h, k,
                               self.theme.accent2, size=4, label="C", theme=self.theme)

        # Radio (línea desde centro a punto de la circunferencia)
        x_end = h + radius
        y_end = k
        x_canvas, y_canvas = transform.math_to_canvas(x_end, y_end)
        origin_x, origin_y = transform.math_to_canvas(h, k)
        self.canvas.create_line(origin_x, origin_y, x_canvas, y_canvas,
                                fill=self.theme.gray, width=1, dash=(2, 2), tags="conic")
        ShapeDrawer.draw_point(self.canvas, transform, x_end, y_end,
                               self.theme.green, size=3, label="P", theme=self.theme)