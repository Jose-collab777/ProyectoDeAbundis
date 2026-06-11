# Importamos las funciones de tus dos módulos obligatorios
from libros import cargar_mis_libros
from recomendaciones import Recomendador

def iniciar_menu():
    print("=" * 60)
    print("¡BIENVENIDO AL SISTEMA DE RECOMENDACIÓN DE LIBROS!")
    print("=" * 60)
    print("Cargando los libros, por favor espera...")

    # Mandamos llamar al módulo libros
    mis_libros = cargar_mis_libros()
    if not mis_libros:
        return

    # Mandamos llamar al módulo recomendaciones
    rec = Recomendador(mis_libros)
    rec.set_pesos()

    print(f"¡Listo! Se procesaron correctamente {len(mis_libros)} libros.\n")

    while True:
        print("¿Qué te gustaría hacer hoy?")
        print("1. Ver el resumen de palabras clave de un libro")
        print("2. Recibir recomendaciones basadas en un libro que te guste")
        print("3. Salir del programa")

        opcion = input("\nSelecciona una opción (1, 2 o 3): ").strip()

        if opcion == "3":
            print("\n¡Gracias por usar el recomendador! Vuelve pronto.")
            break

        if opcion in ["1", "2"]:
            print("\n" + "-" * 40)
            print("CATÁLOGO DE LIBROS DISPONIBLES:")
            print("-" * 40)
            rec.mostrar_libros()
            print("-" * 40)

            try:
                idx = int(input("\nIntroduce el ÍNDICE del libro: "))
                if idx < 0 or idx >= len(mis_libros):
                    print(" Error: Ese índice no existe.")
                    continue
            except ValueError:
                print(" Error: Introduce un número válido.")
                continue

            if opcion == "1":
                try:
                    num_palabras = int(input("¿Cuántas palabras clave deseas ver?: "))
                    palabras_clave = rec.resumen(idx, num_palabras)
                    print(f" PALABRAS CLAVE PARA: {mis_libros[idx].titulo.upper()}")
                    for i, palabra in enumerate(palabras_clave, 1):
                        print(f"  {i}. {palabra}")
                    print("=" * 40)
                except ValueError:
                    print(" Error: Debe ser un número entero.")

            elif opcion == "2":
                try:
                    num_recom = int(input("¿Cuántas recomendaciones deseas?: "))
                    libros_top = rec.libros_similares(idx, num_recom)
                    print(f" LIBROS RECOMENDADOS BASADOS EN TU INTERÉS:")
                    for i, libro in enumerate(libros_top, 1):
                        print(f"  {i}. {libro}")
                    print("=" * 40)
                except ValueError:
                    print("Error: Debe ser un número entero.")
        else:
            print(" Opción no válida.")

if __name__ == "__main__":
    iniciar_menu()
