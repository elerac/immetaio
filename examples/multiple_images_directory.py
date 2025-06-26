import numpy as np
import time
import immetaio

img0 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
timestamp0 = time.time()
img1 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
timestamp1 = time.time()

immetaio.save("multi_dir", [img0, img1], timestamp=[timestamp0, timestamp1], number=[0, 1])

list_image, metadata = immetaio.load("multi_dir")
list_timestamp = metadata["timestamp"]
list_number = metadata["number"]
