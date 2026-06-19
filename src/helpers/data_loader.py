import numpy as np
import cv2
from pathlib import Path

def load_image(file_name: str, subfolder: str = "01_raw") -> np.ndarray:
    current_path = Path(__file__).resolve().parent
    root_path = current_path.parent.parent
    complete_path = root_path / "data" / subfolder / file_name
    if not complete_path.exists():
        raise FileNotFoundError(f"Error: File not found at path: {complete_path}")
    img_array = np.fromfile(complete_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Error: The file was found, but OpenCV could not decode it: {complete_path}")
    return img