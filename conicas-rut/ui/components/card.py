# conicas-rut/ui/components/card.py

import tkinter as tk


class CardFrame(tk.Frame):
    """Marco base para componentes tipo tarjeta."""

    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(
            master,
            bg=theme.card,
            relief="flat",
            borderwidth=1,
            *args,
            **kwargs,
        )
        self.theme = theme

    def update_theme(self, theme):
        """Actualiza el color base de la tarjeta."""
        self.theme = theme
        self.configure(bg=theme.card)