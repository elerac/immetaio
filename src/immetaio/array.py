from pathlib import Path
import os
import numpy as np

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2

from .typing import PathLike
from . import params


def get_filename(filename: PathLike, arr: np.ndarray) -> Path:
    """Resolve the appropriate file extension for saving an array based on its shape and dtype.

    If `filename` already has an extension, it is returned as-is.
    Otherwise, the extension is chosen according to these rules:
      - '.png' for 2D or 3-channel/4-channel uint8 or uint16 images.
      - '.exr' for 2D or 3-channel float32 images.
      - '.npy' for all other array types.
    """
    filename = Path(filename)
    if filename.suffix != "":  # If the extension is already specified, return the filename as is
        return filename
    else:  # If the extension is not specified, determine it based on the array properties
        if (arr.ndim == 2 or (arr.ndim == 3 and arr.shape[-1] in [3, 4])) and (arr.dtype in [np.uint8, np.uint16]):
            # png (uint8, uint16 image)
            ext = ".png"
        elif (arr.ndim == 2 or (arr.ndim == 3 and arr.shape[-1] == 3)) and (arr.dtype == np.float32):
            # exr (float32 image)
            ext = ".exr"
        else:
            # npy (any array)
            ext = ".npy"
        return filename.with_suffix(ext)


def save(filename: PathLike, arr: np.ndarray) -> Path:
    """Save an array to a file."""
    filename = Path(filename)
    filename_array = get_filename(filename, arr)

    filename_array.parent.mkdir(parents=True, exist_ok=True)
    if filename_array.suffix == ".npy":
        np.save(filename_array, arr)
        return filename_array
    else:
        cv2.imwrite(str(filename_array), arr, params.cv2_imwrite_params)
        return filename_array


def load(filename_array: PathLike) -> np.ndarray:
    """Load an array from a file."""
    filename_array = Path(filename_array)
    if not filename_array.exists():
        raise FileNotFoundError(f"'{filename_array}' does not exist.")

    if filename_array.suffix == ".npy":
        return np.load(filename_array)
    else:
        return cv2.imread(str(filename_array), cv2.IMREAD_UNCHANGED)
