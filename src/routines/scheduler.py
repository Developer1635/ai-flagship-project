from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "secure_vault.db"

jobstores = {
    "default": SQLAlchemyJobStore(url=f"sqlite:///{DB_PATH}")
}

class RoutineScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(jobstores=jobstores)
        self.is_running = False

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
            self.is_running = True
            print("[Scheduler] Persistent routine daemon started.")

    def shutdown(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self.is_running = False
            print("[Scheduler] Routine daemon stopped cleanly.")

    def add_scheduled_task(self, func, trigger_type: str, task_id: str, **trigger_args):
        """Adds or replaces a durable scheduled job in the SQLite job store."""
        self.scheduler.add_job(
            func,
            trigger=trigger_type,
            id=task_id,
            replace_existing=True,
            **trigger_args
        )