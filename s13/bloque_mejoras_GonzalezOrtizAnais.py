
import emoji

# ==================================================================
# ---------------------- Traducción emoji --------------------------
# ==================================================================

def traducir_palabra_a_emoji(input_text: str) -> str:
    """Intenta traducir una palabra a emoji."""
    
    for lang in ["es", "alias"]:
        em = emoji.emojize(f":{input_text}:", language=lang)
        if em != f":{input_text}:":
            return em
    return None

def traducir_emoji_a_palabra(input_text: str) -> str:
    """Intenta traducir un emoji a palabra."""
    
    dem_es = emoji.demojize(input_text, language='es')
    dem_en = emoji.demojize(input_text, language='alias')

    if dem_es != input_text:
        return dem_es.strip(":")
    if dem_en != input_text:
        return dem_en.strip(":")
        
    return None

def emoji_translate(input_text: str) -> str:
    """
    Traduce palabra → emoji o emoji → palabra.

    Maneja errores en caso de textos no reconocidos.

    Parámetros:
        input_text (str): Texto o emoji a traducir.

    Retorna:
        str: Emoji correspondiente o palabra; si no se reconoce, devuelve un mensaje de error.
    """
    try:
        input_text = input_text.strip()

        # Intento de traducción palabra → emoji
        emoji_result = traducir_palabra_a_emoji(input_text)
        if emoji_result:
            return emoji_result

        # Intento emoji → palabra
        palabra_result = traducir_emoji_a_palabra(input_text)
        if palabra_result:
            return palabra_result

        return "Emoji desconocido"
        
    except Exception:
        return "Error al traducir"


def formato_clave_legible(clave: dict) -> str:
    """
    Convierte una clave de codificación en un texto legible para mostrar.

    Parámetros:
        clave (dict): Diccionario con caracteres y sus emojis correspondientes.

    Retorna:
        str: Texto formateado mostrando cada par de carácter → emoji.
    """
    texto = "Clave actual:\n\n"
    for caracter in clave:
        emoji = clave[caracter]
        texto += f"{caracter} → {emoji}\n"
    return texto