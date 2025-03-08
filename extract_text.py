import pdfplumber

def extraer_texto(pdf_path):
    """ Extrae el texto completo del PDF. """
    texto_paginas = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text()
            if texto:
                texto_paginas.append(texto)
            #print(f"Página {page_num} procesada")
    texto_completo = "\n".join(texto_paginas)
    print(texto_completo)
    return texto_completo
