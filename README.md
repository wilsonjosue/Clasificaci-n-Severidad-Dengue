# Proyecto Final IA — Predicción semanal de casos de Dengue (Perú, 2000–2024)

Predicción del **número de casos de dengue por semana** (regresión / serie temporal) a partir de
los datos de vigilancia epidemiológica del MINSA, como base para un **sistema de alerta temprana**.
Se evaluaron los tres tipos de problema (clasificación, regresión, clustering) y las métricas
mostraron que el dataset es adecuado para **regresión**. Trabajo orientado a **SIMBIG 2026**.

- 📄 Informe (español): [INFORME.md](INFORME.md)
- 📝 Paper (inglés, borrador): [PAPER.md](PAPER.md)
- 🗺️ Plan de trabajo: [Avance/PlanGeneral.md](Avance/PlanGeneral.md)
- 📊 Fuente: [Datos Abiertos – Vigilancia Epidemiológica de Dengue](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)

## Resultados principales

Se agregó el dataset (1,029,421 registros) a una **serie semanal** de casos (1,305 puntos,
2000–2024) y se comparó la predicción a **1 semana** (ventana de entrada `W=3`, horizonte `H=1`):

| Modelo | R² | RMSE |
|---|---|---|
| **Ridge (mejor)** | **0.975** | 671 |
| Lasso | 0.975 | 671 |
| Perceptrón (MLP) | 0.972 | 708 |
| LSTM | 0.560 | 2817 |
| Random Forest | 0.444 | 3167 |
| Gradient Boosting | 0.374 | 3359 |

*Baseline ingenuo (persistencia): R² 0.959.* Los modelos lineales regularizados ganan y superan
al baseline. La **clasificación** (F1-macro 0.33) y el **clustering** (Silhouette 0.35) resultaron
inadecuados → **regresión es el único abordaje válido** para este dataset.

## Estructura del repositorio

```
Proyecto-final-IA/
├── README.md                       # Este archivo
├── INFORME.md                      # Informe de investigación (español)
├── PAPER.md                        # Paper para SIMBIG (inglés, borrador)
├── requirements.txt                # Dependencias del entorno
├── .gitignore                      # Ignora venv, datos crudos, checkpoints, etc.
├── Avance/
│   ├── PlanGeneral.md              # Plan de trabajo vigente (por fases)
│   ├── contexto.md                 # Enunciado + observaciones del profesor
│   └── avances.md                  # Plan anterior (obsoleto, enfoque viejo)
├── data/
│   ├── raw/                        # Datos ORIGINALES (NO se suben a git)
│   │   └── datos_abiertos_vigilancia_dengue_2000_2024.csv
│   └── processed/                  # Dataset limpio derivado del EDA (.gitkeep)
├── notebooks/
│   ├── 01_EDA_Dengue.ipynb         # EDA general
│   ├── 02_Clasificacion.ipynb      # Experimento secundario: clasificación de severidad
│   ├── 03_Regresion.ipynb          # ★ Abordaje principal: serie temporal (6 técnicas + LSTM)
│   └── 04_Clustering.ipynb         # Experimento secundario: clustering de departamentos
├── src/                            # Código reutilizable (funciones, no notebooks)
│   ├── data.py                     # Carga y limpieza
│   ├── features.py                 # Ingeniería de variables / encoding
│   ├── models.py                   # Definición de modelos
│   └── evaluate.py                 # Métricas y gráficos
├── Ejemplos/                       # Notebooks de referencia del profesor
└── reports/
    └── figures/                    # Gráficos exportados para el paper (.gitkeep)
```

> **Notebook principal:** `03_Regresion.ipynb`. Los notebooks `02` y `04` son experimentos
> comparativos que justifican la elección de la regresión. Todos leen de `data/raw/` y están
> conectados al kernel `dengue-ia`.

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

# 3. Instalar dependencias (incluye TensorFlow para el LSTM; descarga pesada)
pip install -r requirements.txt

# 4. (opcional) Registrar el kernel para Jupyter
python -m ipykernel install --user --name=dengue-ia
```

> Probado con **Python 3.12**. Si `pip` falla por certificados SSL, añade:
> `--trusted-host pypi.org --trusted-host files.pythonhosted.org`.

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
2. Elige el que diga `.venv` (ruta `.\.venv\Scripts\python.exe`). Probado con **Python 3.12**.

### D. Verificar el dataset
- Confirma que existe `data/raw/datos_abiertos_vigilancia_dengue_2000_2024.csv`.
- Si lo clonaste desde GitHub, el CSV **no viene** (está en `.gitignore`): descárgalo del
  [portal](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)
  y colócalo en `data/raw/`.

### E. Ejecutar los notebooks
1. Abre el notebook deseado. **El principal es `notebooks/03_Regresion.ipynb`**; `02` y `04`
   son los experimentos comparativos y `01` es el EDA general.
2. Arriba a la derecha, en **"Select Kernel"**, elige **Python (dengue-ia)** (o el `.venv`).
3. Ejecuta con **"Run All"** (o celda por celda con `Shift+Enter`).
4. Todos los notebooks leen el dataset desde `data/raw/` automáticamente.

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
| EDA general y de serie temporal | |
| Regresión: ventanas (W, H) + modelos lineales y árboles | |
| Regresión: LSTM y comparación de técnicas | |
| Experimentos comparativos (clasificación + clustering) | |
| Estado del arte y citas bibliográficas | |
| Redacción/traducción del paper (inglés, plantilla SIMBIG) | |
