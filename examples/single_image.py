import numpy as np
import immetaio

image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
metadata = {
    "exposure_time": 0.01,
    "camera_matrix": [[1000, 0, 320], [0, 1000, 240], [0, 0, 1]],
    "timestamp": "2025-06-25T12:00:00",
}

immetaio.save("myimage.png", image, **metadata)
# -> Saved as myimage.png and myimage.json

image, metadata = immetaio.load("myimage.png")
exposure_time = metadata["exposure_time"]
camera_matrix = metadata["camera_matrix"]
timestamp = metadata["timestamp"]
