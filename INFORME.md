# Informe de Investigación — Trabajo Final de Inteligencia Artificial

> **Documento de trabajo (español).** El *paper* final para **SIMBIG 2026** se redacta en
> inglés siguiendo esta misma estructura (ver sección *Mapeo a SIMBIG* al final).
> **Deadline SIMBIG 2026: 30 de junio de 2026.**

---

## Metadatos Utilizados

| Campo | Valor |
|---|---|
| **Título tentativo** | *Weekly Dengue Case Forecasting in Peru Using Regression and Time-Series Machine Learning Models (2000–2024)* |
| **Tipo de problema** | Regresión / serie temporal (predicción de casos por semana) |
| **Variable objetivo** | `casos` = nº de casos de dengue por semana epidemiológica (conteo agregado) |
| **Enfoque** | Se evaluaron los 3 abordajes (clasificación, regresión, clustering); las métricas mostraron que el dataset es adecuado para **regresión / serie temporal** |
| **Fuente de datos** | [Datos Abiertos – Vigilancia Epidemiológica de Dengue (MINSA/CDC Perú)](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue) |
| **N.º de registros** | ~1,029,421 |
| **Periodo** | 2000–2024 |
| **Autores** | _(nombres del equipo)_ |
| **Curso / Docente** | _(completar)_ |

---

## Resumen (Abstract)

> _150–250 palabras. Redactar al final, cuando estén los resultados._
> Estructura: contexto (dengue como problema de salud pública) → objetivo (predecir el nº de
> casos por semana para alerta temprana) → datos (vigilancia 2000–2024, ~1M registros agregados
> a serie semanal) → métodos (comparación de modelos de regresión con ventanas de tiempo) →
> resultado principal (Ridge/Lineal, R² = 0.976, supera al baseline ingenuo) →
> implicancia (anticipación de brotes y asignación de recursos).

**Palabras clave:** dengue, regresión, serie temporal, predicción de casos, aprendizaje automático, salud pública, Perú.

---

## 1. Introducción

- Contexto del dengue en Perú (transmisión por *Aedes aegypti*, brotes, regiones endémicas: Loreto, Piura, etc.).
- Problema: **anticipar el número de casos** por semana permite la alerta temprana de brotes y la priorización de recursos.
- Brecha: _¿qué falta en los trabajos previos?_ (ver sección 2).
- **Objetivo general:** predecir el número de casos de dengue por semana epidemiológica mediante modelos de regresión / serie temporal.
- **Objetivos específicos:** (1) EDA, (2) agregación a serie temporal y construcción de ventanas, (3) entrenamiento, (4) comparación con métricas (R², RMSE, MAE), (5) generación de *insights*.
- **Nota metodológica:** se evaluaron también clasificación y clustering; las métricas demostraron que el dataset es adecuado para **regresión** (ver Sección 4), justificando este enfoque.
- **Contribución:** comparación reproducible y modelo de alerta temprana sobre un dataset nacional de 25 años.

## 2. Estado del Arte / Trabajos Relacionados

> Objetivo del docente: **buscar el estado del arte**. Llenar esta tabla con ≥ 6–8 referencias.

| Ref. | Año | Datos / país | Técnicas | Métrica reportada | Limitación |
|---|---|---|---|---|---|
| _(autor)_ | | | | | |

- Buscar en: Google Scholar, PubMed, Scopus, arXiv. Términos: *"dengue severity prediction machine learning"*, *"dengue classification surveillance data"*.
- Revisar trabajos previos de SIMBIG (CEUR-WS / Springer) para alinear estilo y baseline.

## 3. Materiales y Métodos

### 3.1 Conjunto de datos

Diccionario de variables (✔ = candidata a *feature*; ✘ = identificador/no válida):

| Variable | Descripción | Tipo | ¿Feature? |
|---|---|---|---|
| `departamento` | Departamento | Categórica | ✔ (agregada) |
| `provincia` | Provincia | Categórica | ✔ (agregada) |
| `distrito` | Distrito | Categórica | ✘ alta cardinalidad |
| `localidad` | Localidad | Texto | ✘ |
| `enfermedad` | Tipo de dengue (severidad) | Categórica | objetivo del experimento secundario (clasificación) |
| `ano` | Año epidemiológico | Numérica | ✔ → base del objetivo principal (`casos`) |
| `semana` | Semana epidemiológica (1–53) | Numérica | ✔ → base del objetivo principal (`casos`) |
| `diagnostic` | Código CIE-10 (A97.x) | Categórica | ✘ (fuga de info: codifica la clase) |
| `diresa` | Dirección regional de salud | Categórica | ✔ |
| `ubigeo` | Código geográfico | ID | ✘ (no válida) |
| `localcod` | Código de localidad | ID | ✘ |
| `edad` | Edad (valor crudo) | Numérica | ✔ (tras normalizar) |
| `tipo_edad` | Unidad de edad (A/M/D) | Categórica | ✔ (para normalizar) |
| `sexo` | Sexo (M/F) | Categórica | ✔ |

