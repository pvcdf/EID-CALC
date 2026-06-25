# conicas-rut/graphics/conicas/conic_elements_plotter.py

"""
Dibujo de elementos geométricos de cónicas.

- centro o vértice;
- radio de circunferencia;
- vértices;
- co-vértices;
- foco y directriz de parábola.
"""

from graphics.utils.canvas_utils import ShapeDrawer


class ConicElementsPlotter:
    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme

    def clear_elements(self):
        self.canvas.delete("conic_elements", "element_points", "element_lines", "element_labels")

    def plot_from_transform(self, conic_type: str, data: dict, transform):
        self.clear_elements()

        if not data or data.get("imaginary") or data.get("degenerate") or not transform:
            return

        if conic_type == "circle":
            self._circle(data, transform)
        elif conic_type == "ellipse":
            self._ellipse(data, transform)
        elif conic_type == "hyperbola":
            self._hyperbola(data, transform)
        elif conic_type == "parabola":
            self._parabola(data, transform)

    def _circle(self, data, transform):
        center = data.get("center")
        radius = data.get("radius")

        if center is None or radius is None:
            return

        h, k = center
        tags = ("conic_elements", "element_points")
        line_tags = ("conic_elements", "element_lines")

        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.accent2,
                               label="C", theme=self.theme, tags=tags)
        ShapeDrawer.draw_line_segment(self.canvas, transform, h, k, h + radius, k,
                                      self.theme.gray, width=1, dash=(3, 3), tags=line_tags)

    def _ellipse(self, data, transform):
        center = data.get("center")
        a = data.get("a")
        b = data.get("b")

        if center is None or a is None or b is None:
            return

        h, k = center
        orientation = data.get("major_axis", "horizontal")
        tags = ("conic_elements", "element_points")

        if orientation == "vertical":
            vertices = [(h, k - a, "V1"), (h, k + a, "V2")]
            covertices = [(h - b, k, "CV1"), (h + b, k, "CV2")]
        else:
            vertices = [(h - a, k, "V1"), (h + a, k, "V2")]
            covertices = [(h, k - b, "CV1"), (h, k + b, "CV2")]

        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.accent2,
                               label="C", theme=self.theme, tags=tags)

        for x, y, label in vertices:
            ShapeDrawer.draw_point(self.canvas, transform, x, y, self.theme.green,
                                   label=label, theme=self.theme, tags=tags)

        for x, y, label in covertices:
            ShapeDrawer.draw_point(self.canvas, transform, x, y, self.theme.yellow,
                                   label=label, theme=self.theme, tags=tags)

    def _hyperbola(self, data, transform):
        center = data.get("center")
        a = data.get("a")

        if center is None or a is None:
            return

        h, k = center
        orientation = data.get("orientation", "horizontal")
        tags = ("conic_elements", "element_points")

        vertices = [(h, k - a, "V1"), (h, k + a, "V2")] if orientation == "vertical" else [
            (h - a, k, "V1"), (h + a, k, "V2")
        ]

        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.accent2,
                               label="C", theme=self.theme, tags=tags)

        for x, y, label in vertices:
            ShapeDrawer.draw_point(self.canvas, transform, x, y, self.theme.green,
                                   label=label, theme=self.theme, tags=tags)

    def _parabola(self, data, transform):
        vertex = data.get("vertex")
        p = data.get("p")

        if vertex is None or p is None:
            return

        h, k = vertex
        orientation = data.get("orientation", "vertical")
        focus = data.get("focus", (h + p, k) if orientation == "horizontal" else (h, k + p))
        tags = ("conic_elements", "element_points")
        line_tags = ("conic_elements", "element_lines")

        ShapeDrawer.draw_point(self.canvas, transform, h, k, self.theme.accent2,
                               label="V", theme=self.theme, tags=tags)
        ShapeDrawer.draw_point(self.canvas, transform, focus[0], focus[1], self.theme.green,
                               label="F", theme=self.theme, tags=tags)

        if orientation == "horizontal":
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=h - p,
                                       color=self.theme.red, tags=line_tags)
        else:
            ShapeDrawer.draw_asymptote(self.canvas, transform, y_math=k - p,
                                       color=self.theme.red, tags=line_tags)