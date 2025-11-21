@echo off
REM ============================
REM Crear carpeta release y copiar el ejecutable
REM ============================
mkdir release
copy dist\main.exe release\Aerotrip.exe

echo Despliegue completado en la carpeta release
