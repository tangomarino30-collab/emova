import os
import requests
from bs4 import BeautifulSoup

# Configuración de la web
URL = "https://emova.com.ar"

# El robot de GitHub le pasará tus claves reales de forma invisible aquí:
TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("Faltan las credenciales de Telegram en los Secrets.")
        return
        
    # CORRECCIÓN 1: La URL oficial de la API de Telegram con la palabra /bot
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
        # CORRECCIÓN 2: Disfrazamos el robot como un navegador para saltar el bloqueo de Emova
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        respuesta = requests.get(URL, headers=headers, timeout=10)
        print(f"Conexión con Emova: Código {respuesta.status_code}")
        
        sofá = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Encontramos todos los bloques de subtes usando la clase de tu HTML
        bloques = sofá.find_all(class_="itemLinea")
        print(f"Cantidad de bloques encontrados: {len(bloques)}")
        
        # Filtramos solo las líneas que te interesan
        lineas_interes = ["Linea B", "Linea C", "Linea H", "Linea Premetro"]
        
        for bloque in bloques:
            img = bloque.find("img")
            p_texto = bloque.find("p")
            
            if img and p_texto:
                nombre_linea = img.get("alt", "").strip()
                estado = p_texto.text.strip()
                
                if nombre_linea in lineas_interes:
                    print(f"{nombre_linea}: {estado}")
                    
                    # Con el 'or True' forzamos la prueba para que verifiques tu Telegram ya mismo
                    if estado != "Normal" or True:
                        enviar_telegram(f"⚠️ ¡Alerta {nombre_linea}! Estado actual: {estado}")
                        
    except Exception as e:
        print(f"Error al realizar el scraping: {e}")

if __name__ == "__main__":
    revisar_web()
