import numpy as np
import matplotlib.pyplot as plt
import cv2
from pathlib import Path


def interference_model(x, A, w, phi, C): return A * np.sin(w * x + phi) + C

def evaluate_fit(x, data_profile, fit_params, pcov, name="Data"):
  y_theoretical = interference_model(x, *fit_params) 
  residuals = data_profile - y_theoretical
  rmse = np.sqrt(np.mean(residuals**2))
  ss_res = np.sum(residuals**2)
  ss_tot = np.sum((data_profile - np.mean(data_profile))**2)
  if ss_tot == 0:
      print(f"WARNING: The raw data for {name} is a perfectly flat line (variance is 0).")
      r2 = float('-inf')
  else:
      r2 = 1 - (ss_res / ss_tot)
  if np.isinf(pcov).any():
      phi_error = float('inf')
  else:
      phi_error = np.sqrt(np.diag(pcov))[2] # Index 2 corresponds to 'phase'
    
  print(f"--- QUALITY REPORT: {name} ---")
  print(f"R^2                 : {r2:.4f}")
  print(f"RMSE                : {rmse:.2f} intensity units")
  print(f"Phase Uncertainty   : +/- {phi_error:.4f} radians")
  print("-" * 40)
    
#   plt.figure(figsize=(8, 4))
#   plt.plot(x, data_profile, '.', label=f'Raw Data ({name})', color='gray')
#   plt.plot(x, y_theoretical, '-', label='Fitted Curve', color='red', linewidth=2)
#   plt.title(f"Diagnostic Plot - {name}")
#   plt.xlabel("Pixels (X-axis)")
#   plt.ylabel("Intensity (Y-axis)")
#   plt.legend()
#   plt.grid(True)
#   plt.show()

def load_image(file_name: str, subfolder: str = "01_raw") -> np.ndarray:
    current_path = Path(__file__).resolve().parent
    root_path = current_path.parent
    complete_path = root_path / "data" / subfolder / file_name
    if not complete_path.exists():
        raise FileNotFoundError(f"Error: File not found at path: {complete_path}")
    img_array = np.fromfile(complete_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Error: The file was found, but OpenCV could not decode it: {complete_path}")
    return img