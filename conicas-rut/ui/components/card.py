# conicas-rut/ui/components/card.py

import tkinter as tk


class CardFrame(tk.Frame):
    """Marco base para componentes de tarjeta con tema personalizado."""
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, bg=theme.card, relief="flat", borderwidth=1, *args, **kwargs)
        self.theme = theme

    def update_theme(self, theme):
        """Actualiza el tema del componente."""
        self.theme = theme
        self.configure(bg=theme.card)
        for child in self.winfo_children():
            try:
                child.configure(bg=theme.card, fg=theme.fg)
            except tk.TclError:
                pass
