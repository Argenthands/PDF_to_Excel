import re

def procesar_movimientos(texto):
    """ Procesa el texto depurado para identificar correctamente los movimientos bancarios. """
    movimientos = []
    fecha_regex = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")  # Fecha al inicio de la línea
    detalle_extra_regex = re.compile(r"(CUIT Destino:|Originante:)")  # Líneas de detalles adicionales

    for line in texto.split("\n"):
        line = line.strip()
        cols = line.split()

        # Si hay suficientes columnas y la primera es una fecha, y la línea termina en '*'
        if len(cols) > 5 and fecha_regex.match(cols[0]) and cols[-1] == "*":
            fecha = cols[0]
            detalle = " ".join(cols[1:-4])  # Todo hasta antes de los 3 últimos valores
            try:
                debito = float(cols[-4].replace(".", "").replace(",", ".")) if cols[-4] != "0,00" else None
                credito = float(cols[-3].replace(".", "").replace(",", ".")) if cols[-3] != "0,00" else None
                saldo = float(cols[-2].replace(".", "").replace(",", "."))  # Último número antes del '*'
            except ValueError:
                debito, credito, saldo = None, None, None  # En caso de error, asignamos None

            movimientos.append([fecha, detalle, "", debito, credito, saldo])  # Comprobante vacío por ahora

        # Si la línea contiene CUIT Destino o Originante, la agregamos al último movimiento
        elif movimientos and detalle_extra_regex.search(line):
            movimientos[-1][1] += " " + line  

    print(f"Total de movimientos extraídos: {len(movimientos)}")
    return movimientos
