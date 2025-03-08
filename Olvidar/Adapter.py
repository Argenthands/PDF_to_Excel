import pdfplumber
import pandas as pd
import re
import io

# Ruta del archivo PDF (ajusta esto según dónde guardaste el archivo)
pdf_path = "C:/Users/ale/Documents/archivo.pdf"


# Solicitar la clave de lectura
password = input("Ingresa la clave de lectura del PDF: ")

# Inicializar lista para almacenar los datos
movimientos = []

# Función para limpiar los valores monetarios
def limpiar_valor(valor):
    try:
        valor = valor.replace(".", "").replace(",", ".").replace("$", "").strip()
        if valor.startswith("-"):
            return -float(valor[1:])  # Convertir a número negativo si el valor tiene el signo '-'
        return float(valor)
    except:
        return None

# Expresión regular para detectar fechas en formatos d/m/aaaa, dd/m/aaaa, d/mm/aaaa, y dd/mm/aaaa
fecha_regex = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")

# Leer el PDF
try:
    with pdfplumber.open(pdf_path, password=password) as pdf:
        last_date = None  # Para completar fechas faltantes
        last_saldo = None  # Para comparar saldos
        for page_number, page in enumerate(pdf.pages, start=1):
            print(f"Procesando página {page_number}")
            text = page.extract_text()
            if not text:
                print(f"La página {page_number} está vacía o no se pudo extraer texto.")
                continue

            lines = text.split("\n")
            for line in lines:
                cols = line.split()

                # Buscar fecha al inicio de la línea
                if cols and fecha_regex.match(cols[0]):
                    last_date = cols[0]
                    cols = cols[1:]

                    # Extraer datos relevantes
                    if len(cols) >= 4:  # Asegurarse de que tenga suficientes columnas
                        movimiento = " ".join([word for word in cols[:-3]])  # Capturar todo hasta las últimas tres columnas
                        movimiento = movimiento[:30].rstrip()  # Truncar a 30 caracteres y eliminar espacios adicionales
                        debito = limpiar_valor(cols[-3])
                        credito = limpiar_valor(cols[-2])
                        saldo = limpiar_valor(cols[-1])

                        # Verificar si saldo es None y continuar si es así
                        if saldo is None:
                            continue

                        # Determinar el tipo de movimiento basado en saldo
                        if last_saldo is not None:
                            if saldo > last_saldo:
                                tipo_movimiento = "Crédito"
                            elif saldo < last_saldo:
                                tipo_movimiento = "Débito"
                            else:
                                continue  # Ignorar línea si el saldo es igual

                            # Guardar el movimiento
                            movimientos.append([last_date, movimiento, tipo_movimiento, debito, credito, saldo])

                        last_saldo = saldo
except Exception as e:
    print(f"Error al procesar el PDF: {e}")
    raise

# Crear DataFrame
df = pd.DataFrame(movimientos, columns=["Fecha", "Movimiento", "Tipo", "Débito", "Crédito", "Saldo"])

# Guardar en Excel localmente
excel_path = "extracto_banco.xlsx"
df.to_excel(excel_path, index=False, engine='xlsxwriter')

print(f"Archivo Excel generado: {excel_path}")
