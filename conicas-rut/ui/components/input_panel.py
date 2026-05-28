# conicas-rut/ui/components/input_panel.py

import tkinter as tk
from ui.components.card import CardFrame


class InputPanel(CardFrame):
    def __init__(self, master, theme, title, button_text, command, *args, **kwargs):
        super().__init__(master, theme, *args, **kwargs)
        self.theme = theme

        tk.Label(
            self,
            text=title,
            bg=self.theme.card,
            fg=self.theme.fg,
            font=self.theme.fonts["head"],
        ).pack(anchor="center", padx=18, pady=(28, 20))

        self.entry_container = tk.Frame(self, bg=self.theme.card)
        self.entry_container.pack(fill="x", padx=24, pady=(0, 18))

        self.entry = tk.Entry(
            self.entry_container,
            bg=self.theme.panel,
            fg=self.theme.fg,
            insertbackground=self.theme.fg,
            font=self.theme.fonts["label"],
            bd=0,
            relief="flat",
            justify="center",
            width=24,
            highlightbackground=self.theme.border,
            highlightthickness=1,
        )
        self.entry.pack(side="top", ipady=12, padx=0)

        self.action_button = tk.Button(
            self.entry_container,
            text=button_text,
            bg=self.theme.accent,
            fg=self.theme.bg,
            font=self.theme.fonts["head"],
            bd=0,
            cursor="hand2",
            padx=32,
            pady=12,
            activebackground=self.theme.accent2,
            activeforeground=self.theme.bg,
            command=command,
        )
        self.action_button.pack(side="top", pady=(18, 0))

        self.status_label = tk.Label(
            self,
            text="",
            bg=self.theme.card,
            fg=self.theme.red,
            font=self.theme.fonts["small"],
        )
        self.status_label.pack(anchor="center", padx=18, pady=(0, 4))

    def set_status(self, text, color=None):
        self.status_label.configure(text=text, fg=color or self.theme.red)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.card, highlightbackground=theme.border)
        self.entry_container.configure(bg=theme.card)
        self.entry.configure(bg=theme.panel, fg=theme.fg, insertbackground=theme.fg,
                              highlightbackground=theme.border)
        self.action_button.configure(bg=theme.accent, fg=theme.bg,
                                     activebackground=theme.accent2)
        self.status_label.configure(bg=theme.card, fg=theme.red)
