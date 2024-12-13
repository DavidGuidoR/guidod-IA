import os
import re
from PyPDF2 import PdfReader

# Metadatos del documento
titulo = "Reforma integral al sistema de justicia en México: desafíos y propuestas"
fuente = "https://www.scjn.gob.mx/sites/default/files/agenda/documento/2024-09/reforma-integral-al-sistema-de-justicia-en-mexico.pdf"
fecha = "09/2024"
resumen = (
    "La Suprema Corte de Justicia de la Nación, consciente de la importancia de que la sociedad civil "
    "conozca qué es el Poder Judicial de la Federación y cuál es su funcionamiento, ha decidido publicar, "
    "por cuarta vez, la obra ¿Qué es el Poder Judicial de la Federación?, cuya aceptación por el foro y el "
    "público en general ha sido patente desde 1999, año de su primera edición. [...]"
)

# Ruta del archivo PDF
ruta_archivo = "./Documentos PDF/Analisis de la iniciativa de reforma al poder judicial.pdf"
archivo_salida = "documentos_integradosprueba2.txt"

# Página inicial
pagina_inicial = 4


def limpiar_texto_extraido(texto):
    """
    Limpia el texto extraído de un PDF para eliminar ruido y mejorar la legibilidad.
    Aplica formateo a títulos, subtítulos y sub-subtítulos.
    """

    # Eliminar pie de página específico
    texto = re.sub(r'Reforma integral al sistema de justicia en México: desafíos y propuestas', '', texto, flags=re.IGNORECASE)

    # Detectar títulos (líneas solitarias largas, asumidas como encabezados grandes)
    texto = re.sub(r'^\s*(.{20,})\s*$', r'\n=== TÍTULO: \1 ===\n', texto, flags=re.MULTILINE)

    # Detectar subtítulos (letras seguidas de punto, con texto en negritas)
    texto = re.sub(r'^\s*([A-Z])\.\s*(.+)', r'\n--- SUBTÍTULO: \1. \2 ---\n', texto, flags=re.MULTILINE)

    # Detectar sub-subtítulos (números romanos seguidos de un punto)
    texto = re.sub(r'^\s*(I{1,3}|IV|V|VI|VII|VIII|IX|X)\.\s*(.+)', r'\n--- SUB-SUBTÍTULO: \1. \2 ---\n', texto, flags=re.MULTILINE)

    # Eliminar líneas vacías repetidas
    texto = re.sub(r'\n\s*\n', '\n', texto)

    # Eliminar espacios innecesarios
    texto = texto.strip()
    return texto



def extraer_texto_desde_pdf(ruta_archivo, pagina_inicial):
    """
    Extrae texto de un archivo PDF a partir de una página específica y salta cuando detecta números pequeños
    al inicio de una línea seguida de texto.
    """
    try:
        lector = PdfReader(ruta_archivo)
        texto = ""
        for i in range(pagina_inicial - 1, len(lector.pages)):
            pagina = lector.pages[i].extract_text()

            # Saltar página si detecta números pequeños al inicio de una línea seguidos de texto
            if re.search(r'^\s*[¹²³⁴⁵⁶⁷⁸⁹⁰].+', pagina, re.MULTILINE):
                continue 
            
            texto += pagina + "\n"
        return limpiar_texto_extraido(texto.strip())
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return None


def agregar_al_archivo_texto(archivo_salida, titulo, fuente, fecha, contenido, resumen):
    """
    Agrega un nuevo documento al archivo de texto con el formato definido.
    """
    with open(archivo_salida, "a", encoding="utf-8") as f:
        f.write("====== NUEVO DOCUMENTO ======\n")
        f.write(f"TÍTULO: {titulo}\n")
        f.write(f"FUENTE: {fuente}\n")
        f.write(f"FECHA: {fecha}\n\n")
        f.write("CONTENIDO:\n")
        f.write(contenido + "\n")
        f.write("------------------------\n")
        f.write("NOTAS/RESUMEN:\n")
        f.write(resumen + "\n")
        f.write("====== FIN DOCUMENTO ======\n\n")


def main():
    # Verificar si el archivo PDF existe
    if not os.path.isfile(ruta_archivo):
        print(f"El archivo PDF '{ruta_archivo}' no existe. Verifica la ruta.")
        return
    
    # Extraer texto del PDF desde la página indicada
    contenido = extraer_texto_desde_pdf(ruta_archivo, pagina_inicial)
    if not contenido:
        print("No se pudo extraer el texto del archivo. Intenta con otro archivo.")
        return
    
    # Agregar contenido al archivo de salida
    agregar_al_archivo_texto(archivo_salida, titulo, fuente, fecha, contenido, resumen)
    print(f"Documento '{titulo}' agregado exitosamente al archivo de salida: {archivo_salida}")


if __name__ == "__main__":
    main()
