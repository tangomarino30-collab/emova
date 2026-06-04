import os
from playwright.sync_api import sync_playwright

# Configuración
URL = "https://emova.com.ar"
TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

LINEAS_INTERES = ["Linea B", "Linea C", "Linea H", "Linea Premetro"]


def enviar_telegram(mensaje):
    import requests
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("Faltan las credenciales de Telegram en los Secrets.")
        return

    url_api = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
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
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Simulamos un navegador humano real
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="es-AR",
            timezone_id="America/Argentina/Buenos_Aires",
        )

        page = context.new_page()

        # Ocultamos que es un navegador automatizado
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            print(f"Abriendo {URL}...")
            page.goto(URL, wait_until="networkidle", timeout=60000)

            # Esperamos el contenido dinámico
            page.wait_for_selector(".itemLinea p", timeout=30000)

            bloques = page.query_selector_all(".itemLinea")
            print(f"Cantidad de bloques encontrados: {len(bloques)}")

            for bloque in bloques:
                img = bloque.query_selector("img")
                p_texto = bloque.query_selector("p")

                if img and p_texto:
                    nombre_linea = (img.get_attribute("alt") or "").strip()
                    estado = p_texto.inner_text().strip()

                    if nombre_linea in LINEAS_INTERES:
                        print(f"{nombre_linea}: {estado}")

                        if estado.lower() != "normal":
                            enviar_telegram(f"⚠️ ¡Alerta {nombre_linea}! Estado actual: {estado}")

        except Exception as e:
            print(f"Error durante el scraping: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    revisar_web()
