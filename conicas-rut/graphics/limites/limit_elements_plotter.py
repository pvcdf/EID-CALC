# conicas-rut/graphics/limites/limit_elements_plotter.py

"""
Plotter de elementos especiales en funciones por tramos.

Dibuja:
- huecos removibles;
- puntos abiertos y cerrados;
- asíntotas verticales;
- etiquetas del punto crítico.
"""

from graphics.utils.canvas_utils import ShapeDrawer


class LimitElementsPlotter:
    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme

    def clear_elements(self):
        self.canvas.delete(
            "limit_elements",
            "limit_points",
            "limit_lines",
            "limit_labels",
        )

    def plot_from_analysis(self, datos: dict, analysis: dict, transform):
        """
        Dibuja elementos especiales usando los datos de CrearVariables()
        y AnalizarLimites().
        """
        if not datos or not analysis or not transform:
            return

        tipo = datos.get("tipo_discontinuidad")
        a = datos.get("a")

        if a is None:
            return

        if tipo == "removible":
            self._plot_removable(a, analysis, transform)

        elif tipo == "salto":
            self._plot_jump(a, analysis, transform)

        elif tipo == "infinita":
            self._plot_infinite(a, transform)

    def _plot_removable(self, a, analysis, transform):
        lim_value = analysis.get("lim_izquierdo")

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

    def _draw_label(self, transform, x_math, y_math, text, color):
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
        return isinstance(value, int) or isinstance(value, float)

    def _fmt(self, value) -> str:
        if isinstance(value, float):
            rounded = round(value, 3)

            if rounded == int(rounded):
                return str(int(rounded))

            return f"{rounded:.3f}"

        return str(value)