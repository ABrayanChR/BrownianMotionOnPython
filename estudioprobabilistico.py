import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import *
from leerdatos import leerdatos
from scipy.constants import Boltzmann


def estudioprobabilistico(filename, lectura=False):
    """
    Realiza un análisis probabilístico de múltiples trayectorias y las representa en la misma gráfica.

    Parameters:
    -----------  
    filenames : list of str
        Nombres de los archivos .npz a leer.
    
    lectura : bool
        Parámetro que decide si leer todos los archivos de la misma versión que el primer archivo en filenames.
        Si 'lectura' es True, se buscan archivos que coincidan con la versión del primer archivo.
    """
    if lectura:
        version = filename[0]
        filename = []
        for raiz, dirs, archivos in os.walk(os.getcwd()):
            for archivo in archivos:
                if archivo.endswith(version[version.index("_"):]):
                    filename.append(archivo)

    filename = ["simulaciones/" + archivo for archivo in filename]

    velocidades = []
    tiempos = []

    for idx, fichero in tqdm(enumerate(filename)):
        datos = leerdatos(fichero)
        velocidad = datos["trayectoria"][:, 3:]
        t = datos["tiempo"]
        vector_sistema = datos["vector_sistema"]
        velocidades.append(velocidad)
        tiempos.append(t)

    T = vector_sistema[0]
    M = vector_sistema[1]
    gamma = vector_sistema[2]

    # 1. Velocidad cuadrática teórica en 3 Dimensiones (3 * kB * T / M)
    v_cuad_teo_eq = 3 * Boltzmann * T / M

    # Matriz tridimensional: (num_simulaciones, num_pasos, 3_coordenadas)
    velocidades = np.array(velocidades)

    # Módulo de la velocidad en cada instante para cada partícula
    velocidades_modulos = np.sqrt(np.sum(np.square(velocidades), axis=2))

    # Promediando sobre las simulaciones (axis=0)
    velocidades_cuadraticas_medias = np.mean(np.square(velocidades_modulos), axis=0)
    velocidades_medias = np.mean(velocidades_modulos, axis=0)

    # Curva teórica transitoria para V^2 (Arrancando desde la velocidad inicial)
    v0_cuad = velocidades_cuadraticas_medias[0]
    tiempo_eje = tiempos[0]
    # Evolución temporal teórica de <V^2>
    v_cuad_teo_t = v0_cuad * np.exp(-2 * (gamma / M) * tiempo_eje) + v_cuad_teo_eq * (
                1 - np.exp(-2 * (gamma / M) * tiempo_eje))

    fig = plt.figure(figsize=(14, 6))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # Visualizar V^2 experimental vs Teórica exacta en el tiempo
    ax1.plot(tiempo_eje, velocidades_cuadraticas_medias, label=r'$\langle V^2 \rangle$ Experimental', alpha=0.8,
             color='blue')
    ax1.plot(tiempo_eje, v_cuad_teo_t, color='red', linestyle='--', label=r'$\langle V^2 \rangle$ Teórica')
    ax1.legend()  # Activamos la leyenda

    # Velocidad media (Módulo). Termaliza a la distribución de Maxwell-Boltzmann
    v_media_maxwell = np.sqrt(8 * Boltzmann * T / (np.pi * M))
    ax2.plot(tiempo_eje, velocidades_medias, label=r'Promedio $\langle |V| \rangle$ Exp.', color='blue', linewidth=2)
    ax2.axhline(y=v_media_maxwell, color='green', linestyle='--', label='Límite Maxwell-Boltzmann')
    ax2.legend()  # Activamos la leyenda

    # Configurar gráficos
    ax1.set_title("Velocidad Cuadrática Media")
    ax1.set_xlabel("Tiempo (s)")
    ax1.set_ylabel(r"$\langle V^2 \rangle$ ($m^2/s^2$)")

    ax2.set_title("Velocidad Media (Módulo)")
    ax2.set_xlabel("Tiempo (s)")
    ax2.set_ylabel(r"$\langle |V| \rangle$ (m/s)")

    fig.suptitle(f"Análisis de {len(filename)} simulaciones. (T={T}K, M={M}kg, Gamma={gamma})")
    plt.tight_layout()
    plt.show()


#estudioprobabilistico([""])