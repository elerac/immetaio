import numpy as np
import immetaio

img = np.random.rand(480, 640, 3).astype(np.float32)

# Save the image in non-blocking mode
immetaio.save("nonblock/myimage_x1.exr", img * 1, nonblock=True)
immetaio.save("nonblock/myimage_x2.exr", img * 2, nonblock=True)
immetaio.save("nonblock/myimage_x4.exr", img * 4, nonblock=True)
immetaio.save("nonblock/myimage_x8.exr", img * 8, nonblock=True)

immetaio.wait_saves()  # Ensure all non-blocking saves are completed
