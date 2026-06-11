# conicas-rut/ui/views/validation_view.py

import tkinter as tk

class ValidationView(tk.Frame):
    """
    muestra el paso a pasodel algoritmo módulo 11 antes de entrar a la app principal.
    """

    def __init__(self, master, theme, rut_result: dict, on_continue, *args, **kwargs):
        super().__init__(master, bg=theme.bg, *args, **kwargs)
        self.theme = theme
        self.rut_result = rut_result
        self.on_continue = on_continue
        self._build()

    # ── Construcción ──────────────────────────────────────────────────────

    def _build(self):
        t = self.theme
        self._build_topbar()

        body = tk.Frame(self, bg=t.bg)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=0, minsize=550)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_sidebar(body)
        self._build_steps_panel(body)

    def _build_topbar(self):
        t = self.theme
        topbar = tk.Frame(self, bg=t.panel, height=56)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        logo_row = tk.Frame(topbar, bg=t.panel)
        logo_row.place(rely=0.5, anchor="w", x=24)

        tk.Label(logo_row, text="◈", bg=t.panel, fg=t.accent,
                 font=t.fonts["label"]).pack(side="left", padx=(0, 6))
        tk.Label(logo_row, text="CónicasRUT", bg=t.panel, fg=t.fg,
                 font=t.fonts["label"]).pack(side="left")

        rut = self.rut_result["data"]["clean_rut"]
        tk.Label(logo_row, text=f"  ·  {rut}", bg=t.panel, fg=t.gray,
                 font=t.fonts["small"]).pack(side="left")

    def _build_sidebar(self, parent):
        t = self.theme
        left = tk.Frame(parent, bg=t.panel)
        left.grid(row=0, column=0, sticky="nsew")

        tk.Label(left, text="Validación", bg=t.panel, fg=t.accent,
                 font=t.fonts["head"]).pack(anchor="w", padx=24, pady=(32, 4))
        tk.Frame(left, bg=t.accent, height=2).pack(fill="x", padx=24, pady=(0, 20))

        rut = self.rut_result["data"]["clean_rut"]
        v   = self.rut_result["data"]["v"]
        exp = self.rut_result["explanation"]

        self._info_card(left, "RUT ingresado",      rut,  t.accent, t.fonts["head"])
        self._info_card(left, "Variable auxiliar v", str(v), t.accent2, t.fonts["big"])
        self._info_card(left, "Resultado",           exp,  t.green,  t.fonts["label"],
                        wrap=200)

        btn_frame = tk.Frame(left, bg=t.panel)
        btn_frame.pack(side="bottom", fill="x", padx=16, pady=24)
        tk.Button(
            btn_frame, text="Continuar  →",
            bg=t.accent, fg=t.bg,
            font=t.fonts["head"],
            bd=0, cursor="hand2",
            pady=12,
            activebackground=t.accent2,
            activeforeground=t.bg,
            command=self.on_continue,
        ).pack(fill="x")

    def _info_card(self, parent, label_text, value_text, value_color, value_font,
                   accent_color=None, wrap=None):
        t = self.theme
        color = accent_color or value_color

        card = tk.Frame(parent, bg=t.card)
        card.pack(fill="x", padx=16, pady=(0, 12))

        tk.Frame(card, bg=color, width=3).pack(side="left", fill="y")

        inner = tk.Frame(card, bg=t.card)
        inner.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        tk.Label(inner, text=label_text, bg=t.card, fg=t.gray,
                 font=t.fonts["small"]).pack(anchor="w")

        kw = {"wraplength": wrap, "justify": "left"} if wrap else {}
        tk.Label(inner, text=value_text, bg=t.card, fg=value_color,
                 font=value_font, **kw).pack(anchor="w", pady=(2, 0))

    def _build_steps_panel(self, parent):
        t = self.theme
        right = tk.Frame(parent, bg=t.bg)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        # Sub-header
        steps_data = self.rut_result.get("steps", [])
        subheader = tk.Frame(right, bg=t.bg)
        subheader.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 12))
        tk.Label(subheader, text="Proceso módulo 11",
                 bg=t.bg, fg=t.fg, font=t.fonts["head"]).pack(side="left")
        tk.Label(subheader, text=f"{len(steps_data)} pasos",
                 bg=t.bg, fg=t.gray,
                 font=t.fonts["small"]).pack(side="left", padx=(12, 0), pady=(3, 0))

        # Canvas con scroll
        canvas_frame = tk.Frame(right, bg=t.bg)
        canvas_frame.grid(row=1, column=0, sticky="nsew", padx=(32, 0), pady=(0, 16))
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(canvas_frame, bg=t.bg, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical",
                                  command=canvas.yview)
        inner = tk.Frame(canvas, bg=t.bg)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfigure(win_id, width=e.width))

        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _scroll)
        inner.bind("<MouseWheel>", _scroll)

        self._render_steps(inner, steps_data, _scroll)

    def _render_steps(self, parent, steps_data, scroll_fn):
        t = self.theme

        for i, step in enumerate(steps_data):
            row_bg = t.card if i % 2 == 0 else t.panel

            row = tk.Frame(parent, bg=row_bg)
            row.pack(fill="x", pady=(0, 2))
            row.columnconfigure(0, weight=0, minsize=44)
            row.columnconfigure(1, weight=0, minsize=180)
            row.columnconfigure(2, weight=1)

            # Número
            num = tk.Frame(row, bg=row_bg, width=44)
            num.grid(row=0, column=0, rowspan=3, sticky="ns",
                     padx=(12, 0), pady=8)
            num.pack_propagate(False)
            tk.Label(num, text=f"{i+1:02d}", bg=row_bg, fg=t.border,
                     font=t.fonts["mono_sm"]).pack(anchor="n", pady=(4, 0))

            # Separador vertical
            tk.Frame(row, bg=t.border, width=1).grid(
                row=0, column=0, rowspan=3, sticky="nse", pady=8)

            # Título — row=0, col=1
            tk.Label(row, text=step.get("title", ""),
                    bg=row_bg, fg=t.accent,
                    font=t.fonts["label"],
                    anchor="w").grid(row=0, column=1, sticky="ew",
                                    padx=(16, 8), pady=(10, 2))

            # Ecuación — row=0, col=2 (mismo row que título)
            if step.get("equation"):
                eq = tk.Frame(row, bg=row_bg)
                eq.grid(row=0, column=2, sticky="w",
                        padx=(8, 24), pady=(10, 2))
                tk.Label(eq, text=step["equation"],
                        bg=row_bg, fg=t.accent2,
                        font=t.fonts["mono"],
                        anchor="w").pack(side="left")

            # Resultado — row=1, col=2
            if step.get("result"):
                res = tk.Frame(row, bg=row_bg)
                res.grid(row=1, column=2, sticky="w",
                        padx=(8, 24), pady=(0, 2))
                tk.Label(res, text="= ", bg=row_bg, fg=t.gray,
                        font=t.fonts["small"]).pack(side="left")
                tk.Label(res, text=step["result"],
                        bg=row_bg, fg=t.green,
                        font=t.fonts["label"]).pack(side="left")

            # Explanation — row=2, columnspan=2, SIEMPRE debajo de todo
            if step.get("explanation"):
                tk.Label(row, text=step["explanation"],
                        bg=row_bg, fg=t.gray,
                        font=t.fonts["small"],
                        wraplength=700, justify="left",
                        anchor="w").grid(row=2, column=1, columnspan=2,
                                        sticky="ew",
                                        padx=(16, 24), pady=(0, 10))

            # Observación — row=3, columnspan=2
            if step.get("observation"):
                obs = tk.Frame(row, bg=row_bg)
                obs.grid(row=3, column=1, columnspan=2,
                        sticky="ew", padx=(16, 24), pady=(0, 10))
                tk.Label(obs, text=step["observation"],
                        bg=row_bg, fg=t.gray,
                        font=t.fonts["small"],
                        anchor="w").pack(side="left")

            # rowspan del número ajustado a 4
            num.grid(row=0, column=0, rowspan=4, sticky="ns",
                    padx=(12, 0), pady=8)
            tk.Frame(row, bg=t.border, width=1).grid(
                row=0, column=0, rowspan=4, sticky="nse", pady=8)

            # Propagar mousewheel a hijos
            for widget in (*row.winfo_children(), row):
                widget.bind("<MouseWheel>", scroll_fn)