"""Resumen de métricas registradas por el entrenamiento tabular."""

import numpy as np


def moving_average(values, window=50):
    """Promedio de los últimos `window` episodios, con ventanas iniciales parciales."""
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return values
    cumulative = np.cumsum(values)
    starts = np.maximum(0, np.arange(len(values)) - window + 1)
    previous = np.where(starts > 0, cumulative[np.maximum(starts - 1, 0)], 0.0)
    return (cumulative - previous) / (np.arange(len(values)) - starts + 1)


def summarize(history, last=100):
    """Promedios sobre los últimos episodios; éxito se expresa en porcentaje."""
    if not history["g0"]:
        raise ValueError("No hay episodios para resumir")
    sample = slice(-last, None)
    return {
        "G0 medio": float(np.mean(history["g0"][sample])),
        "Éxito (%)": 100.0 * float(np.mean(history["success"][sample])),
        "Pasos medios": float(np.mean(history["steps"][sample])),
    }
