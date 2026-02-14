import os
from flask import Flask, request, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# --- CONFIGURACIÓN SEPARADA: REAL VS. HISTÓRICO ---
data = {
    "cuenta_real": {
        "id": "TF-8532",
        "firm": "TOPSTEP",
        "balance": 100796.91,   # TU CAPITAL REAL ACTUAL
        "inicial": 100000.00,
        "daily_limit": 2000.00,  # Límites de tu prueba actual
        "daily_loss": 0.00,
        "type": "Funded"
    },
    "auditoria_sistema": {
        "nombre": "Stellar v42 Restoration",
        "profit_historico": 33830.25, # RÉCORD DE 14 AÑOS
        "max_drawdown_hist": "14.14%",
        "total_trades": 614,
        "win_rate": "31.43%",
        "periodo": "2012 - 2026",
        "status": "VALIDADO"
    },
    "market": {
        "gdp": "EXPANSIÓN",
        "sentiment": "ESTABLE",
        "z_score": 0.0
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>STELLAR AUDITOR v5.2</title>
    <style>
        :root { --bg: #050505; --card: #0d0d0d; --accent: #00ff88; --risk: #ff3355; --gold: #d4af37; --text: #e0e0e0; }
        body { background: var(--bg); color: var(--text); font-family: 'JetBrains Mono', monospace; margin: 0; padding: 20px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: var(--card); border: 1px solid #1a1a1a; border-radius: 12px; padding: 20px; }
        .header-real { border-left: 4px solid var(--accent); margin-bottom: 20px; padding-left: 15px; }
        .header-audit { border-left: 4px solid var(--gold); margin-bottom: 20px; padding-left: 15px; }
        .balance { font-size: 2.8em; font-weight: bold; color: var(--accent); }
        .stat-box { background: #111; padding: 10px; border-radius: 6px; margin-top: 10px; border: 1px solid #222; }
        .label { color: #666; font-size: 0.7em; text-transform: uppercase; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.7em; font-weight: bold; }
        .bg-gold { background: rgba(212, 175, 55, 0.1); color: var(--gold); border: 1px solid var(--gold); }
    </style>
</head>
<body>
    <h1 style="font-size: 1.2em; color: #444; margin-bottom: 30px;">BASE DE MANDO // {{ cuenta_real.id }}</h1>

    <div class="grid">
        <div class="card">
            <div class="header-real">
                <span class="label">Balance Real en Vivo - {{ cuenta_real.firm }}</span>
                <div class="balance">${{ "{:,.2f}".format(cuenta_real.balance) }}</div>
            </div>
            <div class="stat-box">
                <small class="label">Riesgo Diario Disponible</small><br>
                <b style="color:var(--risk); font-size: 1.2em;">${{ "{:,.2f}".format(cuenta_real.daily_limit - cuenta_real.daily_loss) }}</b>
            </div>
            <div style="margin-top: 15px;">
                <span class="badge" style="background: rgba(0,255,136,0.1); color: var(--accent);">EQUITY REAL: {{ "{:,.2f}".format((cuenta_real.balance/cuenta_real.inicial)*100 - 100) }}%</span>
            </div>
        </div>

        <div class="card">
            <div class="header-audit">
                <span class="label">Auditoría Histórica del Sistema</span>
                <div style="font-size: 2em; font-weight: bold; color: var(--gold);">+${{ "{:,.2f}".format(auditoria_sistema.profit_historico) }}</div>
            </div>
            <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="stat-box">
                    <small class="label">Win Rate Hist.</small><br>
                    <b>{{ auditoria_sistema.win_rate }}</b>
                </div>
                <div class="stat-box">
                    <small class="label">Max DD Hist.</small><br>
                    <b style="color: var(--risk);">{{ auditoria_sistema.max_drawdown_hist }}</b>
                </div>
            </div>
            <div style="margin-top: 15px; font-size: 0.8em; color: #555;">
                <span class="badge bg-gold">MUESTRA: {{ auditoria_sistema.total_trades }} OPERACIONES</span>
                <span class="badge bg-gold">PERIODO: {{ auditoria_sistema.periodo }}</span>
            </div>
        </div>
    </div>

    <div class="card" style="margin-top: 20px; display: flex; justify-content: space-between; align-items: center; padding: 15px;">
        <span class="label">Market Intel: GDP <b style="color:var(--accent)">{{ market.gdp }}</b></span>
        <span class="label">Z-Score: <b style="color:var(--gold)">{{ market.z_score }}</b></span>
        <span class="badge" style="border: 1px solid #333;">SAYAYIN V5.2 ACTIVE</span>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, **data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
