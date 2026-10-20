import fuerzaestocastica
import numpy as np
from scipy.constants import Boltzmann


def dinamica(vector_inicial, vector_sistema, t0, dt, tf, necuacion):
    """
  Función que analiza la dinámica de un sistema a partir de sus condiciones iniciales y el intervalo de tiempo.

  Parameters:
  ----------
  vector_inicial : array
    vector de posiciones iniciales y velocidades iniciales.
  vector_sistema : array
    vector de condiciones del sistema (T, M, gamma).
  t0 : int
    variable donde se aloja el tiempo inicial.
  dt : float
    parámetro que recoje el paso de tiempo de nuestra simulación.
  tf : int
    variable para el tiempo final.
  necuacion : int
    número de ecuación del movimiento a usar (1: ecuación de paso corto. 2: ecuación de paso largo).

  Return:
  -------
  trayectoria : array
    vector de posiciones y velocidades por columnas, siguiendo las
    coordenadas x, y, z, vx, vy, vz.
  t : array
    vector de tiempo.
  """

    # Condiciones del sistema
    T, M, gamma = vector_sistema[0], vector_sistema[1], vector_sistema[2]
    mean = 0
    deviation = 1

    if necuacion == 1:
        pasos = int((tf - t0) / dt)
        t = np.linspace(t0, tf, pasos)

        # Pasamos 'dt' a la fuerza estocástica
        F = fuerzaestocastica.fuerzaestocastica(mean, deviation, t, dt, T, M, gamma, False)

        trayectoria = np.zeros((pasos, len(vector_inicial)))
        trayectoria[0] = vector_inicial

        # Euler-Maruyama explícito:
        for i in range(1, pasos):
            f = F[0:3, i - 1]
            # La aceleración por fricción es -(gamma/M)*v. Se suma la aceleración estocástica f/M
            dvdt = -(gamma / M) * trayectoria[i - 1, 3:6] + (f / M)

            trayectoria[i, 3:6] = trayectoria[i - 1, 3:6] + dt * dvdt
            drdt = trayectoria[i - 1, 3:6]
            trayectoria[i, 0:3] = trayectoria[i - 1, 0:3] + dt * drdt

    elif necuacion == 2:
        dt_adim = (gamma / M) * dt  # El tiempo característico es M/gamma
        pasos = int((tf - t0) / dt)
        t = np.linspace(t0, tf, pasos)

        F = fuerzaestocastica.fuerzaestocastica(mean, deviation, t, dt, T, M, gamma, True)

        trayectoria = np.zeros((pasos, len(vector_inicial)))
        trayectoria[0] = vector_inicial

        # Evitar división por cero si parte del reposo
        vo_norm = np.linalg.norm(trayectoria[0, 3:6])
        if vo_norm == 0:
            v_ref = np.sqrt(Boltzmann * T / M)  # Usar velocidad térmica como referencia
        else:
            v_ref = vo_norm

        trayectoria[0, 3:6] = [1, 1, 1] if vo_norm == 0 else trayectoria[0, 3:6] / v_ref

        # Temperatura adimensionalizada
        T_adim = Boltzmann * T / (M * np.square(v_ref))

        for i in range(1, pasos):
            f = F[0:3, i - 1]
            # Ecuación de Langevin adimensional
            trayectoria[i, 3:6] = trayectoria[i - 1, 3:6] - trayectoria[i - 1, 3:6] * dt_adim + np.sqrt(
                2 * T_adim * dt_adim) * f

            drdt = trayectoria[i - 1, 3:6]
            # Recuperamos dimensiones para la posición
            trayectoria[i, 0:3] = trayectoria[i - 1, 0:3] + dt * drdt * v_ref

    else:
        raise Exception("Introduzca un número de ecuación correcto (1 o 2)")

    return trayectoria, t

