def limpiar_linea(linea, caracteres_especiales):
    """
    Elimina caracteres especiales de una línea usando una tabla de traducción.

    Args:
        linea (str): Línea de texto a limpiar.
        caracteres_especiales (str | None): Caracteres a eliminar.

    Returns:
        str: Línea sin los caracteres especiales, o la misma línea si no se especificaron.
    """
    if caracteres_especiales:
        tabla = str.maketrans("", "", caracteres_especiales)
        return linea.translate(tabla)
    return linea


def limpiar_tokens(tokens, stopwords):
    """
    Filtra stopwords de una lista de tokens en lugar (modifica la lista original).

    Args:
        tokens (list[str]): Lista de tokens a filtrar.
        stopwords (set[str] | None): Palabras a eliminar.

    Returns:
        list[str]: Lista de tokens sin stopwords.
    """
    if stopwords:
        tokens[:] = [token for token in tokens if token not in stopwords]
    return tokens


def preprocesar_linea(linea, caracteres_especiales, stopwords) -> list[str]:
    """
    Normaliza una línea: lowercase, elimina caracteres especiales y stopwords.

    Args:
        linea (str): Línea de texto cruda.
        caracteres_especiales (str | None): Caracteres a eliminar.
        stopwords (set[str] | None): Palabras vacías a filtrar.

    Returns:
        list[str]: Tokens limpios de la línea.
    """
    linea = linea.strip().lower()
    linea = limpiar_linea(linea, caracteres_especiales)
    tokens = linea.split()
    tokens = limpiar_tokens(tokens, stopwords)
    return tokens


def leer_libro(filename) -> list[str]:
    """
    Lee un archivo de texto y retorna sus líneas no vacías.

    Args:
        filename (str): Ruta al archivo.

    Returns:
        list[str]: Líneas con contenido del archivo.
    """
    lineas_no_vacias = []
    with open(filename, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                lineas_no_vacias.append(linea)
    return lineas_no_vacias


def preprocesar_libro(libro: list[str], caracteres_especiales, stopwords) -> dict[str, int]:
    """
    Cuenta la frecuencia de cada token en un libro tras el preprocesamiento.

    Args:
        libro (list[str]): Líneas del libro (salida de leer_libro).
        caracteres_especiales (str | None): Caracteres a eliminar por línea.
        stopwords (set[str] | None): Palabras vacías a filtrar.

    Returns:
        dict[str, int]: Mapa de token → frecuencia de aparición.
    """
    frecuencias = {}
    for linea in libro:
        tokens_limpios = preprocesar_linea(linea, caracteres_especiales, stopwords)
        for token in tokens_limpios:
            frecuencias[token] = frecuencias.get(token, 0) + 1
    return frecuencias