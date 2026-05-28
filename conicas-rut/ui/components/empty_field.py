# conicas-rut/ui/components/empty_field.py

import tkinter as tk


class EmptyState(tk.Frame):
    def __init__(self, master, theme, message="No hay datos para mostrar", *args, **kwargs):
        super().__init__(master, bg=theme.panel, *args, **kwargs)
        self.theme = theme
        tk.Label(
            self,
            text=message,
            bg=theme.panel,
            fg=theme.gray,
            font=theme.fonts["label"],
            wraplength=320,
            justify="center",
        ).pack(fill="both", expand=True, padx=24, pady=24)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.panel)
        for child in self.winfo_children():
            try:
                child.configure(bg=theme.panel, fg=theme.gray)
            except tk.TclError:
                pass
