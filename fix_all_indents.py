with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

inside_res_html = False
for i, line in enumerate(lines):
    if 'res_html = f"""' in line:
        inside_res_html = True
        continue
    
    if inside_res_html:
        if '"""' in line and not 'res_html' in line:
            inside_res_html = False
            continue
        
        # Only left-strip lines that have content
        if line.strip():
            lines[i] = line.lstrip()

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
