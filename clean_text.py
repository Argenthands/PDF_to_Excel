import re

def depurar_texto(texto):
    """
    Depura el texto eliminando encabezados de página y dejando solo los movimientos bancarios.
    """
    SplitLine = '_________________________________________________________________________________________________________________'
    bloques = texto.split(SplitLine)
    patron_fecha = re.compile(r'\d{1,2}/\d{1,2}/\d{4}')  # Fechas tipo DD/MM/AAAA

    informacion_util = []

    for bloque in bloques:
        lineas = bloque.split('\n')
        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()

            # Detecta si inicia una cabecera de página
            if linea.startswith("Hoja............:"):
                # Buscar la línea "Transporte hoja anterior" o saltar hasta el final de la cabecera
                while i < len(lineas) and "Transporte hoja anterior" not in lineas[i]:
                    i += 1
                i += 1  # Saltar la línea "Transporte hoja anterior"
                continue  

            # Filtramos solo los movimientos bancarios
            if patron_fecha.search(linea):  
                informacion_util.append(linea)
            elif "CUIT Destino:" in linea or "Originante:" in linea:
                informacion_util.append(linea)

            i += 1  # Avanzar en la lista de líneas

    return '\n'.join(informacion_util)