# aerotrip-cicd

# Aerotrip - Aplicación de Reservas de Vuelos

Aerotrip es una aplicación de escritorio para reservar vuelos, gestionando destinos, usuarios y pagos. Incluye integración con base de datos SQLite y soporte para ejecución de pruebas automatizadas. También cuenta con scripts para generación del ejecutable `.exe` y despliegue automatizado mediante GitHub Actions.

---

## Contenido del repositorio

```
APP_AEROTRIP_NEW/
│
├─ main.py                    # Script principal de la aplicación
├─ pantallas.py                # Módulos de interfaz (Tkinter)
├─ base_de_datos.db            # Base de datos SQLite
├─ imagenes/                   # Recursos de imágenes
├─ requirements.txt            # Dependencias Python
├─ tests/                      # Pruebas automatizadas con pytest
│   └─ test_app.py
├─ scripts/                    # Scripts para pipeline y despliegue
│   ├─ setup_entorno.bat
│   ├─ run_tests.bat
│   ├─ build_exe.bat
│   └─ deploy.bat
└─ .github/workflows/          # Configuración de CI/CD
    └─ ci_cd.yml
```

---

## Requisitos

* Windows 10/11
* Python 3.13
* Dependencias del proyecto (se instalan con `requirements.txt`):

  * `pytest`
  * `pillow`
  * `tk`
  * `pyinstaller`

---

## Instalación y configuración del entorno

1. Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/Aerotrip.git
cd Aerotrip
```

2. Crear y activar el entorno virtual, e instalar dependencias:

```bat
scripts\setup_entorno.bat
```

---

## Ejecución de la aplicación

Dentro del entorno virtual:

```bat
call venv\Scripts\activate.bat
python main.py
```

---

## Ejecución de pruebas automatizadas

Para correr los tests:

```bat
scripts\run_tests.bat
```

Se ejecutarán todos los archivos de pruebas dentro de la carpeta `tests/` usando `pytest`.

---

## Generación del ejecutable (.exe)

Para crear el ejecutable independiente con PyInstaller:

```bat
scripts\build_exe.bat
```

* El ejecutable se generará en la carpeta `dist/`.
* Todos los recursos (imágenes y base de datos) se empaquetan automáticamente.

---

## Despliegue

Para generar un despliegue local del ejecutable:

```bat
scripts\deploy.bat
```

* Esto copiará el `.exe` a la carpeta `release/` para distribución.

---

## CI/CD con GitHub Actions

Se ha configurado un pipeline de GitHub Actions que realiza:

1. Instalación del entorno y dependencias.
2. Ejecución de pruebas automatizadas.
3. Generación del ejecutable `.exe`.
4. Copia del `.exe` a la carpeta `release/`.
5. Subida del ejecutable como artefacto de la acción.

Archivo de workflow: `.github/workflows/ci_cd.yml`

---

## Flujo de Trabajo (Pipeline)

1. **Desarrollo**: Implementación de nuevas funcionalidades y corrección de errores.
2. **Pruebas**: Ejecución de pruebas unitarias automatizadas (`pytest`).
3. **Build/Compilación**: Generación del `.exe` con PyInstaller.
4. **Despliegue**: Copia de archivos al entorno de liberación y distribución.
5. **Entrega/Producción**: Disponibilidad del ejecutable para los usuarios finales.

---

## Niveles de Servicio (SLA)

* Disponibilidad de la aplicación: 99%
* Tiempo máximo de ejecución de pruebas: < 1 minuto
* Tiempo de generación del ejecutable: < 2 minutos

---

## Métricas para Monitoreo

* Número de reservas realizadas
* Tiempo de ejecución de la aplicación
* Errores en la base de datos
* Logs de fallos durante la generación del ejecutable
* Estado de las pruebas unitarias

---

## Parámetros de Configuración de Herramientas

* **PyInstaller**:

  ```bash
  pyinstaller --onefile --add-data "imagenes;imagenes" main.py
  ```
* **pytest**:

  ```bash
  pytest tests/
  ```
* Variables de entorno necesarias:

  ```text
  PYTHONPATH=.
  ```

---

## Uso del artefacto generado

* Una vez finalizado el workflow en GitHub Actions, el archivo `Aerotrip.exe` estará disponible para descargar desde los **artefactos** del pipeline.
* Se puede ejecutar directamente en Windows sin necesidad de Python instalado.

---

## Notas adicionales

* Las imágenes se encuentran en la carpeta `imagenes/` y deben estar accesibles al ejecutar el `.exe`.
* La base de datos SQLite se encuentra en `base_de_datos.db` y se empaqueta dentro del ejecutable.

---

## Autor

* Neri Torres