> ⚠️ **Cuidado con la fuga de información (*data leakage*):** `diagnostic` (CIE-10) y `enfermedad`
> codifican prácticamente lo mismo que la severidad. **No usar `diagnostic` como feature.**

### 3.2 Preprocesamiento (enfoque principal: regresión / serie temporal)

1. Conversión numérica de `ano` y `semana`; descarte de filas con semana fuera de 1–53.
2. **Agregación a serie temporal:** `GROUP BY (ano, semana)` + `COUNT` → variable objetivo
   `casos` = nº de casos por semana epidemiológica (1,305 puntos continuos, 2000–2024).
3. **Validación del target:** Σ de la serie = nº de registros del CSV (1,029,421) y serie sin
   semanas faltantes → el objetivo es un conteo real, no sintético ni imputado (ver Sección 4.2).
4. **Construcción de ventanas (lags):** para una ventana `w`, se usan los `w` valores previos
   `[t-w, …, t-1]` como *features* para predecir `casos` en `t`.

> *Preprocesamiento de los experimentos secundarios:* para **clasificación** se construyó
> `severidad` ordenada {0,1,2} excluyendo `diagnostic` (leakage), normalizando la edad a años y
> aplicando `class_weight`/SMOTE por el desbalance; para **clustering** se agregó un perfil por
> departamento. Detalle en los notebooks `02` y `04`.

### 3.3 División de datos

- **Split temporal (no aleatorio):** se entrena con el pasado y se evalúa con las últimas
  semanas (≈ último 20 %), preservando el orden del tiempo y evitando *leakage* del futuro.
- ⚠️ En series temporales **no** se usa un split aleatorio ni validación cruzada estándar; si se
  valida en varias ventanas, debe hacerse con *time-series split* (hacia adelante).

### 3.4 Algoritmos comparados (5 técnicas de regresión)

| # | Técnica | Familia | Notas |
|---|---|---|---|
| 1 | Regresión Lineal | Lineal | *Baseline* interpretable; sigue la tendencia |
| 2 | Ridge (L2) | Lineal regularizada | Maneja multicolinealidad de los lags |
| 3 | Lasso (L1) | Lineal regularizada | Selección de variables (lags relevantes) |
| 4 | Random Forest Regressor | Ensamble (bagging) | No extrapola la tendencia (limitación observada) |
| 5 | Gradient Boosting Regressor | Ensamble (boosting) | Potente en patrones no lineales |

> *Trabajo futuro:* comparar con **LSTM**, técnica de referencia para series temporales.
> *Experimentos secundarios:* clasificación (Reg. Logística, Random Forest, XGBoost, LightGBM,
> MLP) y clustering (K-means, jerárquico) — ver Secciones 4.1 y 4.3.

### 3.5 Métricas de evaluación (regresión)

- **R²** (coeficiente de determinación): proporción de varianza explicada (principal).
- **RMSE** (penaliza más los errores grandes) y **MAE** (en las unidades de `casos`).
- **Comparación con baseline ingenuo** (persistencia: `casos[t] = casos[t-1]`): el modelo debe
  superarlo para aportar valor.
- **Selección de la ventana óptima** por método tipo codo (RMSE vs. tamaño de ventana).

> *Métricas de los experimentos secundarios:* clasificación → F1-macro, balanced accuracy,
> recall por clase y matriz de confusión; clustering → Silhouette y Davies-Bouldin.

## 4. Resultados

Se evaluaron los **tres tipos de problema** sobre el mismo dataset, transformándolo según
cada abordaje, y se usaron las métricas propias de cada uno para decidir si el dataset es
**adecuado** para ese tipo de tarea.

