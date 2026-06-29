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
> resultado principal (Ridge, R² = 0.975, supera al baseline ingenuo y al LSTM) →
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

La predicción de casos de dengue mediante *machine learning* y series temporales es un campo
activo, especialmente para **sistemas de alerta temprana**. La literatura muestra tres líneas
relevantes para este trabajo:

1. **Pronóstico semanal de casos como serie temporal**, con foco en vigilancia epidemiológica.
2. **Modelos de aprendizaje profundo (LSTM)**, frecuentemente potenciados con **variables
   climáticas** y de **movilidad**, y a menudo en configuraciones de **ensamble**.
3. **Perú (especialmente Iquitos)** aparece de forma recurrente como sitio de estudio.

| Ref. | Año | Datos / país | Técnicas | Hallazgo / Métrica | Relación con nuestro trabajo |
|---|---|---|---|---|---|
| [1] Iquitos/San Juan/Singapur | ~2019 | Vigilancia semanal + clima (1990–2016) | ML, regresión y series temporales | Pronóstico semanal de casos y brotes; evalúa el aporte de la vigilancia vs. clima | Mismo objetivo (casos/semana) e incluye **Perú (Iquitos)** |
| [2] Rio de Janeiro, Brasil | 2024 | Casos + clima | Estadísticos vs. ML; **LSTM**, ARIMA, ensamble | LSTM fue el mejor ML (con clima); el **ensamble LSTM+ARIMA** mejoró aún más | Compara LSTM vs. clásicos, como nosotros |
| [3] Ensamble reproducible | 2024 | Brasil → transferido a **Perú** | Ensamble de ML, espacio-temporal | Estimación de incidencia a 1 mes a nivel estatal; **transferible a Perú** | Refuerza el enfoque de alerta temprana en Perú |
| [4] Brasil (movilidad+clima) | 2025 | Casos + movilidad + clima | **LSTM** | Marco escalable de pronóstico y detección de brotes | LSTM como referencia; muestra el valor de variables exógenas |
| [5] Jaipur, India | 2025 | Casos + clima complejo | Aprendizaje profundo | Predicción de pacientes bajo condiciones climáticas variables | Deep learning para dengue |
| [6] Revisión Latinoamérica | 2022 | Múltiples países | Revisión de ML (*One Health*) | Síntesis de técnicas y variables usadas en la región | Contexto regional |
| [7] Bangladesh | 2025 | Casos (temporal y espacial) | Híbrido bayesiano + ML | Sistema de alerta temprana | Mismo fin (early warning) |

**Brecha y posicionamiento de nuestro trabajo:** la mayoría de estudios incorporan **variables
climáticas/movilidad** y reportan que **LSTM** suele ganar. Nuestro trabajo usa **solo el
historial de casos** del dataset nacional del MINSA (2000–2024, ~1M registros) y muestra que, en
ese escenario y a **horizonte de 1 semana**, los **modelos lineales simples (Ridge/Lasso) superan
al LSTM** por la fuerte autocorrelación. Esto aporta un *baseline* reproducible y la observación
de que la complejidad del LSTM solo se justifica al añadir variables exógenas (trabajo futuro).

> ⚠️ *Pendiente del equipo:* completar las **citas bibliográficas completas** (autores, revista)
> a partir de los enlaces de la sección Referencias y darles formato SIMBIG.

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

### 3.4 Algoritmos comparados (6 técnicas de regresión)

| # | Técnica | Familia | Notas |
|---|---|---|---|
| 1 | Ridge (L2) | Lineal regularizada | Maneja multicolinealidad de los lags; **mejor modelo** |
| 2 | Lasso (L1) | Lineal regularizada | Selección de variables (lags relevantes) |
| 3 | Perceptrón (MLP) | Red neuronal | Capta no linealidades; requiere escalado |
| 4 | Random Forest Regressor | Ensamble (bagging) | No extrapola la tendencia (limitación observada) |
| 5 | Gradient Boosting Regressor | Ensamble (boosting) | Potente en patrones no lineales |
| 6 | **LSTM** | Red recurrente | Técnica de referencia para series temporales |

> *Experimentos secundarios:* clasificación (Reg. Logística, Random Forest, XGBoost, LightGBM,
> MLP) y clustering (K-means, jerárquico) — ver Secciones 4.1 y 4.3.

### 3.5 Métricas y selección de ventanas (regresión)

- **R²** (coeficiente de determinación): proporción de varianza explicada (principal).
- **RMSE** (penaliza más los errores grandes) y **MAE** (en las unidades de `casos`).
- **Comparación con baseline ingenuo** (persistencia: `casos[t+H] = casos[t]`): el modelo debe
  superarlo para aportar valor.
- **Doble selección de ventana por método tipo codo** (ver §4.2):
  - **Ventana de entrada `W`** (error decreciente → codo de rendimientos decrecientes).
  - **Horizonte `H`** (error creciente → mayor horizonte confiable).

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

### 4.2 Regresión / serie temporal — *dataset ADECUADO* (abordaje principal)

