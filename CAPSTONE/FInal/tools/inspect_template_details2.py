import docx

tmpl = docx.Document('MIA-Project Template.docx')
for i in range(140, 220):
    if i < len(tmpl.paragraphs):
        p = tmpl.paragraphs[i]
        if p.text.strip():
            print(f"T{i:3d}: [{p.style.name}] {p.text.strip()[:100]}")
