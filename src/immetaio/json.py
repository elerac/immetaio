from typing import Dict, Any
from pathlib import Path
import json
import numpy as np
from .types import PathLike


class NdarrayEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.ndarray):
            return {"type": "ndarray", "values": o.tolist(), "dtype": o.dtype.str}
        elif isinstance(o, np.generic):
            # Convert a standard Python scalar
            return o.item()
        else:
            return json.JSONEncoder.default(self, o)


def _ndarray_hook(o):
    if "type" in o:
        if o["type"] == "ndarray":
            dtype = o["dtype"] if "dtype" in o else None
            return np.array(o["values"], dtype)
    return o


class NdarrayDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=_ndarray_hook, *args, **kwargs)


def format_json(obj: Any, indent: int = 4, level: int = 0) -> str:
    """Recursively format JSON for list objects

    This function formats JSON-like objects with the following rules:
    - dicts get multiline formatting with the given indent
    - 1D lists stay on one line
    - 2D lists render as a grid (each sub-list on its own line)
    - primitives use json.dumps to get valid JSON literals
    """
    space = " " * (indent * level)
    next_space = " " * (indent * (level + 1))

    # --- dicts ---
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            key = json.dumps(k)
            val = format_json(v, indent, level + 1)
            items.append(f"{next_space}{key}: {val}")
        body = ",\n".join(items)
        return "{\n" + body + "\n" + space + "}"

    # --- lists ---
    elif isinstance(obj, list):
        # empty list
        if not obj:
            return "[]"

        # detect a “2D” list: every element is a list of non-lists
        is_2d = all(isinstance(el, list) for el in obj) and all(not any(isinstance(sub, list) for sub in el) for el in obj)

        if is_2d:
            # render as a grid
            rows = []
            for row in obj:
                # inline-format each row (which is a 1D list)
                row_text = format_json(row, indent, level + 1)
                rows.append(f"{next_space}{row_text}")
            return "[\n" + ",\n".join(rows) + "\n" + space + "]"

        else:
            # 1D or mixed-depth lists: inline everything
            elems = [format_json(el, indent, level + 1) for el in obj]
            return "[" + ", ".join(elems) + "]"

    # --- primitives ---
    else:
        return json.dumps(obj)


def save(filename_json: PathLike, **data: Any) -> Path:
    """Save dictionary to a json file."""
    filename_json = Path(filename_json)
    filename_json.parent.mkdir(parents=True, exist_ok=True)
    with open(filename_json, "w") as f:
        json.dump(data, f, cls=NdarrayEncoder, indent=4)

    # Reformat the JSON file for better readability
    with open(filename_json, "r") as f:
        data = json.load(f)
    formatted_data = format_json(data, indent=4)
    with open(filename_json, "w") as f:
        f.write(formatted_data + "\n")

    return filename_json


def load(filename_json: PathLike) -> Dict[str, Any]:
    """Load dictionary from a json file."""
    with open(filename_json, "r") as f:
        data = json.load(f, cls=NdarrayDecoder)
    return data
