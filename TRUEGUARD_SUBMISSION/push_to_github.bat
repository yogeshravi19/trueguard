@echo off
title Push TRUEGUARD to GitHub
echo =========================================================================
echo   Pushing to GitHub: https://github.com/yogeshravi19/TRUEGUARD_SUBMISSION
echo =========================================================================
echo.
git push -u origin main --force
echo.
if %errorlevel% equ 0 (
    echo [SUCCESS] Successfully pushed TRUEGUARD_SUBMISSION to GitHub!
) else (
    echo [ERROR] Push failed. Please check your GitHub credentials or Internet connection.
)
echo.
pause
