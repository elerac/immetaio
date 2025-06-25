import atexit
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any
import numpy as np
from .types import PathLike
from . import array_meta

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


def save(filename: PathLike, arr: np.ndarray, **metadata: Any):
    """Save an array and optional metadata in a non-blocking way."""
    fut = _executor.submit(array_meta.save, filename, arr, **metadata)
    _futures.append(fut)
