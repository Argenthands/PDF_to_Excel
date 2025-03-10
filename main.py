from extract_text import extraer_texto
from clean_text import depurar_texto
from process_movements import procesar_movimientos
from generate_excel import generar_excel

pdf_path = r"C:\Users\ale\Documents\AlejandroDavidBenolol\Development\Work\EstudioBS\PDF-ToExccel\NBCH2022.pdf"
output_excel = "extracto_bancario.xlsx"

if __name__ == "__main__":

    texto = extraer_texto(pdf_path)
    texto_depurado = depurar_texto(texto)
    movimientos = procesar_movimientos(texto_depurado)
    generar_excel(movimientos, output_excel)