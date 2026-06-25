# conicas-rut/graphics/canvas_utils.py

"""
Utilidades compartidas para renderizado en canvas.

Proporciona funciones para transformaciones de coordenadas, escalado y
conversión entre espacios de coordenadas matemáticas y canvas.
"""

class CoordinateTransform:
    """Gestiona la transformación entre coordenadas matemáticas y canvas."""

    def __init__(self, canvas_width, canvas_height, math_xmin, math_xmax, math_ymin, math_ymax):
        """
        Inicializa el transformador de coordenadas.

        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.math_xmin = math_xmin
        self.math_xmax = math_xmax
        self.math_ymin = math_ymin
        self.math_ymax = math_ymax

        self._calc_scale()

    def _calc_scale(self):
        """Calcula los factores de escala entre espacios de coordenadas."""
        self.scale_x = self.canvas_width / (self.math_xmax - self.math_xmin)
        self.scale_y = self.canvas_height / (self.math_ymax - self.math_ymin)
        self.offset_x = -self.math_xmin * self.scale_x
        self.offset_y = self.canvas_height + self.math_ymin * self.scale_y

    def math_to_canvas(self, x_math, y_math):
        """
        Convierte coordenadas matemáticas a coordenadas del canvas.
        """
        x_canvas = x_math * self.scale_x + self.offset_x
        y_canvas = self.offset_y - y_math * self.scale_y
        return x_canvas, y_canvas

    def canvas_to_math(self, x_canvas, y_canvas):
        """
        Convierte coordenadas del canvas a coordenadas matemáticas.

        """
        x_math = (x_canvas - self.offset_x) / self.scale_x
        y_math = (self.offset_y - y_canvas) / self.scale_y
        return x_math, y_math


class GridDrawer:
    """Dibuja grillas y ejes en un canvas."""

    @staticmethod
    def draw_grid(canvas, transform, grid_spacing=1, grid_color="#2E2D47", axis_color="#6B6A85"):
        """
        Dibuja una grilla matemática con ejes principales.

        Args:
            canvas: Canvas de tkinter
            transform: Instancia de CoordinateTransform
            grid_spacing: Espaciado en unidades matemáticas
            grid_color: Color de las líneas de grilla
            axis_color: Color de los ejes principales
        """
        # Grilla vertical
        x = transform.math_xmin
        while x <= transform.math_xmax:
            x_canvas, _ = transform.math_to_canvas(x, 0)
            canvas.create_line(
                x_canvas, 0, x_canvas, transform.canvas_height,
                fill=grid_color, width=1, tags="grid"
            )
            x += grid_spacing

        # Grilla horizontal
        y = transform.math_ymin
        while y <= transform.math_ymax:
            _, y_canvas = transform.math_to_canvas(0, y)
            canvas.create_line(
                0, y_canvas, transform.canvas_width, y_canvas,
                fill=grid_color, width=1, tags="grid"
            )
            y += grid_spacing

        # Eje X
        _, origin_y = transform.math_to_canvas(0, 0)
        canvas.create_line(0, origin_y, transform.canvas_width, origin_y, fill=axis_color, width=2, tags="axis")

        # Eje Y
        origin_x, _ = transform.math_to_canvas(0, 0)
        canvas.create_line(origin_x, 0, origin_x, transform.canvas_height, fill=axis_color, width=2, tags="axis")

    @staticmethod
    def draw_axis_labels(canvas, transform, theme, spacing=2):
        """
        Dibuja etiquetas en los ejes.

        """
        origin_x, origin_y = transform.math_to_canvas(0, 0)

        # Etiquetas en eje X
        x = transform.math_xmin
        while x <= transform.math_xmax:
            if x != 0:
                x_canvas, _ = transform.math_to_canvas(x, 0)
                canvas.create_text(
                    x_canvas, origin_y + 12, text=str(int(x)) if x == int(x) else f"{x:.1f}",
                    fill=theme.gray, font=theme.fonts["small"], tags="labels"
                )
            x += spacing

        # Etiquetas en eje Y
        y = transform.math_ymin
        while y <= transform.math_ymax:
            if y != 0:
                _, y_canvas = transform.math_to_canvas(0, y)
                canvas.create_text(
                    origin_x - 12, y_canvas, text=str(int(y)) if y == int(y) else f"{y:.1f}",
                    fill=theme.gray, font=theme.fonts["small"], anchor="e", tags="labels"
                )
            y += spacing

        # Origen
        canvas.create_text(origin_x - 8, origin_y + 12, text="0", fill=theme.gray, font=theme.fonts["small"], tags="labels")


class ShapeDrawer:
    """Dibuja formas geométricas en un canvas."""

    @staticmethod
    def draw_point(canvas, transform, x_math, y_math, color, size=4, label=None, theme=None):
        """
        Dibuja un punto en coordenadas matemáticas.

        """
        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
        canvas.create_oval(
            x_canvas - size, y_canvas - size, x_canvas + size, y_canvas + size,
            fill=color, outline="", tags="shapes"
        )
        if label and theme:
            canvas.create_text(
                x_canvas + 8, y_canvas - 8, text=label, fill=color,
                font=theme.fonts["small"], tags="labels"
            )

    @staticmethod
    def draw_line_segment(canvas, transform, x1_math, y1_math, x2_math, y2_math, color, width=2):
        """
        Dibuja un segmento de línea entre dos puntos matemáticos.

        """
        x1_canvas, y1_canvas = transform.math_to_canvas(x1_math, y1_math)
        x2_canvas, y2_canvas = transform.math_to_canvas(x2_math, y2_math)
        canvas.create_line(x1_canvas, y1_canvas, x2_canvas, y2_canvas, fill=color, width=width, tags="shapes")

    @staticmethod
    def draw_asymptote(canvas, transform, x_math=None, y_math=None, color="#F87171"):
        """
        Dibuja una asíntota (vertical u horizontal).
        """
        if x_math is not None:
            # Asíntota vertical
            x_canvas, _ = transform.math_to_canvas(x_math, 0)
            canvas.create_line(x_canvas, 0, x_canvas, transform.canvas_height, fill=color, dash=(4, 4), width=2, tags="asymptote")
        elif y_math is not None:
            # Asíntota horizontal
            _, y_canvas = transform.math_to_canvas(0, y_math)
            canvas.create_line(0, y_canvas, transform.canvas_width, y_canvas, fill=color, dash=(4, 4), width=2, tags="asymptote")

    @staticmethod
    def draw_hole(canvas, transform, x_math, y_math, color="#F87171", size=6):
        """
        Dibuja un hueco (discontinuidad removible).
        """
        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
        canvas.create_oval(
            x_canvas - size, y_canvas - size, x_canvas + size, y_canvas + size,
            fill="", outline=color, width=2, tags="shapes"
        )
