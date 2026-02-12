import os
from flask import Flask, request, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# --- CONFIGURACIÓN DE AUDITORÍA (MÓDULO ALEX RUIZ STYLE) ---
data = {
    "cuentas": [
        {"id": "TF-8532", "firm": "TOPSTEP", "balance": 100796.91, "inicial": 100000, "dd_limit": 2000, "type": "Funded"},
        {"id": "FT-5287", "firm": "FTMO", "balance": 100000.00, "inicial": 100000, "dd_limit": 5000, "type": "Challenge"}
    ],
    "stats": {
        "pf": 3.22, 
        "sharpe": 0.108, 
        "win_rate": "42.86%",
        "expectancy": "$56.92"
    },
    "market": {
        "z_score": 0.0,
        "stretch": "0.0%",
        "status": "MONITORING"
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STELLAR AUDITOR PRO v5.0</title>
    <meta http-equiv="refresh" content="10">
    <style>
        :root { --bg: #050505; --card: #0d0d0d; --accent: #00ff88; --risk: #ff3355; --text: #e0e0e0; }
        body { background: var(--bg); color: var(--text); font-family: 'JetBrains Mono', monospace; margin: 0; padding: 20px; }
        
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; padding-bottom: 15px; margin-bottom: 25px; }
        .clocks { display: flex; gap: 20px; font-size: 0.9em; color: #888; }
        .clock-box { text-align: right; }
        .clock-box span { color: var(--accent); display: block; font-size: 1.2em; }

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .card { background: var(--card); border: 1px solid #1a1a1a; border-radius: 12px; padding: 20px; position: relative; overflow: hidden; }
        .card::before { content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--accent); }
        .card.danger::before { background: var(--risk); }

        .balance { font-size: 2.5em; font-weight: bold; margin: 10px 0; letter-spacing: -1px; }
        .label { color: #666; font-size: 0.8em; text-transform: uppercase; }
        
        .dd-container { margin-top: 15px; }
        .dd-bar { background: #1a1a1a; height: 8px; border-radius: 4px; margin-top: 5px; }
        .dd-fill { background: var(--risk); height: 100%; width: 5%; border-radius: 4px; } /* Dinámico */

        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px; }
        .stat-item { background: #111; padding: 10px; border-radius: 6px; border: 1px solid #1a1a1a; }
        .stat-item b { color: var(--accent); font-size: 1.2em; }

        .status-badge { background: #1a1a1a; color: var(--accent); padding: 4px 12px; border-radius: 20px; font-size: 0.7em; border: 1px solid var(--accent); }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; font-size:1.5em;">STELLAR <span style="color:var(--accent)">AUDITOR PRO</span></h1>
            <small style="color:#444">v5.0 Institutional Dashboard | Machala Hub</small>
        </div>
        <div class="clocks">
            <div class="clock-box">LOCAL (ECU) <span id="ecu-clock">--:--:--</span></div>
            <div class="clock-box">SERVER (GMT+2) <span id="srv-clock">--:--:--</span></div>
        </div>
    </div>

    <div class="grid">
        {% for c in cuentas %}
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="label">{{ c.firm }} // {{ c.id }}</span>
                <span class="status-badge">{{ c.type }}</span>
            </div>
            <div class="balance">${{ "{:,.2f}".format(c.balance) }}</div>
            <div class="stats-grid">
                <div class="stat-item"><small class="label">Profit</small><br><b>+${{ "{:,.2f}".format(c.balance - c.inicial) }}</b></div>
                <div class="stat-item"><small class="label">Drawdown Avail.</small><br><b style="color:var(--risk)">${{ c.dd_limit }}</b></div>
            </div>
            <div class="dd-container">
                <small class="label">Daily Risk Exposure</small>
                <div class="dd-bar"><div class="dd-fill"></div></div>
            </div>
        </div>
        {% endfor %}

        <div class="card" style="border-color: #222;">
            <span class="label">Stellar Quantum v5.0 Stats</span>
            <div class="stats-grid" style="grid-template-columns: 1fr 1fr 1fr;">
                <div class="stat-item"><small>P. FACTOR</small><br><b>{{ stats.pf }}</b></div>
                <div class="stat-item"><small>WIN RATE</small><br><b>{{ stats.win_rate }}</b></div>
                <div class="stat-item"><small>SHARPE</small><br><b>{{ stats.sharpe }}</b></div>
            </div>
            <div style="margin-top:20px; padding:15px; background:#00ff8811; border-radius:8px; border:1px dashed var(--accent);">
                <small class="label" style="color:var(--accent)">Live Market Intel</small>
                <div style="display:flex; justify-content:space-between; margin-top:5px;">
                    <span>XAUUSD Z-Score: <b>{{ market.z_score }}</b></span>
                    <span>Stretch: <b>{{ market.stretch }}</b></span>
                </div>
            </div>
        </div>
    </div>

    <script>
        function updateClocks() {
            const now = new Date();
            const ecu = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Guayaquil', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }).format(now);
            const srv = new Intl.DateTimeFormat('en-US', { timeZone: 'Europe/Riga', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }).format(now);
            document.getElementById('ecu-clock').innerText = ecu;
            document.getElementById('srv-clock').innerText = srv;
        }
        setInterval(updateClocks, 1000);
        updateClocks();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **data)

@app.route('/telegram-bridge', methods=['POST'])
def bridge():
    global data
    update = request.get_json(force=True)
    if "message" in update:
        texto = update["message"]["text"]
        try:
            # Formato: ZSCORE, STRETCH, EQUITY
            parts = [p.strip() for p in texto.split(',')]
            data["market"]["z_score"] = float(parts[0])
            data["market"]["stretch"] = parts[1] + "%"
            data["cuentas"][0]["balance"] = float(parts[2])
            return "OK", 200
        except: return "Error", 400
    return "No Data", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
