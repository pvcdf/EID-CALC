# conicas-rut/ui/components/conic_elements_input.py

import tkinter as tk

from core.conicas.conic_elements import get_conic_element_fields
from ui.components.card import CardFrame


class ConicElementsInput(CardFrame):
    """
    Componente reutilizable para campos de elementos de cónicas.

    Se usa para:
    - mostrar campos vacíos;
    - revelar valores correctos después;
    - limpiar respuestas.
    """

    def __init__(self, master, theme, title="Elementos para completar", *args, **kwargs):
        super().__init__(master, theme, padx=12, pady=10, *args, **kwargs)

        self.theme = theme
        self.title = title
        self.entries = {}
        self.labels = []
        self.current_conic_type = None

        self.title_label = tk.Label(
            self,
            text=title,
            bg=self.theme.card,
            fg=self.theme.gray,
            font=self.theme.fonts["small"],
        )
        self.title_label.pack(anchor="w", pady=(0, 6))

        self.fields_frame = tk.Frame(self, bg=self.theme.card)
        self.fields_frame.pack(fill="x")

    def set_conic_type(self, conic_type: str):
        """
        Construye los campos correspondientes a una cónica.
        """
        fields = get_conic_element_fields(conic_type)
        self.set_fields(fields)
        self.current_conic_type = conic_type

    def set_fields(self, fields: list[tuple[str, str]]):
        """
        Construye campos desde una lista de:
        """
        self.clear_fields()

        for index, (label_text, key) in enumerate(fields):
            col = index % 2
            row = index // 2

            cell = tk.Frame(self.fields_frame, bg=self.theme.card)
            cell.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=(0, 8) if col == 0 else 0,
                pady=3,
            )
            self.fields_frame.columnconfigure(col, weight=1)

            label = tk.Label(
                cell,
                text=label_text,
                bg=self.theme.card,
                fg=self.theme.gray,
                font=self.theme.fonts["small"],
                anchor="w",
            )
            label.pack(anchor="w")
            self.labels.append(label)

            entry = tk.Entry(
                cell,
                bg=self.theme.panel,
                fg=self.theme.fg,
                insertbackground=self.theme.fg,
                font=self.theme.fonts["mono_sm"],
                bd=0,
                relief="flat",
                highlightbackground=self.theme.border,
                highlightthickness=1,
            )
            entry.pack(fill="x", ipady=4)

            self.entries[key] = entry

    def clear_fields(self):
        """
        Elimina todos los campos.
        """
        for child in self.fields_frame.winfo_children():
            child.destroy()

        self.entries = {}
        self.labels = []

    def clear_values(self):
        """
        Limpia el contenido de los campos, manteniendo la estructura.
        """
        for entry in self.entries.values():
            entry.delete(0, "end")

    def set_values(self, values: dict):
        """
        Inserta valores en los campos existentes.
        """
        if not isinstance(values, dict):
            return

        for key, value in values.items():
            entry = self.entries.get(key)

            if entry is None:
                continue

            entry.delete(0, "end")
            entry.insert(0, str(value))

    def get_values(self) -> dict:
        """
        Retorna los valores escritos por el usuario.
        """
        return {
            key: entry.get().strip()
            for key, entry in self.entries.items()
        }

    def show_message(self, message: str, color=None):
        """
        Muestra un mensaje simple en lugar de campos.
        """
        self.clear_fields()

        label = tk.Label(
            self.fields_frame,
            text=message,
            bg=self.theme.card,
            fg=color or self.theme.gray,
            font=self.theme.fonts["small"],
            justify="left",
            anchor="w",
        )
        label.pack(anchor="w", fill="x")
        self.labels.append(label)

    def update_theme(self, theme):
        self.theme = theme
        super().update_theme(theme)

        self.title_label.configure(
            bg=theme.card,
            fg=theme.gray,
        )
        self.fields_frame.configure(bg=theme.card)

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