# conicas-rut/graphics/conicas/conic_elements_plotter.py

from graphics.utils.canvas_utils import ShapeDrawer


# ── Plotter de elementos geométricos de cónicas ────────────────────────────
# Dibuja elementos derivados de la forma canónica:
# centro, vértices, co-vértices, foco, radio y directriz.

class ConicElementsPlotter:
    """Dibuja los elementos geométricos principales sobre la gráfica de la cónica."""

    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme

    def clear_elements(self):
        """Limpia solo los elementos geométricos, sin borrar la curva principal."""
        self.canvas.delete(
            "conic_elements",
            "element_points",
            "element_lines",
            "element_labels",
        )

    def plot_from_transform(self, conic_type: str, data: dict, transform):
        """Dibuja elementos reales según el tipo de cónica y sus datos canónicos."""
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

    # ── Elementos reales por cónica ────────────────────────────────────────

    def _circle(self, data, transform):
        """Dibuja centro y radio de una circunferencia."""
        center = data.get("center")
        radius = data.get("radius")

        if center is None or radius is None:
            return

        h, k = center
        tags = ("conic_elements", "element_points")
        line_tags = ("conic_elements", "element_lines")

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h,
            k,
            self.theme.accent2,
            label="C",
            theme=self.theme,
            tags=tags,
        )

        ShapeDrawer.draw_line_segment(
            self.canvas,
            transform,
            h,
            k,
            h + radius,
            k,
            self.theme.gray,
            width=1,
            dash=(3, 3),
            tags=line_tags,
        )

    def _ellipse(self, data, transform):
        """Dibuja centro, vértices y co-vértices de una elipse."""
        center = data.get("center")
        a = data.get("a")  # semieje mayor
        b = data.get("b")  # semieje menor

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

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h,
            k,
            self.theme.accent2,
            label="C",
            theme=self.theme,
            tags=tags,
        )

        for x, y, label in vertices:
            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                x,
                y,
                self.theme.green,
                label=label,
                theme=self.theme,
                tags=tags,
            )

        for x, y, label in covertices:
            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                x,
                y,
                self.theme.yellow,
                label=label,
                theme=self.theme,
                tags=tags,
            )

    def _hyperbola(self, data, transform):
        """Dibuja centro y vértices de una hipérbola."""
        center = data.get("center")
        a = data.get("a")  # semieje transversal

        if center is None or a is None:
            return

        h, k = center
        orientation = data.get("orientation", "horizontal")
        tags = ("conic_elements", "element_points")

        if orientation == "vertical":
            vertices = [(h, k - a, "V1"), (h, k + a, "V2")]
        else:
            vertices = [(h - a, k, "V1"), (h + a, k, "V2")]

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h,
            k,
            self.theme.accent2,
            label="C",
            theme=self.theme,
            tags=tags,
        )

        for x, y, label in vertices:
            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                x,
                y,
                self.theme.green,
                label=label,
                theme=self.theme,
                tags=tags,
            )

    def _parabola(self, data, transform):
        """Dibuja vértice, foco y directriz de una parábola."""
        vertex = data.get("vertex")
        p = data.get("p")  # distancia del vértice al foco

        if vertex is None or p is None:
            return

        h, k = vertex
        orientation = data.get("orientation", "vertical")
        focus = data.get(
            "focus",
            (h + p, k) if orientation == "horizontal" else (h, k + p),
        )

        tags = ("conic_elements", "element_points")
        line_tags = ("conic_elements", "element_lines")

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            h,
            k,
            self.theme.accent2,
            label="V",
            theme=self.theme,
            tags=tags,
        )

        ShapeDrawer.draw_point(
            self.canvas,
            transform,
            focus[0],
            focus[1],
            self.theme.green,
            label="F",
            theme=self.theme,
            tags=tags,
        )

        if orientation == "horizontal":
            ShapeDrawer.draw_asymptote(
                self.canvas,
                transform,
                x_math=h - p,
                color=self.theme.red,
                tags=line_tags,
            )
        else:
            ShapeDrawer.draw_asymptote(
                self.canvas,
                transform,
                y_math=k - p,
                color=self.theme.red,
                tags=line_tags,
            )

    # ── Elementos ingresados por el usuario ────────────────────────────────

    def plot_attempt_elements(self, conic_type: str, data: dict, transform):
        """Dibuja elementos aproximados ingresados por el usuario sin borrar los reales."""
        if not data or not transform:
            return

        tags = ("attempt_elements", "element_points")
        line_tags = ("attempt_elements", "element_lines")

        if conic_type == "circle":
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
                label="C",
                theme=self.theme,
                tags=tags,
            )

            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                h + radius,
                k,
                self.theme.accent,
                label=None,
                theme=self.theme,
                tags=tags,
            )

            ShapeDrawer.draw_line_segment(
                self.canvas,
                transform,
                h,
                k,
                h + radius,
                k,
                color=self.theme.gray,
                dash=(3, 3),
                tags=line_tags,
            )

        elif conic_type in ("ellipse", "hyperbola"):
            center = data.get("center")
            a = data.get("a")
            orientation = data.get("orientation") or data.get("major_axis") or "horizontal"

            if center is None or a is None:
                return

            h, k = center

            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                h,
                k,
                self.theme.accent2,
                label="C",
                theme=self.theme,
                tags=tags,
            )

            if orientation == "vertical":
                vx, vy = h, k + a
            else:
                vx, vy = h + a, k

            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                vx,
                vy,
                self.theme.green,
                label="V",
                theme=self.theme,
                tags=tags,
            )

            ShapeDrawer.draw_line_segment(
                self.canvas,
                transform,
                h,
                k,
                vx,
                vy,
                color=self.theme.gray,
                dash=(3, 3),
                tags=line_tags,
            )

        elif conic_type == "parabola":
            vertex = data.get("vertex")
            p = data.get("p")
            orientation = data.get("orientation", "vertical")

            if vertex is None or p is None:
                return

            h, k = vertex

            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                h,
                k,
                self.theme.accent2,
                label="V",
                theme=self.theme,
                tags=tags,
            )

            if orientation == "horizontal":
                focus = (h + p, k)
            else:
                focus = (h, k + p)

            ShapeDrawer.draw_point(
                self.canvas,
                transform,
                focus[0],
                focus[1],
                self.theme.green,
                label="F",
                theme=self.theme,
                tags=tags,
            )

            ShapeDrawer.draw_line_segment(
                self.canvas,
                transform,
                h,
                k,
                focus[0],
                focus[1],
                color=self.theme.gray,
                dash=(3, 3),
                tags=line_tags,
            )
