# arrayio

**arrayio** provides array I/O functionality tailored for visual media applications. It facilitates seamless image handling in both human-readable and machine-parsable formats, supporting metadata storage, batch image operations with parallelized I/O, and non-blocking saving.

## Motivation

In computer vision and graphics, we often working with multiple images and their associated metadata (e.g., camera parameters, timestamps, etc.). Efficient storage and access to this data are essential.
While formats like HDF5 or NPZ offer flexibility for bundling images with metadata, they are incompatible with standard image viewers and require specialized tools to access, which complicates debugging and data inspection.
To address these limitations, arrayio separates image data and metadata into standard image files (like PNG, EXR) and JSON files, respectively. This approach allows images to be easily viewed and processed with common tools while retaining the ability to store rich metadata.

## Example Usage

### Single Image

```python
import numpy as np
import arrayio

image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
metadata = {
    "exposure_time": 0.01,
    "camera_matrix": np.array([[1000, 0, 320], [0, 1000, 240], [0, 0, 1]]),
    "timestamp": "2025-06-25T12:00:00Z"
}

arrayio.save("myimage.png", image, **metadata)
# -> Saved as myimage.png and myimage.json

# Also supported:
# arrayio.save("myimage.png", image, exposure_time=0.01) # specifying metadata directly
# arrayio.save("myimage.png", image) # without metadata

loaded_image, loaded_metadata = arrayio.load("myimage.png")
```

### Automatic Fileformat Detection

```python
import numpy as np
import arrayio

img_u8 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
arrayio.save("myimage_u8", img_u8)
# -> Saved as myimage_u8.png

img_u16 = np.random.randint(0, 65535, (480, 640, 3), dtype=np.uint16)
arrayio.save("myimage_u16", img_u16)
# -> Saved as myimage_u16.png

img_f32 = np.random.rand(480, 640, 3).astype(np.float32)
arrayio.save("myimage_f32", img_f32)
# -> Saved as myimage_f32.exr

img_f64 = np.random.rand(480, 640, 3).astype(np.float64)
arrayio.save("myimage_f64", img_f64)
# -> Saved as myimage_f64.npy

vector = np.linspace(0, 1, 100)
arrayio.save("myvector", vector)
# -> Saved as myvector.npy

tensor = np.random.rand(10, 10, 10)
arrayio.save("mytensor", tensor)
# -> Saved as mytensor.npy
```

### Multiple Images (Specifying All Filenames)

```python
import numpy as np
import time
import arrayio

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

arrayio.save(list_filename, list_image, timestamp=list_timestamp, number=list_number)
# -> Saved under multi/
# as myimage_0.png, myimage_1.png, ..., myimage_19.png
# and metadata in multi/myimage_0.json, multi/myimage_1.json, ..., multi/myimage_19.json

list_image, metadata = arrayio.load(list_filename)
list_timestamp = metadata["timestamp"]
list_number = metadata["number"]
```

### Multiple Images (Specifying a Directory)

```python
import numpy as np
import time
import arrayio

list_image = []
list_timestamp = []
list_number = []
for i in range(20):
    image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    list_image.append(image)
    list_timestamp.append(time.time())
    list_number.append(i)

arrayio.save("multi2", list_image, timestamp=list_timestamp, number=list_number)
# -> Saved under multi2/
# as 0.png, 1.png, ..., 19.png
# and metadata in 0.json, 1.json, ..., 19.json

list_image, metadata = arrayio.load("multi2")
list_timestamp = metadata["timestamp"]
list_number = metadata["number"]
```

### Non-blocking Saving

```python
import time
import numpy as np
import arrayio

# Basic saving
t = time.time()
for i in range(20):
    image = np.random.rand(960, 1280, 3).astype(np.float32)
    arrayio.save(f"non_blocking/false/myimage_{i}", image)
print(f"{time.time() - t:.2f} seconds (blocking)")
# -> 7.65 seconds (blocking)

# Non-blocking saving
t = time.time()
for i in range(20):
    image = np.random.rand(960, 1280, 3).astype(np.float32)
    arrayio.save(f"non_blocking/true/myimage_{i}", image, nonblock=True)
print(f"{time.time() - t:.2f} seconds (non-blocking)")
# -> 0.44 seconds (non-blocking)

arrayio.wait_saves()  # Ensure all non-blocking saves are completed
```
