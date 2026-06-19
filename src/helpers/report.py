def quality_fit_report(metrics: dict, name: str = "Data"):
    """Formatea e imprime el reporte de calidad en la consola."""
    if metrics.get("is_flat_line"):
        print(f"WARNING: The raw data for {name} is a perfectly flat line (variance is 0).")
        
    print(f"--- QUALITY REPORT: {name} ---")
    print(f"R^2                 : {metrics['r2']:.4f}")
    print(f"RMSE                : {metrics['rmse']:.2f} intensity units")
    print(f"Phase Uncertainty   : +/- {metrics['phi_error']:.4f} radians")
    print("-" * 40)