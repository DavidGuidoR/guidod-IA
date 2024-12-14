import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL de la página que deseas scrapear
url = "https://elpais.com/mexico/2024-12-10/norma-pina-lanza-su-critica-mas-dura-a-los-gobiernos-de-morena-se-nos-llamo-traidores-por-no-ser-parte-del-proyecto-politico-dominante.html"  # Reemplaza con la URL de la página web

# Guardar el texto en un archivo TXT
output_path = "articulo_extraido28.txt"
# Realizar la solicitud HTTP para obtener el contenido HTML
response = requests.get(url, verify=False)

if response.status_code == 200:  # Verifica que la solicitud fue exitosa
    html_content = response.text

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extraer el título del artículo
    title = soup.find("title").get_text(strip=True) if soup.find("title") else "Título no disponible"

    # Extraer la fecha si está disponible
    date_meta = soup.find("meta", {"name": "article:published_time"})
    date = date_meta["content"] if date_meta else datetime.now().strftime("%Y-%m-%d")

    # Extraer el contenido del artículo (evitando comerciales)
    article_paragraphs = soup.find_all("p")
    article_text = "\n".join(paragraph.get_text(strip=True) for paragraph in article_paragraphs if paragraph.get_text(strip=True))

    # Crear el contenido con metadatos
    document_content = f"""====== NUEVO DOCUMENTO ======
TÍTULO: {title}
FUENTE: {url}
FECHA: {date}

{article_text}

====== FIN DOCUMENTO ======
"""
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(document_content)

    print(f"Artículo extraído y guardado en {output_path}")
else:
    print(f"No se pudo acceder a la página. Código de estado HTTP: {response.status_code}")
