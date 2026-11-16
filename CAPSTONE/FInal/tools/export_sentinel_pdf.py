import subprocess
from pathlib import Path

pptx_path = Path("TRUEGUARD_NEURAL_SENTINEL_FINAL.pptx").resolve()
pdf_path = Path("TRUEGUARD_NEURAL_SENTINEL_FINAL.pdf").resolve()
ps1_path = Path("export_sentinel_script.ps1").resolve()

ps_content = """$ErrorActionPreference = 'Stop'
$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pres = $ppt.Presentations.Open('__PPTX__')
    $pres.SaveAs('__PDF__', 32)
    $pres.Close()
    Write-Host 'Exported successfully to __PDF__'
} finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
""".replace("__PPTX__", str(pptx_path)).replace("__PDF__", str(pdf_path))

ps1_path.write_text(ps_content, encoding="utf-8")
res = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1_path)], capture_output=True, text=True)
print("Returncode:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)

if ps1_path.exists():
    ps1_path.unlink()

if res.returncode == 0:
    print("PDF export successful!")
    # Copy to FINAL_SUBMISSION and CAPSTONE
    for d in [Path("FINAL_SUBMISSION"), Path("CAPSTONE")]:
        d.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(pdf_path, d / "TRUEGUARD_NEURAL_SENTINEL_FINAL.pdf")
    print("Copied PDF to FINAL_SUBMISSION and CAPSTONE.")
else:
    print("PDF export failed!")

