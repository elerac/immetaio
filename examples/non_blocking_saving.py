import numpy as np
import immetaio

for i in range(10):
    # Get image in time-sensitive processing
    img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    # Save the current image in non-blocking mode
    # This allows the main thread to continue processing without waiting for the save operation to complete
    immetaio.save(f"nonblock/myimage_{i}.png", img, nonblock=True)

immetaio.wait_saves()  # Ensure all non-blocking saves are completed
