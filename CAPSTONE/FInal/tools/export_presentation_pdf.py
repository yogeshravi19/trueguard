import os
import subprocess
from pathlib import Path

pptx_path = Path("FINAL_TRUEGUARD_PRESENTATION.pptx").resolve()
pdf_path = Path("FINAL_TRUEGUARD_PRESENTATION.pdf").resolve()
ps1_path = Path("export_ppt_script.ps1").resolve()

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
else:
    print("PDF export failed!")
