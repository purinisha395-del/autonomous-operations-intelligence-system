import pandas as pd

from src.config import (
    DOWNTIME_EVENTS_FILE,
    MACHINE_CONTEXT_FILE,
    REASON_DICTIONARY_FILE,
    REQUIRED_DOWNTIME_COLUMNS,
    REQUIRED_MACHINE_COLUMNS,
    REQUIRED_REASON_COLUMNS,
)


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_name: str) -> None:
    """
    Check whether a dataframe contains all required columns.
    Raise an error if anything is missing.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing required columns: {missing_columns}"
        )


def clean_null_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace common text placeholders like 'NULL' with real missing values.
    """
    null_like_values = ["NULL", "null", "None", "none", ""]

    return df.replace(null_like_values, pd.NA)


def load_downtime_events() -> pd.DataFrame:
    """
    Load the main downtime events CSV.
    """
    df = pd.read_csv(DOWNTIME_EVENTS_FILE)

    validate_columns(df, REQUIRED_DOWNTIME_COLUMNS, "downtime_events.csv")
    df = clean_null_strings(df)

    return df


def load_machine_context() -> pd.DataFrame:
    """
    Load the machine context CSV.
    """
    df = pd.read_csv(MACHINE_CONTEXT_FILE)

    validate_columns(df, REQUIRED_MACHINE_COLUMNS, "machine_context.csv")
    df = clean_null_strings(df)

    return df


def load_reason_dictionary() -> pd.DataFrame:
    """
    Load the reason dictionary CSV.
    """
    df = pd.read_csv(REASON_DICTIONARY_FILE)

    validate_columns(df, REQUIRED_REASON_COLUMNS, "reason_dictionary.csv")
    df = clean_null_strings(df)

    return df


def load_all_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load all three input files and return them together.
    """
    downtime_df = load_downtime_events()
    machine_df = load_machine_context()
    reason_df = load_reason_dictionary()

    return downtime_df, machine_df, reason_df