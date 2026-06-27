# conicas-rut/graphics/limites/tramo_plotter.py

"""
Plotter principal de funciones por tramos.

Los elementos especiales de límites, como huecos, puntos cerrados,
puntos abiertos y asíntotas, se dibujan en LimitElementsPlotter.
"""

from graphics.utils.canvas_utils import CoordinateTransform, GridDrawer


class TramoPlotter:
    """Dibuja funciones continuas o por tramos sobre un plano cartesiano."""

    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme
        self.last_transform = None

    def clear_plot(self):
        """Limpia el gráfico completo de funciones por tramos."""
        self.canvas.delete(
            "grid",
            "axis",
            "labels",
            "function",
            "piecewise",
            "limit_elements",
            "limit_points",
            "limit_lines",
            "limit_labels",
            "hole",
            "asymptote",
            "shapes",
        )

    # ── Base cartesiana ────────────────────────────────────────────────────

    def _make_transform(self, x_min, x_max, y_min, y_max):
        """Crea la transformación entre coordenadas matemáticas y canvas."""
        transform = CoordinateTransform(
            self.canvas.winfo_width(),
            self.canvas.winfo_height(),
            x_min,
            x_max,
            y_min,
            y_max,
            keep_aspect=False,
        )

        self.last_transform = transform
        return transform

    def _draw_base(self, transform, spacing=1):
        """Dibuja grilla, ejes y etiquetas."""
        GridDrawer.draw_grid(
            self.canvas,
            transform,
            grid_spacing=spacing,
            grid_color=self.theme.border,
            axis_color=self.theme.gray,
        )

        GridDrawer.draw_axis_labels(
            self.canvas,
            transform,
            self.theme,
            spacing=spacing,
        )

    def _draw_message(self, text):
        """Dibuja un mensaje centrado en el canvas."""
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

    # ── Función única ──────────────────────────────────────────────────────

    def plot_function(
        self,
        function,
        x_min=-10,
        x_max=10,
        y_min=-10,
        y_max=10,
        samples=700,
    ):
        """Dibuja una función continua aproximada en un intervalo."""
        self.clear_plot()

        if not callable(function):
            self._draw_message("No se puede graficar: función inválida.")
            return None

        if x_min == x_max or y_min == y_max:
            self._draw_message("No se puede graficar: ventana inválida.")
            return None

        transform = self._make_transform(x_min, x_max, y_min, y_max)
        self._draw_base(transform)

        self._draw_function_segment(
            function=function,
            transform=transform,
            x_start=x_min,
            x_end=x_max,
            samples=samples,
            tag="function",
        )

        return transform

    # ── Función por tramos ─────────────────────────────────────────────────

    def plot_piecewise(
        self,
        pieces,
        x_min=-10,
        x_max=10,
        y_min=-10,
        y_max=10,
        samples_per_piece=350,
    ):
        """
        Dibuja una función por tramos.

        Cada tramo debe incluir:
            "func": función evaluable
            "x_min": inicio del intervalo
            "x_max": fin del intervalo
        """
        self.clear_plot()

        if not pieces:
            self._draw_message("No hay tramos para graficar.")
            return None

        if x_min == x_max or y_min == y_max:
            self._draw_message("No se puede graficar: ventana inválida.")
            return None

        transform = self._make_transform(x_min, x_max, y_min, y_max)
        self._draw_base(transform)

        for piece in pieces:
            function = piece.get("func")

            if not callable(function):
                continue

            piece_x_min = piece.get("x_min", x_min)
            piece_x_max = piece.get("x_max", x_max)

            start = max(piece_x_min, x_min)
            end = min(piece_x_max, x_max)

            if start >= end:
                continue

            self._draw_function_segment(
                function=function,
                transform=transform,
                x_start=start,
                x_end=end,
                samples=samples_per_piece,
                tag="piecewise",
            )

        return transform

    # ── Muestreo y dibujo ──────────────────────────────────────────────────

    def _draw_function_segment(
        self,
        function,
        transform,
        x_start,
        x_end,
        samples=350,
        tag="function",
    ):
        """
        Dibuja un segmento usando muestreo.

        Si aparece error, None o un valor fuera del rango visible,
        se corta el trazo para evitar líneas falsas entre ramas.
        """
        previous = None

        for index in range(samples + 1):
            x_math = x_start + (index / samples) * (x_end - x_start)

            try:
                y_math = function(x_math)

            except (ZeroDivisionError, ValueError, OverflowError):
                previous = None
                continue

            if y_math is None:
                previous = None
                continue

            if not self._is_number(y_math):
                previous = None
                continue

            if not self._is_visible_y(y_math, transform):
                previous = None
                continue

            x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

            if previous is not None:
                self.canvas.create_line(
                    previous[0],
                    previous[1],
                    x_canvas,
                    y_canvas,
                    fill=self.theme.accent,
                    width=2,
                    tags=tag,
                )

            previous = (x_canvas, y_canvas)

    # ── Validaciones internas ──────────────────────────────────────────────

    def _is_number(self, value) -> bool:
        """Verifica que el valor sea numérico."""
        return isinstance(value, int) or isinstance(value, float)

    def _is_visible_y(self, y_value, transform) -> bool:
        """Evita dibujar puntos demasiado alejados del rango visible."""
        margin = (transform.math_ymax - transform.math_ymin) * 0.25

        return (
            transform.math_ymin - margin
            <= y_value
            <= transform.math_ymax + margin
        )