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


def save(filename_json: PathLike, **data: Any) -> None:
    """Save dictionary to a json file."""
    filename_json = Path(filename_json)
    filename_json.parent.mkdir(parents=True, exist_ok=True)
    with open(filename_json, "w") as f:
        json.dump(data, f, cls=NdarrayEncoder, indent=4)


def load(filename_json: PathLike) -> Dict[str, Any]:
    """Load dictionary from a json file."""
    with open(filename_json, "r") as f:
        data = json.load(f, cls=NdarrayDecoder)
    return data
