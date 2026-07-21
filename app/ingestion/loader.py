"""JSON dataset loading utilities for CyberRAG ingestion."""

import json
from pathlib import Path
from typing import Any


def load_json_dataset(file_path: str) -> Any:
    """Load and parse a JSON dataset file.

    Parameters
    ----------
    file_path : str
        Path to the JSON file to load.

    Returns
    -------
    Any
        The parsed Python object (dict, list, etc.) from the JSON file.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file contains malformed JSON or cannot be decoded.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"JSON dataset file not found: {path}")

    try:
        with path.open(encoding="utf-8") as json_file:
            return json.load(json_file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Failed to parse JSON from {path}: "
            f"{exc.msg} at line {exc.lineno}, column {exc.colno}"
        ) from exc
