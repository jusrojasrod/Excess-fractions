import numpy as np

def interference_model(x, A, w, phi, C): return A * np.sin(w * x + phi) + C

def calculate_fit_metrics(x, data_profile, fit_params, pcov):
    """Calcula las métricas de ajuste de forma pura y retorna un diccionario."""
    y_theoretical = interference_model(x, *fit_params) 
    residuals = data_profile - y_theoretical
    
    rmse = np.sqrt(np.mean(residuals**2))
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((data_profile - np.mean(data_profile))**2)
    
    if ss_tot == 0:
        r2 = float('-inf')
    else:
        r2 = 1 - (ss_res / ss_tot)
        
    if np.isinf(pcov).any():
        phi_error = float('inf')
    else:
        phi_error = np.sqrt(np.diag(pcov))[2] # El índice 2 corresponde a la fase
        
    return {
        "r2": r2,
        "rmse": rmse,
        "phi_error": phi_error,
        "is_flat_line": ss_tot == 0
    }