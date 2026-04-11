import pandas as pd


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip extra spaces from text columns.
    """
    df = df.copy()

    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def parse_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert start_time, end_time, and date into proper datetime values.
    """
    df = df.copy()

    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


def convert_duration_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert duration_minutes into numeric values.
    """
    df = df.copy()

    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")

    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add useful derived columns for later pattern analysis.
    """
    df = df.copy()

    df["event_date"] = df["start_time"].dt.date
    df["event_hour"] = df["start_time"].dt.hour
    df["event_weekday"] = df["start_time"].dt.day_name()

    return df


def merge_machine_context(
    downtime_df: pd.DataFrame, machine_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge machine context into downtime events using line + machine.
    """
    merged_df = downtime_df.merge(
        machine_df,
        on=["line", "machine"],
        how="left",
    )

    return merged_df


def merge_reason_dictionary(
    df: pd.DataFrame, reason_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge reason dictionary into the dataframe using reason_code + reason_text.
    """
    merged_df = df.merge(
        reason_df,
        on=["reason_code", "reason_text"],
        how="left",
    )

    return merged_df


def preprocess_data(
    downtime_df: pd.DataFrame,
    machine_df: pd.DataFrame,
    reason_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Full preprocessing pipeline.
    """
    df = downtime_df.copy()

    df = clean_text_columns(df)
    df = parse_datetime_columns(df)
    df = convert_duration_column(df)
    df = add_time_features(df)
    df = merge_machine_context(df, machine_df)
    df = merge_reason_dictionary(df, reason_df)

    return df