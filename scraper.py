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
        
    url_api = f"https://telegram.org{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }
    try:
        requests.post(url_api, json=payload, timeout=10)
    except Exception as e:
        print(f"Error al enviar Telegram: {e}")

def revisar_web():
    try:
        respuesta = requests.get(URL, timeout=10)
        sofá = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Encontramos todos los bloques de subtes usando la clase de tu HTML
        bloques = sofá.find_all(class_="itemLinea")
        
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
                    
                    # Si el estado cambia y NO es "Normal", envía alerta
                    if estado != "Normal":
                        enviar_telegram(f"⚠️ ¡Alerta {nombre_linea}! Estado actual: {estado}")
                        
    except Exception as e:
        print(f"Error al realizar el scraping: {e}")

if __name__ == "__main__":
    revisar_web()
