from pathlib import Path

# Base project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folders
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = DATA_DIR / "outputs"

# Input files
DOWNTIME_EVENTS_FILE = RAW_DIR / "downtime_events.csv"
MACHINE_CONTEXT_FILE = RAW_DIR / "machine_context.csv"
REASON_DICTIONARY_FILE = RAW_DIR / "reason_dictionary.csv"

# Basic settings
REQUIRED_DOWNTIME_COLUMNS = [
    "event_id",
    "start_time",
    "end_time",
    "duration_minutes",
    "line",
    "machine",
    "reason_code",
    "reason_text",
    "operator_comment",
    "shift",
    "operator_id",
    "work_order",
    "sku",
    "date",
]

REQUIRED_MACHINE_COLUMNS = [
    "line",
    "machine",
    "upstream_machine",
    "downstream_machine",
    "criticality",
    "process_step",
]

REQUIRED_REASON_COLUMNS = [
    "reason_code",
    "reason_text",
    "category",
    "impact_type",
    "agent_logic_rule",
]