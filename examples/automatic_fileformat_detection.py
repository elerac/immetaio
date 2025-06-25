import numpy as np
import immetaio

img_u8 = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
immetaio.save("myimage_u8", img_u8)
# -> Saved as myimage_u8.png

img_u16 = np.random.randint(0, 65535, (480, 640, 3), dtype=np.uint16)
immetaio.save("myimage_u16", img_u16)
# -> Saved as myimage_u16.png

img_f32 = np.random.rand(480, 640, 3).astype(np.float32)
immetaio.save("myimage_f32", img_f32)
# -> Saved as myimage_f32.exr

img_f64 = np.random.rand(480, 640, 3).astype(np.float64)
immetaio.save("myimage_f64", img_f64)
# -> Saved as myimage_f64.npy

vector_f32 = np.linspace(0, 1, 100, dtype=np.float32)
immetaio.save("myvector", vector_f32)
# -> Saved as myvector.npy

tensor_f32 = np.random.rand(10, 10, 10).astype(np.float32)
immetaio.save("mytensor", tensor_f32)
# -> Saved as mytensor.npy
