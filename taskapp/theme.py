"""
Central place for the app's visual style: colors and fonts.
Palette: dark maroon / burgundy, minimalist, subtle pixel-art feel.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "VT323-Regular.ttf")
ICON_PATH = os.path.join(BASE_DIR, "assets", "icon", "icon.png")


def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, alpha)


# Backgrounds
COLOR_BG = hex_to_rgba("190D10")            # near-black maroon, app background
COLOR_SURFACE = hex_to_rgba("2B151A")       # cards / buttons
COLOR_SURFACE_LIGHT = hex_to_rgba("3B1E26") # pressed / hover state

# Accents
COLOR_PRIMARY = hex_to_rgba("7C2740")       # deep burgundy
COLOR_ACCENT = hex_to_rgba("B6425A")        # rose accent (cursor, highlights)

# Text
COLOR_TEXT = hex_to_rgba("ECDFD6")          # warm off-white
COLOR_TEXT_DIM = hex_to_rgba("9C7F82")      # muted rose-grey for secondary text

# Structure
COLOR_BORDER = hex_to_rgba("100809")        # near-black pixel outline

# Calendar day states
COLOR_EMPTY = hex_to_rgba("241016")         # day in range, not yet marked
COLOR_COMPLETED = hex_to_rgba("5C7A52")     # muted pixel green
COLOR_MISSED = hex_to_rgba("A1403C")        # muted pixel red
COLOR_DISABLED = hex_to_rgba("1C1013")      # day outside task range
