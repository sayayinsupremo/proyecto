from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# CONFIGURACIÓN MAESTRA
TOKEN = "8532303951:AAFQVWDrh0ZvVIhjUcEN5kki-WIPj0X30ho"
MI_ID = "5287380864"

# Base de datos global
data_store = {
    "ticker": "XAUUSD", "z_score": 0.0, "prob": "68.2%", 
    "equity": 100000.0, "expectancy": 3.06
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>STELLAR v3.5</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { background: #070707; color: #f0f0f0; font-family: sans-serif; text-align: center; }
        .box { border: 3px solid #1a1a1a; padding: 30px; display: inline-block; margin-top: 60px; background: #111; border-radius: 15px; }
        .val { font-size: 4em; color: #00ff88; font-weight: bold; }
        .alert { color: #ff3333; animation: blink 0.8s infinite; }
        @keyframes blink { 50% { opacity: 0.3; } }
    </style>
</head>
<body>
    <h1>STELLAR PRESTAGE v3.5</h1>
    <div class="box">
        <h2>{{ ticker }} Z-SCORE</h2>
        <div class="val {% if z_score|abs > 2 %}alert{% endif %}">{{ z_score }}</div>
        <p>PROB. REVERSIÓN: {{ prob }}</p>
        <hr>
        <h3>EQUITY: ${{ "{:,.2f}".format(equity) }}</h3>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **data_store)

# ESTA ES LA RUTA CRÍTICA QUE DEBE COINCIDIR CON EL WEBHOOK
@app.route('/telegram-bridge', methods=['POST'])
def bridge():
    global data_store
    update = request.json
    if update and "message" in update:
        if str(update["message"]["chat"]["id"]) == MI_ID:
            texto = update["message"]["text"]
            try:
                # El bot espera: ZSCORE, PROB, EQUITY (ej: 2.5, 95, 100000)
                parts = [p.strip() for p in texto.split(',')]
                data_store["z_score"] = float(parts[0])
                data_store["prob"] = parts[1] + "%"
                data_store["equity"] = float(parts[2])
                return "OK", 200
            except:
                return "Error formato", 400
    return "No autorizado", 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000) # Render usa el puerto 10000 por defecto
