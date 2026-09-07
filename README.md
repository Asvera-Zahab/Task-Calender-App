# Task Calendar

A simple, offline task tracker built around a monthly calendar.

Create a task with a start date and end date (e.g. **Workout**, 1 Sept ->
30 Sept) and the app builds the whole calendar for you automatically. Tap a
day to mark it **green** (done) or **red** (missed). Everything saves
locally - no account, no internet needed, no ads.

## What's in this project

```
task_calendar_app/
├── main.py                     # App entry point
├── requirements.txt             # Desktop dependency (Kivy)
├── buildozer.spec               # Android build configuration
├── assets/
│   └── fonts/VT323-Regular.ttf  # Free pixel-style font (OFL license)
└── taskapp/
    ├── theme.py                 # Dark maroon color palette + font path
    ├── db.py                    # SQLite storage (tasks + daily statuses)
    ├── calendar_utils.py        # Month grid / month navigation helpers
    ├── widgets.py                # Custom pixel-style Button & calendar DayCell
    ├── kv/                       # Layout files (one per screen)
    └── screens/                  # Screen logic (one per screen)
        ├── task_list.py          # Task list (home screen)
        ├── task_form.py          # Create / edit a task
        └── calendar_view.py      # A task's monthly calendar
``

## Run it on your computer (Windows + VS Code)

1. Open the `task_calendar_app` folder in VS Code.
2. Open a terminal (`` Ctrl+` ``) and run:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python main.py
   ```
3. A window opens. Tap **+** to add your first task.

Next time, just repeat steps 2's last two lines (`Activate.ps1` then
`python main.py`) - no need to reinstall anything.

---
