@echo off
REM Build the executable using pyinstaller
pyinstaller --onefile script.py

REM Rename the .exe file
rename dist\script.exe script.exe

REM Create "Youtube video downloader" directory if it doesn't exist
if not exist "Youtube video downloader" mkdir "Youtube video downloader"

REM Move the script.exe file to the "Youtube video downloader" directory
move dist\script.exe "Youtube video downloader"

REM Cleanup
rmdir /s /q build
rmdir /s /q dist
del script.spec

echo Build creation complete!
pause