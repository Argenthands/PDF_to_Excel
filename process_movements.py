import re

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
