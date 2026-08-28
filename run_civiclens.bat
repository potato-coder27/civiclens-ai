@echo off
setlocal
cd /d "%~dp0"

echo Starting CivicLens AI...
echo.
echo Local URL: http://localhost:8501
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do for /f "tokens=*" %%B in ("%%A") do echo Wi-Fi URL: http://%%B:8501
echo.
echo Open the Wi-Fi URL on any device connected to the same network.
echo Press Ctrl+C in this window to stop the app.
echo.

python -m streamlit run app.py --server.headless false

if errorlevel 1 (
    echo.
    echo CivicLens AI could not start. Make sure Python and the requirements are installed.
    pause
)
endlocal
