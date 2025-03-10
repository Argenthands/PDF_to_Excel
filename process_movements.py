import re

def procesar_movimientos(texto):

    movimientos = []
    
    # Dividir el texto por el asterisco (eliminando espacios extra)
    tokens = re.split(r'\*\s*', texto)
    
    # Patrón para extraer movimientos que inician con fecha
    movimiento_pattern = re.compile(
        r"^(?P<fecha>\d{1,2}/\d{1,2}/\d{4})\s+"
        r"(?P<rest>.+?)\s+"
        r"(?P<debito>\d{1,3}(?:[.,]\d{3})*,\d{2}|0,00)\s+"
        r"(?P<credito>\d{1,3}(?:[.,]\d{3})*,\d{2}|0,00)\s+"
        r"(?P<saldo>\d{1,3}(?:[.,]\d{3})*,\d{2})\s*$",
        re.DOTALL
    )
    
    # Patrón para detectar tokens extra (líneas que inician con "CUIT Destino:" o "Originante:")
    extra_pattern = re.compile(r"^(CUIT Destino:|Originante:)", re.IGNORECASE)
    
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        # Si el token inicia con fecha, se procesa normalmente
        if re.match(r"^\d{1,2}/\d{1,2}/\d{4}", token):
            m = movimiento_pattern.match(token)
            if m:
                fecha = m.group("fecha")
                rest = m.group("rest").strip()
                debito_str = m.group("debito")
                credito_str = m.group("credito")
                saldo_str = m.group("saldo")
                
                # Función para convertir el número: "4.222,20" -> 4222.20
                def conv(num_str):
                    return float(num_str.replace(".", "").replace(",", "."))
                
                debito = conv(debito_str) if debito_str != "0,00" else 0.0
                credito = conv(credito_str) if credito_str != "0,00" else 0.0
                saldo = conv(saldo_str)
                
                # Intentar separar comprobante si la última palabra de "rest" es solo dígitos
                parts = rest.rsplit(" ", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    detalle = parts[0]
                    comprobante = parts[1]
                else:
                    detalle = rest
                    comprobante = ""
                    
                movimientos.append([fecha, detalle, comprobante, debito, credito, saldo])
            else:
                # Si no coincide con el patrón, se añade al detalle del último movimiento
                if movimientos:
                    movimientos[-1][1] += " " + token
                else:
                    movimientos.append(["00/00/00", token, "", 0.0, 0.0, 0.0])
        else:
            # Si el token no inicia con fecha pero empieza con "CUIT Destino:" u "Originante:",
            # creamos un movimiento dummy con fecha "00/00/00" y campos numéricos en 0.
            if extra_pattern.match(token):
                movimientos.append(["00/00/00", token, "", 0.0, 0.0, 0.0])
            else:
                # De lo contrario, se agrega al detalle del último movimiento (si existe)
                if movimientos:
                    movimientos[-1][1] += " " + token
                else:
                    movimientos.append(["00/00/00", token, "", 0.0, 0.0, 0.0])
    
    print(f"Total de movimientos extraídos: {len(movimientos)}")
    return movimientos
