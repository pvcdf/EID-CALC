# conicas-rut/graphics/conicas/conic_elements_plotter.py

"""
Plotter de elementos geométricos de cónicas.

Este módulo se encarga solo de dibujar elementos:
- centro
- vértices
- co-vértices
- focos
- ejes
- directrices
- asíntotas

"""

from core.utils.manual_math import safe_div
from graphics.utils.canvas_utils import ShapeDrawer


class ConicElementsPlotter:
    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme

    def clear_elements(self):
        """
        Limpia solo los elementos geométricos, no la cónica completa.
        """
        self.canvas.delete(
            "conic_elements",
            "element_points",
            "element_lines",
            "element_labels",
        )

    def plot_from_transform(self, conic_type: str, transform_data: dict, transform):
        """
        Dibuja los elementos geométricos calculados desde transform_data.
        """
        if not transform_data or not transform:
            return

        if transform_data.get("imaginary") or transform_data.get("degenerate"):
            return

        if conic_type == "circle":
            self._plot_circle_elements(transform_data, transform)

        elif conic_type == "ellipse":
            self._plot_ellipse_elements(transform_data, transform)

        elif conic_type == "hyperbola":
            self._plot_hyperbola_elements(transform_data, transform)

        elif conic_type == "parabola":
            self._plot_parabola_elements(transform_data, transform)

    # ── Circunferencia ─────────────────────────────────────────────────────

    def _plot_circle_elements(self, data: dict, transform):
        center = data.get("center")
        radius = data.get("radius")

        if center is None or radius is None:
            return

        h, k = center

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h,
            k,
            self.theme.accent2,
            size=4,
            label="C",
            theme=self.theme,
            tags=("conic_elements", "element_points"),
        )

        ShapeDrawer.draw_line_segment(
            self.canvas,
            transform,
            h,
            k,
            h + radius,
            k,
            color=self.theme.gray,
            width=1,
            dash=(2, 2),
            tags=("conic_elements", "element_lines"),
        )

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h + radius,
            k,
            self.theme.green,
            size=3,
            label="r",
            theme=self.theme,
            tags=("conic_elements", "element_points"),
        )

    # ── Elipse ─────────────────────────────────────────────────────────────

    def _plot_ellipse_elements(self, data: dict, transform):
        center = data.get("center")
        a = data.get("a")
        b = data.get("b")
        c = data.get("c")

        if center is None or a is None or b is None or c is None:
            return

        h, k = center
        orientation = self._ellipse_orientation(data)

        if orientation == "horizontal":
            vertices = [(h - a, k), (h + a, k)]
            covertices = [(h, k - b), (h, k + b)]
            foci = [(h - c, k), (h + c, k)]

            self._draw_horizontal_axis(transform, k, self.theme.gray)
            self._draw_vertical_axis(transform, h, self.theme.border)

        else:
            vertices = [(h, k - a), (h, k + a)]
            covertices = [(h - b, k), (h + b, k)]
            foci = [(h, k - c), (h, k + c)]

            self._draw_vertical_axis(transform, h, self.theme.gray)
            self._draw_horizontal_axis(transform, k, self.theme.border)

        self._draw_center(transform, h, k)
        self._draw_point_pair(transform, vertices, "V", self.theme.green)
        self._draw_point_pair(transform, covertices, "B", self.theme.accent2)
        self._draw_point_pair(transform, foci, "F", self.theme.yellow)

    def _ellipse_orientation(self, data: dict) -> str:
        if data.get("major_axis"):
            return data["major_axis"]

        x_radius_squared = data.get("x_radius_squared", data.get("a2", 0))
        y_radius_squared = data.get("y_radius_squared", data.get("b2", 0))

        if x_radius_squared >= y_radius_squared:
            return "horizontal"

        return "vertical"

    # ── Hipérbola ──────────────────────────────────────────────────────────

    def _plot_hyperbola_elements(self, data: dict, transform):
        center = data.get("center")
        a = data.get("a")
        b = data.get("b")
        c = data.get("c")

        if center is None or a is None or b is None or c is None:
            return

        h, k = center
        orientation = data.get("orientation", "horizontal")

        if orientation == "horizontal":
            vertices = [(h - a, k), (h + a, k)]
            foci = [(h - c, k), (h + c, k)]
            slope = safe_div(b, a)

            self._draw_horizontal_axis(transform, k, self.theme.gray)
            self._draw_vertical_axis(transform, h, self.theme.border)

        else:
            vertices = [(h, k - a), (h, k + a)]
            foci = [(h, k - c), (h, k + c)]
            slope = safe_div(a, b)

            self._draw_vertical_axis(transform, h, self.theme.gray)
            self._draw_horizontal_axis(transform, k, self.theme.border)

        ShapeDrawer.draw_oblique_asymptote(
            self.canvas,
            transform,
            h,
            k,
            slope,
            color=self.theme.red,
        )
        ShapeDrawer.draw_oblique_asymptote(
            self.canvas,
            transform,
            h,
            k,
            -slope,
            color=self.theme.red,
        )

        self._draw_center(transform, h, k)
        self._draw_point_pair(transform, vertices, "V", self.theme.green)
        self._draw_point_pair(transform, foci, "F", self.theme.yellow)

    # ── Parábola ───────────────────────────────────────────────────────────

    def _plot_parabola_elements(self, data: dict, transform):
        vertex = data.get("vertex")
        p = data.get("p")

        if vertex is None or p is None:
            return

        h, k = vertex
        orientation = data.get("orientation", "vertical")

        focus = data.get("focus")
        axis = data.get("axis")
        directrix = data.get("directrix")

        if orientation == "vertical":
            focus = focus or (h, k + p)

            self._draw_vertical_axis(transform, h, self.theme.gray)
            ShapeDrawer.draw_asymptote(
                self.canvas,
                transform,
                y_math=k - p,
                color=self.theme.yellow,
            )

            self._draw_line_label(
                transform,
                x_math=transform.math_xmin,
                y_math=k - p,
                text=directrix or f"y = {round(k - p, 2)}",
                color=self.theme.yellow,
            )

        else:
            focus = focus or (h + p, k)

            self._draw_horizontal_axis(transform, k, self.theme.gray)
            ShapeDrawer.draw_asymptote(
                self.canvas,
                transform,
                x_math=h - p,
                color=self.theme.yellow,
            )

            self._draw_line_label(
                transform,
                x_math=h - p,
                y_math=transform.math_ymax,
                text=directrix or f"x = {round(h - p, 2)}",
                color=self.theme.yellow,
            )

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h,
            k,
            self.theme.green,
            size=5,
            label="V",
            theme=self.theme,
            tags=("conic_elements", "element_points"),
        )

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            focus[0],
            focus[1],
            self.theme.yellow,
            size=5,
            label="F",
            theme=self.theme,
            tags=("conic_elements", "element_points"),
        )

        if axis:
            self._draw_axis_label(transform, h, k, axis)

    # ── Helpers de dibujo ──────────────────────────────────────────────────

    def _draw_center(self, transform, h, k):
        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h,
            k,
            self.theme.accent2,
            size=4,
            label="C",
            theme=self.theme,
            tags=("conic_elements", "element_points"),
        )

    def _draw_point_pair(self, transform, points, prefix, color):
        for index, point in enumerate(points, start=1):
            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                point[0],
                point[1],
                color,
                size=5,
                label=f"{prefix}{index}",
                theme=self.theme,
                tags=("conic_elements", "element_points"),
            )

    def _draw_horizontal_axis(self, transform, y_value, color):
        ShapeDrawer.draw_line_segment(
            self.canvas,
            transform,
            transform.math_xmin,
            y_value,
            transform.math_xmax,
            y_value,
            color=color,
            width=1,
            dash=(3, 3),
            tags=("conic_elements", "element_lines"),
        )

    def _draw_vertical_axis(self, transform, x_value, color):
        ShapeDrawer.draw_line_segment(
            self.canvas,
            transform,
            x_value,
            transform.math_ymin,
            x_value,
            transform.math_ymax,
            color=color,
            width=1,
            dash=(3, 3),
            tags=("conic_elements", "element_lines"),
        )

    def _draw_line_label(self, transform, x_math, y_math, text, color):
        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

        self.canvas.create_text(
            x_canvas + 8,
            y_canvas + 12,
            text=text,
            fill=color,
            font=self.theme.fonts["small"],
            anchor="w",
            tags=("conic_elements", "element_labels"),
        )

    def _draw_axis_label(self, transform, h, k, text):
        x_canvas, y_canvas = transform.math_to_canvas(h, k)

        self.canvas.create_text(
            x_canvas + 12,
            y_canvas + 18,
            text=text,
            fill=self.theme.gray,
            font=self.theme.fonts["small"],
            anchor="w",
            tags=("conic_elements", "element_labels"),
        )