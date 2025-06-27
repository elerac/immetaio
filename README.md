# immetaio: Image and Metadata I/O for Visual Media

**immetaio** (**im**age + **meta**data + **io**) is a Python library that provides saving and loading image arrays and their associated metadata. It is built for computer vision, graphics, and computational imaging workloads where every image paired with user-defined metadata.

## Motivation

When capturing or rendering data, we rarely interact with a single JPEG. More commonly, we acquire dozens—or even hundreds—of high‑resolution frames of the same scene under different conditions, such as exposure times, lighting setups, or viewpoints, each carrying rich metadata. Persisting this bundle in a form that is both **human‑readable** and **machine‑parsable** is harder than it seems.

immetaio tackles the challenge on three fronts:

1. **Human‑friendly, machine‑ready**: Container formats such as  NPZ or HDF5 pack pixels and metadata together, but they are opaque to everyday image viewers. immetaio instead writes the pixel data to any common image format (PNG, EXR) and stores the user-defined metadata alongside it in a plain‑text JSON file. Double‑click the image and open it in a standard viewer—no special tooling is required.

2. **Asynchronous, high‑throughput I/O**: Bulk I/O of hundreds of 4K floating‑point frames is no joke. immetaio offers asynchronous operations so that encoding, compression, and disk access to run in parallel. Non-blocking saving keeps your main processing loop-free to continue working.

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
    "camera_matrix": [[1000, 0, 320], [0, 1000, 240], [0, 0, 1]],
    "timestamp": "2025-06-25T12:00:00",
}

immetaio.save("myimage.png", image, **metadata)  # → myimage.png and myimage.json

image, metadata = immetaio.load("myimage.png")
exposure_time = metadata["exposure_time"]
camera_matrix = metadata["camera_matrix"]
timestamp = metadata["timestamp"]
```

The metadata is saved as a JSON file (`myimage.json`) as follows:

```json
{
    "exposure_time": 0.01,
    "camera_matrix": [[1000, 0, 320], [0, 1000, 240], [0, 0, 1]],
    "timestamp": "2025-06-25T12:00:00"
}
```

### Automatic Fileformat Detection

```python
img_u8 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
immetaio.save("myimage_u8", img_u8)  # → myimage_u8.png

img_u16 = np.random.randint(0, 65535, (480, 640, 3), dtype=np.uint16)
immetaio.save("myimage_u16", img_u16)  # → myimage_u16.png

img_f32 = np.random.rand(480, 640, 3).astype(np.float32)
immetaio.save("myimage_f32", img_f32)  # → myimage_f32.exr

img_f64 = np.random.rand(480, 640, 3).astype(np.float64)
immetaio.save("myimage_f64", img_f64)  # → myimage_f64.npy

vector_f32 = np.linspace(0, 1, 100, dtype=np.float32)
immetaio.save("myvector", vector_f32)  # → myvector.npy

tensor_f32 = np.random.rand(100, 100, 100).astype(np.float32)
immetaio.save("mytensor", tensor_f32)  # → mytensor.npy
```

### Multiple Images (Explicitly Specifying Filenames)

```python
img_0 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
img_1 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

immetaio.save(
    ["myimage_0.png", "myimage_1.png"],
    [img_0, img_1],
    timestamp=[time.time(), time.time()],
    number=[0, 1],
)
# → myimage_0.png, myimage_1.png
# → myimage_0.json, myimage_1.json

list_image, metadata = immetaio.load(["myimage_0.png", "myimage_1.png"])
list_timestamp = metadata["timestamp"]
list_number = metadata["number"]
```

### Multiple Images (Specifying a Directory)

```python
img0 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
img1 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

immetaio.save("multi_dir", [img0, img1], timestamp=[time.time(), time.time()], number=[0, 1])
# → multi_dir/0.png, multi_dir/1.png
# → multi_dir/0.json, multi_dir/1.json

list_image, metadata = immetaio.load("multi_dir")
```

### Non-blocking Saving

Non-blocking saving is particularly useful for time-sensitive applications where you want to avoid blocking the main thread while saving images:

```python
for i in range(10):
    # Time-sensitive processing 
    img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    # Save the current image in non-blocking mode
    # This allows the main thread to continue processing without waiting for the save operation to complete
    immetaio.save(f"nonblock/myimage_{i}.png", img, nonblock=True)

immetaio.wait_saves()  # Ensure all non-blocking saves are completed
```

For a more practical example, you can save multiple images in multiple threads, enabling high-throughput I/O operations in intuitive code:

```python
img = np.random.rand(480, 640, 3).astype(np.float32)

# Save the image in non-blocking mode
immetaio.save("nonblock/myimage_x1.exr", img * 1, nonblock=True)
immetaio.save("nonblock/myimage_x2.exr", img * 2, nonblock=True)
immetaio.save("nonblock/myimage_x4.exr", img * 4, nonblock=True)
immetaio.save("nonblock/myimage_x8.exr", img * 8, nonblock=True)

immetaio.wait_saves()  # Ensure all non-blocking saves are completed
```

### Metadata I/O

You can also save and load metadata independently.

```python
import immetaio.meta

metadata = {
    "exposure_time": 0.01,
    "camera_matrix": [[1000, 0, 320], [0, 1000, 240], [0, 0, 1]],
    "timestamp": "2025-06-25T12:00:00",
}
immetaio.meta.save("myimage.json", **metadata)

metadata = immetaio.meta.load("myimage.json")
```
