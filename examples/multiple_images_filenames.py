import numpy as np
import time
import immetaio

img_0 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
timestamp_0 = time.time()
img_1 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
timestamp_1 = time.time()

immetaio.save(
    ["myimage_0.png", "myimage_1.png"],
    [img_0, img_1],
    timestamp=[timestamp_0, timestamp_1],
    number=[0, 1],
)

list_image, metadata = immetaio.load(["myimage_0.png", "myimage_1.png"])
list_timestamp = metadata["timestamp"]
list_number = metadata["number"]
