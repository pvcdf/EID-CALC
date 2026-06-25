# conicas-rut/ui/components/limit_elements_input.py

import tkinter as tk

from core.limites.limit_elements import get_limit_answer_fields
from ui.components.card import CardFrame
from ui.components.header import SectionHeader


class LimitElementsInput(tk.Frame):
    """
    Componente reutilizable para respuestas de límites y continuidad.

    Mantiene los campos vacíos y permite revelar
    las respuestas calculadas.
    """

    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, bg=theme.panel, *args, **kwargs)

        self.theme = theme
        self.entries = {}
        self.cards = []
        self.labels = []

        self._build()

    def _build(self):
        self._build_limits_section()
        self._build_continuity_section()

    def _build_limits_section(self):
        SectionHeader(self, "Análisis de límites", self.theme).pack(
            fill="x",
            pady=(14, 0),
        )

        for label_text, key, tall in get_limit_answer_fields()[:4]:
            self._add_field(label_text, key, tall=tall)

    def _build_continuity_section(self):
        SectionHeader(self, "Continuidad", self.theme).pack(
            fill="x",
            pady=(12, 0),
        )

        for label_text, key, tall in get_limit_answer_fields()[4:]:
            self._add_field(label_text, key, tall=tall)

    def _add_field(self, label_text, key, tall=False):
        card = CardFrame(self, self.theme, padx=10, pady=8)
        card.pack(fill="x", pady=(5, 0))

        label = tk.Label(
            card,
            text=label_text,
            bg=self.theme.card,
            fg=self.theme.gray,
            font=self.theme.fonts["small"],
            anchor="w",
        )
        label.pack(anchor="w")

        entry = tk.Entry(
            card,
            bg=self.theme.panel,
            fg=self.theme.fg,
            insertbackground=self.theme.fg,
            font=self.theme.fonts["mono_sm"],
            bd=0,
            relief="flat",
            highlightbackground=self.theme.border,
            highlightthickness=1,
            state="normal",
        )
        entry.pack(fill="x", ipady=7 if tall else 4, pady=(3, 0))

        self.entries[key] = entry
        self.cards.append(card)
        self.labels.append(label)

    def set_values(self, values: dict):
        """
        Inserta valores calculados en los campos.
        """
        if not isinstance(values, dict):
            return

        for key, value in values.items():
            entry = self.entries.get(key)

            if entry is None:
                continue

            entry.delete(0, "end")
            entry.insert(0, str(value))

    def clear_values(self):
        """
        Limpia todos los campos.
        """
        for entry in self.entries.values():
            entry.delete(0, "end")

    def get_values(self) -> dict:
        """
        Retorna las respuestas escritas por el usuario.
        """
        return {
            key: entry.get().strip()
            for key, entry in self.entries.items()
        }

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.panel)

        for card in self.cards:
            card.update_theme(theme)

        for label in self.labels:
            label.configure(
                bg=theme.card,
                fg=theme.gray,
            )

        for entry in self.entries.values():
            entry.configure(
                bg=theme.panel,
                fg=theme.fg,
                insertbackground=theme.fg,
                highlightbackground=theme.border,
            )