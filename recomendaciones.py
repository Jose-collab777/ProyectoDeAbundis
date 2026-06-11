import math

class Recomendador:
    def __init__(self, libros) -> None:
        """
        libros: lista con instancias de tipo `Libro`
        """
        self.libros = libros
        self._pesos = None

        vocab = set()
        for libro in self.libros:
            frecuencias = libro.preprocesar_libro()
            vocab.update(frecuencias.keys())
        self.vocabulario = list(vocab)

    def set_pesos(self) -> None:
        """Calcula los pesos del algorítmo TF-IDF requeridos para las
        recomendaciones y los guarda en `self._pesos`
        """
        num_libros = len(self.libros)
        frecuencias_libros = [libro.preprocesar_libro() for libro in self.libros]

        df = {palabra: 0 for palabra in self.vocabulario}
        for frecs in frecuencias_libros:
            for palabra in frecs.keys():
                if palabra in df:
                    df[palabra] += 1

        idf = {}
        for palabra, conteo in df.items():
            if conteo > 0:
                idf[palabra] = math.log(num_libros / conteo)
            else:
                idf[palabra] = 0.0

        self._pesos = []
        for frecs in frecuencias_libros:
            pesos_libro = {}
            for palabra in self.vocabulario:
                tf = frecs.get(palabra, 0)
                pesos_libro[palabra] = tf * idf.get(palabra, 0.0)
            self._pesos.append(pesos_libro)

    def get_pesos(self):
        """Regresa los pesos calculados"""
        return self._pesos

    def _producto_punto(self, idx_1: int, idx_2: int) -> float:
        """Producto punto entre los libros con índices idx_1 y idx_2."""
        pesos_1 = self._pesos[idx_1]
        pesos_2 = self._pesos[idx_2]
        return sum(pesos_1[p] * pesos_2[p] for p in self.vocabulario)

    def _similitud(self, idx_1, idx_2) -> float:
        """Similitud entre los libros con índices idx_1 y idx_2 de acuerdo al
        coseno del ángulo que forman sus vectores.
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
        """Mostrarle al usuario el índice y nombre para cada libro de acuerdo a
        nuestra lista de libros `self.libros`.
        """
        print(f"{'Indice':<8} | {'Titulo del Libro'}")
        print("-" * 50)
        for idx, libro in enumerate(self.libros):
            nombre_limpio = libro.name.replace(".txt", "").replace(".TXT", "")
            print(f"{idx:<8} | {nombre_limpio}")

    def resumen(self, idx_libro, num_palabras) -> list[str]:
        """Regresa una lista con las palabras más representativas de un libro
        de acuerdo a los pesos.
        """
        pesos_libro = self._pesos[idx_libro]
        palabras_ordenadas = sorted(pesos_libro.items(), key=lambda x: x[1], reverse=True)
        return [palabra for palabra, peso in palabras_ordenadas if peso > 0][:num_palabras]

    def libros_similares(self, idx_libro, num_libros) -> list[str]:
        """Regresa una lista con los libros más parecidos a un libro dado.
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
