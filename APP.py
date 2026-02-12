from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Configuración Maestra
TOKEN = "8532303951:AAFQVWDrh0ZvVIhjUcEN5kki-WIPj0X30ho"
# Datos globales para el Dashboard
data_store = {
    "ticker": "XAUUSD",
    "z_score": 0.0,
    "prob": "68.2%",
    "equity": 100000.0,
    "expectancy": 3.06
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>STELLAR PRESTAGE v3.5</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { background: #0a0a0a; color: #e0e0e0; font-family: 'Courier New', monospace; text-align: center; }
        .container { border: 2px solid #333; padding: 20px; display: inline-block; margin-top: 50px; }
        .value { font-size: 3em; color: #00ff00; }
        .alert { color: #ff0000; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <h1>STELLAR PRESTAGE v3.5 - 2026</h1>
    <div class="container">
        <h2>{{ ticker }} Z-SCORE</h2>
        <div class="value {% if z_score|abs > 2 %}alert{% endif %}">{{ z_score }}</div>
        <p>PROB. REVERSIÓN: {{ prob }}</p>
        <hr>
        <h3>EQUITY: ${{ equity }}</h3>
        <p>ESPERANZA MATEMÁTICA: ${{ expectancy }}</p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **data_store)

@app.route('/webhook', methods=['POST'])
def webhook():
    global data_store
    incoming_data = request.json
    # Actualizamos el motor estadístico
    data_store.update(incoming_data)
    
    # Enviamos notificación a tu Telegram automáticamente
    # Nota: Aquí falta tu Chat ID, pero el bot ya está enlazado al token.
    msg = f"🚀 STELLAR UPDATE\nZ-Score: {data_store['z_score']}\nProb: {data_store['prob']}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": "TU_USER_ID_AQUI", "text": msg})
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