Se agregó el dataset a **casos por semana epidemiológica** (1,305 puntos continuos, 2000–2024).

**Doble análisis de ventana** (se distinguen dos conceptos que se comportan de forma opuesta):

| Ventana | Comportamiento del error | Selección | Resultado |
|---|---|---|---|
| **Entrada `W`** (semanas de historia usadas) | **Baja y se aplana** (RMSE 864→671→660) | Codo de rendimientos decrecientes | **W = 3 semanas** |
| **Horizonte `H`** (semanas hacia el futuro) | **Crece** (RMSE 671→1150→…→4664) | Mayor `H` con error aceptable | **H = 1 semana** |

> **Nota técnica (corrección tras la 2.ª revisión):** la afirmación *"el error crece con la
> ventana"* es rigurosa para el **horizonte `H`**, no para la ventana de entrada `W` (donde más
> historia ayuda). Reportar ambos análisis hace el trabajo técnicamente correcto y a la vez
> muestra la curva creciente esperada. El horizonte `H = 1` define la **capacidad de alerta
> temprana** (predicción confiable a 1 semana).

**Comparación de 6 técnicas** (configuración W=3, H=1):

| Modelo | R² | RMSE | MAE | ¿Supera baseline? |
|---|---|---|---|---|
| **Ridge (L2)** | **0.975** | 671 | 278 | ✅ |
| Lasso (L1) | 0.975 | 671 | 278 | ✅ |
| Perceptrón (MLP) | 0.972 | 708 | 297 | ✅ |
| LSTM (referencia) | 0.560 | 2817 | 915 | ❌ |
| Random Forest | 0.444 | 3167 | 1054 | ❌ |
| Gradient Boosting | 0.374 | 3359 | 1128 | ❌ |

*Baseline ingenuo (persistencia): R² 0.959, RMSE 862, MAE 383.*

**Rangos de referencia vs. resultado:**

| Métrica | ❌ Malo | ⚠️ Moderado | ✅ Bueno/Excelente | Resultado |
|---|---|---|---|---|
| R² | < 0.5 | 0.5–0.7 | 0.7–0.9 / > 0.9 | **0.975** ✅ |
| ¿Supera baseline ingenuo? | no | — | sí | R² 0.975 > 0.959; RMSE 671 < 862 ✅ |

**Hallazgos clave:**
- **LSTM no superó a los modelos lineales.** Pese a ser la técnica de referencia, en esta serie
  —con autocorrelación muy alta (lag-1 = 0.982) y horizonte de 1 semana— los modelos lineales,
  que se anclan al último valor, son superiores; el LSTM además sufre con el brote 2023–2024
  (magnitudes nunca vistas en entrenamiento). *Más complejidad no siempre es mejor.*
- **Los árboles (RF, GB) fallan** porque **no extrapolan** la tendencia del brote (de ~63k
  casos/año en 2022 a ~257k y ~272k en 2023–2024).

**Validez del dato (target = casos/semana):** el valor no es sintético ni imputado; es un
**conteo directo** de registros reales (`GROUP BY año, semana` + `COUNT`). Verificación:

| Comprobación | Resultado |
|---|---|
| Σ casos de la serie = nº de registros del CSV | 1,029,421 = 1,029,421 ✅ |
| Semanas faltantes rellenadas artificialmente | NINGUNA (serie continua) ✅ |
| Verificación manual (2000, semana 5) | 59 registros reales = serie 59 ✅ |

> Única limitación de la fuente (no introducida por nosotros): los conteos dependen de la
> vigilancia pasiva del MINSA, con posible subregistro.

### 4.3 Clustering de departamentos — *estructura DÉBIL (no adecuado)*

Se construyó un perfil por departamento (volumen, edad media, % femenino, tasa de severidad,
semana pico) y se agrupó con KMeans / Jerárquico, validando con PCA.

**Corrección metodológica:** se **excluyeron 4 departamentos andinos/fríos con casos casi nulos**
(MOQUEGUA=1, APURIMAC=11, AREQUIPA=28, PUNO=647), donde el *Aedes aegypti* casi no vive y que
**inflaban artificialmente** el Silhouette (un cluster aislaba a MOQUEGUA). Además se aplicó
**escala logarítmica** al volumen. Quedan 19 departamentos.

| Métrica | ❌ Sin estructura | ⚠️ Débil | ✅ Razonable/Fuerte | Resultado (corregido) |
|---|---|---|---|---|
| Silhouette | < 0.25 | 0.25–0.50 | 0.50–0.70 / > 0.70 | **0.35** ⚠️ |
| Davies-Bouldin (menor = mejor) | > 2 | 1–2 | < 1 | **1.12** ⚠️ |

**Conclusión:** una vez corregidos los outliers, la estructura de clusters es **débil**. Los dos
grupos se diferencian sobre todo por la **semana pico** (regiones de pico temprano ~semana 14 vs.
tardío ~semana 40), no por perfiles cualitativos marcados. El dataset **no es claramente adecuado
para clustering**.

