@echo off
REM ============================
REM Activar entorno
REM ============================
call venv\Scripts\activate.bat

REM ============================
REM Establecer PYTHONPATH
REM ============================
set PYTHONPATH=%CD%

REM ============================
REM Ejecutar pruebas automatizadas
REM ============================
pytest tests
