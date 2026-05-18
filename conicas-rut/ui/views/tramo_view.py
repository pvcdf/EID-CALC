from tkinter import Frame, Label, Canvas


class TramoView(Frame):
    """Placeholder view for Funciones por Tramos section.

    Provides left summary, center graph placeholder and right value table placeholder.
    """

    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme = theme
        self._build()

    def _build(self):
        self.columnconfigure(1, weight=1)

        left = Frame(self, bg=self.theme.panel, padx=12, pady=12)
        left.grid(row=0, column=0, sticky="nsew")
        Label(left, text="Función generada", bg=self.theme.panel, fg=self.theme.fg).pack(anchor="w")

        center = Frame(self, bg=self.theme.bg, padx=8, pady=8)
        center.grid(row=0, column=1, sticky="nsew")
        self.canvas = Canvas(center, bg=self.theme.bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_text(220, 140, text="[Gráfica - función por tramos]", fill=self.theme.muted)

        right = Frame(self, bg=self.theme.panel, padx=12, pady=12)
        right.grid(row=0, column=2, sticky="nsew")
        Label(right, text="Tabla de valores", bg=self.theme.panel, fg=self.theme.fg).pack(anchor="w")

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.bg)
        for child in self.winfo_children():
            try:
                child.configure(bg=theme.panel)
            except Exception:
                pass
        self.canvas.configure(bg=theme.bg)
