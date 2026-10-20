import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
from leerdatos import leerdatos
from scipy.constants import Boltzmann

# Ruta de FFmpeg lista para usarse
plt.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'


def representardatos(filenames, animar=False, guardar_mp4=False):
    # Entorno 2D transparente
    fig = plt.figure(figsize=(10, 10), facecolor='none')
    ax = fig.add_subplot(111)

    ax.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_axis_off()

    rutas_archivos = ["simulaciones/" + f if not f.startswith("simulaciones/") else f for f in filenames]

    trayectorias = []
    valores_D = []

    for fichero in rutas_archivos:
        datos = leerdatos(fichero)
        trayectorias.append(datos["trayectoria"])

        T = datos["vector_sistema"][0]
        gamma = datos["vector_sistema"][2]

        # Calculamos D y forzamos precisión para agrupar en la leyenda limpiamente
        D_calculado = float(f"{(Boltzmann * T) / gamma:.1e}")
        valores_D.append(D_calculado)

    todas_x = np.concatenate([t[:, 0] for t in trayectorias])
    todas_y = np.concatenate([t[:, 1] for t in trayectorias])

    def limites_seguros(datos, margen=1e-10):
        d_min, d_max = np.min(datos), np.max(datos)
        if d_min == d_max: return [d_min - margen, d_max + margen]
        return [d_min, d_max]

    ax.set_xlim(limites_seguros(todas_x))
    ax.set_ylim(limites_seguros(todas_y))
    ax.set_aspect('equal')

    # ORDENAR DE MAYOR A MENOR: reverse=True pone los valores más altos primero
    D_unicos = sorted(list(set(valores_D)), reverse=True)
    colores_base = plt.cm.plasma(np.linspace(0.1, 0.9, len(D_unicos)))
    mapa_colores = {d: colores_base[i] for i, d in enumerate(D_unicos)}

    lineas = []
    puntos = []
    labels_usados = set()

    for i, traj in enumerate(trayectorias):
        d_actual = valores_D[i]
        color_actual = mapa_colores[d_actual]

        # Formato limpio (ej: "1e-19")
        label = f"D = {d_actual:.0e} m²/s" if d_actual not in labels_usados else ""
        labels_usados.add(d_actual)

        linea = ax.plot([], [], color=color_actual, alpha=0.6, linewidth=0.3, label=label)[0]
        punto = ax.plot([], [], marker='o', color=color_actual, markersize=3, alpha=0.9)[0]

        lineas.append(linea)
        puntos.append(punto)

    if len(D_unicos) > 0:
        # Leyenda en color negro (o del color que contraste) con líneas de muestra gruesas
        leg = ax.legend(loc="upper left", frameon=False, labelcolor='black')
        for line in leg.get_lines():
            line.set_linewidth(2.0)

    if not animar:
        for i, traj in enumerate(trayectorias):
            lineas[i].set_data(traj[:, 0], traj[:, 1])
        plt.show()

    else:
        num_pasos_totales = len(trayectorias[0])
        paso_animacion = max(1, num_pasos_totales // 300)
        frames_totales = num_pasos_totales // paso_animacion

        def update(frame):
            idx = frame * paso_animacion
            for i, traj in enumerate(trayectorias):
                lineas[i].set_data(traj[:idx, 0], traj[:idx, 1])
                puntos[i].set_data([traj[idx, 0]], [traj[idx, 1]])
            return lineas + puntos

        ani = FuncAnimation(fig, update, frames=frames_totales, interval=30, blit=False)

        if guardar_mp4:
            print("Guardando vídeo 2D con FFmpeg (Fondo Transparente)...")
            try:
                writer = FFMpegWriter(fps=30, codec="png", extra_args=['-pix_fmt', 'rgba'])
                ani.save("simulacion_3D_coeficientes_transparente.mov", writer=writer,
                         savefig_kwargs={'facecolor': 'none', 'transparent': True})
                print("¡Vídeo guardado con éxito como 'simulacion_3D_coeficientes_transparente.mov'!")
            except Exception as e:
                print(f"Error al guardar vídeo. Detalles: {e}")

        plt.show()