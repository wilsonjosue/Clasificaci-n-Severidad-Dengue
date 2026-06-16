# Proyecto Final IA — Clasificación de Severidad de Dengue (Perú, 2000–2024)

Comparación de algoritmos de Machine Learning para clasificar la severidad clínica del
dengue a partir de datos de vigilancia epidemiológica del MINSA. Trabajo orientado a
**SIMBIG 2026**.

- 📄 Informe / documentación: [INFORME.md](INFORME.md)
- 📊 Fuente: [Datos Abiertos – Vigilancia Epidemiológica de Dengue](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)

## Estructura del repositorio

```
Proyecto-final-IA/
├── README.md                       # Este archivo
├── INFORME.md                      # Informe de investigación (documento de trabajo)
├── requirements.txt                # Dependencias del entorno
├── .gitignore                      # Ignora venv, datos crudos, checkpoints, etc.
├── data/
│   ├── raw/                        # Datos ORIGINALES (NO se suben a git)
│   │   └── datos_abiertos_vigilancia_dengue_2000_2024.csv
│   └── processed/                  # Datos limpios derivados del EDA (.gitkeep)
├── notebooks/
│   ├── 01_EDA_Dengue.ipynb         # EDA (antes Avance1_EDA_Dengue.ipynb)
│   ├── 02_preprocesamiento.ipynb   # (pendiente Avance 2)
│   ├── 03_modelado.ipynb           # Entrenamiento de los 5 modelos (pendiente)
│   └── 04_evaluacion.ipynb         # Comparación + insights (pendiente)
├── src/                            # Código reutilizable (funciones, no notebooks)
│   ├── data.py                     # Carga y limpieza
│   ├── features.py                 # Ingeniería de variables / encoding
│   ├── models.py                   # Definición de los 5 modelos
│   └── evaluate.py                 # Métricas y gráficos
└── reports/
    └── figures/                    # Gráficos exportados para el paper (.gitkeep)
```

> Los notebooks `02`–`04` aún no existen; se crearán en el Avance 2.
> El notebook `01_EDA_Dengue.ipynb` ya tiene las rutas ajustadas a esta estructura
> (`../data/raw/...` para leer y `../data/processed/...` para guardar el dataset limpio).

## ⚠️ Sobre el dataset (importante para GitHub)

El CSV crudo pesa **~108 MB** y **supera el límite de 100 MB por archivo de GitHub**.
**No lo subas al repositorio.** Opciones:

1. **(Recomendada)** Mantenerlo solo local en `data/raw/` (ya está en `.gitignore`) y
   documentar el enlace de descarga en este README. Cada integrante lo descarga una vez.
