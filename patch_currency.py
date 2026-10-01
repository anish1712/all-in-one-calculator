with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_currency = """
                # Fetch live rates (using verify=False to bypass local SSL issues)
                url = f"https://api.exchangerate-api.com/v4/latest/{from_code}"
                response = requests.get(url, verify=False, timeout=5)
                data = response.json()
                
                rate = data['rates'][to_code]
                converted_amount = amount * rate
                
                res_html = f\"\"\"
<div class="result-box">
{converted_amount:,.2f} {to_code}
<div class="result-sub">Live Rate: 1 {from_code} = {rate} {to_code}</div>
</div>
                \"\"\"
"""

new_currency = """
                # Fetch live rates using Yahoo Finance
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{from_code}{to_code}=X"
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, verify=False, timeout=5)
                meta = response.json()['chart']['result'][0]['meta']
                
                rate = meta['regularMarketPrice']
                prev_rate = meta.get('previousClose') or meta.get('chartPreviousClose') or rate
                
                converted_amount = amount * rate
                
                diff = rate - prev_rate
                symbol = "📈" if diff >= 0 else "📉"
                color = "#38ef7d" if diff >= 0 else "#ff416c"
                sign = "+" if diff >= 0 else ""
                
                res_html = f\"\"\"<div class="result-box">
<div style="font-size: 32px; font-weight: bold;">{converted_amount:,.2f} {to_code}</div>
<div style="font-size: 16px; color:{color}; margin-top: 5px; font-weight: bold;">
    {symbol} {sign}{diff:,.4f} {to_code} (vs Yesterday)
</div>
<div class="result-sub" style="margin-top: 15px;">Live Rate: 1 {from_code} = {rate:,.4f} {to_code}</div>
</div>\"\"\"
"""

code = code.replace(old_currency.strip(), new_currency.strip())

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
