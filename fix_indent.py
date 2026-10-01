with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

inside_res_html = False
for i, line in enumerate(lines):
    if 'res_html = f"""<div class="result-box">' in line:
        inside_res_html = True
        continue
    
    if inside_res_html:
        if '</div>"""' in line or '</div>"""\n' in line or '</div>"""\r\n' in line:
            inside_res_html = False
            continue
        
        # Strip leading whitespace so Streamlit doesn't render it as a code block
        lines[i] = line.lstrip()

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
