import pandas as pd


def load_data(file_path="data/incidents.csv"):
    """
    Load incident data from CSV and parse timestamp column.
    """
    df = pd.read_csv(file_path, parse_dates=["timestamp"], encoding="latin1")
    return df


def validate_data(df):
    """
    Basic validation to make sure required columns exist
    and critical fields are not missing.
    """
    required_columns = [
        "incident_id",
        "machine_id",
        "timestamp",
        "reason",
        "duration_minutes",
        "shift",
        "operator",
        "repeat_count",
        "past_week_count",
        "impact_score",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values in required columns.")

    return True


def predict_risk(df):
    """
    Simple weighted risk score using recurrence and impact signals.
    This acts as the first version of the prediction layer.
    """
    df = df.copy()

    df["risk_score"] = (
        df["repeat_count"] * 0.4
        + df["past_week_count"] * 0.4
        + df["impact_score"] * 0.2
    )

    return df


def prioritize_incidents(df):
    """
    Rank incidents from highest to lowest risk score.
    """
    df = df.copy()
    df = df.sort_values(by="risk_score", ascending=False)
    return df


def aggregate_issue_priorities(df):
    """
    Aggregate incident rows into machine-level issue priorities.
    Groups by machine and reason to create a more realistic
    operational prioritization view.
    """
    grouped = (
        df.groupby(["machine_id", "reason"], as_index=False)
        .agg(
            incident_count=("incident_id", "count"),
            total_downtime=("duration_minutes", "sum"),
            avg_risk_score=("risk_score", "mean"),
            max_repeat_count=("repeat_count", "max"),
            recent_frequency=("past_week_count", "max"),
        )
    )

    grouped["priority_score"] = (
        grouped["avg_risk_score"] * 0.5
        + grouped["total_downtime"] * 0.2
        + grouped["incident_count"] * 0.2
        + grouped["recent_frequency"] * 0.1
    )

    grouped = grouped.sort_values(by="priority_score", ascending=False)

    return grouped


def generate_explanations(df):
    """
    Add human-readable explanations for why an issue
    is ranked as high priority.
    """
    df = df.copy()

    explanations = []

    for _, row in df.iterrows():
        reasons = []

        if row["recent_frequency"] >= 5:
            reasons.append("high recent recurrence")

        if row["total_downtime"] >= 40:
            reasons.append("large cumulative downtime")

        if row["incident_count"] >= 2:
            reasons.append("multiple incidents recorded")

        if row["avg_risk_score"] >= 5:
            reasons.append("elevated average risk score")

        if not reasons:
            reasons.append("moderate operational risk signals")

        explanation = "Priority due to " + ", ".join(reasons) + "."
        explanations.append(explanation)

    df["explanation"] = explanations
    return df