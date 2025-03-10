import pdfplumber
import re

def limpiar_texto(texto):
    """
    Limpia caracteres repetidos, espacios extra y normaliza el contenido extraído del PDF.
    """
    # Eliminar caracteres repetidos (Ej: "NN UU EE VV OO" -> "NUEVO")
    texto = re.sub(r'([A-Z])\s*\1+', r'\1', texto, flags=re.IGNORECASE)
    
    # Reemplazar múltiples espacios por un solo espacio
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def extraer_texto(pdf_path):
    """ Extrae y limpia el texto del PDF. """
    texto_paginas = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text(x_tolerance=1, y_tolerance=1)  # Ajusta tolerancia de extracción
            if texto:
                texto_limpio = limpiar_texto(texto)
                texto_paginas.append(texto_limpio)
    
    texto_completo = "\n".join(texto_paginas)
    return texto_completo
