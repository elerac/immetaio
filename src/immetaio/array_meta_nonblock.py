from typing import Any, Optional, Tuple
from pathlib import Path
import numpy as np
from . import meta
from . import array_nonblock
from .typing import PathLike


def save(filename: PathLike, arr: np.ndarray, **metadata: Any) -> Tuple[Path, Optional[Path]]:
    filename_array = array_nonblock.save(filename, arr)
    if metadata:
        filename_meta = Path(filename_array).with_suffix(meta.ext)
        meta.save(filename_meta, **metadata)
    else:
        filename_meta = None
    return filename_array, filename_meta
