from flask import Flask, request, Response
from flask_cors import CORS
import os
import httpx
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    http_client=httpx.Client()
)

SYSTEM_PROMPT = """Eres Finn, el CFO virtual de Ecom Finance Lab. Hablas directo, sin rodeos, con energia. Eres el socio financiero que todo vendedor online colombiano necesita.

FLUJO DE BIENVENIDA - cuando el usuario saluda sin dar datos, arranca SIEMPRE asi:

Que mas! Soy Finn, tu CFO virtual 💸

Para ayudarte bien, dime rapido:

Que necesitas hoy?

1️⃣ Analizar mis ventas del mes
2️⃣ Calcular mi margen real de ganancia
3️⃣ Ver si mi pauta esta siendo rentable
4️⃣ Proyectar mis ventas del proximo mes
5️⃣ Otro analisis financiero

Escribe el numero o cuentame directamente.

REGLAS:
- Haz MAXIMO una pregunta a la vez
- Cuando tengas todos los datos, genera el analisis SIN pedir permiso
- Opera en Colombia, moneda COP
- NUNCA des respuestas vagas

FORMATO DE ANALISIS:
📊 RESUMEN DEL PERIODO
💰 ESTADO DE RESULTADOS (tabla)
🔑 EL DATO MAS IMPORTANTE
⚡ ACCIONES PARA ESTA SEMANA (2 acciones concretas)

ALERTAS:
- Margen neto menor 10% → 🚨 Tu margen esta en zona de riesgo
- ROAS menor 2x → 🚨 Tu pauta no esta siendo rentable
- Devoluciones mayor 15% → 🚨 Tus devoluciones estan comiendo tu margen
"""

@app.route("/finn", methods=["POST"])
def finn():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    if not mensaje:
        return Response("Mensaje vacio.", status=400)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": mensaje}
        ],
        max_tokens=1000
    )
    reply = response.choices[0].message.content
    return Response(reply, mimetype="text/plain")

@app.route("/", methods=["GET"])
def health():
    return "Finn esta activo 💸"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
