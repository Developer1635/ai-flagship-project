from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class WellnessMonitor:
    def __init__(self, inactivity_threshold_hours: float = 4.0):
        self.last_interaction_time: datetime = datetime.now()
        self.inactivity_threshold = timedelta(hours=inactivity_threshold_hours)

    def record_interaction(self):
        """Resets the inactivity timer on any user speech or physical interaction."""
        self.last_interaction_time = datetime.now()

    def evaluate_wellness_state(self) -> Dict[str, Any]:
        """Evaluates interaction lapse and flags necessary interventions."""
        now = datetime.now()
        elapsed = now - self.last_interaction_time

        # Tier 3: Inactivity Anomaly
        if elapsed >= self.inactivity_threshold:
            return {
                "tier": 3,
                "status": "ANOMALY_CHECK_REQUIRED",
                "prompt": "Arthur, just conducting our routine afternoon check-in. Please let me know you are comfortable."
            }

        # Tier 1: Routine Hydration / Wellness prompt (if > 2 hours)
        elif elapsed >= timedelta(hours=2.0):
            return {
                "tier": 1,
                "status": "HYDRATION_CHECK",
                "prompt": "Arthur, it has been a couple of hours since your last drink. Staying hydrated will keep your energy up."
            }

        return {"tier": 0, "status": "NOMINAL", "prompt": None}