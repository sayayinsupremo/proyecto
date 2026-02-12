import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Memoria volátil para datos en tiempo real
stellar_data = {
    "ticker": "XAUUSD",
    "z_score": 0.0,
    "prob": "68.2%",
    "equity": 100000,
    "expectancy": 0.0
}

# Plantilla HTML estilo "Stellar Black Edition"
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stellar Cloud Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { background-color: #0a0a0a; color: #ffffff; font-family: 'Courier New', monospace; text-align: center; }
        .card { border: 1px solid #333; padding: 20px; margin: 20px auto; width: 300px; border-radius: 10px; background: #111; }
        .value { font-size: 2em; color: #00ff00; }
        .alert { color: #ff0000; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <h1>STELLAR PRESTAGE v3.1 - 2026</h1>
    <div class="card">
        <h3>{{ ticker }} Z-SCORE</h3>
        <div class="value {% if z_score|abs > 2 %}alert{% endif %}">{{ z_score }}</div>
        <p>PROB. REVERSI&Oacute;N: {{ prob }}</p>
    </div>
    <div class="card">
        <h3>ESPERANZA MATEM&Aacute;TICA</h3>
        <div class="value">${{ expectancy }}</div>
        <p>EQUITY: ${{ equity }}</p>
    </div>
</body>
</html>
'''

@app.route('/webhook', methods=['POST'])
def webhook():
    global stellar_data
    stellar_data = request.json # Recibe el JSON de TradingView
    return {"status": "success"}, 200

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **stellar_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)