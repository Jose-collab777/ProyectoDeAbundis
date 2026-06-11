from libros import crear_lista_libros_ingles
from recomendaciones import Recomendador

def iniciar_menu():
    print("=" * 60)
    print("BIENVENIDO AL SISTEMA DE RECOMENDACION DE LIBROS TF-IDF")
    print("=" * 60)
    print("Este programa analiza de forma automatica una biblioteca utilizando")
    print("frecuencia de palabras y la rareza de terminos para extraer conceptos")
    print("clave y recomendarte lecturas similares basadas en tus gustos.")
    print("=" * 60)
    print("\nCargando los libros desde la carpeta, por favor espera...")

    lista_libros = crear_lista_libros_ingles("Books/")
    if not lista_libros:
        print("Error: No se encontraron libros en la carpeta Books/. Ejecuta primero get_books.py")
        return

    rec = Recomendador(lista_libros)
    rec.set_pesos()

    print(f"Se procesaron correctamente {len(lista_libros)} libros.\n")

    while True:
        print("¿Que te gustaria hacer?")
        print("1. Ver el resumen de palabras clave de un libro")
        print("2. Recibir recomendaciones basadas en un libro que te guste")
        print("3. Salir del programa")

        opcion = input("\nSelecciona una opcion (1, 2 o 3): ").strip()

        if opcion == "3":
            print("\nGracias por usar el recomendador. Vuelve pronto.")
            break

        if opcion in ["1", "2"]:
            print("\n" + "-" * 40)
            print("CATALOGO DE LIBROS DISPONIBLES:")
            print("-" * 40)
            rec.mostrar_libros()
            print("-" * 40)

            try:
                idx = int(input("\nIntroduce el indice del libro: "))
                if idx < 0 or idx >= len(lista_libros):
                    print("Error: Ese indice no existe.")
                    continue
            except ValueError:
                print("Error: Introduce un numero valido.")
                continue

            if opcion == "1":
                try:
                    num_palabras = int(input("¿Cuantas palabras clave deseas ver? "))
                    palabras_clave = rec.resumen(idx, num_palabras)

                    print("\n" + "*" * 40)
                    titulo_limpio = lista_libros[idx].name.replace(".txt", "").replace(".TXT", "").upper()
                    print(f" PALABRAS CLAVE PARA: {titulo_limpio}")
                    print(" " + "*" * 40)

                    for i, palabra in enumerate(palabras_clave, 1):
                        print(f"  {i}. {palabra}")
                    print("=" * 40)
                except ValueError:
                    print("Error: Debe ser un numero entero.")

            elif opcion == "2":
                try:
                    num_recom = int(input("¿Cuantas recomendaciones deseas? "))
                    libros_top = rec.libros_similares(idx, num_recom)

                    print("\n" + "-" * 40)
                    print(f" LIBROS RECOMENDADOS BASADOS EN TU INTERES:")
                    print(" " + "-" * 40)

                    for i, libro in enumerate(libros_top, 1):
                        print(f"  [{i}] {libro}")
                    print("=" * 40)
                except ValueError:
                    print("Error: Debe ser un numero entero.")
        else:
            print("Opcion no valida.")

if __name__ == "__main__":
    iniciar_menu()