### 4.4 Síntesis: ¿para qué abordaje es adecuado el dataset?

| Abordaje | Métrica principal | Resultado | Veredicto |
|---|---|---|---|
| Clasificación | F1-macro / Recall *Grave* | 0.33 / 0.00 | ❌ No adecuado |
| **Regresión (serie temporal)** | R² | **0.975** | ✅ **Adecuado** |
| Clustering | Silhouette | 0.35 (estructura débil) | ⚠️ No adecuado |

> Los tres experimentos, todos con metodología correcta, **confirman que la regresión / serie
> temporal es el único abordaje claramente adecuado** para este dataset.

## 5. Discusión e *Insights*

- **Insight 1 (metodológico):** evaluar los tres abordajes con sus métricas permite *demostrar*
  con evidencia para qué sirve el dataset, en lugar de asumirlo. El dengue, registrado como
  casos individuales, **no** tiene señal para clasificar severidad, pero **sí** tiene una
  estructura temporal muy fuerte.
- **Insight 2 (epidemiológico):** la mejor predicción de los casos de una semana son los de las
  semanas previas (autocorrelación) → confirma la dinámica de propagación de la epidemia.
- **Insight 3 (brote):** el salto 2023–2024 explica por qué los modelos de árboles fallan (no
  extrapolan) y los lineales autorregresivos triunfan.
- **Insight 4 (LSTM):** la técnica de referencia para series temporales **no fue la mejor** aquí.
  Con autocorrelación muy alta y horizonte de 1 semana, los modelos lineales simples ganan →
  *más complejidad no siempre es mejor*.
- **Insight 5 (ventana):** distinguir la **ventana de entrada** (error decreciente) del
  **horizonte** (error creciente) es clave; confundirlos lleva a conclusiones erróneas.
- **Limitaciones:** *leakage* evitado al excluir `diagnostic`; desbalance extremo (*Grave* 0.39 %);
  vigilancia pasiva con posible subregistro; clustering con estructura débil incluso tras corregir
  los departamentos atípicos.

## 6. Conclusiones y Trabajo Futuro

- **El dataset es adecuado para regresión / serie temporal** (Ridge, R² = 0.975, supera el
  baseline ingenuo), **no para clasificación** de severidad (recall de *Grave* = 0), ni para
  clustering (estructura débil, Silhouette = 0.35 tras corregir outliers).
- **Mejor modelo:** lineal regularizado (Ridge/Lasso), simple e interpretable, que superó incluso
  al LSTM en el pronóstico a 1 semana.
- **Aplicabilidad:** modelo de **alerta temprana** de casos de dengue por semana, útil para que
  salud pública anticipe brotes y asigne recursos.
- **Trabajo futuro:** dar más contexto al **LSTM** (más variables/épocas, secuencias más largas),
  incorporar variables exógenas (clima: temperatura y lluvias), y desagregar la predicción por
  departamento.

## Referencias

> Formato del paper: el que pida SIMBIG (normalmente estilo Springer/CEUR). Usar gestor
> (Zotero/Mendeley) y completar autores/revista desde cada enlace.

1. *Weekly dengue forecasts in Iquitos, Peru; San Juan, Puerto Rico; and Singapore.* PMC7567393 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567393/
2. *Assessing dengue forecasting methods: a comparative study of statistical models and machine learning techniques in Rio de Janeiro, Brazil.* PMC11984044 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11984044/
3. *A reproducible ensemble machine learning approach to forecast dengue outbreaks.* Scientific Reports (2024) — https://www.nature.com/articles/s41598-024-52796-9
4. *Dengue forecasting and outbreak detection in Brazil using LSTM: integrating human mobility and climate factors.* PMC12657288 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12657288/
5. *Prediction of dengue patients using deep learning methods amid complex weather conditions in Jaipur, India.* Discover Public Health, Springer (2025) — https://link.springer.com/article/10.1186/s12982-025-00448-2
6. *Dengue Prediction in Latin America Using Machine Learning and the One Health Perspective: A Literature Review.* PMC9611387 — https://pmc.ncbi.nlm.nih.gov/articles/PMC9611387/
7. *Bayesian hybrid statistical and machine learning models for dengue forecasting in Bangladesh.* medRxiv (2025) — https://www.medrxiv.org/content/10.1101/2025.09.14.25335716

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
- [x] Estado del arte documentado (7 referencias reales; faltan citas completas)
- [x] 5 técnicas comparadas (6 en regresión, incluyendo LSTM)
- [x] EDA (general + serie temporal)
- [x] Comparación con métricas (R²/RMSE/MAE + baseline; F1/Silhouette en secundarios)
- [x] Insights (5 documentados)

> ✅ **Enfoque decidido:** el proyecto se centra en **regresión / serie temporal** (predicción de
> casos de dengue por semana), porque las métricas demostraron que es el único abordaje adecuado
> para este dataset. La clasificación y el clustering se reportan como experimentos comparativos
> que justifican esa elección.
