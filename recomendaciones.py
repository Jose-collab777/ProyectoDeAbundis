import math
from libros import Libro

class Recomendador:
    def __init__(self, libros: list[Libro]) -> None:
        self.libros = libros
        self._pesos = None
        self.vocabulario = list(set(palabra for libro in libros for palabra in libro.palabras))

    def set_pesos(self) -> None:
        num_libros = len(self.libros)
        df = {palabra: 0 for palabra in self.vocabulario}
        for libro in self.libros:
            for palabra in set(libro.palabras):
                if palabra in df:
                    df[palabra] += 1

        idf = {palabra: math.log(num_libros / conteo) for palabra, conteo in df.items()}

        self._pesos = []
        for libro in self.libros:
            tf = {}
            for palabra in libro.palabras:
                tf[palabra] = tf.get(palabra, 0) + 1

            pesos_libro = {palabra: (tf.get(palabra, 0) * idf[palabra] if palabra in tf else 0.0) for palabra in self.vocabulario}
            self._pesos.append(pesos_libro)

    def get_pesos(self):
        return self._pesos

    def _producto_punto(self, idx_1: int, idx_2: int) -> float:
        pesos_1 = self._pesos[idx_1]
        pesos_2 = self._pesos[idx_2]
        return sum(pesos_1[p] * pesos_2[p] for p in self.vocabulario)

    def _similitud(self, idx_1, idx_2) -> float:
        if idx_1 == idx_2:
            return 1.0
        prod_punto = self._producto_punto(idx_1, idx_2)
        norma_1 = math.sqrt(sum(peso ** 2 for peso in self._pesos[idx_1].values()))
        norma_2 = math.sqrt(sum(peso ** 2 for peso in self._pesos[idx_2].values()))
        if norma_1 == 0 or norma_2 == 0:
            return 0.0
        return prod_punto / (norma_1 * norma_2)

    def mostrar_libros(self):
        print(f"{'Índice':<8} | {'Título del Libro'}")
        print("-" * 50)
        for idx, libro in enumerate(self.libros):
            print(f"{idx:<8} | {libro.titulo}")

    def resumen(self, idx_libro, num_palabras) -> list[str]:
        pesos_libro = self._pesos[idx_libro]
        palabras_ordenadas = sorted(pesos_libro.items(), key=lambda x: x[1], reverse=True)
        return [palabra for palabra, peso in palabras_ordenadas if peso > 0][:num_palabras]

    def libros_similares(self, idx_libro, num_libros) -> list[str]:
        similitudes = []
        for idx_otro in range(len(self.libros)):
            if idx_otro != idx_libro:
                similitudes.append((idx_otro, self._similitud(idx_libro, idx_otro)))

        similitudes_ordenadas = sorted(similitudes, key=lambda x: x[1], reverse=True)

        recomendaciones = []
        for i in range(min(num_libros, len(similitudes_ordenadas))):
            idx_recom, score = similitudes_ordenadas[i]
            recomendaciones.append(f"{self.libros[idx_recom].titulo} (Similitud: {score:.4f})")

        return recomendaciones
