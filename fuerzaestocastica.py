"""Función que devuelve un vector de fuerzas aleatorias que sigan una distribución normal con
    la función de numpy numpy.random.normal(media, desviación). La función recoje una media,
    un tamaño de vector y genera dicho vector."""

import numpy as np
from scipy.constants import Boltzmann


def fuerzaestocastica(mean, deviation, t, dt, T, M, gamma, normalized):
    """
    Función que devuelve un vector de fuerzas aleatorias que sigan una distribución normal con
    la función de numpy numpy.random.normal(media, desviación). La función recoje una media,
    un tamaño de vector y genera dicho vector.

    Parameters:
    -----------
    mean: float
        Media de la distribución normal.
    deviation: float
        Desviación estándar de la distribución normal.
    t: array
        Tiempos en los que se simulará el fenómeno.
    T : float
        Temperatura del sistema durante la simulación.
    M : float
        Masa de la partícula browniana.
    gamma : float
        Coeficiente de rozamiento de la partícula con el fluido.
    normalized : bool
        Devuelve valores normalizados de la fuerza estocástica o no.

    Returns:
    --------
    fuerzaestocastica: array
        Vector de fuerzas aleatorias junto a los tiempos. Su cuarta fila son los tiempos.
    """

    # Para la obtención del ruido blanco gaussiano se usa
    # Introducción a las descripciones de Langevin y Fokker-Planck: Movimiento browniano pág 37

    if not normalized:
        # Amplitud correcta para integración Euler-Maruyama: sqrt(2 * gamma * kB * T / dt)
        amplitud = np.sqrt(2 * gamma * Boltzmann * T / dt)
        fuerzaestocastica = amplitud * np.random.normal(mean, deviation, [3, len(t)])
    else:
        fuerzaestocastica = np.random.normal(mean, deviation, [3, len(t)])

    return fuerzaestocastica

# f = fuerzaestocastica(0, 1, np.linspace(0, 10, int((10) / 0.1)), 273, 1, 0)

# print(f)
