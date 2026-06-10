# conicas-rut/ui/components/graph_panel.py

import tkinter as tk
from ui.components.card import CardFrame


class GraphPanel(CardFrame):
    def __init__(self, master, theme, title=None, *args, **kwargs):
        super().__init__(master, theme, *args, **kwargs)
        self.theme = theme
        self._has_real_data = False  

        if title:
            tk.Label(
                self,
                text=title,
                bg=self.theme.card,
                fg=self.theme.fg,
                font=self.theme.fonts["label"],
                anchor="w",
            ).pack(fill="x", padx=10, pady=(10, 0))

        self.canvas = tk.Canvas(
            self, bg=self.theme.plot,
            highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", self._on_resize)

        self._draw_placeholder()

    def _on_resize(self, _event):
        # Solo redibuja el placeholder si no hay datos reales todavía
        if not self._has_real_data:
            self._draw_placeholder()

    def _draw_placeholder(self):
        self.canvas.delete("graphgrid")
        width  = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 40 or height < 40:
            return

        gc = self.theme.border
        ac = self.theme.gray

        for x in range(0, width, 50):
            self.canvas.create_line(
                x, 0, x, height, fill=gc, width=1, tags="graphgrid")
        for y in range(0, height, 50):
            self.canvas.create_line(
                0, y, width, y, fill=gc, width=1, tags="graphgrid")

        self.canvas.create_line(
            width // 2, 0, width // 2, height,
            fill=ac, width=2, tags="graphgrid")
        self.canvas.create_line(
            0, height // 2, width, height // 2,
            fill=ac, width=2, tags="graphgrid")

        self.canvas.create_text(
            width // 2, height // 2,
            text="[Panel de gráficos preparado]",
            fill=self.theme.gray,
            font=self.theme.fonts["label"],
            tags="graphgrid")

    def clear_placeholder(self):
        """
        Llamar antes de dibujar datos reales.
        Elimina el placeholder y desactiva su redibujado automático.
        """
        self._has_real_data = True
        self.canvas.delete("graphgrid")

    def reset(self):
        """Vuelve al estado inicial con placeholder (para reutilización)."""
        self._has_real_data = False
        self.canvas.delete("all")
        self._draw_placeholder()

    # ── Tema ──────────────────────────────────────────────────────────────

    def update_theme(self, theme):
        self.theme = theme
        super().update_theme(theme)
        self.canvas.configure(bg=self.theme.plot)
        if not self._has_real_data:
            self._draw_placeholder()