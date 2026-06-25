# conicas-rut/graphics/conicas/conic_plotter.py

"""
Plotter principal de curvas cónicas.

Los elementos geométricos especiales, como focos, vértices, ejes,
directrices y asíntotas, quedan separados
"""

from core.utils.manual_math import (
    PI,
    abs_value,
    cos_taylor,
    sin_taylor,
    sqrt_newton,
)
from graphics.utils.canvas_utils import CoordinateTransform, GridDrawer


class ConicPlotter:
    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme
        self.last_transform = None

    def clear_plot(self):
        """
        Limpia la curva, la grilla y elementos asociados al gráfico.
        """
        self.canvas.delete(
            "grid",
            "axis",
            "labels",
            "conic",
            "conic_elements",
            "element_points",
            "element_lines",
            "element_labels",
            "asymptote",
            "shapes",
        )

    def _draw_base(self, transform, spacing=None):
        spacing = spacing or GridDrawer.auto_spacing(transform)
        label_spacing = spacing * 2 if spacing < 10 else spacing

        GridDrawer.draw_grid(
            self.canvas, transform,
            grid_spacing=spacing,
            grid_color=self.theme.border,
            axis_color=self.theme.gray,
        )

        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=label_spacing)

    def _make_transform(self, x_min, x_max, y_min, y_max):
        """
        Crea y guarda la transformación de coordenadas usada por el gráfico.
        """
        transform = CoordinateTransform(
            self.canvas.winfo_width(),
            self.canvas.winfo_height(),
            x_min,
            x_max,
            y_min,
            y_max,
        )

        self.last_transform = transform

        return transform

    def _draw_message(self, text):
        """
        Muestra un mensaje centrado en el canvas.
        """
        self.clear_plot()

        width = max(self.canvas.winfo_width(), 300)
        height = max(self.canvas.winfo_height(), 220)

        self.canvas.create_text(
            width / 2,
            height / 2,
            text=text,
            fill=self.theme.gray,
            font=self.theme.fonts["body"],
            tags="labels",
            width=width - 40,
            justify="center",
        )

    # ── Circunferencia ─────────────────────────────────────────────────────

    def plot_circle(self, radius, h, k):
        """
        Grafica la curva de una circunferencia.

        Forma canónica:
            (x−h)² + (y−k)² = r²
        """
        self.clear_plot()

        radius = abs_value(radius)

        if radius <= 0:
            self._draw_message(
                "No se puede graficar la circunferencia: radio no positivo."
            )
            return None

        margin = max(1, radius * 0.25)

        transform = self._make_transform(
            h - radius - margin,
            h + radius + margin,
            k - radius - margin,
            k + radius + margin,
        )

        self._draw_base(transform)

        num_points = 260
        previous = None

        for index in range(num_points + 1):
            angle = (index / num_points) * 2 * PI

            x_math = h + radius * cos_taylor(angle)
            y_math = k + radius * sin_taylor(angle)

            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

            if previous is not None:
                self.canvas.create_line(
                    previous[0],
                    previous[1],
                    x_canvas,
                    y_canvas,
                    fill=self.theme.accent,
                    width=2,
                    tags="conic",
                )

            previous = (x_canvas, y_canvas)

        return transform

    # ── Elipse ─────────────────────────────────────────────────────────────

    def plot_ellipse(self, a, b, h, k, rotation=0, major_axis=None):
        """
        Grafica la curva de una elipse.

        Compatibilidad:
            major_axis == "horizontal":
                a se interpreta como semieje mayor horizontal.
                b se interpreta como semieje menor vertical.

            major_axis == "vertical":
                a se interpreta como semieje mayor vertical.
                b se interpreta como semieje menor horizontal.

            major_axis == None:
                a se interpreta como radio en x.
                b se interpreta como radio en y.
        """
        self.clear_plot()

        a = abs_value(a)
        b = abs_value(b)

        if a <= 0 or b <= 0:
            self._draw_message(
                "No se puede graficar la elipse: semiejes no positivos."
            )
            return None

        if major_axis == "vertical":
            x_radius = b
            y_radius = a
        else:
            x_radius = a
            y_radius = b

        margin = 2

        transform = self._make_transform(
            h - x_radius - margin,
            h + x_radius + margin,
            k - y_radius - margin,
            k + y_radius + margin,
        )

        self._draw_base(transform)

        num_points = 260
        previous = None

        for index in range(num_points + 1):
            angle = (index / num_points) * 2 * PI

            x_math = h + x_radius * cos_taylor(angle)
            y_math = k + y_radius * sin_taylor(angle)

            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

            if previous is not None:
                self.canvas.create_line(
                    previous[0],
                    previous[1],
                    x_canvas,
                    y_canvas,
                    fill=self.theme.accent,
                    width=2,
                    tags="conic",
                )

            previous = (x_canvas, y_canvas)

        return transform

    # ── Hipérbola ──────────────────────────────────────────────────────────

    def plot_hyperbola(self, a, b, h, k, orientation="horizontal"):
        """
        Grafica las ramas de una hipérbola.

        Horizontal:
            (x−h)²/a² − (y−k)²/b² = 1

        Vertical:
            (y−k)²/a² − (x−h)²/b² = 1
        """
        self.clear_plot()

        a = abs_value(a)
        b = abs_value(b)

        if a <= 0 or b <= 0:
            self._draw_message(
                "No se puede graficar la hipérbola: semiejes no positivos."
            )
            return None

        margin = 2
        span_x = max(a * 4, b * 4, 6)
        span_y = max(a * 4, b * 4, 6)

        transform = self._make_transform(
            h - span_x - margin,
            h + span_x + margin,
            k - span_y - margin,
            k + span_y + margin,
        )

        self._draw_base(transform)

        if orientation == "vertical":
            self._plot_hyperbola_vertical(transform, a, b, h, k)
        else:
            self._plot_hyperbola_horizontal(transform, a, b, h, k)

        return transform

    def _plot_hyperbola_horizontal(self, transform, a, b, h, k):
        """
        Dibuja:
            (x−h)²/a² − (y−k)²/b² = 1

        Despeje:
            x = h ± a√(1 + ((y−k)²/b²))
        """
        y_min = transform.math_ymin
        y_max = transform.math_ymax
        num_points = 280

        for side in (1, -1):
            previous = None

            for index in range(num_points + 1):
                y_math = y_min + (index / num_points) * (y_max - y_min)
                inside = 1 + ((y_math - k) / b) ** 2
                x_math = h + side * a * sqrt_newton(inside)

                x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

                if previous is not None:
                    self.canvas.create_line(
                        previous[0],
                        previous[1],
                        x_canvas,
                        y_canvas,
                        fill=self.theme.accent,
                        width=2,
                        tags="conic",
                    )

                previous = (x_canvas, y_canvas)

    def _plot_hyperbola_vertical(self, transform, a, b, h, k):
        """
        Dibuja:
            (y−k)²/a² − (x−h)²/b² = 1

        Despeje:
            y = k ± a√(1 + ((x−h)²/b²))
        """
        x_min = transform.math_xmin
        x_max = transform.math_xmax
        num_points = 280

        for side in (1, -1):
            previous = None

            for index in range(num_points + 1):
                x_math = x_min + (index / num_points) * (x_max - x_min)
                inside = 1 + ((x_math - h) / b) ** 2
                y_math = k + side * a * sqrt_newton(inside)

                x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

                if previous is not None:
                    self.canvas.create_line(
                        previous[0],
                        previous[1],
                        x_canvas,
                        y_canvas,
                        fill=self.theme.accent,
                        width=2,
                        tags="conic",
                    )

                previous = (x_canvas, y_canvas)

    # ── Parábola ───────────────────────────────────────────────────────────

    def plot_parabola(self, p, h, k, orientation="vertical"):
        """
        Grafica la curva de una parábola.

        Vertical:
            (x−h)² = 4p(y−k)

        Horizontal:
            (y−k)² = 4p(x−h)
        """
        self.clear_plot()

        if p == 0:
            self._draw_message("No se puede graficar la parábola: p = 0.")
            return None

        p_abs = abs_value(p)
        span = max(4 * p_abs, 5)

        transform = self._make_transform(
            h - span,
            h + span,
            k - span,
            k + span,
        )

        self._draw_base(transform)

        if orientation == "horizontal":
            self._plot_parabola_horizontal(transform, p, h, k, span)
        else:
            self._plot_parabola_vertical(transform, p, h, k, span)

        return transform

    def _plot_parabola_vertical(self, transform, p, h, k, span):
        """
        Dibuja:
            (x−h)² = 4p(y−k)

        Despeje:
            y = k + (x−h)²/(4p)
        """
        num_points = 260
        previous = None

        for index in range(num_points + 1):
            x_math = h - span + (index / num_points) * (2 * span)
            y_math = k + (x_math - h) ** 2 / (4 * p)

            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

            if previous is not None:
                self.canvas.create_line(
                    previous[0],
                    previous[1],
                    x_canvas,
                    y_canvas,
                    fill=self.theme.accent,
                    width=2,
                    tags="conic",
                )

            previous = (x_canvas, y_canvas)

    def _plot_parabola_horizontal(self, transform, p, h, k, span):
        """
        Dibuja:
            (y−k)² = 4p(x−h)

        Despeje:
            x = h + (y−k)²/(4p)
        """
        num_points = 260
        previous = None

        for index in range(num_points + 1):
            y_math = k - span + (index / num_points) * (2 * span)
            x_math = h + (y_math - k) ** 2 / (4 * p)

            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

            if previous is not None:
                self.canvas.create_line(
                    previous[0],
                    previous[1],
                    x_canvas,
                    y_canvas,
                    fill=self.theme.accent,
                    width=2,
                    tags="conic",
                )

            previous = (x_canvas, y_canvas)