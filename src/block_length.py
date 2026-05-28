import math

class GaugeBlockLength:
    def __init__(self, lambda_0, p, f, Lp, C, t_block, obs_fraction):
        self.lambda_0 = lambda_0  # EN MICRÓMETROS (um)
        self.p = p                # EN mm Hg
        self.f = f                # EN mm Hg
        self.Lp = Lp              # EN mm
        self.C = C
        self.t_block = t_block
        self.obs_fraction = obs_fraction

        self.n_tpf = self.refractive_index()
        self.lambda_air = self.wavelength_air()

    def refractive_index(self):
        sigma = 1 / self.lambda_0

        A = ((8342.13 + 2406030 * (130 - sigma**2)**(-1) + 15997 * (38.9 - sigma**2)**(-1)) / 720.775) * self.p * 1e-8
        B = (1 + self.p * (0.817 - 0.0133 * self.t_block) * 1e-6) / (1 + 0.003661 * self.t_block)
        C_vapor = self.f * (5.7224 - 0.0457 * sigma**2) * 1e-8
        n_tpf = (1 + A * B - C_vapor)
        return n_tpf

    def wavelength_air(self):
        lambda_air_mm = (self.lambda_0 / 1000.0) / self.n_tpf
        return lambda_air_mm

    def estimate_integer_fringes(self):
        F = (2 * self.Lp * (1 + self.C * (self.t_block - 20))) / self.lambda_air
        return F

    def block_length(self):
        F_teorico = self.estimate_integer_fringes()
        E = math.floor(F_teorico)
        fraccion_teorica = F_teorico - E

        # Ajuste de tolerancia
        if (self.obs_fraction - fraccion_teorica) > 0.5:
            E -= 1
        elif (fraccion_teorica - self.obs_fraction) > 0.5:
            E += 1

        # Reemplazar la fracción teórica por la fracción observada real
        F_prime = E + self.obs_fraction

        L_20 = (self.lambda_air / 2.0) * F_prime * (1 + self.C * (20 - self.t_block))
        return L_20
    
if __name__ == "__main__":
    bloque = GaugeBlockLength(
        lambda_0=0.63299141, # um
        p=755.0,             # mm Hg
        f=10.0,              # mm Hg
        Lp=2.5,             # mm
        C=11.5e-6,           # exp. acero
        t_block=20.15,       # °C
        obs_fraction=0.391    # Fracción leída
        )

    print("--- RESULTADOS DE LA PRUEBA ---")
    print(f"Índice de refracción (n_tpf) : {bloque.n_tpf:.8f}")
    print(f"Long. de onda en aire (mm)   : {bloque.lambda_air:.8f}")
    print(f"Franjas teóricas calculadas  : {bloque.estimate_integer_fringes():.4f}")
    print(f"Franjas aplicadas (F')       : {math.floor(bloque.estimate_integer_fringes()) + bloque.obs_fraction}")
    print(f"Longitud Final a 20°C (L_20) : {bloque.block_length():.8f} mm")

    # Comprobación de desviación
    desviacion_nm = (bloque.block_length() - 10.0) * 1e6
    print(f"Desviación del nominal       : {desviacion_nm:.2f} nm")