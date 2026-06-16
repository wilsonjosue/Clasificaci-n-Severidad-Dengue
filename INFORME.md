# Informe de Investigación — Trabajo Final de Inteligencia Artificial

> **Documento de trabajo (español).** El *paper* final para **SIMBIG 2026** se redacta en
> inglés siguiendo esta misma estructura (ver sección *Mapeo a SIMBIG* al final).
> **Deadline SIMBIG 2026: 30 de junio de 2026.**

---

## Metadatos

| Campo | Valor |
|---|---|
| **Título tentativo** | *Evaluation of Machine Learning Algorithms to Classify Dengue Severity from Epidemiological Surveillance Data in Peru (2000–2024)* |
| **Tipo de problema** | Clasificación supervisada multiclase (3 clases) |
| **Variable objetivo** | `severidad` ∈ {Sin signos, Con signos, Grave} |
| **Fuente de datos** | [Datos Abiertos – Vigilancia Epidemiológica de Dengue (MINSA/CDC Perú)](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue) |
| **N.º de registros** | ~1,029,421 |
| **Periodo** | 2000–2024 |
| **Autores** | _(nombres del equipo)_ |
| **Curso / Docente** | _(completar)_ |

---

## Resumen (Abstract)

> _150–250 palabras. Redactar al final, cuando estén los resultados._
> Estructura: contexto (dengue como problema de salud pública) → objetivo (clasificar la
> severidad clínica) → datos (vigilancia 2000–2024, ~1M registros) → métodos (5 algoritmos
> comparados + manejo del desbalance) → resultado principal (mejor modelo y métrica) →
> implicancia (apoyo a triaje/priorización epidemiológica).

**Palabras clave:** dengue, clasificación multiclase, aprendizaje automático, salud pública, Perú, desbalance de clases.

---

## 1. Introducción

- Contexto del dengue en Perú (transmisión por *Aedes aegypti*, brotes, regiones endémicas: Loreto, Piura, etc.).
- Problema: anticipar/clasificar la **severidad** del caso ayuda al triaje y a la priorización de recursos.
- Brecha: _¿qué falta en los trabajos previos?_ (ver sección 2).
- **Objetivo general:** comparar 5 algoritmos de ML para clasificar la severidad del dengue.
- **Objetivos específicos:** (1) EDA, (2) preprocesamiento y manejo del desbalance, (3) entrenamiento, (4) comparación con métricas, (5) generación de *insights*.
- **Contribución:** comparación reproducible sobre un dataset nacional de 24 años.

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
| `enfermedad` | Tipo de dengue | Categórica | → **objetivo** |
| `ano` | Año epidemiológico | Numérica | ✔ |
| `semana` | Semana epidemiológica (1–52) | Numérica | ✔ (estacionalidad) |
| `diagnostic` | Código CIE-10 (A97.x) | Categórica | ✘ (fuga de info: codifica la clase) |
| `diresa` | Dirección regional de salud | Categórica | ✔ |
| `ubigeo` | Código geográfico | ID | ✘ (no válida) |
| `localcod` | Código de localidad | ID | ✘ |
| `edad` | Edad (valor crudo) | Numérica | ✔ (tras normalizar) |
| `tipo_edad` | Unidad de edad (A/M/D) | Categórica | ✔ (para normalizar) |
| `sexo` | Sexo (M/F) | Categórica | ✔ |

> ⚠️ **Cuidado con la fuga de información (*data leakage*):** `diagnostic` (CIE-10) y `enfermedad`
> codifican prácticamente lo mismo que la severidad. **No usar `diagnostic` como feature.**

### 3.2 Preprocesamiento

1. Manejo de nulos.
2. Conversión numérica (`ano`, `semana`, `edad`).
3. Normalización de edad a años según `tipo_edad` (A=1, M=1/12, D=1/365).
4. Filtrado de edades imposibles (0–110).
5. Codificación de la variable objetivo: `severidad` ordenada {0: Sin signos, 1: Con signos, 2: Grave}.
6. *Encoding* de categóricas (One-Hot / Target / Ordinal según cardinalidad).
7. Escalado de numéricas cuando el modelo lo requiera (SVM, MLP).
8. **Manejo del desbalance:** `class_weight`, *under/oversampling*, **SMOTE**. Reportar con y sin.

### 3.3 División de datos

- *Train/Validation/Test* estratificado (p. ej. 70/15/15) **o** validación cruzada estratificada (k=5).
- ⚠️ Cuidado con la **dependencia temporal**: considerar un split temporal (entrenar ≤2022, probar 2023–2024) como escenario realista adicional.

### 3.4 Algoritmos comparados (5 técnicas)

| # | Técnica | Familia | Notas |
|---|---|---|---|
| 1 | Regresión Logística (multinomial) | Lineal | *Baseline* interpretable |
| 2 | Random Forest | Ensamble (bagging) | Robusto, *feature importance* |
| 3 | XGBoost / LightGBM | Ensamble (boosting) | Suele ser el mejor en tabular |
| 4 | SVM (kernel RBF) | Margen máximo | Requiere escalado; submuestrear por costo |
| 5 | MLP (red neuronal) | Redes neuronales | Capturar no linealidades |

> Mantener una *pipeline* común (`sklearn.Pipeline`) para que la comparación sea justa.

### 3.5 Métricas de evaluación (clasificación)

Por el desbalance, **no usar solo accuracy**:
- **F1-score macro** y **balanced accuracy** (métricas principales).
- Precision / Recall por clase (la clase *Grave* es la crítica).
- Matriz de confusión.
- ROC-AUC / PR-AUC *one-vs-rest*.
- Cohen's Kappa.

## 4. Resultados

- Tabla comparativa de los 5 modelos (media ± desv. en CV).
- Matrices de confusión del mejor modelo.
- Curvas ROC/PR.
- *Feature importance* / SHAP del mejor modelo.

| Modelo | Acc | Balanced Acc | F1-macro | Recall (Grave) | AUC |
|---|---|---|---|---|---|
| Reg. Logística | | | | | |
| Random Forest | | | | | |
| XGBoost | | | | | |
| SVM | | | | | |
| MLP | | | | | |

## 5. Discusión e *Insights*

- ¿Qué variables pesan más? (edad, semana/estacionalidad, departamento).
- Patrones temporales (brotes) y geográficos.
- Desempeño en la clase minoritaria *Grave*.
- Limitaciones: posible *leakage*, calidad del registro, vigilancia pasiva, sesgos.

## 6. Conclusiones y Trabajo Futuro

- Mejor modelo y justificación.
- Aplicabilidad para salud pública.
- Trabajo futuro: variables climáticas, modelos temporales, predicción de brotes.

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
- [x] Tipo de problema definido (clasificación)
- [ ] Estado del arte documentado
- [ ] 5 técnicas comparadas
- [x] EDA
- [ ] Comparación con métricas
- [ ] Insights
