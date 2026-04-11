import json
from pathlib import Path
from datetime import datetime


class ActionEngine:
    def __init__(
        self,
        config_path="config/settings.json",
        prompt_path="config/prompt_templates.json",
    ):
        self.config = self._load_json(config_path)
        self.prompts = self._load_json(prompt_path)

    def _load_json(self, file_path):
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def determine_status(self, confidence):
        act_threshold = self.config["reasoning"]["act_threshold"]
        inspect_threshold = self.config["reasoning"]["inspect_threshold"]

        if confidence >= act_threshold:
            return "ACT"
        if confidence >= inspect_threshold:
            return "INSPECT"
        return "ESCALATE"

    def get_mode_reason(self, status, confidence):
        if status == "ACT":
            return f"High confidence match ({confidence:.0%}). Clear SOP-based action can be taken."
        if status == "INSPECT":
            return f"Moderate confidence match ({confidence:.0%}). Verify condition before replacing parts."
        return f"Low confidence match ({confidence:.0%}). Pattern does not strongly align to known SOPs."

    def get_escalation_target(self, status):
        if status == "ESCALATE":
            return self.config["reasoning"]["default_escalation_target"]
        return None

    def validate_feedback_type(self, feedback_type):
        allowed_types = self.config["feedback"]["allowed_feedback_types"]
        if feedback_type not in allowed_types:
            raise ValueError(
                f"Invalid feedback type: {feedback_type}. Allowed values: {allowed_types}"
            )

    def generate_action_memo(self, incident):
        confidence = incident["confidence"]
        status = self.determine_status(confidence)

        memo = {
            "incident_id": incident["incident_id"],
            "machine_id": incident["machine_id"],
            "summary": incident["summary"],
            "risk_score": incident["risk_score"],
            "likely_cause": incident["likely_cause"],
            "recommended_action": incident["recommended_action"],
            "required_parts": incident["required_parts"],
            "estimated_time_to_fix_minutes": incident["estimated_time_to_fix_minutes"],
            "status": status,
            "mode_reason": self.get_mode_reason(status, confidence),
            "escalation_target": self.get_escalation_target(status),
            "confidence": confidence,
            "evidence": incident["evidence"],
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

        return memo

    def save_action_memos(self, memos, output_path="outputs/sample_action_memos.json"):
        path = Path(output_path)

        with path.open("w", encoding="utf-8") as f:
            json.dump(memos, f, indent=2)

    def process_incidents(self, input_path="data/sample_incidents.json"):
        incidents = self._load_json(input_path)
        memos = []

        for incident in incidents:
            memo = self.generate_action_memo(incident)
            memos.append(memo)

        return memos

    def save_operator_feedback(self, feedback, output_path="outputs/operator_feedback.json"):
        self.validate_feedback_type(feedback["feedback"])

        path = Path(output_path)

        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                existing_feedback = json.load(f)
        else:
            existing_feedback = []

        existing_feedback.append(feedback)

        with path.open("w", encoding="utf-8") as f:
            json.dump(existing_feedback, f, indent=2)