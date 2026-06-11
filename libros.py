import os
from pathlib import Path
from string import punctuation
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


class Libro:
    def __init__(self, name, filename) -> None:
        self._name = None
        self._filename = None
        self.name = name
        self.filename = filename
        self.CARACTERES_ESPECIALES: str | None = None
        self.STOPWORDS: set[str] | None = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("El nombre del libro debe ser un string.")
        self._name = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if not isinstance(value, str):
            raise TypeError("El filename debe ser un string.")
        if not os.path.exists(value):
            raise FileNotFoundError(f"El archivo no existe: {value}")
        self._filename = value

    def _limpiar_linea(self, linea):
        if self.CARACTERES_ESPECIALES:
            tabla = str.maketrans("", "", self.CARACTERES_ESPECIALES)
            return linea.translate(tabla)
        return linea

    def _limpiar_tokens(self, tokens):
        if self.STOPWORDS:
            tokens[:] = [token for token in tokens if token not in self.STOPWORDS]
        return tokens

    def _preprocesar_linea(self, linea) -> list[str]:
        linea = linea.strip().lower()
        linea = self._limpiar_linea(linea)
        tokens = linea.split()
        tokens = self._limpiar_tokens(tokens)
        return tokens

    def leer_libro(self) -> list[str]:
        lineas_no_vacias = []
        with open(self.filename, "r", encoding="utf-8") as f:
            for linea in f:
                linea_limpia = linea.strip()
                if linea_limpia:
                    lineas_no_vacias.append(linea)
        return lineas_no_vacias

    def preprocesar_libro(self) -> dict[str, int]:
        frecuencias = {}
        lineas = self.leer_libro()
        for linea in lineas:
            tokens_limpios = self._preprocesar_linea(linea)
            for token in tokens_limpios:
                frecuencias[token] = frecuencias.get(token, 0) + 1
        return frecuencias

    def __str__(self) -> str:
        return f"Libro: {self.name} (Archivo: {self.filename})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', filename='{self.filename}')"


class LibroGutenberg(Libro):
    def leer_libro(self) -> list[str]:
        lineas_no_vacias = []
        dentro_del_contenido = False

        with open(self.filename, "r", encoding="utf-8") as f:
            for linea in f:
                linea_original = linea
                linea_strip = linea.strip()

                if not dentro_del_contenido and linea_strip.startswith("*** START"):
                    dentro_del_contenido = True
                    continue

                if dentro_del_contenido and linea_strip.startswith("*** END"):
                    break

                if dentro_del_contenido and linea_strip:
                    lineas_no_vacias.append(linea_original)

        return lineas_no_vacias


class LibroEnglish(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        self.STOPWORDS = set(stopwords.words("english"))


class LibroSpanish(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        self.STOPWORDS = set(stopwords.words("spanish"))


class LibroFrench(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        self.STOPWORDS = set(stopwords.words("french"))


def crear_lista_libros_ingles(directory: str, caract_especiales=punctuation):
    libros = []
    path = Path(directory)
    for file in path.glob("*.txt"):
        filename = str(file.relative_to(path.parent))
        libro = LibroEnglish(file.name, filename)
        libro.CARACTERES_ESPECIALES = caract_especiales
        libros.append(libro)
    return libros
