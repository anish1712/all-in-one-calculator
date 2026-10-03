import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

# 1. Replace the tab initialization
old_tabs_regex = r'tab5, tab6, tab1, tab2, tab3, tab8, tab4, tab7 = st\.tabs\(\[.*?\]\)'

new_tabs = """tab5, tab6, tab1, tab2, tab9, tab3, tab8, tab4, tab10, tab7 = st.tabs([
    "🧮 Basic", 
    "🔬 Scientific", 
    "🏦 EMI", 
    "📈 SIP",
    "💼 Salary",
    "💱 Currency", 
    "🥇 Gold",
    "📅 Age", 
    "❤️ Love",
    "➕ More"
])"""

content = re.sub(old_tabs_regex, new_tabs, content, flags=re.DOTALL)

# 2. Add tab9 and tab10 content before # --- SEO Section ---
new_tab_content = """

# ==========================================
# TAB 9: Salary / PF Calculator
# ==========================================
with tab9:
    st.subheader("💼 Salary / PF / In-Hand Calculator")
    st.markdown("<p style='font-size:14px; opacity:0.8;'>Calculate your exact In-Hand Salary after PF and Tax deductions.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        basic_salary = st.number_input("Monthly Basic Salary (₹)", min_value=0.0, value=25000.0, step=1000.0)
        hra = st.number_input("Monthly HRA & Allowances (₹)", min_value=0.0, value=10000.0, step=1000.0)
    with col2:
        pf_percent = st.number_input("Employee PF Deduction (%)", min_value=0.0, max_value=100.0, value=12.0)
        ptax = st.number_input("Professional Tax (₹)", min_value=0.0, value=200.0, step=50.0)
    
    if st.button("Calculate In-Hand Salary", use_container_width=True):
        gross_salary = basic_salary + hra
        pf_amount = (basic_salary * pf_percent) / 100
        total_deduction = pf_amount + ptax
        in_hand = gross_salary - total_deduction
        
        res_html = f\"\"\"<div class="result-box">
<h4 style="color:#fff; margin-bottom:5px;">💰 In-Hand Salary</h4>
<div style="font-size: 32px; font-weight: bold; color:#38ef7d; margin-bottom: 10px;">₹{int(in_hand):,} <span style="font-size: 16px; color:#aaa;">/ month</span></div>
<div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 15px; font-size: 16px;">
    <b>Gross Salary:</b> ₹{int(gross_salary):,} <br>
    <b style="color: #ff416c;">Total Deductions:</b> ₹{int(total_deduction):,} <br>
    <i>(PF: ₹{int(pf_amount):,} | Tax: ₹{int(ptax):,})</i>
</div>
</div>\"\"\"
        st.markdown(res_html, unsafe_allow_html=True)

# ==========================================
# TAB 10: Love Calculator
# ==========================================
with tab10:
    st.subheader("❤️ Love Calculator (Fun Tool)")
    st.markdown("<p style='font-size:14px; opacity:0.8;'>Check compatibility with your crush! (This is just a fun viral tool, share it with friends! 😄)</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name1 = st.text_input("👦 Your Name")
    with col2:
        name2 = st.text_input("👧 Crush's Name")
    
    if st.button("Calculate Love ❤️", use_container_width=True):
        if name1 and name2:
            import hashlib
            # Create a consistent hash based on both names so it's always same for same names
            combined = ''.join(sorted([name1.lower().strip(), name2.lower().strip()]))
            hash_val = int(hashlib.md5(combined.encode()).hexdigest(), 16)
            percentage = (hash_val % 51) + 50  # Always between 50 and 100 to keep it positive/fun!
            
            if percentage >= 90:
                msg = "Wow! Made for each other! 👩‍❤️‍👨"
                color = "#ff4b2b"
            elif percentage >= 75:
                msg = "Strong Connection! 💖"
                color = "#ff416c"
            else:
                msg = "Good Friends! 💕"
                color = "#ff758c"
                
            res_html = f\"\"\"<div class="result-box" style="text-align: center;">
<h3 style="color:#fff; margin-bottom:5px;">{name1} + {name2}</h3>
<div style="font-size: 48px; font-weight: bold; color:{color}; margin: 15px 0;">{percentage}%</div>
<div style="font-size: 20px; color:#ddd;">{msg}</div>
</div>\"\"\"
            st.markdown(res_html, unsafe_allow_html=True)
            st.success("Share this screenshot with your friends! 😂📱")
        else:
            st.warning("Please enter both names first!")

# --- SEO Section ---
"""

content = content.replace('# --- SEO Section ---', new_tab_content)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
