import time
import numpy as np
import arrayio

# Basic saving
t = time.time()
for i in range(20):
    image = np.random.rand(960, 1280, 3).astype(np.float32)
    arrayio.save(f"non_blocking/false/myimage_{i}", image)
print(f"{time.time() - t:.2f} seconds (blocking)")

# Non-blocking saving
t = time.time()
for i in range(20):
    image = np.random.rand(960, 1280, 3).astype(np.float32)
    arrayio.save(f"non_blocking/true/myimage_{i}", image, nonblock=True)
print(f"{time.time() - t:.2f} seconds (non-blocking)")

arrayio.wait_saves()  # Ensure all non-blocking saves are completed
