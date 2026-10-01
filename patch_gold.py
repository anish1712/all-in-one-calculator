with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Find the block for tab8
old_code = """
            headers = {'User-Agent': 'Mozilla/5.0'}
            g_req = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/GC=F', headers=headers, verify=False, timeout=5).json()
            s_req = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/SI=F', headers=headers, verify=False, timeout=5).json()
            i_req = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/INR=X', headers=headers, verify=False, timeout=5).json()
            
            gold_usd = g_req['chart']['result'][0]['meta']['regularMarketPrice']
            silver_usd = s_req['chart']['result'][0]['meta']['regularMarketPrice']
            usd_inr = i_req['chart']['result'][0]['meta']['regularMarketPrice']
            
            # 1 Troy Ounce = 31.103 grams. We want price per 10 grams in INR.
            gold_10g_base = (gold_usd / 31.103) * 10 * usd_inr
            silver_1kg_base = (silver_usd / 31.103) * 1000 * usd_inr
            
            # With Indian Taxes (~9%)
            gold_10g_24k = gold_10g_base * 1.09
            gold_10g_22k = gold_10g_base * 0.9167 * 1.09
            gold_10g_18k = gold_10g_base * 0.75 * 1.09
            
            silver_1kg_tax = silver_1kg_base * 1.09
            
            res_html = f\"\"\"<div class=\"result-box\">
    <h4 style=\"color:#fff; margin-bottom:5px;\">🥇 Gold (10 Grams)</h4>
    <div style=\"font-size: 20px; color:#ddd; margin-bottom: 10px;\">Global Base Rate (24K): ₹{int(gold_10g_base):,}</div>
    <div style=\"background: rgba(0,0,0,0.2); padding: 15px; border-radius: 15px;\">
        <b style=\"color: #ffd700;\">24K (99.9% Purity):</b> ₹{int(gold_10g_24k):,} <br>
        <b style=\"color: #e6c200;\">22K (91.6% Purity):</b> ₹{int(gold_10g_22k):,} <br>
        <b style=\"color: #ccac00;\">18K (75.0% Purity):</b> ₹{int(gold_10g_18k):,}
    </div>
    <hr style=\"opacity: 0.2; margin: 15px 0;\">
    <h4 style=\"color:#fff; margin-bottom:5px;\">🥈 Silver (1 KG)</h4>
    <div style=\"font-size: 20px; color:#ddd; margin-bottom: 10px;\">Global Base Rate: ₹{int(silver_1kg_base):,}</div>
    <div style=\"background: rgba(0,0,0,0.2); padding: 10px; border-radius: 15px;\">
        <b>Indian Retail Market:</b> ₹{int(silver_1kg_tax):,}
    </div>
    <div class=\"result-sub\">Prices include approx 9% duty/GST | 1 USD = ₹{usd_inr:.2f}</div>
</div>\"\"\"
"""

new_code = """
            headers = {'User-Agent': 'Mozilla/5.0'}
            g_meta = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/GC=F', headers=headers, verify=False, timeout=5).json()['chart']['result'][0]['meta']
            s_meta = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/SI=F', headers=headers, verify=False, timeout=5).json()['chart']['result'][0]['meta']
            i_meta = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/INR=X', headers=headers, verify=False, timeout=5).json()['chart']['result'][0]['meta']
            
            gold_usd = g_meta['regularMarketPrice']
            gold_prev = g_meta.get('previousClose') or g_meta.get('chartPreviousClose') or gold_usd
            
            silver_usd = s_meta['regularMarketPrice']
            silver_prev = s_meta.get('previousClose') or s_meta.get('chartPreviousClose') or silver_usd
            
            usd_inr = i_meta['regularMarketPrice']
            
            # 1 Troy Ounce = 31.103 grams. We want price per 10 grams in INR.
            gold_10g_base = (gold_usd / 31.103) * 10 * usd_inr
            gold_10g_prev = (gold_prev / 31.103) * 10 * usd_inr
            gold_diff = gold_10g_base - gold_10g_prev
            gold_symbol = "📈" if gold_diff >= 0 else "📉"
            gold_color = "#38ef7d" if gold_diff >= 0 else "#ff416c"
            gold_sign = "+" if gold_diff >= 0 else ""
            
            silver_1kg_base = (silver_usd / 31.103) * 1000 * usd_inr
            silver_1kg_prev = (silver_prev / 31.103) * 1000 * usd_inr
            silver_diff = silver_1kg_base - silver_1kg_prev
            silver_symbol = "📈" if silver_diff >= 0 else "📉"
            silver_color = "#38ef7d" if silver_diff >= 0 else "#ff416c"
            silver_sign = "+" if silver_diff >= 0 else ""
            
            # With Indian Taxes (~9%)
            gold_10g_24k = gold_10g_base * 1.09
            gold_10g_22k = gold_10g_base * 0.9167 * 1.09
            gold_10g_18k = gold_10g_base * 0.75 * 1.09
            
            silver_1kg_tax = silver_1kg_base * 1.09
            
            res_html = f\"\"\"<div class=\"result-box\">
    <h4 style=\"color:#fff; margin-bottom:5px;\">🥇 Gold (10 Grams)</h4>
    <div style=\"font-size: 20px; color:#ddd; margin-bottom: 5px;\">Global Base Rate (24K): ₹{int(gold_10g_base):,}</div>
    <div style=\"font-size: 16px; color:{gold_color}; margin-bottom: 15px; font-weight: bold;\">
        {gold_symbol} {gold_sign}₹{int(gold_diff):,} (vs Yesterday)
    </div>
    
    <div style=\"background: rgba(0,0,0,0.2); padding: 15px; border-radius: 15px;\">
        <b style=\"color: #ffd700;\">24K (99.9% Purity):</b> ₹{int(gold_10g_24k):,} <br>
        <b style=\"color: #e6c200;\">22K (91.6% Purity):</b> ₹{int(gold_10g_22k):,} <br>
        <b style=\"color: #ccac00;\">18K (75.0% Purity):</b> ₹{int(gold_10g_18k):,}
    </div>
    <hr style=\"opacity: 0.2; margin: 15px 0;\">
    <h4 style=\"color:#fff; margin-bottom:5px;\">🥈 Silver (1 KG)</h4>
    <div style=\"font-size: 20px; color:#ddd; margin-bottom: 5px;\">Global Base Rate: ₹{int(silver_1kg_base):,}</div>
    <div style=\"font-size: 16px; color:{silver_color}; margin-bottom: 15px; font-weight: bold;\">
        {silver_symbol} {silver_sign}₹{int(silver_diff):,} (vs Yesterday)
    </div>
    
    <div style=\"background: rgba(0,0,0,0.2); padding: 10px; border-radius: 15px;\">
        <b>Indian Retail Market:</b> ₹{int(silver_1kg_tax):,}
    </div>
    <div class=\"result-sub\">Prices include approx 9% duty/GST | 1 USD = ₹{usd_inr:.2f}</div>
</div>\"\"\"
"""

code = code.replace(old_code.strip(), new_code.strip())

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
