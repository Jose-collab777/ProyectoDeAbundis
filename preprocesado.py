def limpiar_linea(linea, caracteres_especiales):
    if caracteres_especiales:
        tabla = str.maketrans("", "", caracteres_especiales)
        return linea.translate(tabla)
    return linea

def limpiar_tokens(tokens, stopwords):
    if stopwords:
        tokens[:] = [token for token in tokens if token not in stopwords]
    return tokens

def preprocesar_linea(linea, caracteres_especiales, stopwords) -> list[str]:
    linea = linea.strip().lower()
    linea = limpiar_linea(linea, caracteres_especiales)
    tokens = linea.split()
    tokens = limpiar_tokens(tokens, stopwords)
    return tokens

def leer_libro(filename) -> list[str]:
    lineas_no_vacias = []
    with open(filename, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                lineas_no_vacias.append(linea)
    return lineas_no_vacias

def preprocesar_libro(libro: list[str], caracteres_especiales, stopwords) -> dict[str, int]:
    frecuencias = {}
    for linea in libro:
        tokens_limpios = preprocesar_linea(linea, caracteres_especiales, stopwords)
        for token in tokens_limpios:
            frecuencias[token] = frecuencias.get(token, 0) + 1
    return frecuencias
