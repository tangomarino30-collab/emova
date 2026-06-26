from flask import Flask, render_template, jsonify
import

def monitorear():
   
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


hilo = threading.Thread(target=monitorear, daemon=True)
hilo.start()

if __name__ == '__main__':
    app.run()
