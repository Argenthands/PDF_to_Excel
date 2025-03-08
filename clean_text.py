import re

def depurar_texto(texto):
    SplitLine = '_________________________________________________________________________________________________________________'
    bloques = texto.split(SplitLine)
    patron_fecha = re.compile(r'\d{1,2}/\d{1,2}/\d{4}')  # Permitir fechas con 1 o 2 dígitos en día/mes
    patron_cabecera = re.compile(r'FECHA\s+DETALLE\s+DEL\s+MOVIMIENTO')

    informacion_util = []

    for bloque in bloques:
        lineas = bloque.split('\n')

        # Buscar la cabecera en cualquier línea del bloque
        cabecera_encontrada = any(patron_cabecera.search(linea) for linea in lineas)

        if cabecera_encontrada:
            for linea in lineas:
                linea = re.sub(r'([A-Z])\1+', r'\1', linea)  # Corrige caracteres duplicados
                linea = re.sub(r'\s+', ' ', linea).strip()  # Elimina espacios extra
                
                if patron_fecha.search(linea):  # Si la línea contiene una fecha
                    informacion_util.append(linea)
                elif "CUIT Destino:" in linea or "Originante:" in linea:
                    informacion_util.append(linea)

    return '\n'.join(informacion_util)
