import docx

tmpl = docx.Document('MIA-Project Template.docx')
print('=== Sections in Template ===')
for idx, sec in enumerate(tmpl.sections):
    print(f'Section {idx}: page_width={sec.page_width.inches:.2f}\", page_height={sec.page_height.inches:.2f}\", top={sec.top_margin.inches:.2f}\", bottom={sec.bottom_margin.inches:.2f}\", left={sec.left_margin.inches:.2f}\", right={sec.right_margin.inches:.2f}\"')

print('\n=== First 60 Paragraphs of Template ===')
for idx, p in enumerate(tmpl.paragraphs[:60]):
    if p.text.strip():
        print(f'{idx:2d}: [{p.style.name}] {p.text.strip()[:100]}')

print('\n=== Template Styles & Fonts ===')
for s in tmpl.styles:
    if s.type == docx.enum.style.WD_STYLE_TYPE.PARAGRAPH:
        font_name = s.font.name if s.font else None
        font_size = s.font.size.pt if s.font and s.font.size else None
        if s.name in ['Normal', 'Heading 1', 'Heading 2', 'Heading 3', 'Title', 'Subtitle', 'Body Text']:
            print(f'Style: {s.name}, Font: {font_name}, Size: {font_size}')

