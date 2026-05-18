from dataclasses import dataclass


@dataclass
class ThemeData:
    name: str
    bg: str
    panel: str
    fg: str
    accent: str
    muted: str


LIGHT = ThemeData(
    name="light",
    bg="#f5f7fb",
    panel="#ffffff",
    fg="#1f2937",
    accent="#6b46c1",
    muted="#6b7280",
)


DARK = ThemeData(
    name="dark",
    bg="#0f1724",
    panel="#0b1220",
    fg="#d1d5db",
    accent="#a78bfa",
    muted="#64748b",
)


def get_theme(name: str) -> ThemeData:
    if name == "light":
        return LIGHT
    return DARK
