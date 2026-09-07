""
from kivy.config import Config

Config.set("graphics", "width", "380")
Config.set("graphics", "height", "700")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition

from taskapp import theme
from taskapp.db import Database
from taskapp.screens.task_list import TaskListScreen
from taskapp.screens.task_form import TaskFormScreen
from taskapp.screens.calendar_view import CalendarViewScreen

Window.clearcolor = theme.COLOR_BG


class RootScreenManager(ScreenManager):
    db = None


class TaskCalendarApp(App):
    def build(self):
        self.title = "Task Calendar"
        self.icon = theme.ICON_PATH

        sm = RootScreenManager(transition=NoTransition())
        sm.db = Database(self.user_data_dir)

        sm.add_widget(TaskListScreen(name="task_list"))
        sm.add_widget(TaskFormScreen(name="task_form"))
        sm.add_widget(CalendarViewScreen(name="calendar_view"))
        sm.current = "task_list"

        return sm

    def on_stop(self):
        if self.root is not None and getattr(self.root, "db", None) is not None:
            self.root.db.close()


if __name__ == "__main__":
    TaskCalendarApp().run()
