from typing import Any, Tuple, Optional, Dict, List, overload
from pathlib import Path
import numpy as np
from . import array_meta
from . import array_meta_nonblock
from . import array_meta_multi
from . import array_meta_dir
from .typing import PathLike


@overload
def save(target: PathLike, arr: np.ndarray, nonblock: bool = False, **metadata: Any) -> Tuple[Path, Optional[Path]]: ...
@overload
def save(target: List[PathLike], arr: List[np.ndarray], max_workers: Optional[int] = None, **metadata: List[Any]) -> List[Tuple[Path, Optional[Path]]]: ...
@overload
def save(target: PathLike, arr: List[np.ndarray], max_workers: Optional[int] = None, **metadata: List[Any]) -> List[Tuple[Path, Optional[Path]]]: ...


def save(target, arr, nonblock=False, max_workers=None, **metadata):
    """Save array(s) and metadata to a file or directory."""
    if isinstance(target, list):
        # If target is a list, save multiple arrays
        return array_meta_multi.save(target, arr, max_workers=max_workers, **metadata)
    elif isinstance(target, PathLike):
        if isinstance(arr, np.ndarray):
            # If arr is a single array, save it to the specified file
            if nonblock:
                return array_meta_nonblock.save(target, arr, **metadata)
            else:
                return array_meta.save(target, arr, **metadata)
        else:
            # If arr is not a single array, assume it's a list of arrays
            return array_meta_dir.save(target, arr, max_workers=max_workers, **metadata)

    raise TypeError("target must be a PathLike object or a list of PathLike objects.")


@overload
def load(target: PathLike, nonblock: bool = False) -> Tuple[np.ndarray, Dict[str, Any]]: ...
@overload
def load(target: List[PathLike], max_workers: Optional[int] = None) -> Tuple[List[np.ndarray], Dict[str, List[Any]]]: ...
@overload
def load(target: PathLike, max_workers: Optional[int] = None) -> Tuple[List[np.ndarray], Dict[str, List[Any]]]: ...


def load(target, max_workers=None):
    """Load array(s) and metadata from a file or directory."""
    if isinstance(target, list):
        # If target is a list, load multiple arrays
        return array_meta_multi.load(target, max_workers=max_workers)
    elif isinstance(target, PathLike):
        is_dir = Path(target).is_dir()
        if is_dir:
            # If target is a directory, load arrays from the directory
            return array_meta_dir.load(target, max_workers=max_workers)
        else:
            # If target is a single file, load the array and metadata
            return array_meta.load(target)

    raise TypeError("target must be a PathLike object or a list of PathLike objects.")
