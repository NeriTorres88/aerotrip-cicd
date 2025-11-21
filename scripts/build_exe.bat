@echo off
REM ============================
REM Activar entorno
REM ============================
call venv\Scripts\activate.bat

REM ============================
REM Generar ejecutable .exe incluyendo recursos
REM ============================
pyinstaller --onefile main.py ^
    --add-data "imagenes;imagenes" ^
    --add-data "base_de_datos.db;." ^
    --noconsole
