
import os
import sqlite3

DB_FILENAME = "task_calendar.db"

STATUS_NONE = 0
STATUS_COMPLETED = 1
STATUS_MISSED = 2


class Database:
    def __init__(self, storage_dir=None):
        if not storage_dir:
            storage_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(storage_dir, exist_ok=True)
        self.path = os.path.join(storage_dir, DB_FILENAME)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS statuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                day TEXT NOT NULL,
                status INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE,
                UNIQUE(task_id, day)
            )
            """
        )
        self.conn.commit()

    # ---------- Tasks ----------

    def add_task(self, name, start_date, end_date):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO tasks (name, start_date, end_date) VALUES (?, ?, ?)",
            (name, start_date, end_date),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_task(self, task_id, name, start_date, end_date):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE tasks SET name=?, start_date=?, end_date=? WHERE id=?",
            (name, start_date, end_date, task_id),
        )
        # Drop statuses that now fall outside the (possibly shrunk) range.
        cur.execute(
            "DELETE FROM statuses WHERE task_id=? AND (day < ? OR day > ?)",
            (task_id, start_date, end_date),
        )
        self.conn.commit()

    def delete_task(self, task_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM statuses WHERE task_id=?", (task_id,))
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def get_tasks(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, start_date, end_date FROM tasks ORDER BY id DESC")
        return cur.fetchall()

    def get_task(self, task_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, name, start_date, end_date FROM tasks WHERE id=?", (task_id,)
        )
        return cur.fetchone()

    # ---------- Statuses ----------

    def get_statuses(self, task_id):
        """Returns {iso_date_str: status_int} for a task."""
        cur = self.conn.cursor()
        cur.execute("SELECT day, status FROM statuses WHERE task_id=?", (task_id,))
        return {row[0]: row[1] for row in cur.fetchall()}

    def set_status(self, task_id, day, status):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO statuses (task_id, day, status) VALUES (?, ?, ?)
            ON CONFLICT(task_id, day) DO UPDATE SET status=excluded.status
            """,
            (task_id, day, status),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
