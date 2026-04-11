import pandas as pd


def assign_owner(row: pd.Series) -> str:
    """
    Assign a suggested owner based on issue type.
    """
    reason_text = row["reason_text"]

    if reason_text in ["Bearing Seizure", "Mechanical Failure", "Motor Overload", "Belt Slip", "Belt Snap"]:
        return "Maintenance"

    if reason_text in ["Infeed Starved", "Operator Adj", "Minor Stop", "E-Stop"]:
        return "Operations"

    if reason_text in ["High Vibration"]:
        return "Maintenance"

    return "Engineering"


def assign_urgency(row: pd.Series) -> str:
    """
    Assign urgency based on priority and issue type.
    """
    reason_text = row["reason_text"]
    priority_label = row["priority_label"]

    if reason_text in ["Bearing Seizure", "Mechanical Failure", "E-Stop", "Belt Snap"]:
        return "Immediate"

    if priority_label == "High":
        return "This shift"

    if priority_label == "Medium":
        return "Next 24 hours"

    return "Next PM window"


def assign_action_type(row: pd.Series) -> str:
    """
    Assign a practical suggested action type.
    """
    reason_text = row["reason_text"]

    if reason_text == "Bearing Seizure":
        return "Escalate and inspect mechanical failure"

    if reason_text == "Mechanical Failure":
        return "Inspect failed equipment and review spare parts"

    if reason_text == "Motor Overload":
        return "Inspect motor and rotating components"

    if reason_text == "Belt Slip":
        return "Inspect conveyor tension and drive path"

    if reason_text == "Belt Snap":
        return "Replace belt and inspect upstream wear conditions"

    if reason_text == "High Vibration":
        return "Inspect vibration source and schedule maintenance review"

    if reason_text == "Infeed Starved":
        return "Review upstream dependency and material flow"

    if reason_text == "Minor Stop":
        return "Trend repeated stops and inspect adjustment points"

    if reason_text == "Operator Adj":
        return "Check for chronic condition masked by operator workaround"

    if reason_text == "E-Stop":
        return "Review shutdown cause and inspect safety-related condition"

    return "Review issue and determine next corrective action"


def add_triage_fields(pattern_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add owner, urgency, and action type columns to pattern dataframe.
    """
    df = pattern_df.copy()

    df["suggested_owner"] = df.apply(assign_owner, axis=1)
    df["urgency"] = df.apply(assign_urgency, axis=1)
    df["action_type"] = df.apply(assign_action_type, axis=1)

    return df