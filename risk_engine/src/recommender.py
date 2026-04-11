def get_recommendation(reason):
    """
    Rule-based recommendations based on incident reason.
    Simulates Project 1 logic (root cause + corrective action).
    """

    rules = {
        "Label Jam": {
            "cause": "Possible misalignment or adhesive feed issue",
            "actions": [
                "Inspect label alignment system",
                "Check adhesive feed mechanism",
                "Clean labeling sensors",
            ],
        },
        "Low Pressure": {
            "cause": "Pressure drop in system or valve issue",
            "actions": [
                "Inspect pressure valves",
                "Check for leaks in system",
                "Verify compressor performance",
            ],
        },
        "Sensor Fault": {
            "cause": "Sensor malfunction or signal interruption",
            "actions": [
                "Reset sensor system",
                "Check wiring connections",
                "Replace faulty sensor if needed",
            ],
        },
        "Conveyor Slip": {
            "cause": "Mechanical wear or belt misalignment",
            "actions": [
                "Inspect conveyor belt tension",
                "Check motor performance",
                "Lubricate moving parts",
            ],
        },
        "Overheat Alarm": {
            "cause": "Thermal overload or cooling failure",
            "actions": [
                "Check cooling system",
                "Inspect airflow and ventilation",
                "Reduce machine load temporarily",
            ],
        },
    }

    return rules.get(reason, {
        "cause": "Unknown issue",
        "actions": ["Perform general inspection"]
    })


def generate_recommendations(df):
    """
    Attach recommendations to prioritized issues.
    """
    df = df.copy()

    causes = []
    actions_list = []

    for _, row in df.iterrows():
        rec = get_recommendation(row["reason"])

        causes.append(rec["cause"])
        actions_list.append("; ".join(rec["actions"]))

    df["likely_cause"] = causes
    df["recommended_actions"] = actions_list

    return df