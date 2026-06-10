# conicas-rut/ui/components/step_display.py

import tkinter as tk
from ui.components.card import CardFrame


class StepItem(CardFrame):
    def __init__(
        self,
        master,
        title,
        explanation,
        theme,
        equation=None,
        result=None,
        observation=None,
        *args,
        **kwargs,
    ):
        super().__init__(master, theme, *args, **kwargs)
        self.theme = theme

        # ── Título ────────────────────────────────────────────────────────
        tk.Label(
            self,
            text=f"▸ {title}",
            bg=self.theme.card,
            fg=self.theme.accent,
            font=self.theme.fonts["label"],
            anchor="w",
            justify="left",
        ).pack(fill="x", padx=8, pady=(8, 4))

        # ── Explicación (texto largo) ──────────────────────────────────────
        if explanation:
            lbl = tk.Label(
                self,
                text=explanation,
                bg=self.theme.card,
                fg=self.theme.fg,
                font=self.theme.fonts["small"],
                anchor="w",
                justify="left",
                wraplength=1,           # ✓ FIX: se actualiza dinámicamente en _update_wrap
            )
            lbl.pack(fill="x", padx=12, pady=(0, 4))
            lbl.bind("<Configure>", lambda e, l=lbl: l.configure(wraplength=e.width - 4))

        # ── Ecuación ──────────────────────────────────────────────────────
        if equation:
            lbl_eq = tk.Label(
                self,
                text=equation,
                bg=self.theme.card,
                fg=self.theme.accent2,
                font=self.theme.fonts["mono"],
                anchor="w",
                justify="left",
                wraplength=1,           # ✓ FIX: mismo tratamiento
            )
            lbl_eq.pack(fill="x", padx=12, pady=(4, 4))
            lbl_eq.bind("<Configure>", lambda e, l=lbl_eq: l.configure(wraplength=e.width - 4))

        # ── Resultado ─────────────────────────────────────────────────────
        if result:
            tk.Label(
                self,
                text=f" Resultado: {result}",
                bg=self.theme.card,
                fg=self.theme.green,
                font=self.theme.fonts["label"],
                anchor="w",
                justify="left",
                wraplength=0,
            ).pack(fill="x", padx=12, pady=(4, 4))

        # ── Observación ───────────────────────────────────────────────────
        if observation:
            lbl_obs = tk.Label(
                self,
                text=f"ℹ {observation}",
                bg=self.theme.card,
                fg=self.theme.gray,
                font=self.theme.fonts["small"],
                anchor="w",
                justify="left",
                wraplength=1,
            )
            lbl_obs.pack(fill="x", padx=12, pady=(4, 8))
            lbl_obs.bind("<Configure>", lambda e, l=lbl_obs: l.configure(wraplength=e.width - 4))

    def update_theme(self, theme):
        super().update_theme(theme)
        self.theme = theme


class StepContainer(tk.Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, bg=theme.panel, *args, **kwargs)
        self.theme = theme

        self._canvas = tk.Canvas(
            self, bg=self.theme.panel, highlightthickness=0, borderwidth=0
        )
        self._vscroll = tk.Scrollbar(
            self, orient="vertical", command=self._canvas.yview
        )
        self._inner = tk.Frame(self._canvas, bg=self.theme.panel)

        self._inner_id = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw"
        )
        self._canvas.configure(yscrollcommand=self._vscroll.set)

        self._canvas.grid(row=0, column=0, sticky="nsew")
        self._vscroll.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._inner.bind("<Configure>", self._on_inner_resize)
        self._canvas.bind("<Configure>", self._on_canvas_resize)

        self.step_items = []

    def _on_inner_resize(self, _event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        # ✓ FIX: el inner siempre ocupa el ancho completo del canvas
        self._canvas.itemconfigure(self._inner_id, width=event.width)

    def add_step(
        self, title, explanation, equation=None, result=None, observation=None
    ):
        item = StepItem(
            self._inner,
            title,
            explanation,
            self.theme,
            equation=equation,
            result=result,
            observation=observation,
            pady=4,
        )
        item.pack(fill="x", pady=(0, 10), padx=4)
        self.step_items.append(item)

    def set_steps(self, steps):
        for child in self._inner.winfo_children():
            child.destroy()
        self.step_items = []
        for step in steps:
            self.add_step(
                step.get("title", "Paso"),
                step.get("explanation", ""),
                equation=step.get("equation"),
                result=step.get("result"),
                observation=step.get("observation"),
            )

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.panel)
        self._canvas.configure(bg=theme.panel)
        self._inner.configure(bg=theme.panel)
        for item in self.step_items:
            item.update_theme(theme)