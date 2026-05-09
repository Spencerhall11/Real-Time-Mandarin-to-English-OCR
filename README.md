# Real-Time-Mandarin-to-English-OCR
Fast system to scan a screen and recognize text, then if it's Mandarin use google translate on it 

uses Zero-Copy with C++ file mapping and python shared memory to move the screen data without constant in/outs
has a translation cache for constants to reduce API calls for consant things
uses DXGI Desktop duplication for hardware accelerated screen capability

reqs:
Windows 10/11
DX11 compatible GPU
VS2019/2022 and Python 3.8+

how to use:
pip install -r requirements.txt
use run_me.bat to start the tool

