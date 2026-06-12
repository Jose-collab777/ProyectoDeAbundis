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
    """
    Representa un libro de texto y provee métodos para leerlo y preprocesarlo.

    Attributes:
        name (str): Título o nombre del libro.
        filename (str): Ruta al archivo de texto.
        CARACTERES_ESPECIALES (str | None): Caracteres a eliminar durante la limpieza.
        STOPWORDS (set[str] | None): Palabras vacías a filtrar durante la tokenización.
    """

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
        """Valida que el nombre sea un string."""
        if not isinstance(value, str):
            raise TypeError("El nombre del libro debe ser un string.")
        self._name = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        """Valida que filename sea un string y que el archivo exista en disco."""
        if not isinstance(value, str):
            raise TypeError("El filename debe ser un string.")
        if not os.path.exists(value):
            raise FileNotFoundError(f"El archivo no existe: {value}")
        self._filename = value

    def _limpiar_linea(self, linea):
        """Elimina CARACTERES_ESPECIALES de una línea usando una tabla de traducción."""
        if self.CARACTERES_ESPECIALES:
            tabla = str.maketrans("", "", self.CARACTERES_ESPECIALES)
            return linea.translate(tabla)
        return linea

    def _limpiar_tokens(self, tokens):
        """Filtra los tokens que estén en STOPWORDS."""
        if self.STOPWORDS:
            tokens[:] = [token for token in tokens if token not in self.STOPWORDS]
        return tokens

    def _preprocesar_linea(self, linea) -> list[str]:
        """
        Normaliza una línea: lowercase, elimina caracteres especiales y stopwords.

        Returns:
            list[str]: Tokens limpios de la línea.
        """
        linea = linea.strip().lower()
        linea = self._limpiar_linea(linea)
        tokens = linea.split()
        tokens = self._limpiar_tokens(tokens)
        return tokens

    def leer_libro(self) -> list[str]:
        """
        Lee el archivo y retorna las líneas no vacías.

        Returns:
            list[str]: Líneas con contenido del archivo.
        """
        lineas_no_vacias = []
        with open(self.filename, "r", encoding="utf-8") as f:
            for linea in f:
                linea_limpia = linea.strip()
                if linea_limpia:
                    lineas_no_vacias.append(linea)
        return lineas_no_vacias

    def preprocesar_libro(self) -> dict[str, int]:
        """
        Cuenta la frecuencia de cada token en el libro tras el preprocesamiento.

        Returns:
            dict[str, int]: Mapa de token → frecuencia de aparición.
        """
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
    """
    Extiende Libro para manejar el formato de Project Gutenberg.

    Sobreescribe leer_libro() para ignorar el encabezado y pie de página
    delimitados por las marcas '*** START' y '*** END'.
    """

    def leer_libro(self) -> list[str]:
        """
        Lee solo el contenido entre '*** START ...' y '*** END ...'.

        Returns:
            list[str]: Líneas no vacías del cuerpo del libro.
        """
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
    """LibroGutenberg con stopwords en inglés (NLTK)."""

    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        self.STOPWORDS = set(stopwords.words("english"))


class LibroSpanish(LibroGutenberg):
    """LibroGutenberg con stopwords en español (NLTK)."""

    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        self.STOPWORDS = set(stopwords.words("spanish"))


class LibroFrench(LibroGutenberg):
    """LibroGutenberg con stopwords en francés (NLTK)."""

    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        self.STOPWORDS = set(stopwords.words("french"))


def crear_lista_libros_ingles(directory: str, caract_especiales=punctuation) -> list[LibroEnglish]:
    """
    Carga todos los archivos .txt de un directorio como instancias de LibroEnglish.

    Args:
        directory (str): Ruta a la carpeta con los archivos de texto.
        caract_especiales (str): Caracteres a eliminar en el preprocesamiento.
                                 Por defecto usa string.punctuation.

    Returns:
        list[LibroEnglish]: Lista de libros listos para preprocesar.
    """
    libros = []
    path = Path(directory)
    for file in path.glob("*.txt"):
        filename = str(file.relative_to(path.parent))
        libro = LibroEnglish(file.name, filename)
        libro.CARACTERES_ESPECIALES = caract_especiales
        libros.append(libro)
    return libros