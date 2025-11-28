import os
from flask import Flask, request
import requests
from groq import Groq

# ===============================
#  CONFIGURACIÓN BÁSICA
# ===============================

VERIFY_TOKEN = "pepedavila1"   # Debe coincidir EXACTO en Meta

# Tokens desde variables de entorno (Render -> Environment)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ===============================
#  CONTEXTO PARA LA IA
# ===============================
INFO_GIMNASIO = """
Eres el asistente virtual de un gimnasio.
Respondes de forma clara, amable y breve.
Datos del gimnasio:
- Plan básico: $15.000 mensual
- Plan full: $22.000 mensual
- Horario: 6:00 a 23:00, lunes a sábado
- Clases: funcional, crossfit, zumba, spinning
- Personal trainer: $10.000 por sesión
- Ubicación: Centro de Graneros
Nunca digas que estás consultando con una IA.
"""

# ===============================
#  INICIALIZAR FLASK
# ===============================
app = Flask(__name__)

# ===============================
#  WEBHOOK DE VERIFICACIÓN
# ===============================
@app.route("/webhook", methods=["GET"])
def verificar():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Token incorrecto", 403

# ===============================
#  WEBHOOK MENSAJES INBOUND
# ===============================
@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.get_json()

    try:
        entrada = data["entry"][0]["changes"][0]["value"]
        mensajes = entrada.get("messages", [])

        if not mensajes:
            return "ok", 200

        mensaje = mensajes[0]
        texto = mensaje.get("text", {}).get("body", "")
        numero = mensaje["from"]

        print(f"Mensaje recibido de {numero}: {texto}")

        respuesta = generar_respuesta_ia(texto)
        enviar_mensaje(numero, respuesta)

    except Exception as e:
        print("Error procesando mensaje:", e)

    return "ok", 200

# ===============================
#  GENERAR RESPUESTA IA
# ===============================
def generar_respuesta_ia(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": INFO_GIMNASIO},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("ERROR IA:", e)
        return "Lo siento, hubo un problema al responder tu consulta."

# ===============================
#  ENVIAR MENSAJE A WHATSAPP
# ===============================
def enviar_mensaje(to: str, texto: str):

    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("ERROR: faltan variables WHATSAPP_TOKEN o PHONE_NUMBER_ID")
        return

    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": texto},
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        print("Respuesta WhatsApp:", r.status_code, r.text)
    except Exception as e:
        print("Error enviando mensaje:", e)

# ===============================
#  RUTA MANUAL DE PRUEBA
# ===============================
@app.route("/test-whatsapp", methods=["GET"])
def test_whatsapp():
    numero_prueba = "56991390956"  # tu número sin "+"
    enviar_mensaje(numero_prueba, "Hola! 👋 Este es un mensaje de prueba del bot.")
    return "Mensaje de prueba enviado (si todo está ok)", 200

# ===============================
#  EJECUCIÓN PRINCIPAL
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
