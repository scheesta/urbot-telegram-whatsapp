import os
from flask import Flask, request
import requests
from groq import Groq

# ===============================
#  CONFIGURACIÓN BÁSICA
# ===============================

# Token que usará Meta para verificar el webhook
VERIFY_TOKEN = "urverifytoken123"   # puedes cambiarlo, pero debe coincidir en Meta

# Estos los puedes dejar aquí o pasarlos como variables de entorno en Render
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "EAAdWjZA8pB9YBQOlXtRayNNI7nD4uXkjA5kxDW146FWe8SAXuMK297yCjKRf9Nef4gD3bRqlDa0bg0BceERLsZCH7FyvHZAevn0EivAwdR5ZBfXy1uzC4pmNYcxToKUZCfLt8khvyoPhwyy5Ev1piOa3VIgj4UwypY47pO1EWTZAR2EZBsCRiuMoZBqwhnBgjGevJwtWgTg7WCUjILdSZBa3Cc2waNYzIJT8E5CZBRo7qnz4ziZBk0ycU2GQdDChOKGmCyx0q4uFSp4cyKj2yUPiH3XZB1Fpsm6mDWOQsSHO3QZDZD")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "931582733364859")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "GROQ_API_KEY = os.environ["GROQ_API_KEY"]")

# Cliente Groq
client = Groq(api_key=GROQ_API_KEY)

# Contexto del gimnasio
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
#  APP FLASK
# ===============================

app = Flask(__name__)

@app.route("/", methods=["GET"])
def verificar():
    """
    Endpoint que usa Meta para verificar el webhook.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Token incorrecto", 403


@app.route("/", methods=["POST"])
def recibir_mensaje():
    """
    Endpoint que recibe los mensajes de WhatsApp.
    """
    data = request.get_json()
    # print("WEBHOOK DATA:", data)

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
#  LÓGICA DE IA
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
        return "Lo siento, hubo un problema al responder tu consulta. Intenta de nuevo en un momento."


# ===============================
#  ENVÍO DE MENSAJES A WHATSAPP
# ===============================

def enviar_mensaje(to: str, texto: str):
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
        print("Respuesta de WhatsApp:", r.status_code, r.text)
    except Exception as e:
        print("Error enviando mensaje a WhatsApp:", e)


# ===============================
#  EJECUCIÓN LOCAL / RENDER
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)import os
from flask import Flask, request
import requests
from groq import Groq

# ===============================
#  CONFIGURACIÓN BÁSICA
# ===============================

# Token que usará Meta para verificar el webhook
VERIFY_TOKEN = "urverifytoken123"   # puedes cambiarlo, pero debe coincidir en Meta

# Estos los puedes dejar aquí o pasarlos como variables de entorno en Render
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "TU_TOKEN_WHATSAPP_COMPLETO")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "931582733364859")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "TU_GROQ_API_KEY_COMPLETA")

# Cliente Groq
client = Groq(api_key=GROQ_API_KEY)

# Contexto del gimnasio
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
#  APP FLASK
# ===============================

app = Flask(__name__)

@app.route("/", methods=["GET"])
def verificar():
    """
    Endpoint que usa Meta para verificar el webhook.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Token incorrecto", 403


@app.route("/", methods=["POST"])
def recibir_mensaje():
    """
    Endpoint que recibe los mensajes de WhatsApp.
    """
    data = request.get_json()
    # print("WEBHOOK DATA:", data)

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
#  LÓGICA DE IA
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
        return "Lo siento, hubo un problema al responder tu consulta. Intenta de nuevo en un momento."


# ===============================
#  ENVÍO DE MENSAJES A WHATSAPP
# ===============================

def enviar_mensaje(to: str, texto: str):
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
        print("Respuesta de WhatsApp:", r.status_code, r.text)
    except Exception as e:
        print("Error enviando mensaje a WhatsApp:", e)


# ===============================
#  EJECUCIÓN LOCAL / RENDER
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)