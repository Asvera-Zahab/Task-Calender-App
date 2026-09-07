"""
Small custom widgets that give the app its flat, sharp-edged "pixel art"
look: a solid border color behind a slightly inset fill, no rounded
corners, no shadows, no animation.
"""
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import ColorProperty, StringProperty, BooleanProperty

from taskapp import theme


class PixelBackground(BoxLayout):
    """A box with a flat border + inset fill. No rounded corners, no shadow."""

    bg_color = ColorProperty(theme.COLOR_SURFACE)
    border_color = ColorProperty(theme.COLOR_BORDER)
    border_width = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._border_instr = Color(*self.border_color)
            self._border_rect = Rectangle(pos=self.pos, size=self.size)
            self._bg_instr = Color(*self.bg_color)
            self._bg_rect = Rectangle(pos=self._inner_pos(), size=self._inner_size())
        self.bind(pos=self._update_rects, size=self._update_rects)
        self.bind(bg_color=self._update_bg_color, border_color=self._update_border_color)

    def _inner_pos(self):
        bw = self.border_width
        return (self.x + bw, self.y + bw)

    def _inner_size(self):
        bw = self.border_width
        return (max(self.width - 2 * bw, 0), max(self.height - 2 * bw, 0))

    def _update_rects(self, *args):
        self._border_rect.pos = self.pos
        self._border_rect.size = self.size
        self._bg_rect.pos = self._inner_pos()
        self._bg_rect.size = self._inner_size()

    def _update_bg_color(self, *args):
        self._bg_instr.rgba = self.bg_color

    def _update_border_color(self, *args):
        self._border_instr.rgba = self.border_color


class PixelButton(ButtonBehavior, PixelBackground):
    """A flat, borderless-corner button used everywhere in the app."""

    text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._label = Label(
            text=self.text,
            font_name=theme.FONT_PATH,
            color=theme.COLOR_TEXT,
            font_size="20sp",
        )
        self.add_widget(self._label)
        self.bind(text=self._sync_text)

    def _sync_text(self, *args):
        self._label.text = self.text

    def on_press(self):
        self.bg_color = theme.COLOR_PRIMARY

    def on_release(self):
        self.bg_color = theme.COLOR_SURFACE


class DayCell(ButtonBehavior, BoxLayout):
    """
    One square in the month calendar. `status` is one of:
      "none"      -> within the task's range, not marked yet
      "completed" -> green
      "missed"    -> red
      "disabled"  -> outside the task's date range (not tappable)
    """

    day_text = StringProperty("")
    status = StringProperty("disabled")
    in_range = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._border_instr = Color(*theme.COLOR_BORDER)
            self._border_rect = Rectangle(pos=self.pos, size=self.size)
            self._bg_instr = Color(*self._bg_for_status())
            self._bg_rect = Rectangle(pos=self._inner_pos(), size=self._inner_size())
        self._label = Label(
            text=self.day_text,
            font_name=theme.FONT_PATH,
            font_size="18sp",
            color=theme.COLOR_TEXT if self.in_range else theme.COLOR_TEXT_DIM,
        )
        self.add_widget(self._label)
        self.bind(
            pos=self._update_rects,
            size=self._update_rects,
            day_text=self._sync_text,
            status=self._update_bg,
            in_range=self._update_bg,
        )

    def _inner_pos(self):
        return (self.x + 1, self.y + 1)

    def _inner_size(self):
        return (max(self.width - 2, 0), max(self.height - 2, 0))

    def _update_rects(self, *args):
        self._border_rect.pos = self.pos
        self._border_rect.size = self.size
        self._bg_rect.pos = self._inner_pos()
        self._bg_rect.size = self._inner_size()

    def _sync_text(self, *args):
        self._label.text = self.day_text

    def _bg_for_status(self):
        if not self.in_range:
            return theme.COLOR_DISABLED
        if self.status == "completed":
            return theme.COLOR_COMPLETED
        if self.status == "missed":
            return theme.COLOR_MISSED
        return theme.COLOR_EMPTY

    def _update_bg(self, *args):
        self._bg_instr.rgba = self._bg_for_status()
        self._label.color = theme.COLOR_TEXT if self.in_range else theme.COLOR_TEXT_DIM
