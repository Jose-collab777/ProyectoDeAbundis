from string import punctuation
from typing import Dict
import nltk
from nltk.corpus import stopwords
import preprocesado

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


def main(filename: str) -> Dict[str, int]:
    """
    Preprocesa un libro y retorna la frecuencia de sus tokens.

    Usa puntuación estándar como caracteres especiales y stopwords en inglés (NLTK).

    Args:
        filename (str): Ruta al archivo de texto del libro.

    Returns:
        Dict[str, int]: Mapa de token → frecuencia de aparición.
    """
    caracteres_especiales = punctuation
    stops = set(stopwords.words("english"))

    libro_lineas = preprocesado.leer_libro(filename)

    resultado = preprocesado.preprocesar_libro(libro_lineas, caracteres_especiales, stops)

    print(f"Palabras unicas encontradas: {len(resultado)}")
    return resultado


if __name__ == '__main__':
    # Prueba rápida: toma el primer .txt encontrado en Books/
    import os
    directory = 'Books/'
    filename = None

    if os.path.exists(directory):
        archivos = [f for f in os.listdir(directory) if f.endswith('.txt')]
        if archivos:
            filename = os.path.join(directory, archivos[0])

    if filename and os.path.exists(filename):
        main(filename)
    else:
        print("Para ejecutar de forma individual, asegurese de tener libros en la carpeta Books/")