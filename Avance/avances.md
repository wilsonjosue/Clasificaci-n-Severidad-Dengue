# Plan de Avances — Trabajo Final de Inteligencia Artificial

**Tema:** Clasificación de la severidad del Dengue en el Perú (2000–2024)
**Dataset:** `Dengue/datos_abiertos_vigilancia_dengue_2000_2024.csv` (1,029,421 registros, 14 columnas, separador `;`)
**Entregable técnico:** un único **Notebook Jupyter (`.ipynb`)** que se irá ampliando en cada avance.

El enunciado pide dos cosas: **(1) Selección de tema** y **(2) Selección de
estrategia** (elegir regresión/clasificación/clustering, estado del arte, **5
técnicas** para comparar, EDA, comparación con métricas e insights). El trabajo
se divide en **3 avances**, cada uno corresponde a una sección del notebook y a
una entrega.

---

## Avance 1 — Selección del tema y Análisis Exploratorio de Datos (EDA)

**Objetivo:** justificar el dataset, entenderlo y dejarlo limpio para modelar.

### Qué se presenta
1. **Justificación del tema**
   - Fuente: datos abiertos (vigilancia epidemiológica del MINSA, datosabiertos.gob.pe).
   - Cumplimiento de requisitos: ≥10 mil registros (1,029,421 ✓) y ≥10 características
     interesantes (se alcanzan vía feature engineering; ver Avance 2).
   - Relevancia: el dengue es una enfermedad epidémica recurrente y de alto impacto en el Perú.
2. **Descripción del dataset**
   - Diccionario de variables: departamento, provincia, distrito, localidad, enfermedad,
     ano, semana, diagnostic, diresa, ubigeo, localcod, edad, tipo_edad, sexo.
   - Identificación de variables válidas vs. inválidas (geográficas/IDs: ubigeo, localcod,
     diresa, departamento/provincia/distrito/localidad).
3. **Carga y limpieza**
   - Lectura con separador `;` y manejo de encoding (BOM).
   - Tratamiento de nulos (p. ej. `localcod` vacío), tipos de dato y normalización.
4. **EDA**
   - Distribución de la variable objetivo (severidad: SIN signos 915,243 / CON signos 110,166 / GRAVE 4,012).
   - Distribuciones de edad, sexo, tendencia anual y estacional (por semana).
   - Visualizaciones: histogramas, series temporales de casos, barras por región.
   - Detección del **desbalance de clases** (~89% clase mayoritaria).
5. **Definición del problema**
   - Tipo de problema elegido: **clasificación** (severidad del dengue, 3 clases).

### Entregable
Notebook con secciones 1–5 + conclusiones preliminares del EDA.

---

## Avance 2 — Estrategia: Estado del arte, Feature Engineering y Modelado

**Objetivo:** revisar el estado del arte, preparar las características y entrenar 5 modelos.

### Qué se presenta
1. **Estado del arte**
   - Revisión de trabajos previos de predicción/clasificación de dengue y de brotes
     epidémicos con machine learning.
2. **Feature engineering** (alcanzar ≥10 características válidas)
   - Temporales: año, semana → mes y estación, codificación cíclica (seno/coseno) de la semana,
     flag de año epidémico.
   - Demográficas: grupos de edad, tipo_edad, sexo.
   - Epidemiológicas: incidencia/conteo de casos por región y *lags* (semanas previas).
3. **Preparación para el modelado**
   - Codificación de categóricas, escalado, división train/test (estratificada).
   - Tratamiento del desbalance: class weights, remuestreo o SMOTE.
4. **Selección y entrenamiento de 5 técnicas** (clasificación), por ejemplo:
   - Regresión Logística, Árbol de Decisión, Random Forest, Gradient Boosting (XGBoost/LightGBM), y SVM o KNN.

### Entregable
Notebook ampliado con secciones 6–9 + los 5 modelos entrenados.

---

## Avance 3 — Comparación de Técnicas, Insights y Conclusiones

**Objetivo:** comparar los modelos con métricas, generar insights y cerrar el proyecto.

### Qué se presenta
1. **Comparación con métricas**
   - Accuracy, **F1 macro**, Precision/Recall por clase, ROC-AUC, matriz de confusión.
   - Tabla comparativa de los 5 modelos y validación cruzada.
   - Selección del mejor modelo y análisis de errores.
2. **Insights**
   - Importancia de variables (feature importance / SHAP).
   - Patrones estacionales y geográficos, perfiles de riesgo.
3. **Conclusiones**
   - Hallazgos principales, limitaciones y trabajo futuro.
4. **Reproducibilidad**
   - Notebook final ordenado, comentado y ejecutable de principio a fin;
     lista de dependencias.

### Entregable
Notebook final completo con la comparación, los insights y las conclusiones.

---

## Resumen rápido

| Avance | Foco | Secciones del notebook |
|---|---|---|
| 1 | Tema + EDA + limpieza | Justificación, dataset, limpieza, EDA, definición del problema |
| 2 | Estado del arte + feature engineering + 5 modelos | Estado del arte, features, preparación, entrenamiento |
| 3 | Comparación + insights + conclusiones | Métricas, mejor modelo, insights, conclusiones |
