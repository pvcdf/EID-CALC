# conicas-rut/graphics/limites/limit_elements_plotter.py

"""
Dibuja elementos especiales del análisis de límites:
huecos removibles, puntos abiertos, puntos cerrados,
asíntotas verticales y etiquetas del punto crítico.
"""

from graphics.utils.canvas_utils import ShapeDrawer


class LimitElementsPlotter:
    """Dibuja sobre la gráfica los elementos asociados a discontinuidades."""

    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme

    def clear_elements(self):
        """Limpia solo elementos de límites, sin borrar la función."""
        self.canvas.delete(
            "limit_elements",
            "limit_points",
            "limit_lines",
            "limit_labels",
        )

    def plot_from_analysis(self, datos: dict, analysis: dict, transform):
        """Dibuja elementos especiales usando CrearVariables() y AnalizarLimites()."""
        if not datos or not analysis or not transform:
            return

        tipo = datos.get("tipo_discontinuidad")
        a = datos.get("a")  # punto crítico

        if a is None:
            return

        if tipo == "removible":
            self._plot_removable(a, analysis, transform)
        elif tipo == "salto":
            self._plot_jump(a, analysis, transform)
        elif tipo == "infinita":
            self._plot_infinite(a, transform)

    # ── Tipos de discontinuidad ────────────────────────────────────────────

    def _plot_removable(self, a, analysis, transform):
        """Dibuja el hueco de una discontinuidad removible."""
        lim_value = analysis.get("lim_izquierdo")  # valor del límite bilateral

        if not self._is_numeric(lim_value):
            return

        ShapeDrawer.draw_hole(
            self.canvas,
            transform,
            a,
            lim_value,
            color=self.theme.red,
            size=6,
        )

        self._draw_label(
            transform,
            a,
            lim_value,
            f"hueco ({a}, {self._fmt(lim_value)})",
            self.theme.red,
        )

    def _plot_jump(self, a, analysis, transform):
        """Dibuja punto abierto y punto cerrado en una discontinuidad de salto."""
        lim_izq = analysis.get("lim_izquierdo")
        lim_der = analysis.get("lim_derecho")
        valor = analysis.get("valor_en_punto")

        if self._is_numeric(lim_izq):
            ShapeDrawer.draw_hole(
                self.canvas,
                transform,
                a,
                lim_izq,
                color=self.theme.red,
                size=5,
            )

            self._draw_label(
                transform,
                a,
                lim_izq,
                f"lím⁻ = {self._fmt(lim_izq)}",
                self.theme.red,
            )

        if self._is_numeric(valor):
            y_closed = valor
            label = f"f({a}) = {self._fmt(valor)}"
        elif self._is_numeric(lim_der):
            y_closed = lim_der
            label = f"f({a}) = {self._fmt(lim_der)}"
        else:
            return

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            a,
            y_closed,
            color=self.theme.accent2,
            size=5,
            label=None,
            theme=self.theme,
            tags=("limit_elements", "limit_points"),
        )

        self._draw_label(
            transform,
            a,
            y_closed,
            label,
            self.theme.accent2,
        )

    def _plot_infinite(self, a, transform):
        """Dibuja la asíntota vertical x = a."""
        ShapeDrawer.draw_asymptote(
            self.canvas,
            transform,
            x_math=a,
            color=self.theme.red,
        )

        self._draw_label(
            transform,
            a,
            transform.math_ymax,
            f"x = {a}",
            self.theme.red,
        )

    # ── Utilidades internas ────────────────────────────────────────────────

    def _draw_label(self, transform, x_math, y_math, text, color):
        """Dibuja una etiqueta cerca de un punto matemático."""
        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

        self.canvas.create_text(
            x_canvas + 8,
            y_canvas - 10,
            text=text,
            fill=color,
            font=self.theme.fonts["small"],
            anchor="w",
            tags=("limit_elements", "limit_labels"),
        )

    def _is_numeric(self, value) -> bool:
        """Verifica si un valor puede graficarse como coordenada."""
        return isinstance(value, int) or isinstance(value, float)

    def _fmt(self, value) -> str:
        """Formatea números para etiquetas del gráfico."""
        if isinstance(value, float):
            rounded = round(value, 3)

            if rounded == int(rounded):
                return str(int(rounded))

            return f"{rounded:.3f}"

        return str(value)