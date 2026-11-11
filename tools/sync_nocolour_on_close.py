import shutil
import time
import os
import sys

src = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour_ready_to_replace.docx"
dst = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour.docx"

# Wait up to 30 minutes (900 checks x 2 seconds)
for _ in range(900):
    try:
        if not os.path.exists(src):
            print("Source file no longer exists. Done.")
            sys.exit(0)
        with open(dst, "a"):
            pass
        # Unlocked!
        shutil.copy2(src, dst)
        print("SUCCESSFULLY OVERWROTE Toward Trustworthy Large Language Models_nocolour.docx!")
        if os.path.exists(src):
            os.remove(src)
        sys.exit(0)
    except PermissionError:
        time.sleep(2)

print("Timeout after 30 minutes waiting for Word to close.")
