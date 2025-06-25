from pathlib import Path
import os
import numpy as np

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2

from .types import PathLike
from . import params


def save(filename: PathLike, arr: np.ndarray) -> Path:
    """Save an array to a file.

    If a file extension of array is not specified, the file format is determined based on the array's shape and dtype.
    Since this module is intended for image data handling, standard image formats are prioritized over the .npy format.

    The following conventions are used for format selection:
    - `.png` for uint8 or uint16 image
    - `.exr` for float32 images
    - `.npy` for any other array type
    """
    filename = Path(filename)
    ext = filename.suffix
    if ext != "":  # if the suffix is specified
        filename_array = filename
        filename_array.parent.mkdir(parents=True, exist_ok=True)
        if ext == ".npy":
            np.save(filename_array, arr)
            return filename_array
        else:
            cv2.imwrite(str(filename_array), arr, params.cv2_imwrite_params)
            return filename_array
    else:  # if the suffix is not specified
        shape = arr.shape
        dtype = arr.dtype
        ndim = arr.ndim

        # png (uint8, uint16 image)
        if (ndim == 2 or (ndim == 3 and shape[-1] in [3, 4])) and (dtype in [np.uint8, np.uint16]):
            ext = ".png"
            filename_array = Path(filename).with_suffix(ext)
            filename_array.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(filename_array), arr, params.cv2_imwrite_params)
            return filename_array

        # exr (float32 image)
        if (ndim == 2 or (ndim == 3 and shape[-1] == 3)) and (dtype == np.float32):
            ext = ".exr"
            filename_array = Path(filename).with_suffix(ext)
            filename_array.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(filename_array), arr, params.cv2_imwrite_params)
            return filename_array

        # npy (any array)
        ext = ".npy"
        filename_array = Path(filename).with_suffix(ext)
        filename_array.parent.mkdir(parents=True, exist_ok=True)
        np.save(filename_array, arr)
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
