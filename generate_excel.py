import pandas as pd

def generar_excel(movimientos, output_path):
    """ Genera un archivo Excel con formato mejorado. """
    df = pd.DataFrame(movimientos, columns=["FECHA", "DETALLE DEL MOVIMIENTO", "COMPROBANTE", "DÉBITO", "CRÉDITO", "SALDO"])

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Movimientos", index=False)
        workbook = writer.book
        worksheet = writer.sheets["Movimientos"]

        # Formato de números con dos decimales
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        worksheet.set_column("D:F", None, number_format)  # Aplica formato a Débito, Crédito y Saldo

        # Ajuste automático del ancho de las columnas
        for col_num, col_name in enumerate(df.columns):
            max_length = max(df[col_name].astype(str).map(len).max(), len(col_name))
            worksheet.set_column(col_num, col_num, max_length + 2)

    print(f"Archivo Excel generado: {output_path}")