# conicas-rut/ui/components/graph_panel.py

import tkinter as tk

from ui.components.card import CardFrame


class GraphPanel(CardFrame):
    def __init__(self, master, theme, title=None, *args, **kwargs):
        super().__init__(master, theme, *args, **kwargs)
        self.theme = theme
        self._has_real_data = False
        self._resize_callback = None

        self.title_label = None

        if title:
            self.title_label = tk.Label(
                self,
                text=title,
                bg=self.theme.card,
                fg=self.theme.fg,
                font=self.theme.fonts["label"],
                anchor="w",
            )
            self.title_label.pack(fill="x", padx=10, pady=(10, 0))

        self.canvas = tk.Canvas(
            self,
            bg=self.theme.plot,
            highlightthickness=0,
            borderwidth=0,
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", self._on_resize)

        self._draw_placeholder()

    def _on_resize(self, _event):
        if self._has_real_data and callable(self._resize_callback):
            self._resize_callback()
            return

        if not self._has_real_data:
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
            self.canvas.create_line(
                x,
                0,
                x,
                height,
                fill=grid_color,
                width=1,
                tags="graphgrid",
            )

        for y in range(0, height, 50):
            self.canvas.create_line(
                0,
                y,
                width,
                y,
                fill=grid_color,
                width=1,
                tags="graphgrid",
            )

        self.canvas.create_line(
            width // 2,
            0,
            width // 2,
            height,
            fill=axis_color,
            width=2,
            tags="graphgrid",
        )
        self.canvas.create_line(
            0,
            height // 2,
            width,
            height // 2,
            fill=axis_color,
            width=2,
            tags="graphgrid",
        )

        self.canvas.create_text(
            width // 2,
            height // 2,
            text="[Panel de gráficos]",
            fill=self.theme.gray,
            font=self.theme.fonts["label"],
            tags="graphgrid",
        )

    def clear_placeholder(self):
        """
        Elimina el placeholder y marca el panel como listo para datos reales.
        """
        self._has_real_data = True
        self.canvas.delete("graphgrid")

    def clear_graph(self):
        """
        Limpia todo el canvas y mantiene el estado de gráfico real.
        Útil antes de redibujar una cónica o función.
        """
        self._has_real_data = True
        self.canvas.delete("all")

    def reset(self):
        """Vuelve al estado inicial con placeholder."""
        self._has_real_data = False
        self._resize_callback = None
        self.canvas.delete("all")
        self._draw_placeholder()

    def set_resize_callback(self, callback):
        """
        Define una función para redibujar cuando el canvas cambie de tamaño.
        """
        self._resize_callback = callback

    def has_real_data(self) -> bool:
        return self._has_real_data

    def get_canvas(self):
        return self.canvas

    def update_theme(self, theme):
        self.theme = theme
        super().update_theme(theme)

        if self.title_label is not None:
            self.title_label.configure(
                bg=self.theme.card,
                fg=self.theme.fg,
            )

        self.canvas.configure(bg=self.theme.plot)

        if not self._has_real_data:
            self._draw_placeholder()