from pathlib import Path
from typing import Any, Tuple, Dict, List, Optional, Iterable
from concurrent.futures import ThreadPoolExecutor
import warnings
import numpy as np
import numpy.typing as npt
from . import array_meta
from .typing import PathLike


def save(filenames: List[PathLike], arrs: npt.ArrayLike, max_workers: Optional[int] = None, **metadata: List[Any]) -> List[Tuple[Path, Optional[Path]]]:
    """Save multiple arrays and optional metadata in parallel."""
    arrs = np.asarray(arrs)

    if not isinstance(filenames, Iterable) or isinstance(filenames, (str, bytes)):
        raise TypeError("filenames must be iterable.")
    if len(filenames) != len(arrs):
        raise ValueError(f"filenames and arrays must have the same length ({len(filenames)} != {len(arrs)}).")

    # Ensure metadata is a dictionary with lists of the same length as arrays
    keys = list(metadata.keys())
    for key in keys:
        if not hasattr(metadata[key], "__len__") or isinstance(metadata[key], (str, bytes)):
            raise TypeError(f"metadatas['{key}'] must be a list-like object.")
        if len(metadata[key]) != len(arrs):
            raise ValueError(f"The length of metadatas['{key}'] ({len(metadata[key])}) must match the length of arrays ({len(arrs)}).")

    results = []
    if max_workers == 1:
        # Naive loop implementation (no parallelism)
        for i, (filename, arr) in enumerate(zip(filenames, arrs)):
            metadata_i = {key: metadata[key][i] for key in keys}
            result = array_meta.save(filename, arr, **metadata_i)
            results.append(result)
    else:
        # Save arrays and metadata in parallel
        with ThreadPoolExecutor(max_workers) as executor:
            futures = []
            for i, (filename, arr) in enumerate(zip(filenames, arrs)):
                metadata_i = {key: metadata[key][i] for key in keys}
                future = executor.submit(array_meta.save, filename, arr, **metadata_i)
                futures.append(future)

            for future in futures:
                result = future.result()
                results.append(result)

    return results


def load(filenames_array: List[PathLike], filenames_meta: Optional[List[Optional[PathLike]]] = None, max_workers: Optional[int] = None) -> Tuple[List[np.ndarray], Dict[str, List[Any]]]:
    """Load multiple arrays and optional metadata in parallel."""
    # Ensure filenames_array is a list
    if not isinstance(filenames_array, list):
        raise TypeError("filenames_array must be a list of PathLike objects.")

    # Ensure filenames_meta is a list or None
    if filenames_meta is not None and not isinstance(filenames_meta, list):
        raise TypeError("filenames_meta must be a list of PathLike objects or None.")

    # If filenames_meta is None, create a sequence of None with the same length as filenames_array
    if filenames_meta is None:
        filenames_meta = [None for _ in range(len(filenames_array))]

    # Ensure filenames_array and filenames_meta have the same length
    if len(filenames_array) != len(filenames_meta):
        raise ValueError(f"filenames_array and filenames_meta must have the same length ({len(filenames_array)} != {len(filenames_meta)}).")

    if len(filenames_array) == 0:
        warnings.warn("No filenames provided. Returning empty arrays and metadata.")
        return [], {}

    results = []
    if max_workers == 1:
        # Naive loop implementation (no parallelism)
        for i, (filename_array, filename_meta) in enumerate(zip(filenames_array, filenames_meta)):
            result = array_meta.load(filename_array, filename_meta)
            results.append(result)
    else:
        # Load arrays and metadata in parallel
        with ThreadPoolExecutor(max_workers) as executor:
            futures = []
            for i, (filename_array, filename_meta) in enumerate(zip(filenames_array, filenames_meta)):
                future = executor.submit(array_meta.load, filename_array, filename_meta)
                futures.append(future)

            results = []
            for i, future in enumerate(futures):
                results.append(future.result())

    # Process the results
    arrays: List[np.ndarray] = []
    metadata = {}
    for i, (arr_i, metadata_i) in enumerate(results):
        # Array
        arrays.append(arr_i)

        # Metadata
        for key in metadata_i:
            if i == 0:  # Initialize metadata[key] as a empty list on the first iteration
                metadata[key] = []
            metadata[key].append(metadata_i[key])

    return arrays, metadata
