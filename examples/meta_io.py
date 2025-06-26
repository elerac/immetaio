import numpy as np
import immetaio
import immetaio.meta


image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
metadata = {
    "exposure_time": 0.01,
    "camera_matrix": [[1000, 0, 320], [0, 1000, 240], [0, 0, 1]],
    "timestamp": "2025-06-25T12:00:00",
}

immetaio.save("myimage.png", image, **metadata)  # → myimage.png and myimage.json


metadata = immetaio.meta.load("myimage.json")

metadata["exposure_time"] = 0.02  # Update metadata
metadata["quantity"] = "example"  # Add new metadata field
immetaio.meta.save("myimage.json", **metadata)  # Save updated metadata
