import tkinter as tk


class SectionHeader(tk.Frame):
    def __init__(self, master, title, theme, *args, **kwargs):
        super().__init__(master, bg=theme.panel, *args, **kwargs)
        self.theme = theme

        self.title_label = tk.Label(
            self,
            text=title,
            bg=theme.panel,
            fg=theme.fg,
            font=theme.fonts["head"],
            anchor="w",
        )
        self.title_label.pack(fill="x")

        self.underline = tk.Frame(self, bg=theme.accent, height=2)
        self.underline.pack(fill="x", pady=(6, 12))

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.panel)
        self.title_label.configure(bg=theme.panel, fg=theme.fg)
        self.underline.configure(bg=theme.accent)
