import pdfplumber
import pandas as pd
import re

# Cuidado con los espacios que en algunos sistemas operativos pueden generar errores
pdf_path = r"C:\Users\ale\Documents\AlejandroDavidBenolol\Development\Work\EstudioBS\PDF-ToExccel\NBCH2022.pdf"

output_excel = "extracto_bancario.xlsx"

def extraer_texto(pdf_path):
    """ Extrae el texto completo del PDF. """
    texto_paginas = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text()
            if texto:
                texto_paginas.append(texto)
            print(f"Página {page_num} procesada")
    texto_completo = "\n".join(texto_paginas)
    return texto_completo

def depurar_texto(texto):
    """ Extrae solo la sección útil del texto, entre líneas de guiones bajos. """
    lineas = texto.split("\n")
    inicio, fin = None, None
    
    for i, line in enumerate(lineas):
        if "___" in line:
            if inicio is None:
                inicio = i  # Primera línea con "___"
            else:
                fin = i  # Segunda línea con "___"
                break  # Solo nos interesa la primera sección de datos
    
    if inicio is not None and fin is not None:
        texto_depurado = "\n".join(lineas[inicio + 1:fin])  # Extraer entre los guiones
        print("Texto depurado correctamente.")
    else:
        texto_depurado = ""
        print("No se encontraron delimitadores de datos.")
    
    print("Texto depurado:")
    print(texto_depurado)  # Imprimir el texto depurado para revisión
    return texto_depurado

def procesar_movimientos(texto):
    """ Procesa el texto depurado para identificar movimientos bancarios. """
    movimientos = []
    fecha_regex = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")
    
    for line_num, line in enumerate(texto.split("\n")):
        line = line.strip()
        cols = line.split()
        if cols and fecha_regex.match(cols[0]):
            fecha = cols[0]
            cols = cols[1:]
            debito, credito, saldo = None, None, None
            if len(cols) >= 3:
                try:
                    saldo = float(cols[-1].replace(".", "").replace(",", "."))
                    credito = float(cols[-2].replace(".", "").replace(",", ".")) if cols[-2] != "0,00" else None
                    debito = float(cols[-3].replace(".", "").replace(",", ".")) if cols[-3] != "0,00" else None
                    detalle = " ".join(cols[:-3])
                except ValueError:
                    detalle = " ".join(cols)
            else:
                detalle = " ".join(cols)
            movimientos.append([fecha, detalle, "", debito, credito, saldo])
        elif movimientos:
            movimientos[-1][1] += " " + line  # Agregar detalles adicionales a la última transacción
    
    print(f"Total de movimientos extraídos: {len(movimientos)}")
    return movimientos

def generar_excel(movimientos, output_path):
    """ Genera un archivo Excel con los movimientos bancarios procesados. """
    df = pd.DataFrame(movimientos, columns=["FECHA", "DETALLE DEL MOVIMIENTO", "COMPROBANTE", "DÉBITO", "CRÉDITO", "SALDO"])
    df.to_excel(output_path, index=False, engine="xlsxwriter")
    print(f"Archivo Excel generado: {output_path}")

# Aquí está la instanciación del programa
if __name__ == "__main__":
    print("Procesando")
    texto = extraer_texto(pdf_path)
    print("Texto extraído")
    texto_depurado = depurar_texto(texto)
    print("Texto depurado")
    movimientos = procesar_movimientos(texto_depurado)
    print("Movimientos procesados")
    generar_excel(movimientos, output_excel)
    print("Proceso completado")
