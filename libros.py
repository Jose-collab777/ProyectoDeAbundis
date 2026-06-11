import os
import string

class Libro:
    def __init__(self, titulo: str, palabras: list[str]):
        self.titulo = titulo
        self.palabras = palabras


def cargar_mis_libros(ruta_carpeta="./Books"):
    """Lee la carpeta y regresa la lista de objetos tipo Libro"""
    mis_libros = []
    if not os.path.exists(ruta_carpeta):
        print(f" Error: No se encontró la carpeta '{ruta_carpeta}'")
        return mis_libros

    archivos = sorted([f for f in os.listdir(ruta_carpeta) if f.endswith(".txt")])
    for archivo in archivos:
        with open(os.path.join(ruta_carpeta, archivo), "r", encoding="utf-8") as f:
            texto = f.read().lower()
            texto_limpio = texto.translate(str.maketrans("", "", string.punctuation))
            palabras = texto_limpio.split()

            titulo_libro = archivo.replace(".txt", "").replace("_", " ")
            mis_libros.append(Libro(titulo=titulo_libro, palabras=palabras))

    return mis_libros

