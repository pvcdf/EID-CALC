# conicas-rut/ui/components/result_section.py

import tkinter as tk
from ui.components.card import CardFrame
from ui.components.header import SectionHeader


class ResultSection(CardFrame):
    def __init__(self, master, theme, title, *args, **kwargs):
        super().__init__(master, theme, *args, **kwargs)
        self.header = SectionHeader(self, title, theme)
        self.header.pack(fill="x", padx=12, pady=(12, 8))
        self.body = tk.Frame(self, bg=theme.card)
        self.body.pack(fill="both", expand=True, padx=14, pady=(0, 12))

    def add_line(self, text):
        tk.Label(
            self.body,
            text=f"• {text}",
            bg=self.theme.card,
            fg=self.theme.fg,
            font=self.theme.fonts["label"],
            wraplength=240,
            justify="left",
        ).pack(anchor="w", pady=6)

    def update_theme(self, theme):
        super().update_theme(theme)
        self.header.update_theme(theme)
        self.body.configure(bg=theme.card)
