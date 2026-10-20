""" Guarda la simulación en un array formato npz para su posterior uso (evitar simular muchas veces) """

import numpy as np
import os
import uuid


def guardarsimulacion(trayectoria, tiempo, vector_inicial, vector_sistema, necuacion):
    """
  Función que guarda la simulación en un array .npz.

  Parameters:
  -----------
  trayectoria : array
    vector de posiciones y velocidades.
  tiempo : array
    vector de tiempo.
  vector_inicial : array
    vector de posiciones y velocidades iniciales.
  vector_sistema : array
    vector de condiciones del sistema (T, M, gamma)
  necuacion : array
    vector que contiene la ecuación usada

  Returns:
  --------
  datos : file .npz
    archivo que contiene los datos anteriores en formato .npz.
  """
    # Buscamos el nombre de los archivos de este directorio, para poder guardar nuestro archivo con un nombre único.

    #Creación de la carpeta "simulaciones"
    carpeta = "simulaciones"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Creamos la cadena que define la versión (parámetros físicos)
    version_str = [str(cadena) for cadena in np.hstack((vector_inicial, vector_sistema, necuacion))]
    version_str = "_".join(version_str)

    # Generamos un ID único de 6 caracteres para este archivo concreto
    id_unico = uuid.uuid4().hex[:6]

    # Nombre: datos_[ID]_[VERSION].npz
    savename = f"{carpeta}/datos_{id_unico}_{version_str}.npz"

    np.savez(savename, trayectoria=trayectoria, tiempo=tiempo, vector_inicial=vector_inicial,
             vector_sistema=vector_sistema, necuacion=necuacion)
