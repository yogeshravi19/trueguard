import zipfile
from PIL import Image
import io

docx_path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"

with zipfile.ZipFile(docx_path, 'r') as z:
    for i in range(1, 12):
        name = f"word/media/image{i}.png"
        if name not in z.namelist():
            name = f"word/media/image{i}.tiff"
            
        data = z.read(name)
        img = Image.open(io.BytesIO(data))
        print(f"Image {i} ({name}): size={img.size}, format={img.format}, bytes={len(data)}")
