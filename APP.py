import os
import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

def obtener_datos():
    # Mantenemos la integridad de tus datos validados
    return {
        "balance_real": 100796.91,
        "profit_audit": 33830.25,
        "trades_audit": 614,
        "wr_audit": "31.43%",
        "dd_audit": "14.14%",
        "daily_limit": 5000.00,
        "daily_used": 450.00
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STELLAR COMMANDER | TERMINAL</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@100;400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #020202;
            --card: #080808;
            --accent: #00ffa3;
            --gold: #ffcc00;
            --risk: #ff3e3e;
            --border: #1a1a1a;
            --text-dim: #555;
        }

        body {
            background-color: var(--bg);
            color: white;
            font-family: 'JetBrains Mono', monospace;
            margin: 0;
            padding: 40px;
            overflow-x: hidden;
        }

        /* Scanline effect for Terminal feel */
        body::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 2;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 40px;
        }

        .header h1 {
            margin: 0;
            font-weight: 100;
            letter-spacing: 15px;
            font-size: 1.2rem;
            color: var(--text-dim);
        }

        .header .status {
            font-size: 0.7rem;
            color: var(--accent);
            text-transform: uppercase;
        }

        .grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 25px;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            padding: 30px;
            position: relative;
            transition: all 0.3s ease;
        }

        .card:hover { border-color: #333; }

        .label {
            font-size: 0.65rem;
            text-transform: uppercase;
            color: var(--text-dim);
            letter-spacing: 2px;
            display: block;
            margin-bottom: 15px;
        }

        .value {
            font-size: 3.5rem;
            font-weight: 700;
            letter-spacing: -3px;
        }

        .accent-text { color: var(--accent); text-shadow: 0 0 20px rgba(0, 255, 163, 0.3); }
        .gold-text { color: var(--gold); text-shadow: 0 0 20px rgba(255, 204, 0, 0.3); }

        /* Performance Bar */
        .risk-meter {
            height: 4px;
            background: #111;
            margin-top: 20px;
            position: relative;
        }

        .risk-fill {
            position: absolute;
            height: 100%;
            background: var(--accent);
            box-shadow: 0 0 10px var(--accent);
        }

        .stats-table {
            width: 100%;
            margin-top: 25px;
            font-size: 0.75rem;
        }

        .stats-table td {
            padding: 10px 0;
            border-bottom: 1px solid #111;
        }

        .stats-table .val-right {
            text-align: right;
            color: white;
        }

        .tag {
            font-size: 0.6rem;
            padding: 4px 8px;
            border: 1px solid var(--border);
            color: var(--text-dim);
            margin-top: 20px;
            display: inline-block;
        }
    </style>
</head>
<body>

    <div class="header">
        <div>
            <div class="status">● SYSTEM_ONLINE // SECURE_ENCRYPTION</div>
            <h1>STELLAR COMMANDER</h1>
        </div>
        <div style="text-align: right; color: var(--text-dim); font-size: 0.7rem;">
            AUDIT_REF: XAU_V42_14Y<br>
            {{ d.balance_real }} USD
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <span class="label">Funded Account / Live Balance</span>
            <div class="value accent-text">${{ "{:,.2f}".format(d.balance_real) }}</div>
            
            <div style="margin-top: 40px;">
                <span class="label">Daily Drawdown Limit</span>
                <div style="display:flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 8px;">
                    <span>Used: ${{ d.daily_used }}</span>
                    <span>Remaining: ${{ d.daily_limit - d.daily_used }}</span>
                </div>
                <div class="risk-meter">
                    <div class="risk-fill" style="width: {{ (d.daily_used/d.daily_limit)*100 }}%"></div>
                </div>
            </div>
            
            <div class="tag">PROP FIRM: TOPSTEP // TYPE: QUANT_ALGO</div>
        </div>

        <div class="card">
            <span class="label">Engine Performance / 14Y Backtest</span>
            <div class="value gold-text">+${{ "{:,.2f}".format(d.profit_audit) }}</div>
            
            <table class="stats-table">
                <tr>
                    <td style="color: var(--text-dim);">TOTAL_TRADES</td>
                    <td class="val-right">{{ d.trades_audit }}</td>
                </tr>
                <tr>
                    <td style="color: var(--text-dim);">WIN_RATE</td>
                    <td class="val-right">{{ d.wr_audit }}</td>
                </tr>
                <tr>
                    <td style="color: var(--text-dim);">MAX_DRAWDOWN</td>
                    <td class="val-right" style="color: var(--risk);">{{ d.dd_audit }}</td>
                </tr>
                <tr>
                    <td style="color: var(--text-dim);">PERIOD</td>
                    <td class="val-right">2012 - 2026</td>
                </tr>
            </table>

            <div class="tag" style="color: var(--gold); border-color: rgba(255,204,0,0.2);">STRATEGY: STELLAR_V42</div>
        </div>
    </div>

</body>
</html>
'''

@app.route('/')
def home():
    contexto = obtener_datos()
    return render_template_string(HTML_TEMPLATE, d=contexto)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
