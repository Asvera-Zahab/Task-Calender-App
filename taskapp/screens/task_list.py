import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from taskapp import theme

Builder.load_file(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "task_list.kv")
)


class TaskRow(BoxLayout):
    """One row in the task list: name + open / edit / delete."""

    task_id = ObjectProperty(None)


class TaskListScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        container = self.ids.task_container
        container.clear_widgets()
        db = self.manager.db
        tasks = db.get_tasks()

        if not tasks:
            container.add_widget(
                Label(
                    text="No tasks yet. Tap + to add one.",
                    font_name=theme.FONT_PATH,
                    color=theme.COLOR_TEXT_DIM,
                    font_size="18sp",
                    halign="center",
                    size_hint_y=None,
                    height="80dp",
                )
            )
            return

        for task_id, name, start_date, end_date in tasks:
            row = TaskRow()
            row.task_id = task_id
            row.ids.open_btn.text = name
            row.ids.open_btn.bind(
                on_release=lambda inst, tid=task_id: self.open_task(tid)
            )
            row.ids.edit_btn.bind(
                on_release=lambda inst, tid=task_id: self.edit_task(tid)
            )
            row.ids.delete_btn.bind(
                on_release=lambda inst, tid=task_id: self.delete_task(tid)
            )
            container.add_widget(row)

    def open_task(self, task_id):
        cal_screen = self.manager.get_screen("calendar_view")
        cal_screen.load_task(task_id)
        self.manager.current = "calendar_view"

    def edit_task(self, task_id):
        form_screen = self.manager.get_screen("task_form")
        form_screen.load_task(task_id)
        self.manager.current = "task_form"

    def delete_task(self, task_id):
        self.manager.db.delete_task(task_id)
        self.refresh()

    def add_task(self):
        form_screen = self.manager.get_screen("task_form")
        form_screen.load_task(None)
        self.manager.current = "task_form"
