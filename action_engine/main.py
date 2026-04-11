from datetime import datetime
from src.action_engine import ActionEngine


def main():
    engine = ActionEngine()

    memos = engine.process_incidents()
    engine.save_action_memos(memos)

    sample_feedback = {
        "incident_id": "INC-1002",
        "feedback": "not_helpful",
        "operator_comment": "Cap chute was clear. Root cause was loose guide rail.",
        "actual_resolution": "Adjusted guide rail and restarted line.",
        "actual_time_to_fix_minutes": 18,
        "submitted_at": datetime.now().isoformat(timespec="seconds"),
    }

    engine.save_operator_feedback(sample_feedback)

    print("Action memos and operator feedback saved successfully.")


if __name__ == "__main__":
    main()