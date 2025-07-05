import atexit
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import numpy as np
from .types import PathLike
from . import array

_executor = ThreadPoolExecutor()
_futures = []


def wait_saves():
    """Wait for all pending background saves to complete."""
    for fut in as_completed(_futures):
        fut.result()


def _shutdown_executor():
    wait_saves()
    _executor.shutdown(wait=True)


atexit.register(_shutdown_executor)


def save(filename: PathLike, arr: np.ndarray) -> Path:
    """Save an array in a non-blocking way."""
    fut = _executor.submit(array.save, filename, arr)
    _futures.append(fut)
    filename_array = array.get_filename(filename, arr)
    return filename_array
