from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "pepedavila11"

# ===============================
# 🔹 1. Ruta de prueba (para Render)
# ===============================
@app.get("/test-whatsapp")
async def test_whatsapp():
    return {"status": "ok", "message": "Servidor funcionando ✔️"}


# ===============================
# 🔹 2. Validación del Webhook (GET)
# ===============================
@app.get("/")
async def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse("Error: token inválido", status_code=403)


# ===============================
# 🔹 3. Recepción de mensajes (POST)
# ===============================
@app.post("/")
async def webhook_handler(request: Request):
    data = await request.json()
    print("📩 Nuevo mensaje recibido:", data)

    return JSONResponse({"status": "received"})
