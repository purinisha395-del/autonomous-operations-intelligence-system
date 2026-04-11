import pandas as pd
from pathlib import Path
from src.config import OUTPUTS_DIR

def save_pattern_table(pattern_df: pd.DataFrame, filename: str = "pattern_table.csv") -> Path:
    """
    Save the full pattern table to the outputs folder.
    """
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUTS_DIR / filename
    pattern_df.to_csv(output_path, index=False)

    return output_path


def detect_recurring_issues(df: pd.DataFrame) -> pd.DataFrame:
    recurring = (
        df.groupby(["line", "machine", "reason_code", "reason_text"], dropna=False)
        .agg(
            event_count=("event_id", "count"),
            total_duration=("duration_minutes", "sum"),
            avg_duration=("duration_minutes", "mean"),
        )
        .reset_index()
    )

    recurring["pattern_type"] = "recurring_issue"
    return recurring


def detect_top_loss_drivers(df: pd.DataFrame) -> pd.DataFrame:
    losses = (
        df.groupby(["line", "machine", "reason_code", "reason_text"], dropna=False)
        .agg(
            event_count=("event_id", "count"),
            total_duration=("duration_minutes", "sum"),
            avg_duration=("duration_minutes", "mean"),
        )
        .reset_index()
    )

    losses["pattern_type"] = "top_loss_driver"
    return losses


def detect_short_stop_clusters(df: pd.DataFrame, max_minutes: int = 5) -> pd.DataFrame:
    short_df = df[df["duration_minutes"] <= max_minutes].copy()

    clusters = (
        short_df.groupby(["line", "machine", "reason_code", "reason_text"], dropna=False)
        .agg(
            event_count=("event_id", "count"),
            total_duration=("duration_minutes", "sum"),
            avg_duration=("duration_minutes", "mean"),
        )
        .reset_index()
    )

    clusters["pattern_type"] = "short_stop_cluster"
    return clusters


def detect_symptom_source_patterns(df: pd.DataFrame) -> pd.DataFrame:
    symptom_df = df[df["category"] == "Symptom"].copy()

    grouped = (
        symptom_df.groupby(
            ["line", "machine", "reason_code", "reason_text", "upstream_machine"],
            dropna=False,
        )
        .agg(
            event_count=("event_id", "count"),
            total_duration=("duration_minutes", "sum"),
            avg_duration=("duration_minutes", "mean"),
        )
        .reset_index()
    )

    grouped["pattern_type"] = "symptom_source_pattern"
    return grouped


def add_priority_score(pattern_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a simple rule-based priority score.
    """
    df = pattern_df.copy()

    df["priority_score"] = (
        df["event_count"].fillna(0) * 2
        + df["total_duration"].fillna(0) / 10
        + df["avg_duration"].fillna(0) / 5
    )

    return df


def add_priority_label(pattern_df: pd.DataFrame) -> pd.DataFrame:
    """
    Turn numeric priority into a simple label.
    """
    df = pattern_df.copy()

    def label_score(score):
        if score >= 20:
            return "High"
        elif score >= 10:
            return "Medium"
        else:
            return "Low"

    df["priority_label"] = df["priority_score"].apply(label_score)
    return df


def build_pattern_table(df: pd.DataFrame) -> pd.DataFrame:
    recurring_df = detect_recurring_issues(df)
    loss_df = detect_top_loss_drivers(df)
    short_df = detect_short_stop_clusters(df)
    symptom_df = detect_symptom_source_patterns(df)

    all_patterns = pd.concat(
        [recurring_df, loss_df, short_df, symptom_df],
        ignore_index=True,
        sort=False,
    )

    all_patterns = add_priority_score(all_patterns)
    all_patterns = add_priority_label(all_patterns)

    all_patterns = all_patterns.sort_values(
        by=["priority_score", "event_count", "total_duration"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    return all_patterns