from src.helpers.data_loader import load_image
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

