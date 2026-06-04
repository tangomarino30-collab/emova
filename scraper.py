import os
import requests

# Configuración
CLIENT_ID = os.environ.get("GCBA_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GCBA_CLIENT_SECRET")
TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

LINEAS_INTERES = {"LineaB", "LineaC", "LineaH", "LineaP"}  # P = Premetro

API_URL = (
    "https://apitransporte.buenosaires.gob.ar/subtes/serviceAlerts"
    f"?client_id={{CLIENT_ID}}&client_secret={{CLIENT_SECRET}}&json=1"
)


def enviar_telegram(mensaje):
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("Faltan las credenciales de Telegram en los Secrets.")
        return
    url_api = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    try:
        r = requests.post(url_api, json={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
        print(f"Telegram: {r.status_code}")
    except Exception as e:
        print(f"Error Telegram: {e}")


def revisar_alertas():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Faltan las credenciales de la API GCBA en los Secrets.")
        return

    url = (
        f"https://apitransporte.buenosaires.gob.ar/subtes/serviceAlerts"
        f"?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&json=1"
    )

    try:
        r = requests.get(url, timeout=15)
        print(f"API GCBA: {r.status_code}")
        data = r.json()

        entidades = data.get("entity", [])
        print(f"Alertas encontradas: {len(entidades)}")

        lineas_alertadas = set()

        for entidad in entidades:
            alerta = entidad.get("alert", {})
            informed_entities = alerta.get("informed_entity", [])
            descripcion = (
                alerta.get("description_text", {})
                .get("translation", [{}])[0]
                .get("text", "Sin descripción")
            )

            for ie in informed_entities:
                route_id = ie.get("route_id", "")
                if route_id in LINEAS_INTERES and route_id not in lineas_alertadas:
                    lineas_alertadas.add(route_id)
                    nombre = route_id.replace("Linea", "Línea ")
                    print(f"Alerta {nombre}: {descripcion}")
                    enviar_telegram(f"⚠️ ¡Alerta {nombre}!\n{descripcion}")

        if not lineas_alertadas:
            print("Todas las líneas de interés funcionan con normalidad.")

    except Exception as e:
        print(f"Error al consultar la API: {e}")


if __name__ == "__main__":
    revisar_alertas()
