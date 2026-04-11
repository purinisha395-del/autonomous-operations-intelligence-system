import json
from pathlib import Path
from typing import Any

from src.config import OUTPUTS_DIR


def save_run_log(log_data: dict[str, Any], filename: str = "run_log.json") -> Path:
    """
    Save structured run metadata to a JSON file in the outputs folder.
    """
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUTS_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4)

    return output_path