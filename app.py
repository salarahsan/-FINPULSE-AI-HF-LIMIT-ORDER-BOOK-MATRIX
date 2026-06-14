import sys
import types
import random
import numpy as np

# 🚨 DYNAMIC COMPATIBILITY PATCH: Python 3.13 Clean Runtime Layer
if 'audioop' not in sys.modules:
    dummy_audioop = types.ModuleType('audioop')
    dummy_audioop.error = Exception
    sys.modules['audioop'] = dummy_audioop

import gradio as gr

def process_lob_matrix(market_pair, volatility_factor):
    base_price = 68250.00 if "BTC" in market_pair else 1.08450
    spread_multiplier = 0.00015 if "BTC" in market_pair else 0.00008
    volatility = float(volatility_factor) / 100.0
    
    step_sizes = np.array([1, 2, 3, 4, 5])
    raw_asks = base_price + (step_sizes * (base_price * spread_multiplier * (1 + volatility * random.uniform(0.2, 1.8))))
    raw_bids = base_price - (step_sizes * (base_price * spread_multiplier * (1 + volatility * random.uniform(0.2, 1.8))))
    
    ask_volumes = [random.randint(15, 140) for _ in range(5)]
    bid_volumes = [random.randint(15, 140) for _ in range(5)]
    
    total_ask_vol = sum(ask_volumes)
    total_bid_vol = sum(bid_volumes)
    volume_imbalance = (total_bid_vol - total_ask_vol) / (total_bid_vol + total_ask_vol)
    
    bid_ask_spread = raw_asks[0] - raw_bids[0]
    market_state = "🟢 BULLISH PRESSURE" if volume_imbalance > 0.05 else ("🔴 BEARISH REJECTION" if volume_imbalance < -0.05 else "🟡 NEUTRAL EQUILIBRIUM")
    
    ask_rows_html = ""
    for price, vol in zip(reversed(raw_asks), reversed(ask_volumes)):
        width_ratio = min(max(int((vol / 140) * 100), 15), 100)
        format_str = f"{price:.2f}" if "BTC" in market_pair else f"{price:.5f}"
        ask_rows_html += f"""
        <div class='lob-data-row ask-strip'>
            <span style='color: #f43f5e; font-weight: 700;'>{format_str}</span>
            <span style='color: #cbd5e1; font-family: monospace;'>{vol}.4K</span>
            <div class='depth-bar-ask' style='width: {width_ratio}%;'></div>
        </div>"""
        
    bid_rows_html = ""
    for price, vol in zip(raw_bids, bid_volumes):
        width_ratio = min(max(int((vol / 140) * 100), 15), 100)
        format_str = f"{price:.2f}" if "BTC" in market_pair else f"{price:.5f}"
        bid_rows_html += f"""
        <div class='lob-data-row bid-strip'>
            <span style='color: #10b981; font-weight: 700;'>{format_str}</span>
            <span style='color: #cbd5e1; font-family: monospace;'>{vol}.2K</span>
            <div class='depth-bar-bid' style='width: {width_ratio}%;'></div>
        </div>"""

    terminal_dashboard_html = f"""
    <div style='background: #020617; border: 1px solid #1e293b; padding: 20px; border-radius: 10px; animation: scaleInTerminal 0.4s cubic-bezier(0.16, 1, 0.3, 1);'>
        <div class='terminal-grid-layout'>
            <div class='grid-panel'>
                <h4 style='color: #f43f5e; margin: 0 0 12px 0; font-size: 13px; font-weight: 800; letter-spacing: 0.5px;'>🛑 ASK DEPTH MATRIX (RESISTANCE OVERLAY)</h4>
                {ask_rows_html}
            </div>
            <div class='grid-panel' style='border-left: 1px solid #1e293b; padding-left: 20px;'>
                <h4 style='color: #10b981; margin: 0 0 12px 0; font-size: 13px; font-weight: 800; letter-spacing: 0.5px;'>🟩 BID DEPTH MATRIX (SUPPORT OVERLAY)</h4>
                {bid_rows_html}
            </div>
        </div>
        
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 22px;'>
            <div class='quant-badge-container metric-update-flash'>
                <div class='badge-label'>BID-ASK SPREAD VECTOR</div>
                <div class='badge-value' style='color: #38bdf8;'>{bid_ask_spread:.5f}</div>
            </div>
            <div class='quant-badge-container metric-update-flash'>
                <div class='badge-label'>VOLUME IMBALANCE RATIO</div>
                <div class='badge-value' style='color: #fbbf24;'>{volume_imbalance:+.4f}</div>
            </div>
            <div class='quant-badge-container metric-update-flash'>
                <div class='badge-label'>ORDER FLOW SPECTRUM STATUS</div>
                <div class='badge-value' style='color: {"#10b981" if "BULLISH" in market_state else ("#f43f5e" if "BEARISH" in market_state else "#94a3b8")};'>{market_state}</div>
            </div>
        </div>
    </div>
    """
    return terminal_dashboard_html

