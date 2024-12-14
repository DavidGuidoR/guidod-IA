import whisper

# Configuración de metadatos
TITULO = "Audiencia ante la Comisión Interamericana de Derechos Humanos. México"
FUENTE = "https://www.youtube.com/watch?v=GonCN4PuT-Q&t=1697s"
FECHA = "12/10/2024"

# Ruta del archivo MP3 y salida
ruta_audio_mp3 = "./ScrapVideo/InteramericanadeDerechosHumanos.mp3"
ruta_salida = "Audienciavid.txt"
# Cargar el modelo de Whisper
print("Cargando el modelo de Whisper...")
modelo = whisper.load_model("base") 

# Transcribir el audio
print("Transcribiendo el audio...")
resultado = modelo.transcribe(ruta_audio_mp3, language="es")

# Crear archivo TXT con metadatos
print("Guardando la transcripción en un archivo...")
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write("====== NUEVO DOCUMENTO ======\n")
    archivo.write(f"TÍTULO: {TITULO}\n")
    archivo.write(f"FUENTE: {FUENTE}\n")
    archivo.write(f"FECHA: {FECHA}\n\n")
    archivo.write(resultado["text"])

print(f"Transcripción completa guardada en {ruta_salida}")
