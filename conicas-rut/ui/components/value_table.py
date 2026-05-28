# conicas-rut/ui/components/value_table.py

import tkinter as tk
from ui.components.card import CardFrame


class ValueTable(CardFrame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, theme, *args, **kwargs)
        self.row_frames = []
        self._build_placeholder()

    def _build_placeholder(self):
        self.headers = tk.Frame(self, bg=self.theme.card)
        self.headers.pack(fill="x", pady=(8, 6))

        for text, weight in [("x", 1), ("y", 1), ("f(x)", 1)]:
            tk.Label(
                self.headers,
                text=text,
                bg=self.theme.card,
                fg=self.theme.accent,
                font=self.theme.fonts["mono_sm"],
                width=12,
                anchor="w",
            ).pack(side="left", padx=(0, 6))

        self.body = tk.Frame(self, bg=self.theme.card)
        self.body.pack(fill="both", expand=True)
        self.set_rows([
            ("0", "0", "0"),
            ("1", "2", "2"),
            ("2", "4", "8"),
        ])

    def set_rows(self, rows):
        for child in self.body.winfo_children():
            child.destroy()
        for row in rows:
            row_frame = tk.Frame(self.body, bg=self.theme.card)
            row_frame.pack(fill="x", pady=2)
            for value in row:
                tk.Label(
                    row_frame,
                    text=value,
                    bg=self.theme.card,
                    fg=self.theme.fg,
                    font=self.theme.fonts["mono_sm"],
                    width=12,
                    anchor="w",
                ).pack(side="left", padx=(0, 6))
            self.row_frames.append(row_frame)

    def update_theme(self, theme):
        super().update_theme(theme)
        self.headers.configure(bg=theme.card)
        self.body.configure(bg=theme.card)
        for child in self.body.winfo_children():
            try:
                child.configure(bg=theme.card)
                for label in child.winfo_children():
                    label.configure(bg=theme.card, fg=theme.fg)
            except tk.TclError:
                pass
