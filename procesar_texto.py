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
    caracteres_especiales = punctuation
    stops = set(stopwords.words("english"))

    libro_lineas = preprocesado.leer_libro(filename)

    resultado = preprocesado.preprocesar_libro(libro_lineas, caracteres_especiales, stops)

    print(f"Palabras unicas encontradas: {len(resultado)}")
    return resultado

if __name__ == '__main__':
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
