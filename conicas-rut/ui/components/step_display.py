import tkinter as tk
from ui.components.card import CardFrame


class StepItem(CardFrame):
    def __init__(self, master, title, description, theme, *args, **kwargs):
        super().__init__(master, theme, *args, **kwargs)
        self.theme = theme
        tk.Label(
            self,
            text=title,
            bg=self.theme.card,
            fg=self.theme.accent,
            font=self.theme.fonts["label"],
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            self,
            text=description,
            bg=self.theme.card,
            fg=self.theme.fg,
            font=self.theme.fonts["small"],
            wraplength=260,
            justify="left",
        ).pack(fill="x", pady=(4, 0))

    def update_theme(self, theme):
        super().update_theme(theme)
        self.theme = theme


class StepContainer(tk.Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, bg=theme.panel, *args, **kwargs)
        self.theme = theme
        self.step_items = []

    def add_step(self, title, description):
        item = StepItem(self, title, description, self.theme, pady=6)
        item.pack(fill="x", pady=(0, 6))
        self.step_items.append(item)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.panel)
        for item in self.step_items:
            item.update_theme(theme)
