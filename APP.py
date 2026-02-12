from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# CONFIGURACIÓN MAESTRA
TOKEN = "8532303951:AAFQVWDrh0ZvVIhjUcEN5kki-WIPj0X30ho"
MI_ID = "5287380864"

# Base de datos del sistema
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
        body { background: #070707; color: #f0f0f0; font-family: sans-serif; text-align: center; }
        .box { border: 3px solid #1a1a1a; padding: 30px; display: inline-block; margin-top: 60px; border-radius: 15px; background: #111; }
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
        <h3>EQUITY ACTUAL</h3>
        <div style="font-size: 2em;">${{ "{:,.2f}".format(equity) }}</div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **data_store)

# RUTA UNIFICADA: Procesa Telegram y Webhooks directos
@app.route('/webhook', methods=['POST'])
@app.route('/telegram-bridge', methods=['POST'])
def bridge():
    global data_store
    update = request.json
    
    # Si el mensaje viene de Telegram
    if update and "message" in update:
        if str(update["message"]["chat"]["id"]) == MI_ID:
            texto = update["message"]["text"]
            try:
                parts = [p.strip() for p in texto.split(',')]
                data_store["z_score"] = float(parts[0])
                data_store["prob"] = parts[1] + "%"
                data_store["equity"] = float(parts[2])
                return "Actualizado desde Telegram", 200
            except:
                return "Error en formato de texto", 400
                
    # Si el mensaje viene directo de TradingView (Webhook)
    elif update and "z_score" in update:
        data_store.update(update)
        return "Actualizado desde Webhook", 200
        
    return "Datos no reconocidos", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
