import pytest
import math
from src.block_length import GaugeBlockLength

def test_gauge_block_length_logic():
    """
    Tests the GaugeBlockLength calculation using the parameters 
    defined in the module's test block.
    """
    # Input parameters
    l0 = 0.63299141
    p = 755.0
    f = 10.0
    Lp = 2.5
    C = 11.5e-6
    t = 20.15
    obs = 0.391

    bloque = GaugeBlockLength(
        lambda_0=l0, p=p, f=f, Lp=Lp, C=C, t_block=t, obs_fraction=obs
    )

    # 1. Test refractive index calculation
    n = bloque.refractive_index()
    assert 1.00026 < n < 1.00028

    # 2. Test wavelength in air
    # (l0 / 1000) / n
    expected_air_mm = (l0 / 1000.0) / n
    assert bloque.lambda_air == pytest.approx(expected_air_mm)

    # 3. Test absolute length calculation
    l_20 = bloque.block_length()
    
    # For a 2.5mm block, the result should be very close to 2.5mm
    # even with small thermal expansion and air index corrections.
    assert 2.499 < l_20 < 2.501
    assert isinstance(l_20, float)