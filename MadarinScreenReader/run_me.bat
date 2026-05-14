@echo off
echo Initializing Mandarin Translator...
start "" "TranslationEye.exe"
timeout /t 2
python brain.py
pause