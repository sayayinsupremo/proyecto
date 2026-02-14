import os
from flask import Flask, request, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# --- CONFIGURACIÓN DE AUDITORÍA INSTITUCIONAL (DATOS VALIDADOS) ---
# Se integra el beneficio histórico de 14 años y los límites de Prop Firm
data = {
    "cuentas": [
        {
            "id": "XAU-AUDIT-14Y", 
            "firm": "PROP FIRM ELITE", 
            "balance": 133830.25, # $100k inicial + $33k profit
            "inicial": 100000.00, 
            "daily_limit": 5000.00,  # 5% Max Daily Loss
            "daily_loss": 0.00,      # Dinámico vía Webhook
            "max_dd_limit": 10000.00, # 10% Max Total Loss
            "total_loss": 0.00,      # Distancia al cierre
            "type": "Funded Account"
        }
    ],
    "stats": {
        "pf": 1.194,             # Factor de Ganancias (14 años)
        "win_rate": "31.43%",    # Validado en 614 operaciones
        "total_trades": 614,
        "expectancy": "$55.10"
    },
    "intel": {
        "gdp": "EXPANSIÓN",      # Contexto Macro US GDP
        "sentiment": "ESTABLE",   # Proxy de Reddit/Social
        "z_score": 0.0,
        "dxy_confluence": "ALTA"
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>STELLAR COMMANDER v5.1</title>
    <meta http-equiv="refresh" content="30">
    <style>
        :root { --bg: #020202; --card: #0a0a0a; --accent: #00ff88; --risk: #ff3355; --text: #f0f0f0; --gold: #d4af37; }
        body { background: var(--bg); color: var(--text); font-family: 'Consolas', monospace; margin: 0; padding: 20px; }
        
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1a1a1a; padding-bottom: 20px; margin-bottom: 30px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 25px; }
        
        .card { background: var(--card); border: 1px solid #222; border-radius: 8px; padding: 25px; position: relative; }
        .card.alert { border-color: var(--risk); box-shadow: 0 0 15px rgba(255, 51, 85, 0.2); }
        
        .balance { font-size: 3em; font-weight: 800; color: var(--accent); letter-spacing: -2px; }
        .label { color: #555; font-size: 0.75em; text-transform: uppercase; font-weight: bold; }
        
        /* MONITORES DE RIESGO */
        .risk-box { background: #111; padding: 15px; border-radius: 4px; margin-top: 15px; border-left: 4px solid var(--risk); }
        .bar-bg { background: #222; height: 12px; border-radius: 6px; margin: 10px 0; overflow: hidden; }
        .bar-fill { background: linear-gradient(90deg, var(--risk), #ff6688); height: 100%; transition: width 0.5s; }
        
        .intel-badge { display: inline-block; padding: 5px 12px; border-radius: 4px; font-size: 0.8em; font-weight: bold; margin-right: 10px; }
        .bg-green { background: rgba(0, 255, 136, 0.1); color: var(--accent); border: 1px solid var(--accent); }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0;">STELLAR <span style="color:var(--gold)">COMMANDER</span></h1>
            <div style="margin-top:5px;">
                <span class="intel-badge bg-green">GDP: {{ intel.gdp }}</span>
                <span class="intel-badge bg-green">SENTIMENT: {{ intel.sentiment }}</span>
            </div>
        </div>
        <div style="text-align:right">
            <small class="label">Auditoría Global 14 Años</small><br>
            <span style="font-size:1.2em; color:var(--accent)">Net Profit: +$33,830.25</span>
        </div>
    </div>

    <div class="grid">
        {% for c in cuentas %}
        <div class="card">
            <div style="display:flex; justify-content:space-between;">
                <span class="label">{{ c.firm }} // {{ c.id }}</span>
                <span style="color:var(--gold); font-size:0.8em;">{{ c.type }}</span>
            </div>
            <div class="balance">${{ "{:,.2f}".format(c.balance) }}</div>
            
            <div class="risk-box">
                <div style="display:flex; justify-content:space-between;">
                    <span class="label" style="color:var(--risk)">Daily Loss Limit</span>
                    <span>${{ "{:,.2f}".format(c.daily_limit - c.daily_loss) }} LEFT</span>
                </div>
                <div class="bar-bg"><div class="bar-fill" style="width: {{ (c.daily_loss / c.daily_limit) * 100 }}%"></div></div>
                <small style="color:#444">Current Loss: ${{ c.daily_loss }} / Max: ${{ c.daily_limit }}</small>
            </div>

            <div style="margin-top:20px; border-top: 1px solid #222; padding-top:15px;">
                <span class="label">Max Drawdown Protection</span>
                <div style="font-size:1.5em; color:var(--risk); font-weight:bold;">
                    ${{ "{:,.2f}".format(c.max_dd_limit - c.total_loss) }} TO TERMINATION
                </div>
            </div>
        </div>
        {% endfor %}

        <div class="card">
            <span class="label">Stellar Quantum v42 Engine Stats</span>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin-top:15px;">
                <div style="background:#111; padding:15px;">
                    <small class="label">Profit Factor</small><br>
                    <b style="font-size:1.4em; color:var(--gold)">{{ stats.pf }}</b>
                </div>
                <div style="background:#111; padding:15px;">
                    <small class="label">Win Rate (614 Ops)</small><br>
                    <b style="font-size:1.4em;">{{ stats.win_rate }}</b>
                </div>
            </div>
            <div style="margin-top:20px; padding:15px; background:rgba(0,255,136,0.05); border:1px dashed var(--accent);">
                <span class="label" style="color:var(--accent)">Live Market Signals</span>
                <div style="display:flex; justify-content:space-between; margin-top:10px;">
                    <span>Z-Score: <b>{{ intel.z_score }}</b></span>
                    <span>DXY: <b>{{ intel.dxy_confluence }}</b></span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **data)

@app.route('/webhook', methods=['POST'])
def webhook():
    global data
    payload = request.get_json(force=True)
    # Formato esperado: {"balance": 133830, "daily_loss": 500, "z_score": 1.2}
    try:
        if "balance" in payload: data["cuentas"][0]["balance"] = payload["balance"]
        if "daily_loss" in payload: data["cuentas"][0]["daily_loss"] = payload["daily_loss"]
        if "z_score" in payload: data["intel"]["z_score"] = payload["z_score"]
        return "SUCCESS", 200
    except: return "DATA_ERROR", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
