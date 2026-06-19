import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from src.utils.math_utils import interference_model, calculate_fit_metrics
from src.helpers.report import quality_fit_report


class FringeFractionMeasurement:
    def __init__(self, image: np.ndarray, roi_platina: tuple, roi_bloque: tuple):
        self.img = image
        
        yp1, yp2, xp1, xp2 = roi_platina
        yb1, yb2, xb1, xb2 = roi_bloque
        
        self.img_platina = image[yp1:yp2, xp1:xp2]
        self.img_bloque = image[yb1:yb2, xb1:xb2]
        
        self.perfil_platina = None
        self.perfil_bloque = None
        self.pixel_indices = None
        
        self.params_platina = None
        self.params_bloque = None
        self.fraccion_fase = None
        
    def get_fringe_profiles(self) -> tuple:
        self.perfil_platina = np.mean(self.img_platina, axis=1)
        self.perfil_bloque = np.mean(self.img_bloque, axis=1)
        self.pixel_indices = np.arange(len(self.perfil_platina))
        return self.perfil_platina, self.perfil_bloque, self.pixel_indices
    
    def _initial_parameter_guess(self, perfil, pixeles_between_fringes: float = 175.0):
        guess_A = (np.max(perfil) - np.min(perfil)) / 2
        guess_C = np.mean(perfil)
        guess_w = 2 * np.pi / pixeles_between_fringes
        guess_phi = 0.0
        return [guess_A, guess_w, guess_phi, guess_C]
    
    def fit(self, pixeles_between_fringes: float = 175.0, max_iterations: int = 5000):
        if self.perfil_platina is None or self.perfil_bloque is None or self.pixel_indices is None:
            self.get_fringe_profiles()
        
        # Platina fit
        p0_platina = self._initial_parameter_guess(self.perfil_platina, pixeles_between_fringes)
        self.params_platina, cov_platina = curve_fit(
            interference_model, self.pixel_indices, self.perfil_platina, 
            p0=p0_platina, maxfev=max_iterations
        )
        metrics_platina = calculate_fit_metrics(x=self.pixel_indices, 
                                        data_profile=self.perfil_platina, 
                                        fit_params=self.params_platina, 
                                        pcov=cov_platina)
        quality_fit_report(metrics=metrics_platina, name = "Platina")
        
        # Block fit
        _, w_ref, _, _ = self.params_platina
        p0_bloque = self._initial_parameter_guess(self.perfil_bloque,pixeles_between_fringes)
        p0_bloque[1] = w_ref # Forzamos la misma estimación de frecuencia
        
        self.params_bloque, cov_bloque = curve_fit(
            interference_model, self.pixel_indices, self.perfil_bloque, 
            p0=p0_bloque, maxfev=max_iterations
        )
        metrics_blocks = calculate_fit_metrics(x=self.pixel_indices, 
                                        data_profile=self.perfil_bloque, 
                                        fit_params=self.params_bloque, 
                                        pcov=cov_bloque)
        quality_fit_report(metrics=metrics_blocks, name = "Bloque")
        
        
    def calculate_fraction(self) -> float:
        if self.params_platina is None or self.params_bloque is None:
            raise ValueError("Debes ejecutar ajustar_franjas() antes de calcular la fracción.")

        phi_ref = self.params_platina[2] % (2 * np.pi)
        phi_blk = self.params_bloque[2] % (2 * np.pi)

        diferencia_fase = phi_blk - phi_ref
        if diferencia_fase < 0:
            diferencia_fase += 2 * np.pi

        self.fraccion_fase = diferencia_fase / (2 * np.pi)
        
        print(f"Fase Platina: {phi_ref:.3f} rad")
        print(f"Fase Bloque:  {phi_blk:.3f} rad")
        print(f"Fracción de Franja (f = a/b): {self.fraccion_fase:.4f}")
        
    def plot(self):
        if self.fraccion_fase is None:
            raise ValueError("Debes calcular la fracción antes de graficar.")

        plt.figure(figsize=(10, 5))
        plt.plot(self.pixel_indices, self.perfil_platina, '.', label="Datos Platina", color='blue')
        plt.plot(self.pixel_indices, self.perfil_bloque, '.', label="Datos Bloque", color='red')

        ajuste_platina = interference_model(self.pixel_indices, *self.params_platina)
        ajuste_bloque = interference_model(self.pixel_indices, *self.params_bloque)

        plt.plot(self.pixel_indices, ajuste_platina, '-', label="Ajuste Platina", color='cyan', linewidth=2)
        plt.plot(self.pixel_indices, ajuste_bloque, '-', label="Ajuste Bloque", color='orange', linewidth=2)

        plt.title(f"Ajuste de Franjas | Fracción calculada: {self.fraccion_fase:.3f}")
        plt.xlabel("Píxeles")
        plt.ylabel("Intensidad de Luz")
        plt.legend()
        plt.show()
    
if __name__ == "__main__":
    from src.helpers.data_loader import load_image
    
    img_label = "block_100.0001582_mm(simulated).png"
    img = load_image(img_label)

    roi_platina = (700, 1900, 500, 900)  # (yp1, yp2, xp1, xp2)
    roi_bloque  = (700, 1900, 1000, 1400) # (yb1, yb2, xb1, xb2)

    medicion = FringeFractionMeasurement(img, roi_platina, roi_bloque)
    medicion.fit()
    medicion.calculate_fraction()
    fraction = medicion.fraccion_fase
    print(f"Fracción de franja medida: {fraction:.4f}")
    # medicion.plot()
    
    
