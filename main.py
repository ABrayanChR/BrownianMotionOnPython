import os
from multiprocessing import Pool
from tqdm import tqdm
from scipy.constants import Boltzmann
from dinamica import dinamica
from guardarsimulacion import guardarsimulacion
from representardatos import representardatos


def ejecutar_simulacion(args):
    v_ini, v_sis, cond = args
    tray, tiempo = dinamica(v_ini, v_sis, cond[0], cond[1], cond[2], cond[3])
    guardarsimulacion(tray, tiempo, v_ini, v_sis, [cond[3]])
    return True


if __name__ == '__main__':
    mode = int(input("0: Leer / 1: Crear\n>>>"))

    if mode == 1:
        # Velocidad inicial estrictamente NULA
        v_ini = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Condiciones del sistema base
        T = 298.15
        M = 1e-12

        # Tiempo de simulación ampliado (de 2e-11 a 2e-10) para observar bien la difusión
        cond = [0.0, 1e-15, 2e-10, 1]

        # Coeficientes de difusión deseados
        D_targets = [1e-19, 1e-20, 1e-21]
        particulas_por_D = 10

        tareas = []

        # Calculamos la fricción (gamma) necesaria para cada D usando D = (kB * T) / gamma
        for D in D_targets:
            gamma = (Boltzmann * T) / D
            v_sis = [T, M, gamma]

            for _ in range(particulas_por_D):
                tareas.append((v_ini, v_sis, cond))

        print(f"Generando {len(tareas)} simulaciones con D = {D_targets}...")
        with Pool() as pool:
            list(tqdm(pool.imap_unordered(ejecutar_simulacion, tareas), total=len(tareas)))
        print("Simulaciones listas.")

    elif mode == 0:
        carpeta = "simulaciones"
        archivos = [f for f in os.listdir(carpeta) if f.endswith(".npz")] if os.path.exists(carpeta) else []

        if not archivos:
            print("No hay simulaciones en la carpeta.")
        else:
            for i, f in enumerate(archivos):
                print(f"{i}: {f}")

            idx = int(input("Índice de referencia: "))
            op = input("¿Representar [T]odos o solo [S]eleccionado?\n>>>").upper()

            archivos_final = archivos if op == 'T' else [archivos[idx]]

            anim = input("¿Animar vídeo transparente en 2D? (s/n): ").lower()
            if anim == 's':
                representardatos(archivos_final, animar=True, guardar_mp4=True)
            else:
                representardatos(archivos_final, animar=False)