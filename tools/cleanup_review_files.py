"""
Post-Review Workspace Cleanup Script:
Safely removes university review reports, PPT presentations, and viva notes.
STRICTLY PROTECTS humanised.docx, IEEE LaTeX files, Colab notebooks, and research results.
"""
from pathlib import Path
import os
import shutil

ROOT = Path(r"E:\trueguard")

# Explicit list of files to remove in ROOT directory
FILES_TO_REMOVE_ROOT = [
    # PPTX and Presentation PDFs
    "TRUEGUARD_NEURAL_SENTINEL_FINAL.pptx",
    "TRUEGUARD_NEURAL_SENTINEL_FINAL.pdf",
    "FINAL_TRUEGUARD_PRESENTATION.pptx",
    "FINAL_TRUEGUARD_PRESENTATION.pdf",
    "FINAL_PRESENTATION.pptx",
    "FINAL_PRESENTATION.pdf",
    "Review2.pptx",
    "TRUEGUARD_Review2.pptx",
    "TRUEGUARD_Final_Review.pptx",
    "PRESENTATION_SOURCE_VERIFICATION.md",

    # University Reports (DOCX and PDF)
    "FINAL_REPORT_PRINT_READY.docx",
    "FINAL_REPORT_PRINT_READY.pdf",
    "FINAL_REPORT_PRINT_READY_PRE_POLISH_BACKUP.docx",
    "FINAL_REPORT_VERIFIED.docx",
    "FINAL_REPORT_VERIFIED.pdf",
    "FINAL_REPORT_VERIFIED_BACKUP.docx",
    "FINAL_REPORT.docx",
    "FINAL_REPORT.pdf",
    "FINAL_REPORT_NO_IMAGES.docx",
    "FINAL_REPORT_NO_IMAGES.pdf",
    "FINAL_REPORT_OPTIMIZED.docx",
    "FINAL_REPORT_OPTIMIZED.pdf",
    "Final_Project_Report.docx",
    "TRUEGUARD_BEST_FINAL_Report.docx",
    "TRUEGUARD_Final_MTech_Report_Cleaned.docx",
    "TRUEGUARD_Final_MTech_Report_Expanded.docx",
    "TRUEGUARD_Final_MTech_Report_Fixed.docx",
    "TRUEGUARD_Final_Project_Report_MIA.docx",
    "TRUEGUARD_Final_Project_Report_V2.docx",
    "REVIEWED_FINAL-1.docx",
    "Review 2 Important Instructions V1.docx",
    "Review 2 Important Instructions V1 (1).docx",
    "MIA-Project Template.docx",
    "friend report.pdf",
    "New Microsoft Word Document.docx",
    "template_extracted.txt",
    "TRUEGUARD_FINAL_VERIFICATION.md",

    # Viva and Prompt Notes
    "VIVA_QA.md",
    "TRUEGUARD_VIVA_NOTES.md",
    "TRUEGUARD_ZenSpark_Prompt.md",
    "TRUEGUARD_GammaAI_Prompt.md",
    "EXPERIMENTAL_VERIFICATION_GUIDE.docx",
    "EXPERIMENTAL_VERIFICATION_GUIDE.md",
    "CHAT_RESTORE_STATE.md",

    # Temporary assembly scripts in root
    "merge_final_report.py",
    "export_print_ready_pdf.ps1",
]

# Folders in root to remove
DIRS_TO_REMOVE_ROOT = [
    "template_extracted",
]

# Strict protection assertion
PROTECTED_MUST_EXIST = [
    "humanised.docx",
    "humanised.backup.docx",
    "TRUEGUARD_IEEE_FINAL.tex",
    "TRUEGUARD_IEEE.tex",
    "bare_jrnl.tex",
    "CAPSTONE/FInal/TRUEGUARD_Colab_REAL.ipynb",
    "CAPSTONE/FInal/results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/detection_report.json",
    "outputs/figures",
    "foundational_papers",
]

for p in PROTECTED_MUST_EXIST:
    target = ROOT / p
    assert target.exists(), f"CRITICAL SAFETY CHECK FAILED: {target} does not exist!"
print("Safety check passed: All core publication assets are verified and intact.")

# Execute deletion in ROOT
deleted_bytes = 0
deleted_count = 0

for fname in FILES_TO_REMOVE_ROOT:
    fpath = ROOT / fname
    if fpath.exists() and fpath.is_file():
        sz = fpath.stat().st_size
        fpath.unlink()
        deleted_bytes += sz
        deleted_count += 1
        print(f"Deleted file: {fname} ({sz / (1024*1024):.2f} MB)")

# Remove Word temporary ~$ lock files
for lock_file in ROOT.glob("~$*"):
    if lock_file.is_file():
        sz = lock_file.stat().st_size
        lock_file.unlink()
        deleted_bytes += sz
        deleted_count += 1
        print(f"Deleted temp lock file: {lock_file.name}")

# Remove designated root directories
for dname in DIRS_TO_REMOVE_ROOT:
    dpath = ROOT / dname
    if dpath.exists() and dpath.is_dir():
        sz = sum(f.stat().st_size for f in dpath.rglob("*") if f.is_file())
        shutil.rmtree(dpath)
        deleted_bytes += sz
        deleted_count += 1
        print(f"Deleted directory: {dname} ({sz / (1024*1024):.2f} MB)")

# Clean duplicate review items inside FINAL_SUBMISSION
final_sub = ROOT / "FINAL_SUBMISSION"
if final_sub.exists():
    items_to_clean_sub = [
        "FINAL_PRESENTATION.pdf",
        "FINAL_PRESENTATION.pptx",
        "FINAL_TRUEGUARD_PRESENTATION.pdf",
        "FINAL_TRUEGUARD_PRESENTATION.pptx",
        "TRUEGUARD_NEURAL_SENTINEL_FINAL.pdf",
        "TRUEGUARD_NEURAL_SENTINEL_FINAL.pptx",
        "FINAL_REPORT_PRINT_READY.docx",
        "FINAL_REPORT_PRINT_READY.pdf",
        "FINAL_REPORT_PRINT_READY_4K.pdf",
        "FINAL_REPORT_VERIFIED.docx",
        "FINAL_REPORT_VERIFIED.pdf",
        "FINAL_REPORT_VERIFIED_BACKUP.docx",
        "friend report.pdf",
        "PRESENTATION_SOURCE_VERIFICATION.md",
        "TRUEGUARD_FINAL_VERIFICATION.md",
        "TRUEGUARD_VIVA_NOTES.md",
        "VIVA_QA.md",
        "CLAUDE_PPT_KIT",
        "small changes",
    ]
    for sub_item in items_to_clean_sub:
        p = final_sub / sub_item
        if p.exists():
            if p.is_file():
                sz = p.stat().st_size
                p.unlink()
                deleted_bytes += sz
                deleted_count += 1
                print(f"Deleted in FINAL_SUBMISSION: {sub_item} ({sz / (1024*1024):.2f} MB)")
            elif p.is_dir():
                sz = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
                shutil.rmtree(p)
                deleted_bytes += sz
                deleted_count += 1
                print(f"Deleted directory in FINAL_SUBMISSION: {sub_item} ({sz / (1024*1024):.2f} MB)")

print(f"\n=======================================================")
print(f"CLEANUP COMPLETE: Removed {deleted_count} review items.")
print(f"Freed Disk Space: {deleted_bytes / (1024*1024):.2f} MB.")
print(f"=======================================================")