> **Nota de reproducibilidad:** la clasificación se entrenó sobre una muestra estratificada de
> 30,000 registros (por costo computacional); regresión y clustering usan el dataset completo
> agregado. Notebooks: `02_Clasificacion.ipynb`, `03_Regresion.ipynb`, `04_Clustering.ipynb`.

### 4.1 Clasificación de severidad — *dataset NO adecuado*

Variable objetivo `severidad` (3 clases), **sin** `diagnostic` (para evitar *leakage*).
Distribución: 88.9 % *Sin signos* / 10.7 % *Con signos* / **0.39 % *Grave***.

| Modelo | Accuracy | Balanced Acc | F1-macro | Recall *Grave* |
|---|---|---|---|---|
| Random Forest | 0.790 | 0.374 | 0.365 | 0.000 |
| LightGBM | 0.698 | 0.411 | 0.364 | 0.034 |
| XGBoost | 0.886 | 0.344 | 0.337 | 0.000 |
| MLP (red neuronal) | 0.887 | 0.342 | 0.333 | 0.000 |
| Regresión Logística (balanceada) | 0.446 | 0.452 | 0.281 | 0.517 |

**Rangos de referencia vs. resultado:**

| Métrica | ❌ Malo | ⚠️ Aceptable | ✅ Bueno | Resultado |
|---|---|---|---|---|
| Accuracy | < 0.889\* | — | — | 0.886–0.887 (no supera el baseline) |
| Balanced Acc | ≈ 0.33 (azar) | 0.50–0.65 | > 0.65 | 0.34–0.45 ❌ |
| F1-macro | < 0.40 | 0.50–0.60 | > 0.60 | 0.28–0.37 ❌ |
| Recall *Grave* | < 0.30 | 0.50–0.70 | > 0.70 | 0.00 (0.52 solo Log. balanceada) ❌ |

\* *El baseline trivial "predecir siempre Sin signos" ya alcanza 0.889; ningún modelo lo supera.*

**Conclusión:** con las variables disponibles (edad, sexo, semana, año, departamento) **no
existe señal suficiente** para predecir la severidad clínica. Los modelos solo aprenden a
predecir la clase mayoritaria (recall de *Grave* = 0). Es un resultado negativo válido y
reportable.

### 4.2 Regresión / serie temporal — *dataset ADECUADO*

Se agregó el dataset a **casos por semana epidemiológica** (1,305 puntos, 2000–2024) y se
predijo el valor de la semana siguiente con **ventanas de tiempo** (lags).

**Selección de ventana óptima (método tipo codo):** se eligió **W = 10 semanas**.

| Modelo | R² | RMSE | MAE |
|---|---|---|---|
| **Ridge / Lineal** | **0.976** | 659 | 272 |
| Lasso | 0.976 | 659 | 272 |
| Random Forest | 0.427 | 3220 | 1074 |
| Gradient Boosting | 0.353 | 3421 | 1154 |

**Rangos de referencia vs. resultado:**

| Métrica | ❌ Malo | ⚠️ Moderado | ✅ Bueno/Excelente | Resultado |
|---|---|---|---|---|
| R² | < 0.5 | 0.5–0.7 | 0.7–0.9 / > 0.9 | **0.976** ✅ |
| ¿Supera baseline ingenuo? | no | — | sí | R² 0.976 > 0.959; MAE 272 < 383 ✅ |
| MAE relativo a la media (789) | > 50 % | 20–50 % | < 20 % | 34.5 % ⚠️ |

**Por qué los lineales ganan a los árboles:** la serie tiene una fuerte tendencia creciente
por el brote 2023–2024 (de ~63k casos/año en 2022 a ~257k y ~272k en 2023–2024). Los árboles
**no extrapolan** fuera del rango visto en entrenamiento, mientras que los modelos lineales
autorregresivos sí siguen la tendencia. *Insight* relevante para el paper.

**Validez del dato (target = casos/semana):** el valor no es sintético ni imputado; es un
**conteo directo** de registros reales (`GROUP BY año, semana` + `COUNT`). Verificación:

| Comprobación | Resultado |
|---|---|
| Σ casos de la serie = nº de registros del CSV | 1,029,421 = 1,029,421 ✅ |
| Semanas faltantes rellenadas artificialmente | NINGUNA (serie continua) ✅ |
| Verificación manual (2000, semana 5) | 59 registros reales = serie 59 ✅ |

> Única limitación de la fuente (no introducida por nosotros): los conteos dependen de la
> vigilancia pasiva del MINSA, con posible subregistro.

