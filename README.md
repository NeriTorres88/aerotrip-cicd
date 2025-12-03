# 🚀 Aerotrip – Pipeline CI/CD con GitHub Actions

Este repositorio implementa un flujo completo de Integración Continua (CI) y Entrega Continua (CD) para la aplicación **Aerotrip**, cumpliendo con los requisitos de automatización, pruebas, construcción del ejecutable y despliegue mediante GitHub Actions.

---

## ✅ 1. Scripts del flujo de trabajo (pipeline)

El repositorio incluye un pipeline automatizado ubicado en:

.github/workflows/aerotrip-ci.yml

yaml
Copiar código

Este script contiene:
- Instalación del entorno base (Python)
- Instalación de dependencias
- Ejecución de pruebas automatizadas
- Construcción del ejecutable con PyInstaller
- Generación del entorno de liberación
- Subida del artefacto final

---

## ✅ 2. Scripts para la generación del entorno de liberación

El pipeline instala automáticamente todas las dependencias necesarias:

```yaml
pip install -r requirements.txt
pip install pyinstaller pillow pytest tk
Luego genera el ejecutable mediante:

yaml
Copiar código
pyinstaller --onefile main.py --add-data "imagenes;imagenes" --add-data "base_de_datos.db;." --noconsole
El archivo resultante se crea en:

bash
Copiar código
dist/main.exe
✅ 3. Scripts de pruebas en el entorno de liberación
Las pruebas automatizadas se encuentran en:

bash
Copiar código
tests/test_app.py
El pipeline ejecuta:

yaml
Copiar código
pytest tests
Estas pruebas garantizan el correcto funcionamiento de la aplicación antes de generar el ejecutable final.

✅ 4. Scripts para la generación del despliegue
El pipeline genera automáticamente el entorno de despliegue:

yaml
Copiar código
mkdir release
copy dist\main.exe release\Aerotrip.exe
Finalmente, el ejecutable se publica como artefacto descargable mediante:

yaml
Copiar código
uses: actions/upload-artifact@v4
with:
  name: aerotrip-exe
  path: release/Aerotrip.exe
Puedes descargar el .exe desde:

Actions → Artifacts → aerotrip-exe

🏁 Resultado final del pipeline
Cada vez que se hace un push o pull request a la rama main, el pipeline:

Configura el entorno

Instala dependencias

Corre pruebas unitarias

Construye el ejecutable

Genera la carpeta de liberación

Publica el ejecutable como artefacto

Garantizando un flujo CI/CD profesional, reproducible y confiable.
