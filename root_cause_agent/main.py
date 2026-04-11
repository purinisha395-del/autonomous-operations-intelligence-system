from datetime import datetime

from src.data_loader import load_all_data
from src.preprocess import preprocess_data
from src.pattern_detector import build_pattern_table, save_pattern_table
from src.report_generator import build_diagnostic_brief, save_diagnostic_brief
from src.triage_engine import add_triage_fields
from src.utils import save_run_log


def main():
    downtime_df, machine_df, reason_df = load_all_data()

    clean_df = preprocess_data(downtime_df, machine_df, reason_df)
    pattern_df = build_pattern_table(clean_df)
    pattern_df = add_triage_fields(pattern_df)

    diagnostic_brief = build_diagnostic_brief(pattern_df)

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event_count = len(clean_df)
    pattern_count = len(pattern_df)

    if not pattern_df.empty:
        top_issue = f"{pattern_df.iloc[0]['machine']} - {pattern_df.iloc[0]['reason_text']}"
    else:
        top_issue = "No issue detected"

    metadata = f"""
RUN METADATA
============
Generated at: {run_time}
Events analyzed: {event_count}
Patterns detected: {pattern_count}
Top ranked issue: {top_issue}

"""

    full_report = metadata + diagnostic_brief

    brief_path = save_diagnostic_brief(full_report)
    pattern_path = save_pattern_table(pattern_df)

    run_log = {
        "generated_at": run_time,
        "events_analyzed": event_count,
        "patterns_detected": pattern_count,
        "top_ranked_issue": top_issue,
        "diagnostic_brief_file": str(brief_path),
        "pattern_table_file": str(pattern_path),
    }

    run_log_path = save_run_log(run_log)

    print("\n" + full_report)
    print(f"\nDiagnostic brief saved to: {brief_path}")
    print(f"Pattern table saved to: {pattern_path}")
    print(f"Run log saved to: {run_log_path}")


if __name__ == "__main__":
    main()