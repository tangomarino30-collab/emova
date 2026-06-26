from flask import Flask, render_template, jsonify
import requests, threading, time

app = Flask(__name__)

CLIENT_ID = "1455ea4d286148fb8026b4f162c008c3"
CLIENT_SECRET = "0EaEC1da661F4Bf6B3B847272499Dac3"
TELEGRAM_TOKEN = "8761348817:AAFxr-cfpuiP3vnzpckxYu-7LtMaVRJBKYM"
TELEGRAM_CHAT_ID = "154576029"

alertas_anteriores = set()

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})

def monitorear():
    global alertas_anteriores
    while True:
        try:
            url = f"https://apitransporte.buenosaires.gob.ar/subtes/serviceAlerts?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&json=1"
            res = requests.get(url)
            data = res.json()
            alertas = data.get("entity", [])

            actuales = set()
            for e in alertas:
                alerta = e.get("alert", {})
                texto = alerta.get("header_text", {}).get("translation", [{}])[0].get("text", "")
                linea = alerta.get("informed_entity", [{}])[0].get("route_id", "?")
                clave = f"{linea}:{texto}"
                actuales.add(clave)
                if clave not in alertas_anteriores:
                    enviar_telegram(f"🚇 Alerta Subte\nLínea {linea}: {texto}")

            alertas_anteriores = actuales
        except Exception as ex:
            print("Error monitor:", ex)

        time.sleep(1200)  # 20 minutos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alertas')
def alertas():
    url = f"https://apitransporte.buenosaires.gob.ar/subtes/serviceAlerts?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&json=1"
    res = requests.get(url)
    return jsonify(res.json())

hilo = threading.Thread(target=monitorear, daemon=True)
hilo.start()

if __name__ == '__main__':
    app.run()
