# immetaio: Image and Metadata I/O for Visual Media

**immetaio** (**im**age + **meta**data + **io**) is a Python library that provides saving and loading image arrays and their associated metadata. It is built for computer vision, graphics, and computational imaging workloads where every image has unique metadata.

## Motivation

When capturing or rendering data, we rarely interact with a single JPEG. More commonly, we acquire dozens—or even hundreds—of high‑resolution frames of the same scene under different conditions, such as exposure times, lighting setups, or viewpoints, each carrying rich metadata. Persisting this bundle in a form that is both **human‑readable** and **machine‑parsable** is harder than it seems.

immetaio tackles the challenge on three fronts:

1. **Human‑friendly, machine‑ready**: Container formats such as  NPZ or HDF5 pack pixels and metadata together, but they are opaque to everyday image viewers. immetaio instead writes the pixel data to any common image format (PNG, EXR) and stores the metadata alongside it in a plain‑text JSON file. Double‑click the image, open the JSON in your editor—no special tooling required.

2. **Asynchronous, high‑throughput I/O**: Bulk I/O of hundreds of 4K floating‑point frames is no joke. immetaio offers asynchronous `save()` and `load()` operations so that encoding, compression, and disk access happen in the background while your main thread keeps crunching numbers.

3. **One‑liner API**: Two verbs, save and load, cover the common cases: single image, image sequences, with or without metadata, integer or float buffers. The functions detect the optimal file format automatically and keep your codebase tidy.

![motivation](docs/motivation.jpg)

## Installation

```bash
pip install git+https://github.com/elerac/immetaio.git
```

## Example Usage

### Single Image

```python
import numpy as np
import immetaio

image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
metadata = {
    "exposure_time": 0.01,
    "camera_matrix": np.array([[1000, 0, 320], [0, 1000, 240], [0, 0, 1]]),
    "timestamp": "2025-06-25T12:00:00"
}

immetaio.save("myimage.png", image, **metadata)
# -> Saved as myimage.png and myimage.json

image, metadata = immetaio.load("myimage.png")
# -> metadata is loaded from myimage.json
```

### Automatic Fileformat Detection

```python
import numpy as np
import immetaio

img_u8 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
immetaio.save("myimage_u8", img_u8)
# -> Saved as myimage_u8.png

img_u16 = np.random.randint(0, 65535, (480, 640, 3), dtype=np.uint16)
immetaio.save("myimage_u16", img_u16)
# -> Saved as myimage_u16.png

img_f32 = np.random.rand(480, 640, 3).astype(np.float32)
immetaio.save("myimage_f32", img_f32)
# -> Saved as myimage_f32.exr

img_f64 = np.random.rand(480, 640, 3).astype(np.float64)
immetaio.save("myimage_f64", img_f64)
# -> Saved as myimage_f64.npy

vector_f32 = np.linspace(0, 1, 100, dtype=np.float32)
immetaio.save("myvector", vector_f32)
# -> Saved as myvector.npy

tensor_f32 = np.random.rand(10, 10, 10).astype(np.float32)
immetaio.save("mytensor", tensor_f32)
# -> Saved as mytensor.npy
```

### Multiple Images (Explicitly Specifying Filenames)

```python
import numpy as np
import time
import immetaio

list_image = []
list_filename = []
list_timestamp = []
list_number = []
for i in range(20):
    image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    list_image.append(image)
    list_timestamp.append(time.time())
    list_number.append(i)
    list_filename.append(f"multi/myimage_{i}.png")

immetaio.save(list_filename, list_image, timestamp=list_timestamp, number=list_number)
# -> Saved under multi/
# as myimage_0.png, myimage_1.png, ..., myimage_19.png
# and metadata in multi/myimage_0.json, multi/myimage_1.json, ..., multi/myimage_19.json

list_image, metadata = immetaio.load(list_filename)
list_timestamp = metadata["timestamp"]
list_number = metadata["number"]
```

### Multiple Images (Specifying a Directory)

```python
import numpy as np
import time
import immetaio

list_image = []
list_timestamp = []
list_number = []
for i in range(20):
    image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    list_image.append(image)
    list_timestamp.append(time.time())
    list_number.append(i)

immetaio.save("multi2", list_image, timestamp=list_timestamp, number=list_number)
# -> Saved under multi2/
# as 0.png, 1.png, ..., 19.png
# and metadata in 0.json, 1.json, ..., 19.json

list_image, metadata = immetaio.load("multi2")
list_timestamp = metadata["timestamp"]
list_number = metadata["number"]
```

### Non-blocking Saving

```python
import time
import numpy as np
import immetaio

# Basic saving
t = time.time()
for i in range(20):
    image = np.random.rand(960, 1280, 3).astype(np.float32)
    immetaio.save(f"non_blocking/false/myimage_{i}", image)
print(f"{time.time() - t:.2f} seconds (blocking)")
# -> 7.65 seconds (blocking)

# Non-blocking saving
t = time.time()
for i in range(20):
    image = np.random.rand(960, 1280, 3).astype(np.float32)
    immetaio.save(f"non_blocking/true/myimage_{i}", image, nonblock=True)
print(f"{time.time() - t:.2f} seconds (non-blocking)")
# -> 0.44 seconds (non-blocking)

immetaio.wait_saves()  # Ensure all non-blocking saves are completed
```

This non-blocking feature is particularly useful for capturing high-speed video streams, where you want to save frames without stalling the main processing loop. See the [examples/non_blocking_camera_capture.py](examples/non_blocking_camera_capture.py) for a complete example.
