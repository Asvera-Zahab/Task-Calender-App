import os
import calendar as calendar_module
from datetime import date

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import StringProperty

from taskapp import theme
from taskapp.widgets import DayCell
from taskapp.calendar_utils import month_grid, add_months, WEEKDAY_LABELS

Builder.load_file(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "calendar_view.kv")
)

STATUS_CODE_TO_NAME = {0: "none", 1: "completed", 2: "missed"}
STATUS_NAME_TO_CODE = {"none": 0, "completed": 1, "missed": 2}
NEXT_STATUS = {"none": "completed", "completed": "missed", "missed": "none"}


class CalendarViewScreen(Screen):
    header_text = StringProperty("")
    month_label = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_id = None
        self.task_start = None
        self.task_end = None
        self.view_year = None
        self.view_month = None

    def load_task(self, task_id):
        self.task_id = task_id
        row = self.manager.db.get_task(task_id)
        if not row:
            self.manager.current = "task_list"
            return
        _, name, start_str, end_str = row
        self.header_text = name
        self.task_start = date.fromisoformat(start_str)
        self.task_end = date.fromisoformat(end_str)
        self.view_year = self.task_start.year
        self.view_month = self.task_start.month
        self.render_calendar()

    def prev_month(self):
        self.view_year, self.view_month = add_months(self.view_year, self.view_month, -1)
        self.render_calendar()

    def next_month(self):
        self.view_year, self.view_month = add_months(self.view_year, self.view_month, 1)
        self.render_calendar()

    def render_calendar(self):
        self.month_label = f"{calendar_module.month_name[self.view_month]} {self.view_year}"

        grid = self.ids.calendar_grid
        grid.clear_widgets()
        statuses = self.manager.db.get_statuses(self.task_id)

        for label_text in WEEKDAY_LABELS:
            grid.add_widget(
                Label(
                    text=label_text,
                    font_name=theme.FONT_PATH,
                    color=theme.COLOR_TEXT_DIM,
                    font_size="16sp",
                    size_hint_y=None,
                    height="26dp",
                )
            )

        weeks = month_grid(self.view_year, self.view_month)
        for week in weeks:
            for day_date in week:
                same_month = day_date.month == self.view_month and day_date.year == self.view_year
                in_range = same_month and (self.task_start <= day_date <= self.task_end)

                cell = DayCell()
                cell.day_text = str(day_date.day)
                cell.size_hint_y = None
                cell.height = "44dp"
                cell.in_range = in_range

                if in_range:
                    iso = day_date.isoformat()
                    code = statuses.get(iso, 0)
                    cell.status = STATUS_CODE_TO_NAME.get(code, "none")
                    cell.bind(on_release=self._make_toggle(day_date))
                else:
                    cell.status = "disabled"

                grid.add_widget(cell)

    def _make_toggle(self, day_date):
        def _toggle(instance):
            new_status = NEXT_STATUS.get(instance.status, "none")
            instance.status = new_status
            self.manager.db.set_status(
                self.task_id, day_date.isoformat(), STATUS_NAME_TO_CODE[new_status]
            )

        return _toggle

    def go_back(self):
        self.manager.current = "task_list"
