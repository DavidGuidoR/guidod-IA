import fitz  # PyMuPDF
import re

# Metadatos del documento
titulo = "ANÁLISIS DE LA INICIATIVA DE REFORMA AL PODER JUDICIAL EN MÉXICO Problemas asociados con la iniciativa de reforma constitucional del Poder Judicial presentada el 5 de febrero de 2024"
fuente = "https://www.sitios.scjn.gob.mx/cec/sites/default/files/page/files/2024-06/Análisis%20de%20la%20iniciativa%20de%20reforma.%20Problemas%20asociados_final.pdf"
fecha = "02/2024"
resumen = ("""
Este estudio no representa una posición institucional de la
Suprema Corte de Justicia de la Nación, sino que constituye
un análisis académico realizado por las personas integrantes
del Centro de Estudios Constitucionales."""
)

# Ruta del archivo PDF
ruta_archivo = "./Documentos PDF/Analisis de la iniciativa de reforma al poder judicial.pdf"
archivo_salida = "documentos_integradosprueba3.txt"

# Página inicial
pagina_inicial = 5


def limpiar_texto(texto):
    """
    Limpia el texto para eliminar números de página y referencias.
    """
    # Eliminar números de página (líneas con solo un número)
    texto = re.sub(r'^\s*\d+\s*$', '', texto, flags=re.MULTILINE)



    return texto.strip()


def extraer_texto_y_formatear(ruta_archivo, pagina_inicial):
    """
    Extrae texto del PDF y organiza el contenido eliminando números de página y referencias.
    """
    contenido = []
    try:
        documento = fitz.open(ruta_archivo)
        for i in range(pagina_inicial - 1, len(documento)):
            pagina = documento[i]
            bloques = pagina.get_text("dict")["blocks"]
            texto_pagina = ""
            for bloque in bloques:
                if "lines" in bloque:
                    for linea in bloque["lines"]:
                        for span in linea["spans"]:
                            texto = span["text"].strip()
                            tamaño_fuente = span["size"]
                            fuente = span["font"]  # Nombre de la fuente

                            # Detectar títulos (negritas según el nombre de la fuente)
                            if "Bold" in fuente or "Black" in fuente:
                                texto_pagina += f"\n-- TITULO (NEGRITAS): {texto} --\n"

                            # Texto normal
                            else:
                                texto_pagina += texto + " "

            # Limpiar texto de la página
            texto_pagina = limpiar_texto(texto_pagina)
            contenido.append(texto_pagina)

        documento.close()
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
    return "\n".join(contenido)



def agregar_al_archivo_texto(archivo_salida, titulo, fuente, fecha, contenido, resumen):
    """
    Agrega un nuevo documento al archivo de texto con metadatos y contenido extraído.
    """
    with open(archivo_salida, "a", encoding="utf-8") as archivo:
        archivo.write("====== NUEVO DOCUMENTO ======\n")
        archivo.write(f"TÍTULO: {titulo}\n")
        archivo.write(f"FUENTE: {fuente}\n")
        archivo.write(f"FECHA: {fecha}\n\n")
        archivo.write("CONTENIDO:\n")
        archivo.write(contenido + "\n")
        archivo.write("------------------------\n")
        archivo.write("NOTAS/RESUMEN:\n")
        archivo.write(resumen + "\n")
        archivo.write("====== FIN DOCUMENTO ======\n\n")


def main():
    # Extraer y limpiar contenido desde el PDF
    contenido = extraer_texto_y_formatear(ruta_archivo, pagina_inicial)

    if not contenido:
        print("No se pudo extraer contenido del archivo PDF.")
        return

    # Agregar contenido al archivo de salida con metadatos
    agregar_al_archivo_texto(archivo_salida, titulo, fuente, fecha, contenido, resumen)
    print(f"El contenido ha sido extraído y guardado en '{archivo_salida}'.")


if __name__ == "__main__":
    main()