### 4.3 Clustering de departamentos — *adecuado solo tras limpieza*

Se construyó un perfil por departamento (volumen, edad media, % femenino, tasa de severidad,
semana pico) y se agrupó con KMeans / Jerárquico, validando con PCA.

| Métrica | ❌ Sin estructura | ⚠️ Débil | ✅ Razonable/Fuerte | Resultado |
|---|---|---|---|---|
| Silhouette | < 0.25 | 0.25–0.50 | 0.50–0.70 / > 0.70 | 0.547 |
| Davies-Bouldin (menor = mejor) | > 2 | 1–2 | < 1 | 0.309 |

**Advertencia:** aunque las métricas son "buenas", con `k=2` el algoritmo solo aísla
**MOQUEGUA (1 solo caso en 25 años, dato atípico)** frente a los otros 22 departamentos → el
resultado es **trivial**. Requiere filtrar departamentos con muy pocos casos y/o aplicar
escala logarítmica al volumen para obtener agrupaciones interpretables.

### 4.4 Síntesis: ¿para qué abordaje es adecuado el dataset?

| Abordaje | Métrica principal | Resultado | Veredicto |
|---|---|---|---|
| Clasificación | F1-macro / Recall *Grave* | 0.33 / 0.00 | ❌ No adecuado |
| **Regresión (serie temporal)** | R² | **0.976** | ✅ **Adecuado** |
| Clustering | Silhouette | 0.547 (degenerado) | ⚠️ Solo tras limpieza |

## 5. Discusión e *Insights*

- **Insight 1 (metodológico):** evaluar los tres abordajes con sus métricas permite *demostrar*
  con evidencia para qué sirve el dataset, en lugar de asumirlo. El dengue, registrado como
  casos individuales, **no** tiene señal para clasificar severidad, pero **sí** tiene una
  estructura temporal muy fuerte.
- **Insight 2 (epidemiológico):** la mejor predicción de los casos de una semana son los de las
  semanas previas (autocorrelación) → confirma la dinámica de propagación de la epidemia.
- **Insight 3 (brote):** el salto 2023–2024 explica por qué los modelos de árboles fallan (no
  extrapolan) y los lineales autorregresivos triunfan.
- **Limitaciones:** *leakage* evitado al excluir `diagnostic`; desbalance extremo (*Grave* 0.39 %);
  vigilancia pasiva con posible subregistro; un departamento atípico (MOQUEGUA) distorsiona el
  clustering.

## 6. Conclusiones y Trabajo Futuro

- **El dataset es adecuado para regresión / serie temporal** (R² = 0.976, supera el baseline
  ingenuo), **no para clasificación** de severidad (recall de *Grave* = 0), y para clustering
  solo tras limpiar outliers.
- **Aplicabilidad:** modelo de **alerta temprana** de casos de dengue por semana, útil para que
  salud pública anticipe brotes y asigne recursos.
- **Trabajo futuro:** comparar con **LSTM** (referencia en series temporales), incorporar
  variables exógenas (clima, temperatura, lluvias), y desagregar la predicción por departamento.

## Referencias

> Formato del paper: el que pida SIMBIG (normalmente estilo Springer/CEUR). Usar gestor (Zotero/Mendeley).

1. _…_

---

## Mapeo a SIMBIG 2026 (paper en inglés)

| Sección de este informe | Sección del paper |
|---|---|
| Resumen | Abstract |
| 1. Introducción | Introduction |
| 2. Estado del arte | Related Work |
| 3. Materiales y Métodos | Materials and Methods |
| 4. Resultados | Experiments and Results |
| 5. Discusión | Discussion |
| 6. Conclusiones | Conclusions |

**Checklist del enunciado:**
- [x] Tema con ≥ 10 mil registros (~1M ✔)
- [x] ≥ 10 características interesantes (sin contar nombre/dirección/ubigeo)
- [x] Tipo de problema definido (los 3 evaluados; **regresión** es el adecuado)
- [ ] Estado del arte documentado
- [x] 5 técnicas comparadas (por abordaje)
- [x] EDA
- [x] Comparación con métricas
- [x] Insights

> ✅ **Enfoque decidido:** el proyecto se centra en **regresión / serie temporal** (predicción de
> casos de dengue por semana), porque las métricas demostraron que es el único abordaje adecuado
> para este dataset. La clasificación y el clustering se reportan como experimentos comparativos
> que justifican esa elección.
