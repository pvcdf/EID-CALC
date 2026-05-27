"""
Funciones para la graficación de funciones por tramos.

Proporciona métodos para renderizar funciones definidas a trozos,
mostrando discontinuidades, huecos, asíntotas y valores puntuales.
"""

from graphics.canvas_utils import CoordinateTransform, GridDrawer, ShapeDrawer

class TramoPlotter:
    """Grafica funciones definidas por tramos."""

    def __init__(self, canvas, theme):
        """
        Inicializa el plotter de funciones por tramos.

        Args:
            canvas: Canvas de tkinter donde se dibujará
            theme: Objeto de tema con colores y fuentes
        """
        self.canvas = canvas
        self.theme = theme

    def clear_plot(self):
        """Limpia todos los elementos dibujados excepto grid."""
        self.canvas.delete("function", "discontinuity", "hole", "labels")

    def plot_function(self, func, x_min, x_max, y_min, y_max, num_points=300):
        """
        Grafica una función continua.

        Args:
            func: Función callable que toma x y retorna y
            x_min, x_max: Rango en X
            y_min, y_max: Rango en Y
            num_points: Número de puntos para aproximación
        """
        transform = CoordinateTransform(
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            x_min, x_max, y_min, y_max
        )

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1, grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=2)

        # Graficar función
        prev_x_canvas, prev_y_canvas = None, None
        for i in range(num_points + 1):
            x_math = x_min + (i / num_points) * (x_max - x_min)
            try:
                y_math = func(x_math)
                if y_min <= y_math <= y_max:
                    x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                    if prev_x_canvas is not None:
                        self.canvas.create_line(
                            prev_x_canvas, prev_y_canvas, x_canvas, y_canvas,
                            fill=self.theme.accent, width=2, tags="function"
                        )
                    prev_x_canvas, prev_y_canvas = x_canvas, y_canvas
                else:
                    prev_x_canvas, prev_y_canvas = None, None
            except (ValueError, ZeroDivisionError):
                prev_x_canvas, prev_y_canvas = None, None

    def plot_piecewise(self, pieces, x_min, x_max, y_min, y_max):
        """
        Grafica una función definida por tramos.

        Args:
            pieces: Lista de diccionarios con estructura:
                {
                    "func": callable,
                    "x_min": float,
                    "x_max": float,
                    "color": str (opcional, default accent),
                    "discontinuity_type": str (opcional: "jump", "infinite", "removable")
                }
            x_min, x_max: Rango global en X
            y_min, y_max: Rango global en Y
        """
        transform = CoordinateTransform(
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            x_min, x_max, y_min, y_max
        )

        GridDrawer.draw_grid(self.canvas, transform, grid_spacing=1, grid_color=self.theme.border, axis_color=self.theme.gray)
        GridDrawer.draw_axis_labels(self.canvas, transform, self.theme, spacing=2)

        # Graficar cada tramo
        for piece in pieces:
            func = piece.get("func")
            piece_x_min = max(piece.get("x_min", x_min), x_min)
            piece_x_max = min(piece.get("x_max", x_max), x_max)
            color = piece.get("color", self.theme.accent)
            num_points = 150

            prev_x_canvas, prev_y_canvas = None, None
            for i in range(num_points + 1):
                x_math = piece_x_min + (i / num_points) * (piece_x_max - piece_x_min)
                try:
                    y_math = func(x_math)
                    if y_min <= y_math <= y_max:
                        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)
                        if prev_x_canvas is not None:
                            self.canvas.create_line(
                                prev_x_canvas, prev_y_canvas, x_canvas, y_canvas,
                                fill=color, width=2, tags="function"
                            )
                        prev_x_canvas, prev_y_canvas = x_canvas, y_canvas
                    else:
                        prev_x_canvas, prev_y_canvas = None, None
                except (ValueError, ZeroDivisionError):
                    prev_x_canvas, prev_y_canvas = None, None

            # Marcar discontinuidad
            disc_type = piece.get("discontinuity_type")
            if disc_type:
                self._draw_discontinuity(transform, piece_x_max, disc_type)

    def _draw_discontinuity(self, transform, x_math, disc_type):
        """
        Dibuja una discontinuidad en el gráfico.

        Args:
            transform: Instancia de CoordinateTransform
            x_math: Coordenada X donde ocurre la discontinuidad
            disc_type: "jump", "infinite" o "removable"
        """
        x_canvas, _ = transform.math_to_canvas(x_math, 0)

        if disc_type == "jump":
            # Línea punteada vertical para salto
            self.canvas.create_line(
                x_canvas, 0, x_canvas, transform.canvas_height,
                fill=self.theme.red, dash=(4, 4), width=2, tags="discontinuity"
            )

        elif disc_type == "infinite":
            # Asíntota vertical
            ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=x_math, color=self.theme.red)

        elif disc_type == "removable":
            # Hueco (círculo vacío)
            try:
                y_math = self.last_y_value
                ShapeDrawer.draw_hole(self.canvas, transform, x_math, y_math, color=self.theme.red, size=6)
            except AttributeError:
                pass

    def add_point(self, transform, x_math, y_math, color=None, label=None):
        """
        Añade un punto especial al gráfico.

        Args:
            transform: Instancia de CoordinateTransform
            x_math, y_math: Coordenadas matemáticas
            color: Color del punto (default: accent)
            label: Etiqueta opcional
        """
        if color is None:
            color = self.theme.accent
        ShapeDrawer.draw_point(self.canvas, transform, x_math, y_math, color, size=4, label=label, theme=self.theme)

    def add_discontinuity_point(self, transform, x_math, y_math):
        """
        Añade un punto de discontinuidad removible.

        Args:
            transform: Instancia de CoordinateTransform
            x_math, y_math: Coordenadas matemáticas del hueco
        """
        ShapeDrawer.draw_hole(self.canvas, transform, x_math, y_math, color=self.theme.red, size=5)

    def add_asymptote(self, transform, x_math=None, y_math=None):
        """
        Añade una asíntota al gráfico.

        Args:
            transform: Instancia de CoordinateTransform
            x_math: Si es vertical, coordenada X
            y_math: Si es horizontal, coordenada Y
        """
        ShapeDrawer.draw_asymptote(self.canvas, transform, x_math=x_math, y_math=y_math, color=self.theme.yellow)
