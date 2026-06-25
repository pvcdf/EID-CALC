# conicas-rut/graphics/utils/canvas_utils.py


class CoordinateTransform:
    """Transforma coordenadas matemáticas a coordenadas de canvas y viceversa."""

    def __init__(self, canvas_width, canvas_height, math_xmin, math_xmax, math_ymin, math_ymax):
        self.canvas_width = max(int(canvas_width), 300)
        self.canvas_height = max(int(canvas_height), 220)

        self.math_xmin = math_xmin
        self.math_xmax = math_xmax if math_xmax != math_xmin else math_xmin + 1
        self.math_ymin = math_ymin
        self.math_ymax = math_ymax if math_ymax != math_ymin else math_ymin + 1

        self._calc_scale()

    def _calc_scale(self):
        self.scale_x = self.canvas_width / (self.math_xmax - self.math_xmin)
        self.scale_y = self.canvas_height / (self.math_ymax - self.math_ymin)
        self.offset_x = -self.math_xmin * self.scale_x
        self.offset_y = self.canvas_height + self.math_ymin * self.scale_y

    def math_to_canvas(self, x_math, y_math):
        x_canvas = x_math * self.scale_x + self.offset_x
        y_canvas = self.offset_y - y_math * self.scale_y
        return x_canvas, y_canvas

    def canvas_to_math(self, x_canvas, y_canvas):
        x_math = (x_canvas - self.offset_x) / self.scale_x
        y_math = (self.offset_y - y_canvas) / self.scale_y
        return x_math, y_math


class GridDrawer:
    """Dibuja grilla cartesiana, ejes y etiquetas."""

    @staticmethod
    def draw_grid(canvas, transform, grid_spacing=1, grid_color="#2E2D47", axis_color="#6B6A85"):
        if grid_spacing <= 0:
            grid_spacing = 1

        x = int(transform.math_xmin) - 1
        while x <= transform.math_xmax + 1:
            x_canvas, _ = transform.math_to_canvas(x, 0)
            canvas.create_line(x_canvas, 0, x_canvas, transform.canvas_height,
                               fill=grid_color, width=1, tags="grid")
            x += grid_spacing

        y = int(transform.math_ymin) - 1
        while y <= transform.math_ymax + 1:
            _, y_canvas = transform.math_to_canvas(0, y)
            canvas.create_line(0, y_canvas, transform.canvas_width, y_canvas,
                               fill=grid_color, width=1, tags="grid")
            y += grid_spacing

        origin_x, origin_y = transform.math_to_canvas(0, 0)
        canvas.create_line(0, origin_y, transform.canvas_width, origin_y,
                           fill=axis_color, width=2, tags="axis")
        canvas.create_line(origin_x, 0, origin_x, transform.canvas_height,
                           fill=axis_color, width=2, tags="axis")

    @staticmethod
    def draw_axis_labels(canvas, transform, theme, spacing=2):
        if spacing <= 0:
            spacing = 1

        origin_x, origin_y = transform.math_to_canvas(0, 0)

        x = int(transform.math_xmin) - 1
        while x <= transform.math_xmax + 1:
            if x != 0:
                x_canvas, _ = transform.math_to_canvas(x, 0)
                canvas.create_text(x_canvas, origin_y + 12, text=_fmt_axis_value(x),
                                   fill=theme.gray, font=theme.fonts["small"], tags="labels")
            x += spacing

        y = int(transform.math_ymin) - 1
        while y <= transform.math_ymax + 1:
            if y != 0:
                _, y_canvas = transform.math_to_canvas(0, y)
                canvas.create_text(origin_x - 12, y_canvas, text=_fmt_axis_value(y),
                                   fill=theme.gray, font=theme.fonts["small"],
                                   anchor="e", tags="labels")
            y += spacing

        canvas.create_text(origin_x - 8, origin_y + 12, text="0",
                           fill=theme.gray, font=theme.fonts["small"], tags="labels")


class ShapeDrawer:
    """Dibuja formas geométricas usando coordenadas matemáticas."""

    @staticmethod
    def draw_point(canvas, transform, x_math, y_math, color, size=4, label=None,
                   theme=None, tags=("shapes",), label_tags=None):
        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

        canvas.create_oval(x_canvas - size, y_canvas - size, x_canvas + size, y_canvas + size,
                           fill=color, outline="", tags=tags)

        if label and theme:
            canvas.create_text(x_canvas + 8, y_canvas - 8, text=label, fill=color,
                               font=theme.fonts["small"],
                               tags=label_tags or _merge_tags(tags, ("labels",)))

    @staticmethod
    def draw_open_point(canvas, transform, x_math, y_math, color, size=5, label=None,
                        theme=None, tags=("shapes", "hole"), label_tags=None):
        x_canvas, y_canvas = transform.math_to_canvas(x_math, y_math)

        canvas.create_oval(x_canvas - size, y_canvas - size, x_canvas + size, y_canvas + size,
                           fill="", outline=color, width=2, tags=tags)

        if label and theme:
            canvas.create_text(x_canvas + 8, y_canvas - 8, text=label, fill=color,
                               font=theme.fonts["small"],
                               tags=label_tags or _merge_tags(tags, ("labels",)))

    @staticmethod
    def draw_line_segment(canvas, transform, x1_math, y1_math, x2_math, y2_math,
                          color, width=2, dash=None, tags=("shapes",)):
        x1_canvas, y1_canvas = transform.math_to_canvas(x1_math, y1_math)
        x2_canvas, y2_canvas = transform.math_to_canvas(x2_math, y2_math)

        canvas.create_line(x1_canvas, y1_canvas, x2_canvas, y2_canvas,
                           fill=color, width=width, dash=dash, tags=tags)

    @staticmethod
    def draw_asymptote(canvas, transform, x_math=None, y_math=None, color="#F87171",
                       tags=("asymptote", "shapes")):
        if x_math is not None:
            x_canvas, _ = transform.math_to_canvas(x_math, 0)
            canvas.create_line(x_canvas, 0, x_canvas, transform.canvas_height,
                               fill=color, dash=(4, 4), width=2, tags=tags)
            return

        if y_math is not None:
            _, y_canvas = transform.math_to_canvas(0, y_math)
            canvas.create_line(0, y_canvas, transform.canvas_width, y_canvas,
                               fill=color, dash=(4, 4), width=2, tags=tags)

    @staticmethod
    def draw_oblique_asymptote(canvas, transform, h, k, slope, color="#F87171",
                               tags=("asymptote", "shapes")):
        x1 = transform.math_xmin
        x2 = transform.math_xmax
        y1 = k + slope * (x1 - h)
        y2 = k + slope * (x2 - h)

        ShapeDrawer.draw_line_segment(canvas, transform, x1, y1, x2, y2,
                                      color=color, width=2, dash=(4, 4), tags=tags)

    @staticmethod
    def draw_hole(canvas, transform, x_math, y_math, color="#F87171", size=6,
                  tags=("shapes", "hole"), label=None, theme=None):
        ShapeDrawer.draw_open_point(canvas, transform, x_math, y_math, color=color,
                                    size=size, label=label, theme=theme, tags=tags)


def _fmt_axis_value(value):
    return str(int(value)) if value == int(value) else f"{value:.1f}"


def _merge_tags(base_tags, extra_tags):
    base = tuple(base_tags) if isinstance(base_tags, (tuple, list)) else (base_tags,)
    extra = tuple(extra_tags) if isinstance(extra_tags, (tuple, list)) else (extra_tags,)
    return base + tuple(tag for tag in extra if tag not in base)