import tkinter as tk


class PanelFrame(tk.Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, bg=theme.panel, *args, **kwargs)
        self.theme = theme

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.panel)
        for child in self.winfo_children():
            try:
                child.configure(bg=theme.panel, fg=theme.fg)
            except tk.TclError:
                pass
