import zipfile
import os

docx_path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"
out_dir = r"E:\trueguard\tools\extracted_media"
os.makedirs(out_dir, exist_ok=True)

with zipfile.ZipFile(docx_path, 'r') as z:
    for name in z.namelist():
        if name.startswith("word/media/"):
            out_path = os.path.join(out_dir, os.path.basename(name))
            with open(out_path, "wb") as f:
                f.write(z.read(name))
            print(f"Extracted {name} -> {out_path} ({os.path.getsize(out_path)} bytes)")
