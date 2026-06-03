import os
import requests
from bs4 import BeautifulSoup

URL = "https://emova.com.ar"

TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("Faltan las credenciales de Telegram en los Secrets.")
        return
        
    url_api = f"https://telegram.org{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }
    try:
        r = requests.post(url_api, json=payload, timeout=10)
        print(f"Resultado envío Telegram: {r.status_code}")
    except Exception as e:
        print(f"Error al enviar Telegram: {e}")

def revisar_web():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
        }
        
        respuesta = requests.get(URL, headers=headers, timeout=10)
        print(f"Conexión con Emova: Código {respuesta.status_code}")
        
        sofá = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Mapeo exacto de las imágenes fijas que subiste en tu HTML
        lineas_monitorear = {
            "Linea B": "past-b-60.png",
            "Linea C": "past-c-60.png",
            "Linea H": "past-h-60.png",
            "Linea Premetro": "past-p-60.png"
        }
        
        for nombre_linea, nombre_archivo in lineas_monitorear.items():
            # Buscamos la etiqueta de la imagen que contenga el nombre del archivo
            img_subte = sofá.find("img", src=lambda x: x and nombre_archivo in x)
            
            if img_subte:
                # Buscamos el párrafo de texto que está dentro de su mismo bloque contenedor
                # Primero intentamos al lado, y si no en todo su contenedor padre
                p_texto = img_subte.find_next_sibling("p") or img_subte.parent.find("p")
                
                if p_texto:
                    estado = p_texto.text.strip()
                    print(f"{nombre_linea} detectada -> Estado: {estado}")
                    
                    # Con el 'or True' forzamos la prueba para verificar tu Telegram ya mismo
                    if estado != "Normal" or True:
                        enviar_telegram(f"⚠️ ¡Alerta {nombre_linea}! Estado actual: {estado}")
                else:
                    print(f"Se encontró la imagen de {nombre_linea} pero no su texto <p>")
            else:
                print(f"No se pudo encontrar la imagen para la {nombre_linea} en el HTML")
                        
    except Exception as e:
        print(f"Error al realizar el scraping: {e}")

if __name__ == "__main__":
    revisar_web()
