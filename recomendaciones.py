import math

class Recomendador:
    def __init__(self, libros) -> None:
        """
        Inicializa el recomendador y construye el vocabulario global.

        Preprocesa todos los libros para reunir el conjunto de palabras únicas
        que servirá de base para los vectores TF-IDF.

        Args:
            libros (list[Libro]): Instancias de Libro a analizar.

        Attributes:
            libros (list[Libro]): Lista de libros cargados.
            vocabulario (list[str]): Palabras únicas en toda la colección.
            _pesos (list[dict] | None): Pesos TF-IDF; None hasta llamar set_pesos().
        """
        self.libros = libros
        self._pesos = None

        vocab = set()
        for libro in self.libros:
            frecuencias = libro.preprocesar_libro()
            vocab.update(frecuencias.keys())
        self.vocabulario = list(vocab)

    def set_pesos(self) -> None:
        """
        Calcula y almacena los pesos TF-IDF de cada libro.

        Para cada palabra del vocabulario:
        - TF: frecuencia bruta en el libro.
        - IDF: log(N / df), donde N = total de libros y df = libros que contienen la palabra.
        - Peso final: TF * IDF.

        Los pesos se guardan en self._pesos como lista de dicts {palabra: peso}.
        """
        num_libros = len(self.libros)
        frecuencias_libros = [libro.preprocesar_libro() for libro in self.libros]

        # Frecuencia de documento: cuántos libros contienen cada palabra
        df = {palabra: 0 for palabra in self.vocabulario}
        for frecs in frecuencias_libros:
            for palabra in frecs.keys():
                if palabra in df:
                    df[palabra] += 1

        # IDF: log(N / df); 0 si ningún libro contiene la palabra
        idf = {}
        for palabra, conteo in df.items():
            idf[palabra] = math.log(num_libros / conteo) if conteo > 0 else 0.0

        # Peso TF-IDF por libro
        self._pesos = []
        for frecs in frecuencias_libros:
            pesos_libro = {}
            for palabra in self.vocabulario:
                tf = frecs.get(palabra, 0)
                pesos_libro[palabra] = tf * idf.get(palabra, 0.0)
            self._pesos.append(pesos_libro)

    def get_pesos(self):
        """Retorna los pesos TF-IDF calculados por set_pesos()."""
        return self._pesos

    def _producto_punto(self, idx_1: int, idx_2: int) -> float:
        """
        Calcula el producto punto entre los vectores TF-IDF de dos libros.

        Args:
            idx_1 (int): Índice del primer libro.
            idx_2 (int): Índice del segundo libro.

        Returns:
            float: Suma de productos de los pesos por cada palabra del vocabulario.
        """
        pesos_1 = self._pesos[idx_1]
        pesos_2 = self._pesos[idx_2]
        return sum(pesos_1[p] * pesos_2[p] for p in self.vocabulario)

    def _similitud(self, idx_1, idx_2) -> float:
        """
        Calcula la similitud coseno entre dos libros.

        Retorna 1.0 si ambos índices son iguales. Retorna 0.0 si alguno
        de los vectores tiene norma cero.

        Args:
            idx_1 (int): Índice del primer libro.
            idx_2 (int): Índice del segundo libro.

        Returns:
            float: Valor en [0, 1] donde 1 indica máxima similitud.
        """
        if idx_1 == idx_2:
            return 1.0
        prod_punto = self._producto_punto(idx_1, idx_2)
        norma_1 = math.sqrt(sum(peso ** 2 for peso in self._pesos[idx_1].values()))
        norma_2 = math.sqrt(sum(peso ** 2 for peso in self._pesos[idx_2].values()))
        if norma_1 == 0 or norma_2 == 0:
            return 0.0
        return prod_punto / (norma_1 * norma_2)

    def mostrar_libros(self):
        """Imprime el catálogo con índice y título de cada libro en self.libros."""
        print(f"{'Indice':<8} | {'Titulo del Libro'}")
        print("-" * 50)
        for idx, libro in enumerate(self.libros):
            nombre_limpio = libro.name.replace(".txt", "").replace(".TXT", "")
            print(f"{idx:<8} | {nombre_limpio}")

    def resumen(self, idx_libro, num_palabras) -> list[str]:
        """
        Retorna las palabras más representativas de un libro según su peso TF-IDF.

        Args:
            idx_libro (int): Índice del libro en self.libros.
            num_palabras (int): Cantidad de palabras a retornar.

        Returns:
            list[str]: Palabras ordenadas de mayor a menor peso (solo peso > 0).
        """
        pesos_libro = self._pesos[idx_libro]
        palabras_ordenadas = sorted(pesos_libro.items(), key=lambda x: x[1], reverse=True)
        return [palabra for palabra, peso in palabras_ordenadas if peso > 0][:num_palabras]

    def libros_similares(self, idx_libro, num_libros) -> list[str]:
        """
        Retorna los libros más similares al libro dado, ordenados por similitud coseno.

        Args:
            idx_libro (int): Índice del libro de referencia.
            num_libros (int): Cantidad de recomendaciones a retornar.

        Returns:
            list[str]: Títulos con su puntaje, formato "Título (Similitud: X.XXXX)".
        """
        similitudes = []
        for idx_otro in range(len(self.libros)):
            if idx_otro != idx_libro:
                similitudes.append((idx_otro, self._similitud(idx_libro, idx_otro)))

        similitudes_ordenadas = sorted(similitudes, key=lambda x: x[1], reverse=True)

        recomendaciones = []
        for i in range(min(num_libros, len(similitudes_ordenadas))):
            idx_recom, score = similitudes_ordenadas[i]
            nombre_limpio = self.libros[idx_recom].name.replace(".txt", "").replace(".TXT", "")
            recomendaciones.append(f"{nombre_limpio} (Similitud: {score:.4f})")

        return recomendaciones