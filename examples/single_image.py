import numpy as np
import arrayio

image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
metadata = {"exposure_time": 0.01, "camera_matrix": np.array([[1000, 0, 320], [0, 1000, 240], [0, 0, 1]]), "timestamp": "2025-06-25T12:00:00Z"}

arrayio.save("myimage.png", image, **metadata)

loaded_image, loaded_metadata = arrayio.load("myimage.png")