2. Usar [Git LFS](https://git-lfs.com/) si necesitan versionarlo.
3. Subir solo el **dataset procesado** (mucho más liviano) si cabe bajo 100 MB.

> Descarga del CSV: ver enlace de la fuente arriba → archivo
> `datos_abiertos_vigilancia_dengue_2000_2024.csv`. Colocarlo en `data/raw/`.

## Puesta en marcha (entorno virtual local)

> El entorno virtual local es **seguro y la práctica recomendada**: aísla las dependencias
> del proyecto y **no se sube a git** (está en `.gitignore`).

```bash
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activarlo
#    Windows (Git Bash):
source .venv/Scripts/activate
#    Windows (PowerShell):
#    .venv\Scripts\Activate.ps1
#    Linux / macOS:
#    source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (opcional) Registrar el kernel para Jupyter
python -m ipykernel install --user --name=dengue-ia
```

## Guía paso a paso en Visual Studio Code (entorno virtual + notebook)

Esta guía conecta el entorno virtual con `notebooks/01_EDA_Dengue.ipynb`.

### A. Preparar VS Code (una sola vez)
1. Instala las extensiones (icono de extensiones, `Ctrl+Shift+X`):
   - **Python** (Microsoft)
   - **Jupyter** (Microsoft)
2. Abre la carpeta del proyecto: `File ▸ Open Folder…` → selecciona `Proyecto-final-IA`.

### B. Crear y activar el entorno virtual
1. Abre la terminal integrada: `Ctrl+ñ` (o `Terminal ▸ New Terminal`).
2. Crea el entorno e instala dependencias:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate      # Git Bash en Windows
   #  PowerShell:  .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. VS Code suele detectar el nuevo `.venv` y preguntar *"We noticed a new virtual
   environment… ¿Seleccionarlo para el workspace?"* → pulsa **Yes**.

### C. Seleccionar el intérprete del proyecto
1. `Ctrl+Shift+P` → escribe **"Python: Select Interpreter"**.
2. Elige el que diga `.venv` (ruta `.\.venv\Scripts\python.exe`). Recomendado **3.11**.

### D. Verificar el dataset
- Confirma que existe `data/raw/datos_abiertos_vigilancia_dengue_2000_2024.csv`.
- Si lo clonaste desde GitHub, el CSV **no viene** (está en `.gitignore`): descárgalo del
  [portal](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)
  y colócalo en `data/raw/`.

### E. Ejecutar el notebook de EDA
1. Abre `notebooks/01_EDA_Dengue.ipynb`.
2. Arriba a la derecha, en **"Select Kernel"**, elige el intérprete `.venv`
   (o el kernel `dengue-ia` si lo registraste).
3. Ejecuta:
   - Celda por celda con `Shift+Enter`, o
   - Todo con el botón **"Run All"** de la barra superior del notebook.
4. Al terminar, se genera `data/processed/dengue_limpio_avance1.csv` (insumo del Avance 2).

### F. Usar el código de `src/` desde un notebook (opcional)
Al inicio del notebook puedes reutilizar las funciones del paquete `src`:
```python
import sys; sys.path.append('../src')
from data import cargar_crudo, normalizar_edad

df = cargar_crudo()          # lee data/raw/ automáticamente
df = normalizar_edad(df)
```

### Solución de problemas
| Síntoma | Causa / Solución |
|---|---|
| `FileNotFoundError` con el CSV | Falta el dataset en `data/raw/` (ver paso D). |
| El kernel no aparece | Reinstala: `pip install ipykernel`; recarga VS Code (`Ctrl+Shift+P ▸ Reload Window`). |
| `ModuleNotFoundError` | El intérprete no es el `.venv` (repite el paso C) o falta `pip install -r requirements.txt`. |
| Activate.ps1 bloqueado (PowerShell) | Ejecuta `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` o usa Git Bash. |

## Flujo de trabajo en equipo (Git)

1. `git clone <url-del-repo>` y crear el `.venv` (no se comparte por git).
2. Cada integrante descarga el CSV crudo a `data/raw/` (ver aviso arriba).
3. Trabajar en **ramas**: `git checkout -b feature/modelado-rf`.
4. Commits pequeños y descriptivos; `git pull --rebase` antes de subir.
5. Abrir **Pull Request** para integrar a `main` (revisión entre compañeros).

### Convención de ramas
- `feature/<tarea>` — nuevas funciones (modelos, EDA, etc.)
- `fix/<tarea>` — correcciones
- `docs/<tarea>` — documentación / informe

> 💡 Los notebooks generan mucho *diff* por las salidas. Recomendado: **limpiar las salidas
> antes de commitear** (Jupyter → *Clear All Outputs*) o usar
> [`nbstripout`](https://github.com/kynan/nbstripout) para evitar conflictos.

## Reparto de tareas sugerido

| Tarea | Responsable |
|---|---|
| EDA y limpieza | |
| Preprocesamiento + manejo de desbalance | |
| Modelos 1–3 (LogReg, RF, XGBoost) | |
| Modelos 4–5 (SVM, MLP) | |
| Evaluación, métricas e insights | |
| Redacción del paper (inglés) | |
