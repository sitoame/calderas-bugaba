import pickle
import os
# Cargar archivo pickle
def loadFileAsDictionary(file_path):
    with open(file_path, 'rb') as file:
        try:
            data = pickle.load(file)
            return data
        except EOFError:
            # En caso de que el archivo esté vacío o corrupto
            return {}