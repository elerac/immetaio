from pathlib import Path
from typing import Any, Tuple, List, Dict, Optional
import re
import warnings
import numpy as np
from . import array_meta_multi
from . import meta
from .typing import PathLike


def _numerical_sort(string):
    """Sort the file names numerically."""
    string = str(string)
    numbers = re.compile(r"(\d+)")
    parts = numbers.split(string)
    parts[1::2] = map(int, parts[1::2])
    return parts


def retrieve_array_meta_files(dirname: PathLike) -> Tuple[List[Path], List[Optional[Path]]]:
    """Get filenames of arrays and metadata in a directory."""
    dirname = Path(dirname)
    if not dirname.is_dir():
        raise FileNotFoundError(f"'{dirname}' is not a existing directory.")

    ext_candidates = [".png", ".exr", ".npy"]
    filenames_array = []
    for child in dirname.iterdir():
        if child.suffix in ext_candidates:
            filenames_array.append(child)
    filenames_array = sorted(filenames_array, key=_numerical_sort)

    filenames_meta = []
    for filename_array in filenames_array:
        filename_meta = filename_array.with_suffix(meta.ext)
        if filename_meta.exists():
            filenames_meta.append(filename_meta)
        else:
            filenames_meta.append(None)

    return filenames_array, filenames_meta


def save(dirname: PathLike, arrs: List[np.ndarray], max_workers: Optional[int] = None, **metadata: List[Any]) -> List[Tuple[Path, Optional[Path]]]:
    """Save multiple arrays and optional metadata in a directory."""
    dirname = Path(dirname)
    filenames_array = [dirname / f"{i}" for i in range(len(arrs))]
    if isinstance(arrs, np.ndarray):
        arrs = arrs.tolist()
    return array_meta_multi.save(filenames_array, arrs, max_workers=max_workers, **metadata)


def load(dirname: PathLike, max_workers: Optional[int] = None) -> Tuple[List[np.ndarray], Dict[str, List[Any]]]:
    """Load multiple arrays and optional metadata from a directory."""
    dirname = Path(dirname)
    filenames_array, filenames_meta = retrieve_array_meta_files(dirname)

    if len(filenames_array) == 0:
        warnings.warn(f"No array files found in '{dirname}'. Returning empty list.")

    return array_meta_multi.load(filenames_array, filenames_meta, max_workers=max_workers)
