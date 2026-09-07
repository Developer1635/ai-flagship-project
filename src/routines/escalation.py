import os
from datetime import datetime
from typing import Dict, Any, List

class EmergencyDispatcher:
    def __init__(self, caregiver_contact: str = "+1-555-019-2834"):
        self.caregiver_contact = caregiver_contact
        self.escalation_log: List[Dict[str, Any]] = []

    def trigger_tier_4_escalation(self, incident_reason: str) -> Dict[str, Any]:
        """
        Executes multi-tier alert escalation:
        Logs incident, stages SMS/Voice dispatch payload, and initiates caregiver contact.
        """
        timestamp = datetime.now().isoformat()
        alert_payload = {
            "timestamp": timestamp,
            "recipient": self.caregiver_contact,
            "reason": incident_reason,
            "action_taken": "DISPATCH_VOICE_AND_SMS",
            "status": "DISPATCHED"
        }
        self.escalation_log.append(alert_payload)

        # Simulated dispatch output (pluggable with Twilio REST client)
        print(f"\n[CRITICAL SAFETY ESCALATION] Tier 4 Triggered at {timestamp}")
        print(f"[DISPATCH -> {self.caregiver_contact}]: ALERT: Arthur did not acknowledge check-in. Reason: {incident_reason}")

        return alert_payload

    def get_dispatch_history(self) -> List[Dict[str, Any]]:
        return self.escalation_log