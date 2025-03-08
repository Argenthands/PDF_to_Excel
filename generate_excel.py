import pandas as pd

def generar_excel(movimientos, output_path):
    """ Genera un archivo Excel con los movimientos bancarios procesados. """
    df = pd.DataFrame(movimientos, columns=["FECHA", "DETALLE DEL MOVIMIENTO", "COMPROBANTE", "DÉBITO", "CRÉDITO", "SALDO"])
    df.to_excel(output_path, index=False, engine="xlsxwriter")
    print(f"Archivo Excel generado: {output_path}")