from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# CONFIGURACIÓN MAESTRA DE EDUARDO
TOKEN = "8532303951:AAFQVWDrh0ZvVIhjUcEN5kki-WIPj0X30ho"
MI_ID = "5287380864"

# Base de datos temporal del sistema
data_store = {
    "ticker": "XAUUSD", "z_score": 0.0, "prob": "68.2%", 
    "equity": 100000.0, "expectancy": 3.06
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>STELLAR v3.5 - MACHALA HUB</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { background: #070707; color: #f0f0f0; font-family: 'Segoe UI', Tahoma, sans-serif; text-align: center; }
        .box { border: 3px solid #1a1a1a; padding: 30px; display: inline-block; margin-top: 60px; border-radius: 15px; background: #111; box-shadow: 0 0 20px rgba(0,255,0,0.1); }
        .val { font-size: 4em; color: #00ff88; font-weight: bold; text-shadow: 0 0 10px rgba(0,255,136,0.5); }
        .alert { color: #ff3333; animation: blink 0.8s infinite; text-shadow: 0 0 15px rgba(255,51,51,0.7); }
        @keyframes blink { 50% { opacity: 0.3; } }
        hr { border: 0.5px solid #333; margin: 20px 0; }
    </style>
</head>
<body>
    <h1 style="letter-spacing: 5px;">STELLAR PRESTAGE v3.5</h1>
    <div class="box">
        <h2 style="color: #888;">{{ ticker }} Z-SCORE</h2>
        <div class="val {% if z_score|abs > 2 %}alert{% endif %}">{{ z_score }}</div>
        <p style="font-size: 1.2em;">PROB. REVERSIÓN: <span style="color: #00ff88;">{{ prob }}</span></p>
        <hr>
        <h3 style="color: #aaa;">EQUITY ACTUAL</h3>
        <div style="font-size: 2em; color: #fff;">${{ "{:,.2f}".format(equity) }}</div>
        <p style="color: #555;">ESPERANZA MATEMÁTICA: ${{ expectancy }}</p>
    </div>
    <p style="margin-top: 20px; color: #333;">MACHALA HUB - 2026</p>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **data_store)

@app.route('/telegram-bridge', methods=['POST'])
def bridge():
    global data_store
    update = request.json
    # Solo acepta mensajes de TU cuenta de Telegram
    if "message" in update and str(update["message"]["chat"]["id"]) == MI_ID:
        texto = update["message"]["text"]
        try:
            # Formato esperado: z_score, prob, equity (ej: 2.45, 95.4, 99800)
            parts = texto.split(',')
            data_store["z_score"] = float(parts[0])
            data_store["prob"] = parts[1].strip() + "%"
            data_store["equity"] = float(parts[2])
            return "Dashboard Actualizado", 200
        except:
            return "Error de formato", 400
    return "No autorizado", 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
