import os
import calendar as calendar_module
from datetime import date

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty

Builder.load_file(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "task_form.kv")
)

MONTHS = [f"{m:02d}" for m in range(1, 13)]


def days_in(month_str, year_str):
    try:
        month = int(month_str)
        year = int(year_str)
        _, last_day = calendar_module.monthrange(year, month)
    except (TypeError, ValueError):
        last_day = 31
    return [f"{d:02d}" for d in range(1, last_day + 1)]


def years_around_today():
    y = date.today().year
    return [str(v) for v in range(y - 2, y + 6)]


class TaskFormScreen(Screen):
    error_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editing_task_id = None

    def load_task(self, task_id):
        """task_id is None when creating a brand new task."""
        self.editing_task_id = task_id
        self.error_text = ""

        today = date.today()
        self.ids.start_year.values = years_around_today()
        self.ids.end_year.values = years_around_today()
        self.ids.start_month.values = MONTHS
        self.ids.end_month.values = MONTHS

        if task_id is None:
            self.ids.title_label.text = "New Task"
            self.ids.name_input.text = ""
            self.ids.delete_btn.opacity = 0
            self.ids.delete_btn.disabled = True

            self.ids.start_year.text = str(today.year)
            self.ids.end_year.text = str(today.year)
            self.ids.start_month.text = f"{today.month:02d}"
            self.ids.end_month.text = f"{today.month:02d}"
            self._refresh_days()
            self.ids.start_day.text = f"{today.day:02d}"
            self.ids.end_day.text = f"{today.day:02d}"
        else:
            row = self.manager.db.get_task(task_id)
            if not row:
                self.manager.current = "task_list"
                return
            _, name, start_date, end_date = row
            self.ids.title_label.text = "Edit Task"
            self.ids.name_input.text = name
            self.ids.delete_btn.opacity = 1
            self.ids.delete_btn.disabled = False

            sy, sm, sd = start_date.split("-")
            ey, em, ed = end_date.split("-")
            if sy not in self.ids.start_year.values:
                self.ids.start_year.values = self.ids.start_year.values + [sy]
            if ey not in self.ids.end_year.values:
                self.ids.end_year.values = self.ids.end_year.values + [ey]

            self.ids.start_year.text = sy
            self.ids.start_month.text = sm
            self.ids.end_year.text = ey
            self.ids.end_month.text = em
            self._refresh_days()
            self.ids.start_day.text = sd
            self.ids.end_day.text = ed

    def _refresh_days(self, *args):
        start_days = days_in(self.ids.start_month.text, self.ids.start_year.text)
        end_days = days_in(self.ids.end_month.text, self.ids.end_year.text)
        self.ids.start_day.values = start_days
        self.ids.end_day.values = end_days
        if self.ids.start_day.text not in start_days:
            self.ids.start_day.text = start_days[-1] if start_days else "01"
        if self.ids.end_day.text not in end_days:
            self.ids.end_day.text = end_days[-1] if end_days else "01"

    def save(self):
        name = self.ids.name_input.text.strip()
        if not name:
            self.error_text = "Please enter a task name."
            return
        try:
            start_date = date(
                int(self.ids.start_year.text),
                int(self.ids.start_month.text),
                int(self.ids.start_day.text),
            )
            end_date = date(
                int(self.ids.end_year.text),
                int(self.ids.end_month.text),
                int(self.ids.end_day.text),
            )
        except (TypeError, ValueError):
            self.error_text = "Please choose valid start and end dates."
            return

        if end_date < start_date:
            self.error_text = "End date must be on or after the start date."
            return

        db = self.manager.db
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()
        if self.editing_task_id is None:
            db.add_task(name, start_str, end_str)
        else:
            db.update_task(self.editing_task_id, name, start_str, end_str)

        self.manager.get_screen("task_list").refresh()
        self.manager.current = "task_list"

    def delete(self):
        if self.editing_task_id is not None:
            self.manager.db.delete_task(self.editing_task_id)
            self.manager.get_screen("task_list").refresh()
        self.manager.current = "task_list"

    def cancel(self):
        self.manager.current = "task_list"
