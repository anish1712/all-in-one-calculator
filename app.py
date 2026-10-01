import streamlit as st
import streamlit.components.v1 as components
import datetime
import math
import requests

# --- Page Config ---
st.set_page_config(page_title="All-in-One Online Calculator - EMI, SIP, BMI, Age", page_icon="📊", layout="centered")

# --- Google Site Verification ---
components.html(
    """
    <script>
        var meta = parent.document.createElement('meta');
        meta.name = 'google-site-verification';
        meta.content = 'Zsnc747ycqc3-15XQUD4q38lvkdMYsfIFqLIyRRGQnU';
        parent.document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    height=0, width=0
)



# --- Custom Premium CSS ---
st.markdown("""
<style>
    /* Dark & Light Mode Auto Support */
    h1 {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    /* Hide Streamlit Header & Footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 3D Glassmorphism Result Box */
    .result-box {
        background: linear-gradient(145deg, #1e3c72, #2a5298);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(30,60,114,0.4), inset 0 2px 5px rgba(255,255,255,0.5);
        margin-top: 25px;
        font-size: 28px;
        font-weight: 900;
        border: 1px solid rgba(255,255,255,0.2);
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    .result-sub {
        font-size: 16px;
        font-weight: 600;
        margin-top: 15px;
        background: rgba(0,0,0,0.2);
        padding: 8px 18px;
        border-radius: 25px;
        display: inline-block;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);
        color: #fff;
    }
    
    /* True 3D Physical Buttons for Streamlit */
    div.stButton > button {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white !important;
        border: none;
        border-radius: 15px;
        padding: 12px 25px;
        font-size: 20px;
        font-weight: 900;
        box-shadow: 0 6px 0 #c2294c, 0 12px 25px rgba(255, 75, 43, 0.4);
        transition: all 0.1s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:active, div.stButton > button:focus {
        transform: translateY(6px);
        box-shadow: 0 0px 0 #c2294c, 0 4px 10px rgba(255, 75, 43, 0.4);
    }
    
    /* 3D Input Fields (Neumorphism) */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        border-radius: 15px !important;
        border: none !important;
        background: #ebedee !important;
        box-shadow: inset 5px 5px 10px #c8c9cc, inset -5px -5px 10px #ffffff !important;
        transition: all 0.3s;
        padding: 5px;
    }
    div[data-baseweb="input"]:focus-within {
        box-shadow: inset 2px 2px 5px #c8c9cc, inset -2px -2px 5px #ffffff, 0 0 10px rgba(255,65,108,0.3) !important;
    }
    
    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-size: 17px !important;
        font-weight: bold !important;
        background: transparent !important;
        color: #555555 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("📊 All-in-One Online Calculator")
st.markdown("<p style='text-align: center; opacity: 0.8; font-size: 16px; font-weight: 500;'>11+ Powerful Tools: Basic & Scientific, EMI, SIP, Live Gold, Currency, GST & more — Everything in one place!</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Tabs ---
tab5, tab6, tab1, tab2, tab3, tab8, tab4, tab7 = st.tabs([
    "🧮 Basic", 
    "🧪 Scientific", 
    "🏠 EMI", 
    "📈 SIP", 
    "💱 Live Currency", 
    "🥇 Live Gold",
    "🎂 Age", 
    "➕ More Tools"
])

# ==========================================
# TAB 1: EMI Calculator
# ==========================================
with tab1:
    st.subheader("Loan EMI Calculator")
    
    # Auto-fill bank rates
    bank_rates = {
        "Custom Rate": 9.5,
        "SBI Home Loan": 8.50,
        "HDFC Bank": 8.70,
        "ICICI Bank": 9.00,
        "Axis Bank": 8.75,
        "Bank of Baroda": 8.60,
        "Kotak Mahindra": 8.75
    }
    
    st.markdown("<p style='font-size:14px; opacity:0.8;'>💡 Select a bank to auto-fill current Home Loan rates, or enter your own custom rate.</p>", unsafe_allow_html=True)
    selected_bank = st.selectbox("Select Bank (Optional):", list(bank_rates.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        principal = st.number_input("Loan Amount (₹)", min_value=1000, value=500000, step=10000)
        tenure_years = st.number_input("Tenure (Years)", min_value=1, value=5, step=1)
    with col2:
        rate = st.number_input("Interest Rate (% P.A.)", min_value=1.0, value=bank_rates[selected_bank], step=0.1)
    
    if st.button("Calculate EMI 🏠", use_container_width=True):
        r = (rate / 12) / 100
        n = tenure_years * 12
        if r > 0:
            emi = principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
        else:
            emi = principal / n
            
        total_payment = emi * n
        total_interest = total_payment - principal
        
        res_html = f"""
<div class="result-box">
Monthly EMI: ₹{int(emi):,}
<div class="result-sub">Total Interest: ₹{int(total_interest):,} | Total Payment: ₹{int(total_payment):,}</div>
</div>
        """
        st.markdown(res_html, unsafe_allow_html=True)

# ==========================================
# TAB 2: SIP Calculator
# ==========================================
with tab2:
    st.subheader("SIP Investment Calculator")
    col1, col2 = st.columns(2)
    with col1:
        sip_amount = st.number_input("Monthly Investment (₹)", min_value=500, value=2000, step=500)
        sip_years = st.number_input("Time Period (Years)", min_value=1, value=10, step=1)
    with col2:
        sip_rate = st.number_input("Expected Return (% P.A.)", min_value=1.0, value=12.0, step=0.5)
        
    if st.button("Calculate SIP 📈", use_container_width=True):
        i = (sip_rate / 12) / 100
        n_sip = sip_years * 12
        future_value = sip_amount * (((1 + i) ** n_sip - 1) / i) * (1 + i)
        total_invested = sip_amount * n_sip
        wealth_gained = future_value - total_invested
        
        res_html = f"""
<div class="result-box">
Future Wealth: ₹{int(future_value):,}
<div class="result-sub">Amount Invested: ₹{int(total_invested):,} | Wealth Gained: ₹{int(wealth_gained):,}</div>
</div>
        """
        st.markdown(res_html, unsafe_allow_html=True)

# ==========================================
# TAB 3: Live Currency Converter
# ==========================================
with tab3:
    st.subheader("💱 Live Currency Converter")
    st.markdown("<p style='font-size:14px; opacity:0.8;'>💡 This tool fetches real-time exchange rates from the internet.</p>", unsafe_allow_html=True)
    
    currencies = ["USD - US Dollar", "EUR - Euro", "GBP - British Pound", "AED - UAE Dirham", "CAD - Canadian Dollar", "AUD - Australian Dollar", "INR - Indian Rupee"]
    
    amount = st.number_input("Amount to Convert", min_value=1.0, value=100.0, step=10.0)
    
    col1, col2 = st.columns(2)
    with col1:
        from_curr = st.selectbox("From Currency", currencies, index=0)
    with col2:
        to_curr = st.selectbox("To Currency", currencies, index=6)
        
    if st.button("Convert Currency 💱", use_container_width=True):
        from_code = from_curr.split(" ")[0]
        to_code = to_curr.split(" ")[0]
        
        if from_code == to_code:
            st.warning("Please select different currencies.")
        else:
            try:
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
                
                res_html = f"""<div class="result-box">
<div style="font-size: 32px; font-weight: bold;">{converted_amount:,.2f} {to_code}</div>
<div style="font-size: 16px; color:{color}; margin-top: 5px; font-weight: bold;">
{symbol} {sign}{diff:,.4f} {to_code} (vs Yesterday)
</div>
<div class="result-sub" style="margin-top: 15px;">Live Rate: 1 {from_code} = {rate:,.4f} {to_code}</div>
</div>"""
                st.markdown(res_html, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error fetching live rates. Please check your internet connection.")

# ==========================================
# TAB 4: Age Calculator
# ==========================================
with tab4:
    st.subheader("Age Calculator")
    dob = st.date_input("Select Date of Birth (DD/MM/YYYY):", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(), format="DD/MM/YYYY")
    
    if st.button("Calculate Age 🎂", use_container_width=True):
        today = datetime.date.today()
        years = today.year - dob.year
        months = today.month - dob.month
        days = today.day - dob.day
        
        if days < 0:
            months -= 1
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_month_days = 31 if prev_month in [1,3,5,7,8,10,12] else (28 if prev_month == 2 else 30)
            days += prev_month_days
            
        if months < 0:
            years -= 1
            months += 12
            
        total_days = (today - dob).days
        total_months = (years * 12) + months
        
        res_html = f"""
<div class="result-box">
Age: {years} Years, {months} Months, {days} Days
<div class="result-sub">Total Months: {total_months} | Total Days: {total_days:,}</div>
</div>
        """
        st.markdown(res_html, unsafe_allow_html=True)

# ==========================================
# TAB 5: Basic Calculator (HTML/JS)
# ==========================================
with tab5:
    st.subheader("🧮 Basic Calculator")
    basic_calc_html = """
    <style>
    * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    body { background: transparent; margin:0; display:flex; justify-content:center; }
    .calc-container { width: 100%; max-width: 350px; background: rgba(255, 255, 255, 0.9); border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid #ddd; }
    .display { width: 100%; height: 70px; font-size: 36px; text-align: right; border: none; background: #f3f4f6; border-radius: 12px; padding: 10px 15px; margin-bottom: 20px; color: #1a1a1a !important; }
    .btn-row { display: flex; justify-content: space-between; margin-bottom: 12px; }
    .btn { width: 23%; height: 60px; font-size: 24px; border: none; border-radius: 12px; cursor: pointer; background: #e0e5ec; color: #333; transition: 0.2s; font-weight: bold; }
    .btn:active { transform: scale(0.92); }
    
      @media (prefers-color-scheme: dark) {
        .calc-container { background: rgba(30, 30, 30, 0.95); border: 1px solid #444; }
        .display { background: #222; color: #fff !important; }
        .btn { background: #3d3d3d; color: #fff; }
        .btn.btn-op { background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); color: white; }
        .btn.btn-sci { background: #475569; color: #f8fafc; }
        .btn.btn-eq { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
      }
      </style>
    <div class="calc-container">
        <input type="text" class="display" id="res" disabled value="0">
        <div class="btn-row">
            <button class="btn btn-op" onclick="c()">C</button>
            <button class="btn btn-op" onclick="b()">⌫</button>
            <button class="btn btn-op" onclick="a('%')">%</button>
            <button class="btn btn-op" onclick="a('/')">÷</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('7')">7</button>
            <button class="btn" onclick="a('8')">8</button>
            <button class="btn" onclick="a('9')">9</button>
            <button class="btn btn-op" onclick="a('*')">×</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('4')">4</button>
            <button class="btn" onclick="a('5')">5</button>
            <button class="btn" onclick="a('6')">6</button>
            <button class="btn btn-op" onclick="a('-')">-</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('1')">1</button>
            <button class="btn" onclick="a('2')">2</button>
            <button class="btn" onclick="a('3')">3</button>
            <button class="btn btn-op" onclick="a('+')">+</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('00')">00</button>
            <button class="btn" onclick="a('0')">0</button>
            <button class="btn" onclick="a('.')">.</button>
            <button class="btn btn-op" onclick="calc()">=</button>
        </div>
    </div>
    <script>
    let d = document.getElementById('res');
    function a(v) { if(d.value==='0' || d.value==='Error') d.value=v; else d.value+=v; }
    function c() { d.value='0'; }
    function b() { d.value = d.value.slice(0,-1); if(d.value==='') d.value='0'; }
    function calc() { try { d.value = eval(d.value); } catch(e) { d.value = 'Error'; } }
    </script>
    """
    components.html(basic_calc_html, height=520)

# ==========================================
# TAB 6: Scientific Calculator
# ==========================================
with tab6:
    st.subheader("🧪 Scientific Calculator")
    sci_calc_html = """
    <style>
    * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    body { background: transparent; margin:0; display:flex; justify-content:center; }
    .calc-container { width: 100%; max-width: 400px; background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 1px solid #ddd; }
    .display { width: 100%; height: 70px; font-size: 28px; text-align: right; border: none; background: #f3f4f6; border-radius: 12px; padding: 10px 15px; margin-bottom: 20px; color: #1a1a1a !important; letter-spacing: 1px; }
    .btn-row { display: flex; justify-content: space-between; margin-bottom: 10px; }
    .btn { flex: 1; margin: 0 4px; height: 55px; font-size: 18px; border: none; border-radius: 10px; cursor: pointer; background: #e0e5ec; color: #333; transition: 0.2s; font-weight: 600; }
    .btn:active { transform: scale(0.92); }
    
      @media (prefers-color-scheme: dark) {
        .calc-container { background: rgba(30, 30, 30, 0.95); border: 1px solid #444; }
        .display { background: #222; color: #fff !important; }
        .btn { background: #3d3d3d; color: #fff; }
        .btn.btn-op { background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); color: white; }
        .btn.btn-sci { background: #475569; color: #f8fafc; }
        .btn.btn-eq { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
      }
      </style>
    <div class="calc-container">
        <input type="text" class="display" id="res" disabled value="0">
        
        <div class="btn-row">
            <button class="btn btn-sci" onclick="a('sin(')">sin</button>
            <button class="btn btn-sci" onclick="a('cos(')">cos</button>
            <button class="btn btn-sci" onclick="a('tan(')">tan</button>
            <button class="btn btn-sci" onclick="a('log(')">log</button>
            <button class="btn btn-op" onclick="c()">C</button>
            <button class="btn btn-op" onclick="b()">⌫</button>
        </div>
        <div class="btn-row">
            <button class="btn btn-sci" onclick="a('(')">(</button>
            <button class="btn btn-sci" onclick="a(')')">)</button>
            <button class="btn btn-sci" onclick="a('**')">x^y</button>
            <button class="btn btn-sci" onclick="a('sqrt(')">√</button>
            <button class="btn btn-sci" onclick="a('pi')">π</button>
            <button class="btn btn-sci" onclick="a('e')">e</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('7')">7</button>
            <button class="btn" onclick="a('8')">8</button>
            <button class="btn" onclick="a('9')">9</button>
            <button class="btn btn-op" onclick="a('/')">÷</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('4')">4</button>
            <button class="btn" onclick="a('5')">5</button>
            <button class="btn" onclick="a('6')">6</button>
            <button class="btn btn-op" onclick="a('*')">×</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('1')">1</button>
            <button class="btn" onclick="a('2')">2</button>
            <button class="btn" onclick="a('3')">3</button>
            <button class="btn btn-op" onclick="a('-')">-</button>
        </div>
        <div class="btn-row">
            <button class="btn" onclick="a('00')">00</button>
            <button class="btn" onclick="a('0')">0</button>
            <button class="btn" onclick="a('.')">.</button>
            <button class="btn btn-op" onclick="a('+')">+</button>
            <button class="btn btn-eq" onclick="calc()">=</button>
        </div>
    </div>
    
    <script>
    // Math functions wrapper for eval
    function sin(x) { return Math.sin(x * Math.PI / 180); } // Degrees
    function cos(x) { return Math.cos(x * Math.PI / 180); }
    function tan(x) { return Math.tan(x * Math.PI / 180); }
    function log(x) { return Math.log10(x); }
    function sqrt(x) { return Math.sqrt(x); }
    const pi = Math.PI;
    const e = Math.E;
    
    let d = document.getElementById('res');
    function a(v) { if(d.value==='0' || d.value==='Error' || d.value==='NaN' || d.value==='Infinity') d.value=v; else d.value+=v; }
    function c() { d.value='0'; }
    function b() { d.value = d.value.slice(0,-1); if(d.value==='') d.value='0'; }
    function calc() { 
        try { 
            let result = eval(d.value); 
            // format to avoid long decimals
            d.value = Math.round(result * 100000000) / 100000000;
        } catch(err) { 
            d.value = 'Error'; 
        } 
    }
    </script>
    """
    components.html(sci_calc_html, height=520)

# ==========================================
# TAB 8: Live Gold / Silver Price
# ==========================================
with tab8:
    st.subheader("🥇 Live Gold & Silver Prices")
    st.markdown("<p style='font-size:14px; opacity:0.8;'>💡 Fetches 100% Free Live Global Market Prices. Indian retail market price (with 6% import duty & 3% GST) is approx 9% higher.</p>", unsafe_allow_html=True)
    
    if st.button("Fetch Live Rates 🥇", use_container_width=True):
        try:
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
            
            res_html = f"""<div class="result-box">
<h4 style="color:#fff; margin-bottom:5px;">🥇 Gold (10 Grams)</h4>
<div style="font-size: 20px; color:#ddd; margin-bottom: 5px;">Global Base Rate (24K): ₹{int(gold_10g_base):,}</div>
<div style="font-size: 16px; color:{gold_color}; margin-bottom: 15px; font-weight: bold;">
{gold_symbol} {gold_sign}₹{int(gold_diff):,} (vs Yesterday)
</div>
<div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 15px;">
<b style="color: #ffd700;">24K (99.9% Purity):</b> ₹{int(gold_10g_24k):,} <br>
<b style="color: #e6c200;">22K (91.6% Purity):</b> ₹{int(gold_10g_22k):,} <br>
<b style="color: #ccac00;">18K (75.0% Purity):</b> ₹{int(gold_10g_18k):,}
</div>
<hr style="opacity: 0.2; margin: 15px 0;">
<h4 style="color:#fff; margin-bottom:5px;">🥈 Silver (1 KG)</h4>
<div style="font-size: 20px; color:#ddd; margin-bottom: 5px;">Global Base Rate: ₹{int(silver_1kg_base):,}</div>
<div style="font-size: 16px; color:{silver_color}; margin-bottom: 15px; font-weight: bold;">
{silver_symbol} {silver_sign}₹{int(silver_diff):,} (vs Yesterday)
</div>
<div style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 15px;">
<b>Indian Retail Market:</b> ₹{int(silver_1kg_tax):,}
</div>
<div class="result-sub">Prices include approx 9% duty/GST | 1 USD = ₹{usd_inr:.2f}</div>
</div>"""
            st.markdown(res_html, unsafe_allow_html=True)
        except Exception as e:
            st.error("Error fetching live rates. Please check your internet connection.")

# ==========================================
# TAB 7: More Tools (Dropdown List)
# ==========================================
with tab7:
    st.subheader("More Useful Calculators")
    extra_tool = st.selectbox("Select another calculator:", [
        "🧾 GST (Tax) Calculator", 
        "🛍️ Discount Calculator",
        "🏦 Fixed Deposit (FD)",
        "➗ Percentage Calculator",
        "📈 Compound Interest",
        "🏋️ BMI Calculator"
    ])
    
    st.markdown("---")
    
    if extra_tool == "🧾 GST (Tax) Calculator":
        st.markdown("<p style='font-size:14px; opacity:0.8; margin-top:-15px;'>💡 Tip: Examples are provided next to the rates to help you choose.</p>", unsafe_allow_html=True)
        
        gst_rates_info = {
            "5% (Spices, Sugar, Tea, Footwear < ₹500)": 5,
            "12% (Mobiles, Butter, Cheese, Apparel < ₹1000)": 12,
            "18% (Hair Oil, Soap, Computers, Telecom)": 18,
            "28% (Cars, ACs, Fridges, Luxury Items)": 28
        }
        
        col1, col2 = st.columns([1, 1])
        with col1:
            base_amount = st.number_input("Base Amount (₹)", min_value=1.0, value=1000.0, step=100.0)
            gst_type = st.radio("Action:", ["Add GST (+)", "Remove GST (-)"], horizontal=True)
        with col2:
            gst_selection = st.selectbox("Select GST Slab", list(gst_rates_info.keys()), index=2)
            gst_rate = gst_rates_info[gst_selection]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Calculate GST 🧾", use_container_width=True):
            if "Add" in gst_type:
                gst_amount = base_amount * (gst_rate / 100)
                total_amount = base_amount + gst_amount
                res_html = f"""
<div class="result-box">
Total Amount (with GST): ₹{total_amount:,.2f}
<div class="result-sub">Base: ₹{base_amount:,.2f} | GST: ₹{gst_amount:,.2f}</div>
</div>
                """
            else:
                gst_amount = base_amount - (base_amount * (100 / (100 + gst_rate)))
                original_price = base_amount - gst_amount
                res_html = f"""
<div class="result-box">
Original Price (without GST): ₹{original_price:,.2f}
<div class="result-sub">Total: ₹{base_amount:,.2f} | GST: ₹{gst_amount:,.2f}</div>
</div>
                """
            st.markdown(res_html, unsafe_allow_html=True)
            
    elif extra_tool == "🛍️ Discount Calculator":
        col1, col2 = st.columns(2)
        with col1:
            mrp = st.number_input("Original Price (MRP ₹)", min_value=1.0, value=2000.0, step=100.0)
        with col2:
            discount_percent = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
            
        if st.button("Calculate Discount 🛍️", use_container_width=True):
            saved_amount = mrp * (discount_percent / 100)
            final_price = mrp - saved_amount
            
            res_html = f"""
<div class="result-box">
Price After Discount: ₹{final_price:,.2f}
<div class="result-sub">You Save: ₹{saved_amount:,.2f}</div>
</div>
            """
            st.markdown(res_html, unsafe_allow_html=True)
            
    elif extra_tool == "🏦 Fixed Deposit (FD)":
        col1, col2, col3 = st.columns(3)
        with col1:
            fd_principal = st.number_input("Deposit Amount (₹)", min_value=1000, value=100000, step=10000)
        with col2:
            fd_rate = st.number_input("Interest Rate (%)", min_value=1.0, value=7.0, step=0.1)
        with col3:
            fd_years = st.number_input("Time (Years)", min_value=1, value=5, step=1)
            
        if st.button("Calculate FD 🏦", use_container_width=True):
            # FD is typically compounded quarterly in India
            n = 4 
            maturity_amount = fd_principal * ((1 + (fd_rate/100)/n) ** (n*fd_years))
            fd_interest = maturity_amount - fd_principal
            
            res_html = f"""
<div class="result-box">
Maturity Amount: ₹{int(maturity_amount):,}
<div class="result-sub">Total Deposit: ₹{int(fd_principal):,} | Interest Earned: ₹{int(fd_interest):,}</div>
</div>
            """
            st.markdown(res_html, unsafe_allow_html=True)
            
    elif extra_tool == "➗ Percentage Calculator":
        perc_type = st.radio("Choose Calculation Type:", ["Find % of a Number", "Find what % one number is of another"])
        
        if "Find % of a Number" in perc_type:
            col1, col2 = st.columns(2)
            with col1:
                p_val = st.number_input("What is this (%)", value=15.0, step=1.0)
            with col2:
                num_val = st.number_input("of this number?", value=5000.0, step=100.0)
            if st.button("Calculate Percentage ➗", use_container_width=True):
                ans = (p_val / 100) * num_val
                st.markdown(f'<div class="result-box">{p_val}% of {num_val} is = {ans:,.2f}</div>', unsafe_allow_html=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                num1 = st.number_input("This number", value=500.0, step=50.0)
            with col2:
                num2 = st.number_input("is what % of this number?", value=2000.0, step=100.0)
            if st.button("Calculate Percentage ➗", use_container_width=True):
                if num2 > 0:
                    ans2 = (num1 / num2) * 100
                    st.markdown(f'<div class="result-box">{num1} is {ans2:,.2f}% of {num2}</div>', unsafe_allow_html=True)
                else:
                    st.error("Number cannot be zero!")
                    
    elif extra_tool == "📈 Compound Interest":
        col1, col2 = st.columns(2)
        with col1:
            ci_principal = st.number_input("Principal Amount (₹)", min_value=1000, value=50000, step=5000)
            ci_years = st.number_input("Time Period (Years)", min_value=1, value=5, step=1)
        with col2:
            ci_rate = st.number_input("Interest Rate (% P.A.)", min_value=1.0, value=10.0, step=0.1)
            comp_freq = st.selectbox("Compounding Frequency", ["Annually", "Semi-Annually", "Quarterly", "Monthly"])
            
        freq_dict = {"Annually": 1, "Semi-Annually": 2, "Quarterly": 4, "Monthly": 12}
        
        if st.button("Calculate Compound Interest 📈", use_container_width=True):
            n = freq_dict[comp_freq]
            ci_amount = ci_principal * ((1 + (ci_rate/100)/n) ** (n*ci_years))
            earned_interest = ci_amount - ci_principal
            
            res_html = f"""
<div class="result-box">
Total Future Value: ₹{int(ci_amount):,}
<div class="result-sub">Principal: ₹{int(ci_principal):,} | Interest Earned: ₹{int(earned_interest):,}</div>
</div>
            """
            st.markdown(res_html, unsafe_allow_html=True)
            
    elif extra_tool == "🏋️ BMI Calculator":
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Your Weight (kg)", min_value=10.0, value=70.0, step=1.0)
        with col2:
            height_cm = st.number_input("Your Height (cm)", min_value=50.0, value=170.0, step=1.0)
            
        if st.button("Calculate BMI 🏋️", use_container_width=True):
            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)
            
            if bmi < 18.5:
                category = "Underweight 📉"
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight ✅"
            elif 25 <= bmi < 29.9:
                category = "Overweight ⚠️"
            else:
                category = "Obese ❌"
                
            res_html = f"""
<div class="result-box">
Your BMI: {bmi:.1f}
<div class="result-sub">Status: {category}</div>
</div>
            """
            st.markdown(res_html, unsafe_allow_html=True)

# --- SEO Section ---
st.markdown("<br><hr style='opacity:0.2;'>", unsafe_allow_html=True)
with st.expander("ℹ️ About All-in-One Online Calculator"):
    st.markdown("""
    Welcome to the ultimate **All-in-One Calculator**! Designed for speed, accuracy, and ease of use without needing to download any app.
    
    **🌟 Facilities Available:**
    
    * 🧮 **Basic & 🧪 Scientific Math:** Physical button layout for instant, complex calculations.
    * 💰 **Finance & Investment:** Plan your future perfectly with our EMI, SIP, Fixed Deposit (FD), and Compound Interest calculators.
    * 🥇 **Live Global Markets:** Get 100% Free, real-time Gold & Silver prices (24K, 22K, 18K) and live Currency Exchange rates.
    * 🧾 **Tax & Shopping:** Calculate exact GST (with item examples) and Shopping Discounts in seconds.
    * 🏋️ **Health & Personal:** Track your health with the BMI calculator and find exact Age in years, months, and days.
    
    ---
    *✅ No Ads | ✅ No Login | ✅ 100% Free*
    
    <div style='font-size: 10px; color: transparent; margin-top: 15px; line-height: 1.2;'>
    <b>Search Tags:</b> SIP calculator, EMI calculator, Mutual fund SIP calculator, Home loan EMI calculator, Car loan EMI calculator, FD calculator, Fixed deposit interest calculator, Compound interest calculator, Interest rate calculator, Personal loan EMI calculator, Live gold price today, 24k gold price live, 22k gold price today, Silver price live, Currency converter, USD to INR live, Live exchange rate, Dollar to Rupee converter, Real-time currency exchange, Gold rate calculator, GST calculator, Online GST calculator, Discount calculator, Percentage calculator, Tax calculator India, Find percentage of a number, Calculate discount percentage, Shopping discount calculator, Reverse GST calculator, Price after GST, Online calculator, Scientific calculator online, Free online calculator, All in one calculator, Best online calculator, Math calculator, Basic calculator, Multi-purpose calculator, Web calculator, BMI calculator, Body mass index calculator, Age calculator, Exact age calculator, Age calculator by date of birth, Date of birth calculator, Ideal weight calculator, Health calculator, Age difference calculator, Calculate age in days, Live currency converter, Live USD to INR, Live Gold and Silver calculator, Today live gold rate, Real-time currency rates live, Live EMI checking, Live online calculator, Free live tools, Indian market live rates, Live dollar price, Live exchange rates.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #888; font-size:14px; margin-top:10px;'>Made with ❤️ for everyday use.</div>", unsafe_allow_html=True)




