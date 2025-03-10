import re

def procesar_movimientos(texto):
    """
    Procesa el texto depurado para identificar correctamente los movimientos bancarios.
    Esta versión usa expresiones regulares para extraer bloques de movimientos
    que comienzan con una fecha y terminan con un asterisco (*).
    """
    movimientos = []
    
    # Extrae bloques que comienzan con fecha y terminan con '*' (modo DOTALL para abarcar saltos de línea)
    bloque_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{4}.*?\*)", re.DOTALL)
    bloques = bloque_pattern.findall(texto)
    
    # Patrón para extraer los campos de cada movimiento.
    # Se asume que los números tienen formato: miles con punto y decimales con coma, ej. 4.222,20 o 0,00
    movimiento_pattern = re.compile(
        r"^(?P<fecha>\d{1,2}/\d{1,2}/\d{4})\s+"
        r"(?P<rest>.+?)\s+"
        r"(?P<debito>\d{1,3}(?:[.,]\d{3})*,\d{2}|0,00)\s+"
        r"(?P<credito>\d{1,3}(?:[.,]\d{3})*,\d{2}|0,00)\s+"
        r"(?P<saldo>\d{1,3}(?:[.,]\d{3})*,\d{2})\s+\*$",
        re.DOTALL
    )
    
    detalle_extra_regex = re.compile(r"(CUIT Destino:|Originante:)")
    
    for bloque in bloques:
        # Reemplazamos saltos de línea por espacios para trabajar con el bloque en una sola línea
        bloque = bloque.strip().replace("\n", " ")
        m = movimiento_pattern.match(bloque)
        if m:
            fecha = m.group("fecha")
            rest = m.group("rest").strip()
            debito_str = m.group("debito")
            credito_str = m.group("credito")
            saldo_str = m.group("saldo")
            
            # Función para convertir el formato numérico
            def conv(num_str):
                return float(num_str.replace(".", "").replace(",", "."))
            
            debito = conv(debito_str) if debito_str != "0,00" else None
            credito = conv(credito_str) if credito_str != "0,00" else None
            saldo = conv(saldo_str)
            
            # Intentamos separar un comprobante (última palabra numérica) del detalle, si existe
            parts = rest.rsplit(" ", 1)
            if len(parts) == 2 and parts[1].isdigit():
                detalle = parts[0]
                comprobante = parts[1]
            else:
                detalle = rest
                comprobante = ""
            
            movimientos.append([fecha, detalle, comprobante, debito, credito, saldo])
        else:
            # Si el bloque no coincide con el patrón, pero contiene datos extra (como CUIT Destino u Originante),
            # se añade al detalle del último movimiento (si existe)
            if movimientos and detalle_extra_regex.search(bloque):
                movimientos[-1][1] += " " + bloque

    print(f"Total de movimientos extraídos: {len(movimientos)}")
    return movimientos
