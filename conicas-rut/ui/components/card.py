import tkinter as tk


class CardFrame(tk.Frame):
    def __init__(self, master, theme, *args, **kwargs):
        bg = getattr(theme, "card", theme.bg)
        border = getattr(theme, "border", "#2E2D47")
        super().__init__(master, bg=bg, highlightbackground=border, highlightthickness=1, *args, **kwargs)
        self.theme = theme

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.card, highlightbackground=theme.border)
        for child in self.winfo_children():
            try:
                child.configure(bg=theme.card, fg=theme.fg)
            except tk.TclError:
                pass
