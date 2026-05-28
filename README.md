# Excess Fractions – Calibration of Gage Blocks Using Interferometry

This repository provides a comprehensive set of tools for determining the **absolute length of gauge blocks** using the **excess fractions method** based on interferograms. This project combines principles of dimensional metrology, image processing, and numerical fitting to achieve high-precision measurements.

## Description

The calibration of gauge blocks by interferometry requires accurately measuring the interference fringe fraction for various wavelengths. This repository implements the classical **excess fractions** method to resolve fringe order ambiguity and calculate the absolute length of the block.

## Workflow and Features

1.  **Interferogram Loading and ROI Selection**: Use an interactive tool (`coordenadas.py`) to define the regions of interest for the gauge block and the reference surface.
2.  **Fringe Profile Extraction**: Extract 1D intensity profiles by averaging pixels in the ROIs.
3.  **Interference Model Fitting**: Fit a sinusoidal model using non-linear least squares to determine fringe parameters.
4.  **Fringe Fraction Calculation**: Calculate the phase difference between the block and the reference to find the "excess fraction".
5.  **Length Determination**: Apply the excess fractions method considering environmental factors (Edlén/Ciddor equations) to find the absolute length.
6.  **Visualization**: Diagnostic plots to verify the quality of the fit and measurements.

## Repository structure
```text
├── data/
│   └── 01_raw/                 # Input interferogram images (.png)
├── scripts/
│   └── calibrar_bloque.py      # Main execution script
├── src/
│   ├── block_length.py         # Absolute length calculation logic
│   ├── coordenadas.py          # Interactive ROI selection tool
│   ├── fringe_fraction_measurement.py # Profile extraction and fitting
│   └── utils.py                # Mathematical models and helpers
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

## Usage

### 1. Identify Regions of Interest (ROI)
Run the interactive tool to get coordinates:
```bash
python src/coordenadas.py
```
*Copy the coordinates printed in the terminal for the next step.*

### 2. Measure the Fringe Fraction
Update the ROI coordinates and image path in `src/fringe_fraction_measurement.py`, then run:
```bash
python src/fringe_fraction_measurement.py
```
This will fit the sinusoidal model and output the **measured fringe fraction** (e.g., `0.3910`).

### 3. Calculate Absolute Length
Input the measured fraction and environmental data (temperature, pressure, humidity) into `src/block_length.py` and run:
```bash
python src/block_length.py
```
The script will calculate the refractive index of air, the corrected wavelength, and the final length of the block at the standard 20°C.

## Use Case: Calibrating a 2.5 mm Gauge Block

Suppose you are calibrating a **2.5 mm** nominal gauge block using the provided simulated image.

### 1. Setup Environmental Parameters
In `scripts/calibrar_bloque.py`, the following conditions are defined based on laboratory sensors:
*   **Vacuum Wavelength ($\lambda_0$)**: 0.63299141 µm (He-Ne Laser)
*   **Air Pressure**: 755.0 mm Hg
*   **Block Temperature**: 20.15 °C

### 2. Execute Measurement
The script `calibrar_bloque.py` processes `block_2.5_mm(simulated).png` using the selected ROIs. The fitting algorithm extracts the phase shift between the reference surface (platina) and the gauge block surface.

### 3. Final Results
The output provides the absolute length corrected to the standard 20°C:
*   **Measured Fraction**: `0.3910`
*   **Calculated Absolute Length ($L_{20}$)**: `2.50000173 mm`
*   **Deviation from Nominal**: `+1.73 nm`

### Quick example
```python
from src.utils import load_image
from src.fringe_fraction_measurement import FringeFractionMeasurement
from src.block_length import GaugeBlockLength


img = load_image("block_2.5_mm(simulated).png")
coords_platina = (700, 1900, 500, 900)
coords_bloque  = (700, 1900, 1000, 1400)
medicion = FringeFractionMeasurement(img, coords_platina, coords_bloque)
medicion.fit()
medicion.calculate_fraction()
fraction = medicion.fraccion_fase

bloque = GaugeBlockLength(
        lambda_0=0.63299141, # um
        p=755.0,             # mm Hg
        f=10.0,              # mm Hg
        Lp=2.5,             # mm
        C=11.5e-6,           # exp. acero
        t_block=20.15,       # °C
        obs_fraction=fraction    # Fracción leída
        )
bloque_length = bloque.block_length()
print(f"Longitud Final a 20°C (L_20) : {bloque_length:.8f} mm")
```

This demonstrates how the tool converts visual interference patterns into high-precision dimensional measurements.

## Mathematical Background

This project implements several metrological standards:
- **Edlén/Ciddor Equations**: Used to determine the refractive index of air ($n_{tpf}$) to correct the laser wavelength.
- **Sinusoidal Regression**: Employs `scipy.optimize.curve_fit` to extract phase information from noisy interferograms.
