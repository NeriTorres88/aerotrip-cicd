@echo off
REM ============================
REM Crear entorno virtual
REM ============================
python -m venv venv
call venv\Scripts\activate.bat

REM ============================
REM Instalar dependencias
REM ============================
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller pytest pillow tk
