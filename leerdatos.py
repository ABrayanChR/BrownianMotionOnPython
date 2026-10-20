import numpy as np

def leerdatos(filename):
    """
    Función que lee los datos de un fichero dado (formato .npz)

    Parameters:
    -----------
    filename : str
      Nombre del fichero a leer

    Returns:
    --------
    datos : dict
      Diccionario con los datos leídos:
        'trayectoria'  : trayectorias (np.array)
        'tiempo'       : tiempos (np.array)
        'vector_inicial': vector_inicial (np.array)
        'vector_sistema': vector_sistema (np.array)
        'necuacion'    : necuacion (np.array)
    """
    data = np.load(filename)
    
    # Asegurarse de que las claves existen en el archivo .npz
    datos = {
        "trayectoria": data["trayectoria"],
        "tiempo": data["tiempo"],
        "vector_inicial": data["vector_inicial"],
        "vector_sistema": data["vector_sistema"],
        "necuacion": data["necuacion"]
    }
    
    return datos
