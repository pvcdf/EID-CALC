# conicas-rut/ui/components/graph_panel.py

import tkinter as tk
from ui.components.card import CardFrame


class GraphPanel(CardFrame):
    def __init__(self, master, theme, title=None, *args, **kwargs):
        super().__init__(master, theme, *args, **kwargs)
        self.theme = theme

        if title:
            tk.Label(
                self,
                text=title,
                bg=self.theme.card,
                fg=self.theme.fg,
                font=self.theme.fonts["label"],
                anchor="w",
            ).pack(fill="x", padx=10, pady=(10, 0))

        self.canvas = tk.Canvas(self, bg=self.theme.plot, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", self._on_resize)

        self._draw_placeholder()

    def _on_resize(self, _event):
        self._draw_placeholder()

    def _draw_placeholder(self):
        self.canvas.delete("graphgrid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 40 or height < 40:
            return

        grid_color = self.theme.border
        axis_color = self.theme.gray
        for x in range(0, width, 50):
            self.canvas.create_line(x, 0, x, height, fill=grid_color, width=1, tags="graphgrid")
        for y in range(0, height, 50):
            self.canvas.create_line(0, y, width, y, fill=grid_color, width=1, tags="graphgrid")

        self.canvas.create_line(width // 2, 0, width // 2, height, fill=axis_color, width=2, tags="graphgrid")
        self.canvas.create_line(0, height // 2, width, height // 2, fill=axis_color, width=2, tags="graphgrid")

        self.canvas.create_text(
            20, 20,
            text="ejes",
            fill=axis_color,
            font=self.theme.fonts["small"],
            anchor="nw",
            tags="graphgrid"
        )
        self.canvas.create_text(
            width - 20,
            height - 20,
            text="puntos / discontinuidades",
            fill=self.theme.gray,
            font=self.theme.fonts["small"],
            anchor="se",
            tags="graphgrid"
        )
        self.canvas.create_text(
            width // 2,
            height // 2,
            text="[Panel de gráficos preparado]",
            fill=self.theme.gray,
            font=self.theme.fonts["label"],
            tags="graphgrid"
        )

    def update_theme(self, theme):
        self.theme = theme
        super().update_theme(theme)
        self.canvas.configure(bg=self.theme.plot)
        self._draw_placeholder()

    def draw_point(self, x, y, label=None):
        self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=self.theme.accent, outline="", tags="graphgrid")
        if label:
            self.canvas.create_text(x + 8, y - 8, text=label, fill=self.theme.fg, font=self.theme.fonts["small"], tags="graphgrid")

    def draw_discontinuity(self, x1, x2):
        self.canvas.create_line(x1, 0, x1, self.canvas.winfo_height(), fill=self.theme.red, dash=(4, 4), tags="graphgrid")
        self.canvas.create_line(x2, 0, x2, self.canvas.winfo_height(), fill=self.theme.red, dash=(4, 4), tags="graphgrid")
