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

print(f"Loaded {len(list_image)} images with timestamps and numbers:")
for i, (img, ts, num) in enumerate(zip(list_image, list_timestamp, list_number)):
    print(f"Image {i}: Timestamp = {ts}, Number = {num}, Shape = {img.shape}")
