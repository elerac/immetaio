import cv2

cv2_imwrite_params = {}
cv2_imwrite_params[".png"] = [cv2.IMWRITE_PNG_COMPRESSION, 9]
cv2_imwrite_params[".exr"] = [cv2.IMWRITE_EXR_COMPRESSION, cv2.IMWRITE_EXR_COMPRESSION_PIZ]