custom_css = """
body, .gradio-container { background-color: #030712 !important; color: #f1f5f9 !important; font-family: system-ui, -apple-system, sans-serif; }
.dashboard-card { border: 1px solid #1e293b !important; border-radius: 14px; padding: 26px; background: #090d16 !important; box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important; position: relative; }
.dashboard-card:hover { border-color: #38bdf8 !important; box-shadow: 0 0 25px rgba(56,189,248,0.12) !important; }
.execution-trigger-btn { background: linear-gradient(135deg, #1d4ed8, #2563eb) !important; color: #ffffff !important; font-weight: 800 !important; border-radius: 8px !important; border: none !important; height: 48px; font-size: 14px !important; letter-spacing: 0.5px; box-shadow: 0 4px 15px rgba(37,99,235,0.3); transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); cursor: pointer; }
.execution-trigger-btn:hover { background: linear-gradient(135deg, #2563eb, #3b82f6) !important; transform: translateY(-1px); box-shadow: 0 0 20px rgba(56,189,248,0.4); }
.execution-trigger-btn:active { transform: scale(0.98); }
.quant-badge-container { background-color: #050b14; border: 1px solid #1e293b; padding: 14px; border-radius: 8px; text-align: center; transition: border-color 0.3s; }
.badge-label { color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; }
.badge-value { font-size: 16px; font-weight: 800; font-family: monospace; margin-top: 5px; }
.terminal-grid-layout { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.grid-panel { display: flex; flex-direction: column; gap: 7px; }
.lob-data-row { display: flex; justify-content: space-between; padding: 9px 14px; border-radius: 5px; font-family: monospace; font-size: 13px; position: relative; overflow: hidden; background: #070a13; border: 1px solid #111a2e; transition: all 0.2s ease; }
.lob-data-row:hover { border-color: #38bdf8; background: #0c1324; }
/* 🌀 ADVANCED REAL-TIME BROWSER CSS KEYFRAMES */
@keyframes depthBreathing {
    0% { opacity: 0.6; }
    50% { opacity: 0.95; filter: brightness(1.2); }
    100% { opacity: 0.6; }
}
@keyframes scaleInTerminal {
    from { opacity: 0; transform: scale(0.98) translateY(10px); filter: blur(2px); }
    to { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); }
}
@keyframes flashUpdate {
    0% { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56,189,248,0.3); }
    100% { border-color: #1e293b; box-shadow: none; }
}
@keyframes pulseStatusDot {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.6; background: #38bdf8; }
    100% { transform: scale(1); opacity: 1; }
}
.depth-bar-ask { position: absolute; top: 0; right: 0; height: 100%; background: rgba(244, 63, 94, 0.14); border-left: 2px solid rgba(244, 63, 94, 0.5); animation: depthBreathing 3s infinite ease-in-out; width: 0; transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.depth-bar-bid { position: absolute; top: 0; left: 0; height: 100%; background: rgba(16, 185, 129, 0.14); border-right: 2px solid rgba(16, 185, 129, 0.5); animation: depthBreathing 3s infinite ease-in-out; width: 0; transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.metric-update-flash { animation: flashUpdate 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.live-status-pipeline { height: 38px; background: #040811; border: 1px solid #1e293b; border-radius: 6px; margin-top: 18px; display: flex; align-items: center; justify-content: center; font-family: monospace; font-size: 12px; color: #38bdf8; font-weight: bold; letter-spacing: 0.5px; animation: pulseStatusDot 2.5s infinite ease-in-out; }
select { background-color: #0f172a !important; color: #ffffff !important; border: 1px solid #1e293b !important; height: 42px !important; font-size: 14px !important; font-weight: bold !important; border-radius: 6px !important; transition: all 0.2s; }
select:focus { border-color: #38bdf8 !important; }
input[type="range"] { accent-color: #38bdf8 !important; }
label span { color: #94a3b8 !important; font-weight: 700 !important; font-size: 13px !important; }
"""

with gr.Blocks(title="FinPulse AI: Zero GPU Node") as demo:
    gr.HTML(
        """
        <div style="text-align: center; margin-bottom: 25px; padding: 24px; background: #070d19; border: 1px solid #1e293b; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
            <h1 style='margin: 0; font-size: 25px; color: #ffffff; font-weight: 800; letter-spacing: 0.5px; text-shadow: 0 0 15px rgba(56,189,248,0.25);'>💹 FINPULSE AI: HF LIMIT ORDER BOOK MATRIX</h1>
            <p style='margin: 6px 0 0 0; color: #38bdf8; font-size: 14px; font-weight: 700;'>Zero GPU Architecture // Native Vector Processing Pipeline</p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=4, elem_classes="dashboard-card"):
            gr.Markdown("### 📥 Order Book Ingestion Controls")
            market_pair = gr.Dropdown(
                label="Target Financial Asset Node",
                choices=["BTC/USDT (Crypto Liquidity Index)", "EUR/USD (Macro Spot Influx)"],
                value="BTC/USDT (Crypto Liquidity Index)"
            )
            volatility_factor = gr.Slider(
                label="Micro-Imbalance Variance Delta (%)",
                minimum=10,
                maximum=90,
                value=50,
                step=1
            )
            process_btn = gr.Button("⚡ Run In-Memory Liquidity Ingest Loop", elem_classes="execution-trigger-btn")
            
            gr.HTML(
                """
                <div class='live-status-pipeline'>
                    ⚙️ ENGINE READY // FREE CPU TIER ARCHITECTURE // LATENCY: <10ms
                </div>
                """
            )
            
        with gr.Column(scale=6, elem_classes="dashboard-card"):
            gr.Markdown("### 📊 Order Flow Heat-Map Output Visualizer")
            analytics_output = gr.HTML(
                "<div style='background-color: #040711; border: 1px solid #1e293b; padding: 40px; border-radius: 8px; color: #64748b; font-style: italic; font-size: 13px; text-align: center;'>Engine initialized on Basic CPU. Select parameters above to compile order flow metrics...</div>"
            )

    process_btn.click(
        fn=process_lob_matrix,
        inputs=[market_pair, volatility_factor],
        outputs=[analytics_output]
    )

demo.launch(css=custom_css)
