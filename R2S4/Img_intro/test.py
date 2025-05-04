import cv2 as cv
import numpy as np
import sys

print(f"--- Running Simple ArUco Test ---")
print(f"Using OpenCV version: {cv.__version__}")
print(f"OpenCV installed at: {cv.__file__}")

# Generate a known marker
test_dict_name = cv.aruco.DICT_4X4_50
try:
    test_dict = cv.aruco.getPredefinedDictionary(test_dict_name)
except AttributeError:
    print(f"FATAL: cv.aruco module or dictionary {test_dict_name} not found.")
    sys.exit(1)

marker_id_to_generate = 0
marker_size_pixels = 200
test_marker_img_array = cv.aruco.generateImageMarker(test_dict, marker_id_to_generate, marker_size_pixels)

if test_marker_img_array is None:
    print("FATAL: Failed to generate marker image.")
    sys.exit(1)
print(f"Generated marker array shape: {test_marker_img_array.shape}, dtype: {test_marker_img_array.dtype}")

# Try detecting the marker directly from the NumPy array
print("\nAttempting detection directly on the generated NumPy array...")
test_params = cv.aruco.DetectorParameters()
test_detector = cv.aruco.ArucoDetector(test_dict, test_params)

try:
    corners, ids, rejected = test_detector.detectMarkers(test_marker_img_array)

    if ids is not None and len(ids) > 0:
        print(f"SUCCESS: Detected generated marker directly from array. ID: {ids.flatten()}")
    else:
        print(f"FAILURE: Could NOT detect the locally generated marker directly from array.")
        if rejected is not None and len(rejected)>0:
             print(f"Found {len(rejected)} rejected candidates even on clean array.")
        else:
             print("No rejected candidates found either.")

except cv.error as e:
    print(f"OpenCV Error during detection: {e}")
except Exception as e:
    print(f"Unexpected Error during detection: {e}")

print("--- Test Finished ---")
