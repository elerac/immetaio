from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import numpy as np
from .types import PathLike
from . import array
from . import meta


def save(filename: PathLike, arr: np.ndarray, **metadata: Any) -> Tuple[Path, Optional[Path]]:
    """Save an array and optional metadata."""
    filename_array = array.save(filename, arr)

    if metadata:
        filename_meta = Path(filename_array).with_suffix(meta.ext)
        meta.save(filename_meta, **metadata)
    else:
        filename_meta = None

    return filename_array, filename_meta


def load(filename_array: PathLike, filename_meta: Optional[PathLike] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Load an array and optional metadata."""
    arr = array.load(filename_array)

    if filename_meta is not None:
        filename_meta = Path(filename_meta)
        if not filename_meta.exists():
            raise FileNotFoundError(f"'{filename_meta}' does not exist.")
        metadata = meta.load(filename_meta)
    else:
        filename_meta = Path(filename_array).with_suffix(meta.ext)
        metadata = meta.load(filename_meta) if Path(filename_meta).exists() else {}

    return arr, metadata
