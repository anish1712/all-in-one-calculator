import sys

content = open('app.py', encoding='utf-8').read()
content = content.replace('</div>\n    """)', '</div>\n    """, unsafe_allow_html=True)')
content = content.replace('color: #aaa', 'color: transparent')
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
