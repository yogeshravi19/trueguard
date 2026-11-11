import docx

doc = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

# Let's inspect the body elements (paragraphs and tables) in document order!
body = doc._body._element
print(f"Total elements in body: {len(body)}")

element_order = []
for child in body:
    tag = child.tag.split("}")[-1]
    if tag == "p":
        # find paragraph
        for i, p in enumerate(doc.paragraphs):
            if p._p is child:
                text = p.text.strip()
                if text:
                    element_order.append(("p", i, text))
                break
    elif tag == "tbl":
        for i, t in enumerate(doc.tables):
            if t._tbl is child:
                element_order.append(("tbl", i, [c.text.strip() for c in t.rows[0].cells]))
                break

print("\n=== DOCUMENT FLOW AROUND TABLES & FIGURES ===")
for item in element_order:
    if item[0] == "tbl":
        print(f"\n---> [TABLE {item[1]}] Header: {item[2][:3]}")
    elif any(kw in item[2].lower() for kw in ["figure", "fig.", "table 1", "table 2", "table 3", "table 4", "prisma", "expandr", "trustllm"]):
        print(f"P[{item[1]}]: {item[2][:90]}")
