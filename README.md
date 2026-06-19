# Excess Fractions – Calibration of Gage Blocks Using Interferometry

This repository provides a comprehensive set of tools for determining the **absolute length of gauge blocks** using the **excess fractions method** based on interferograms. This project combines principles of dimensional metrology, image processing, and numerical fitting to achieve high-precision measurements.

## Description

The calibration of gauge blocks by interferometry requires accurately measuring the interference fringe fraction for various wavelengths. This repository implements the classical **excess fractions** method to resolve fringe order ambiguity and calculate the absolute length of the block. It includes a robust calculation of the refractive index of air using the modified Edlén equations and solves the monochromatic excess fraction problem.

## Workflow and Features

1.  **Interferogram Loading and ROI Selection**: Use an interactive tool (`coordenadas.py`) to define the regions of interest for the gauge block and the reference surface (platen).
2.  **Fringe Profile Extraction**: Extract 1D intensity profiles by averaging pixels in the ROIs.
3.  **Interference Model Fitting**: Fit a sinusoidal model using non-linear least squares to determine fringe parameters and assess fit quality.
4.  **Fringe Fraction Calculation**: Calculate the phase difference between the block and the reference to find the "excess fraction".
5.  **Environmental Correction**: Apply the modified Edlén equations to accurately determine the refractive index of air and the wavelength in air based on temperature, pressure, and humidity/dew point.
6.  **Length Determination**: Resolve optical ambiguity using the Monochromatic Excess Fraction Method (MEFM) considering mechanical preconditioning, or calculate the absolute length at the standard 20 °C reference temperature.
7.  **Exploratory Notebooks**: Detailed Jupyter notebooks demonstrating simulations, single-wavelength interferometry, uncertainty evaluation (Decker 1997), and end-to-end calculations.

## Repository Structure

```text
├── data/
│   ├── 01_raw/                 # Input interferogram images (.png)
│   ├── 02_interim/             # Intermediate processed data
│   └── 03_processed/           # Final data outputs
├── docs/                       # Figures and calibration reports
├── notebooks/                  # Jupyter notebooks for exploration and simulation
├── scripts/
│   └── calibrar_bloque.py      # Main execution script example
├── src/
│   ├── block_length.py         # Absolute length calculation logic
│   ├── coordenadas.py          # Interactive ROI selection tool
│   ├── fringe_fraction_measurement.py # Profile extraction and fitting
│   ├── mefm_solver.py          # Monochromatic Excess Fraction Method solver
│   ├── refraction_index.py     # Modified Edlén equations for air refractive index
│   ├── helpers/                # Data loaders and reporting functions
│   └── utils/                  # Mathematical models and metrics (interference_model)
├── tests/                      # Pytest unit tests for core modules
├── requirements.txt            # Python dependencies
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Exccess_fractions.git
   cd Exccess_fractions
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   If you plan to run the tests, you may also need to install `pytest`:
   ```bash
   pip install pytest
   ```

## Usage

### 1. Identify Regions of Interest (ROI)
Run the interactive tool to get coordinates from your interferogram images:
```bash
python src/coordenadas.py
```
*A window will open. Draw a rectangle over the desired region and press ENTER. Copy the coordinates printed in the terminal for the next step.*

### 2. Measure the Fringe Fraction
Update the ROI coordinates and image path in the script, or run the module directly to test with simulated data:
```bash
python src/fringe_fraction_measurement.py
```
This will fit the sinusoidal model and output the **measured fringe fraction** (e.g., `0.3910`), along with fit quality metrics ($R^2$, RMSE, Phase Uncertainty).

### 3. Calculate Absolute Length
Input the measured fraction and environmental data (temperature, pressure, humidity) into `src/block_length.py` and run:
```bash
python src/block_length.py
```
The script will calculate the refractive index of air, the corrected wavelength, and the final length of the block at the standard 20 °C.

### 4. Advanced: MEFM Solver
If you want to evaluate an individual gauge block using the Monochromatic Excess Fraction Method based on mechanical pre-measurements, you can use `src/mefm_solver.py`:
```bash
python src/mefm_solver.py
```

## Use Case: Calibrating a 2.5 mm Gauge Block

Suppose you are calibrating a **2.5 mm** nominal gauge block using the provided simulated image.

### 1. Setup Environmental Parameters
In `scripts/calibrar_bloque.py`, the following conditions are defined based on laboratory sensors:
*   **Vacuum Wavelength ($\lambda_0$)**: 0.63299141 µm (He-Ne Laser)
*   **Air Pressure**: 755.0 mm Hg
*   **Vapor Pressure / Humidity factor ($f$)**: 10.0 mm Hg
*   **Block Temperature**: 20.15 °C

### 2. Execute Measurement
The script `calibrar_bloque.py` processes `block_2.5_mm(simulated).png` using the selected ROIs. The fitting algorithm extracts the phase shift between the reference surface (platen) and the gauge block surface.

```bash
python scripts/calibrar_bloque.py
```

### 3. Final Results
The output provides the absolute length corrected to the standard 20 °C:
*   **Measured Fraction**: `0.3910`
*   **Calculated Absolute Length ($L_{20}$)**: `2.50000173 mm`
*   **Deviation from Nominal**: `+1.73 nm`

### Quick Example (Python API)
```python
from src.helpers.data_loader import load_image
from src.fringe_fraction_measurement import FringeFractionMeasurement
from src.block_length import GaugeBlockLength

# 1. Load Image and define ROIs
img = load_image("block_2.5_mm(simulated).png")
coords_platina = (700, 1900, 500, 900)
coords_bloque  = (700, 1900, 1000, 1400)

# 2. Extract Phase Fraction
medicion = FringeFractionMeasurement(img, coords_platina, coords_bloque)
medicion.fit()
medicion.calculate_fraction()
fraction = medicion.fraccion_fase

# 3. Calculate Absolute Length
bloque = GaugeBlockLength(
        lambda_0=0.63299141, # um
        p=755.0,             # mm Hg
        f=10.0,              # mm Hg
        Lp=2.5,              # mm
        C=11.5e-6,           # thermal expansion (steel)
        t_block=20.15,       # °C
        obs_fraction=fraction # Measured fraction
)
bloque_length = bloque.block_length()
print(f"Longitud Final a 20°C (L_20) : {bloque_length:.8f} mm")
```

## Running Tests

The project uses `pytest` for unit testing the core calculation modules (`block_length.py`, `mefm_solver.py`, `refraction_index.py`). To run the tests:
```bash
pytest tests/
```

## Mathematical Background

This project implements several metrological standards and methods:
- **Modified Edlén Equations**: Used to determine the refractive index of air ($n_{tpf}$) to correct the laser wavelength for varying environmental conditions.
- **Sinusoidal Regression**: Employs `scipy.optimize.curve_fit` to extract phase information from noisy interferograms.
- **Monochromatic Excess Fraction Method (MEFM)**: Resolves the fringe ambiguity by combining a single wavelength optical measurement with a prior mechanical measurement.
