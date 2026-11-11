import shutil
import time
import os
import sys

src = r"E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004_bright_yellow.docx"
dst = r"E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx"

for _ in range(600):
    try:
        with open(dst, "a"):
            pass
        shutil.copy2(src, dst)
        print("SUCCESSFULLY SYNCED Response_to_Reviewers_269790004.docx!")
        sys.exit(0)
    except PermissionError:
        time.sleep(2)

print("Timeout waiting for Word to close.")
