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

print(f"Loaded {len(list_image)} images with timestamps and numbers:")
for i, (img, ts, num) in enumerate(zip(list_image, list_timestamp, list_number)):
    print(f"Image {i}: Timestamp = {ts}, Number = {num}, Shape = {img.shape}")
