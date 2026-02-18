import os
import requests
import MetaTrader5 as mt5
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN INSTITUCIONAL (EDITE AQUÍ)
# ==========================================
CONFIG = {
    "TELEGRAM_TOKEN": "TU_BOT_TOKEN",
    "CHAT_ID": "TU_CHAT_ID",
    "SECRET_KEY": "STELLAR_SECURE_2026",
    "PROP_FIRM": {
        "login": 12345678,            # Tu cuenta de FundeNext
        "password": "TU_PASSWORD",
        "server": "FundeNext-Server",
        "lot_size": 2.0               # Lotaje para cuenta de $200k
    }
}

# ==========================================
# MOTOR DE TELEMETRÍA (TELEGRAM)
# ==========================================
def enviar_alerta(mensaje):
    url = f"https://api.telegram.org/bot{CONFIG['TELEGRAM_TOKEN']}/sendMessage"
    payload = {"chat_id": CONFIG['CHAT_ID'], "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error Telegram: {e}")

# ==========================================
# NODO DE EJECUCIÓN (METATRADER 5)
# ==========================================
def ejecutar_orden(symbol, type_str, price):
    if not mt5.initialize(login=CONFIG['PROP_FIRM']['login'], 
                          server=CONFIG['PROP_FIRM']['server'], 
                          password=CONFIG['PROP_FIRM']['password']):
        return "ERROR_CONEXION"

    order_type = mt5.ORDER_TYPE_BUY if type_str == "BUY" else mt5.ORDER_TYPE_SELL
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": CONFIG['PROP_FIRM']['lot_size'],
        "type": order_type,
        "price": price,
        "magic": 202601,
        "comment": "STELLAR_AMD_EXECUTION",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    mt5.shutdown()
    return result

# ==========================================
# WEBHOOK ENDPOINT (RECEPCIÓN DE SEÑALES)
# ==========================================
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    
    # Validar seguridad
    if data.get("token") != CONFIG['SECRET_KEY']:
        return jsonify({"status": "unauthorized"}), 401

    fase = data.get("fase", "AMD")
    precio = data.get("precio")
    high = data.get("high")
    low = data.get("low")
    
    # Lógica de Zona Premium/Discount
    equilibrio = (high + low) / 2
    zona = "🔴 PREMIUM" if precio > equilibrio else "🔵 DISCOUNT"
    
    # Notificar a Telegram
    msg = (f"🛰️ **STELLAR SIGNAL: {fase}**\n"
           f"───────────────────\n"
           f"**ACTIVO:** XAUUSD\n"
           f"**PRECIO:** `{precio}`\n"
           f"**ZONA:** {zona}\n"
           f"───────────────────\n"
           f"🚀 *Ejecutando en FundeNext...*")
    enviar_alerta(msg)
    
    # Ejecutar en MT5
    # (Opcional: puedes poner condicionales aquí)
    # ejecutar_orden("XAUUSD", "SELL" if zona == "🔴 PREMIUM" else "BUY", precio)
    
    return jsonify({"status": "executed", "zona": zona}), 200

# ==========================================
# DASHBOARD PARA EL INVERSOR (HTML/CSS)
# ==========================================
@app.route('/')
def dashboard():
    # Datos simulados basados en tu auditoría de 14 años
    stats = {
        "balance": 200000.00,
        "profit_anual": 33830.25,
        "win_rate": "31.43%",
        "status": "CONECTADO A HETZNER"
    }
    
    HTML = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>STELLAR COMMANDER</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { background: #050505; color: #00ffa3; font-family: 'Courier New', monospace; padding: 50px; }
            .card { border: 1px solid #1a1a1a; padding: 20px; background: #0a0a0a; border-radius: 8px; margin-bottom: 20px; }
            .stat { font-size: 2.5em; color: white; font-weight: bold; }
            .label { color: #444; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8em; }
            .status-on { color: #00ffa3; animation: blink 1s infinite; }
            @keyframes blink { 50% { opacity: 0.5; } }
        </style>
    </head>
    <body>
        <h1 style="color:white">STELLAR <span style="color:#00ffa3">QUANT</span> TERMINAL v9.0</h1>
        <p class="status-on">● {{ stats.status }}</p>
        <div style="display: flex; gap: 20px;">
            <div class="card" style="flex:1"><div class="label">Capital Gestionado</div><div class="stat">${{ "{:,.2f}".format(stats.balance) }}</div></div>
            <div class="card" style="flex:1"><div class="label">Backtest Profit (14Y)</div><div class="stat" style="color:#ffcc00">+${{ "{:,.2f}".format(stats.profit_anual) }}</div></div>
            <div class="card" style="flex:1"><div class="label">Win Rate</div><div class="stat">{{ stats.win_rate }}</div></div>
        </div>
        <div class="card">
            <div class="label">Algorithmic Growth Curve</div>
            <canvas id="chart" height="80"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('chart'), {
                type: 'line',
                data: { labels: ['2010', '2015', '2020', '2024'], datasets: [{ data: [0, 12000, 24000, 33830], borderColor: '#00ffa3', tension: 0.4 }] },
                options: { plugins: { legend: { display: false } } }
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(HTML, stats=stats)

if __name__ == "__main__":
    # Escucha en el puerto que Render o Hetzner asignen
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
