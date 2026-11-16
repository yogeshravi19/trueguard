$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Host "Opening E:\trueguard\FINAL_REPORT_PRINT_READY.docx in Word COM..."
    $doc = $word.Documents.Open('E:\trueguard\FINAL_REPORT_PRINT_READY.docx')
    $pdfPath = 'E:\trueguard\FINAL_REPORT_PRINT_READY.pdf'
    Write-Host "Exporting to $pdfPath..."
    # 17 is wdExportFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]$false)
    Write-Host "PDF export successful!"
    Copy-Item -Path $pdfPath -Destination 'E:\trueguard\FINAL_SUBMISSION\FINAL_REPORT_PRINT_READY.pdf' -Force
    Write-Host "Copied to FINAL_SUBMISSION\FINAL_REPORT_PRINT_READY.pdf"
} catch {
    Write-Error $_
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
