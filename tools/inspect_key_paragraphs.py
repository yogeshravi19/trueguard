import docx

doc = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

target_indices = [15, 33, 92, 96, 120, 137, 162, 177, 188, 189, 190, 198, 200, 201, 202, 208, 227, 228, 230, 231, 232, 236, 241, 244, 245, 264, 265, 267, 269, 273, 295]

for idx in target_indices:
    if idx < len(doc.paragraphs):
        print(f"P[{idx}]: {doc.paragraphs[idx].text}")
