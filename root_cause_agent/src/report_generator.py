from pathlib import Path
import pandas as pd

from src.config import OUTPUTS_DIR


def deduplicate_patterns(pattern_df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only the highest-ranked row for each unique issue.
    Unique issue = line + machine + reason_text
    """
    df = pattern_df.copy()

    df = df.sort_values(
        by=["priority_score", "event_count", "total_duration"],
        ascending=[False, False, False],
    )

    df = df.drop_duplicates(subset=["line", "machine", "reason_text"], keep="first")
    df = df.reset_index(drop=True)

    return df


def build_executive_summary(pattern_df: pd.DataFrame) -> str:
    if pattern_df.empty:
        return "No significant downtime patterns were detected."

    top_row = pattern_df.iloc[0]

    return (
        f"The most significant issue is {top_row['reason_text']} on {top_row['machine']} "
        f"({top_row['line']}), with {top_row['event_count']} events and "
        f"{top_row['total_duration']} total downtime minutes."
    )


def build_top_priority_section(pattern_df: pd.DataFrame) -> str:
    """
    Highlight the single most important issue.
    """
    if pattern_df.empty:
        return "No top-priority issue detected."

    top_row = pattern_df.iloc[0]

    return (
        f"- {top_row['machine']} on {top_row['line']} is the top priority this shift. "
        f"Issue: {top_row['reason_text']}. "
        f"Owner: {top_row['suggested_owner']}. "
        f"Urgency: {top_row['urgency']}. "
        f"Recommended action: {top_row['action_type']}."
    )


def build_top_issues_section(pattern_df: pd.DataFrame, top_n: int = 5) -> str:
    """
    Cleaner and shorter top issues list.
    """
    top_df = pattern_df.head(top_n)

    lines = []
    for _, row in top_df.iterrows():
        line = (
            f"- {row['machine']} | {row['reason_text']} | "
            f"{int(row['event_count'])} events | {int(row['total_duration'])} min | "
            f"Owner: {row['suggested_owner']} | Urgency: {row['urgency']}"
        )
        lines.append(line)

    return "\n".join(lines)


def build_symptom_source_section(pattern_df: pd.DataFrame) -> str:
    symptom_df = pattern_df[pattern_df["pattern_type"] == "symptom_source_pattern"].copy()

    if symptom_df.empty:
        return "No symptom-source patterns detected."

    lines = []
    for _, row in symptom_df.iterrows():
        line = (
            f"- {row['machine']} showed '{row['reason_text']}' with likely upstream dependency on "
            f"{row['upstream_machine']} ({int(row['event_count'])} events, {int(row['total_duration'])} min)."
        )
        lines.append(line)

    return "\n".join(lines)


def infer_root_cause_for_row(row: pd.Series) -> str:
    machine = row["machine"]
    reason_text = row["reason_text"]
    line = row["line"]

    if reason_text == "Infeed Starved":
        return (
            f"- {machine} ({line}) is likely showing a downstream symptom rather than the true root cause. "
            f"The probable source is an upstream material flow issue, likely related to Conveyor_04."
        )

    if reason_text == "Bearing Seizure":
        return (
            f"- {machine} ({line}) likely failed due to unresolved mechanical deterioration, "
            f"possibly preceded by vibration or lubrication-related warning signs."
        )

    if reason_text == "High Vibration":
        return (
            f"- {machine} ({line}) may be showing an early warning of mechanical failure, "
            f"possibly related to bearing wear, imbalance, or gearbox issues."
        )

    if reason_text == "Minor Stop":
        return (
            f"- {machine} ({line}) appears to have a chronic nuisance-loss condition, likely tied to "
            f"roller looseness, alignment drift, or film tracking instability."
        )

    if reason_text == "Motor Overload":
        return (
            f"- {machine} ({line}) may have an underlying motor or rotating equipment problem, "
            f"such as overheating, overload, bearing drag, or mechanical resistance."
        )

    if reason_text == "Mechanical Failure":
        return (
            f"- {machine} ({line}) experienced a severe equipment breakdown that likely requires "
            f"maintenance follow-up, parts review, and investigation into earlier warning signs."
        )

    if reason_text == "Operator Adj":
        return (
            f"- {machine} ({line}) may have a recurring condition being temporarily managed by operators "
            f"instead of being permanently corrected at the equipment level."
        )

    if reason_text == "E-Stop":
        return (
            f"- {machine} ({line}) likely triggered a protective shutdown in response to an unsafe or abnormal condition, "
            f"which may point to a deeper equipment issue."
        )

    if reason_text == "Belt Slip":
        return (
            f"- {machine} ({line}) likely has a developing conveyor drive issue, such as belt tension loss, "
            f"roller wear, or load-related slipping."
        )

    if reason_text == "Belt Snap":
        return (
            f"- {machine} ({line}) likely reached failure after repeated unresolved belt stress or slip conditions."
        )

    return (
        f"- {machine} ({line}) shows a recurring issue that needs direct review to determine the true root cause."
    )


def build_root_cause_hypotheses_section(pattern_df: pd.DataFrame, top_n: int = 5) -> str:
    top_df = pattern_df.head(top_n)

    lines = []
    for _, row in top_df.iterrows():
        lines.append(infer_root_cause_for_row(row))

    return "\n".join(lines)


def build_recommended_actions(pattern_df: pd.DataFrame, top_n: int = 5) -> str:
    """
    Cleaner manager-friendly actions.
    """
    top_df = pattern_df.head(top_n)

    actions = []
    for _, row in top_df.iterrows():
        action = (
            f"- {row['suggested_owner']} to {row['action_type'].lower()} on {row['machine']} "
            f"for '{row['reason_text']}' ({row['urgency']})."
        )
        actions.append(action)

    return "\n".join(actions)


def build_diagnostic_brief(pattern_df: pd.DataFrame) -> str:
    dedup_df = deduplicate_patterns(pattern_df)

    executive_summary = build_executive_summary(dedup_df)
    top_priority = build_top_priority_section(dedup_df)
    top_issues = build_top_issues_section(dedup_df)
    symptom_source = build_symptom_source_section(pattern_df)
    hypotheses = build_root_cause_hypotheses_section(dedup_df)
    actions = build_recommended_actions(dedup_df)

    report = f"""
ROOT CAUSE AGENT - DIAGNOSTIC BRIEF
==================================

EXECUTIVE SUMMARY
-----------------
{executive_summary}

TOP PRIORITY THIS SHIFT
-----------------------
{top_priority}

TOP ISSUES
----------
{top_issues}

SYMPTOM-SOURCE LINKS
--------------------
{symptom_source}

LIKELY ROOT CAUSE HYPOTHESES
----------------------------
{hypotheses}

RECOMMENDED ACTIONS
-------------------
{actions}
""".strip()

    return report


def save_diagnostic_brief(report_text: str, filename: str = "diagnostic_brief.txt") -> Path:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUTS_DIR / filename
    output_path.write_text(report_text, encoding="utf-8")

    return output_path