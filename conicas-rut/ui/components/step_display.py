# conicas-rut/ui/components/step_display.py

import tkinter as tk

from ui.components.card import CardFrame


def _has_value(value) -> bool:
    return value is not None and value != ""


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
        self.labels = []

        self.title_label = tk.Label(
            self,
            text=f"▸ {title}",
            bg=self.theme.card,
            fg=self.theme.accent,
            font=self.theme.fonts["label"],
            anchor="w",
            justify="left",
        )
        self.title_label.pack(fill="x", padx=8, pady=(8, 4))
        self.labels.append(("title", self.title_label))

        if _has_value(explanation):
            self.explanation_label = tk.Label(
                self,
                text=explanation,
                bg=self.theme.card,
                fg=self.theme.fg,
                font=self.theme.fonts["small"],
                anchor="w",
                justify="left",
                wraplength=1,
            )
            self.explanation_label.pack(fill="x", padx=12, pady=(0, 4))
            self.explanation_label.bind(
                "<Configure>",
                lambda event, label=self.explanation_label: label.configure(
                    wraplength=max(event.width - 4, 40)
                ),
            )
            self.labels.append(("text", self.explanation_label))

        if _has_value(equation):
            self.equation_label = tk.Label(
                self,
                text=equation,
                bg=self.theme.card,
                fg=self.theme.accent2,
                font=self.theme.fonts["mono"],
                anchor="w",
                justify="left",
                wraplength=1,
            )
            self.equation_label.pack(fill="x", padx=12, pady=(4, 4))
            self.equation_label.bind(
                "<Configure>",
                lambda event, label=self.equation_label: label.configure(
                    wraplength=max(event.width - 4, 40)
                ),
            )
            self.labels.append(("equation", self.equation_label))

        if _has_value(result):
            self.result_label = tk.Label(
                self,
                text=f"Resultado: {result}",
                bg=self.theme.card,
                fg=self.theme.green,
                font=self.theme.fonts["label"],
                anchor="w",
                justify="left",
                wraplength=1,
            )
            self.result_label.pack(fill="x", padx=12, pady=(4, 4))
            self.result_label.bind(
                "<Configure>",
                lambda event, label=self.result_label: label.configure(
                    wraplength=max(event.width - 4, 40)
                ),
            )
            self.labels.append(("result", self.result_label))

        if _has_value(observation):
            self.observation_label = tk.Label(
                self,
                text=f"ℹ {observation}",
                bg=self.theme.card,
                fg=self.theme.gray,
                font=self.theme.fonts["small"],
                anchor="w",
                justify="left",
                wraplength=1,
            )
            self.observation_label.pack(fill="x", padx=12, pady=(4, 8))
            self.observation_label.bind(
                "<Configure>",
                lambda event, label=self.observation_label: label.configure(
                    wraplength=max(event.width - 4, 40)
                ),
            )
            self.labels.append(("observation", self.observation_label))

    def update_theme(self, theme):
        self.theme = theme
        super().update_theme(theme)

        for kind, label in self.labels:
            if kind == "title":
                label.configure(bg=theme.card, fg=theme.accent)
            elif kind == "equation":
                label.configure(bg=theme.card, fg=theme.accent2)
            elif kind == "result":
                label.configure(bg=theme.card, fg=theme.green)
            elif kind == "observation":
                label.configure(bg=theme.card, fg=theme.gray)
            else:
                label.configure(bg=theme.card, fg=theme.fg)


class StepContainer(tk.Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, bg=theme.panel, *args, **kwargs)
        self.theme = theme

        self._canvas = tk.Canvas(
            self,
            bg=self.theme.panel,
            highlightthickness=0,
            borderwidth=0,
        )
        self._vscroll = tk.Scrollbar(
            self,
            orient="vertical",
            command=self._canvas.yview,
        )
        self._inner = tk.Frame(self._canvas, bg=self.theme.panel)

        self._inner_id = self._canvas.create_window(
            (0, 0),
            window=self._inner,
            anchor="nw",
        )

        self._canvas.configure(yscrollcommand=self._vscroll.set)

        self._canvas.grid(row=0, column=0, sticky="nsew")
        self._vscroll.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._inner.bind("<Configure>", self._on_inner_resize)
        self._canvas.bind("<Configure>", self._on_canvas_resize)

        self._canvas.bind("<MouseWheel>", self._on_mousewheel)
        self._inner.bind("<MouseWheel>", self._on_mousewheel)

        self.step_items = []

    def _on_inner_resize(self, _event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self._canvas.itemconfigure(self._inner_id, width=event.width)

    def _on_mousewheel(self, event):
        if event.delta:
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_step(
        self,
        title,
        explanation,
        equation=None,
        result=None,
        observation=None,
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

    def clear(self):
        for child in self._inner.winfo_children():
            child.destroy()

        self.step_items = []
        self._canvas.yview_moveto(0)

    def set_steps(self, steps):
        self.clear()

        if not steps:
            return

        for index, step in enumerate(steps, start=1):
            if isinstance(step, dict):
                self.add_step(
                    step.get("title", f"Paso {index}"),
                    step.get("explanation", ""),
                    equation=step.get("equation"),
                    result=step.get("result"),
                    observation=step.get("observation"),
                )
            else:
                self.add_step(
                    f"Paso {index}",
                    str(step),
                )

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.panel)
        self._canvas.configure(bg=theme.panel)
        self._inner.configure(bg=theme.panel)

        for item in self.step_items:
            item.update_theme(theme)