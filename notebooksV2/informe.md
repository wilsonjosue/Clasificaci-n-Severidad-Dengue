# Machine Learning aplicado a datos abiertos de vigilancia del dengue en Perú: predicción de brotes, clasificación de gravedad y segmentación geográfica del riesgo

## Resumen
Este proyecto explora el potencial y los límites de los datos abiertos de vigilancia epidemiológica del dengue del Ministerio de Salud del Perú (2000–2024) mediante tres enfoques complementarios de Machine Learning: **(1) predicción de la incidencia semanal** usando modelos de regresión con series temporales, **(2) clasificación del riesgo de dengue grave** a nivel de paciente, y **(3) segmentación no supervisada** de departamentos según sus perfiles epidemiológicos. Los resultados muestran que es posible pronosticar con alta precisión la magnitud de brotes epidémicos (incluso eventos atípicos como el ciclón Yaku 2023-2024) mediante una estrategia de diferenciación que permite a los modelos de árboles extrapolar valores no vistos. Sin embargo, las variables demográficas y espaciotemporales disponibles son insuficientes para predecir la gravedad clínica individual (PR-AUC ≈ 0.0056). Finalmente, el clustering revela la existencia de dos macrorregiones epidemiológicas diferenciadas —la costa explosiva y la selva endémica severa— con estacionalidades y perfiles de riesgo opuestos, lo que subraya la necesidad de políticas de prevención diferenciadas.

## Contexto y objetivos
El dengue es un problema de salud pública prioritario en el Perú, con brotes cada vez más intensos como el asociado al ciclón Yaku en 2023. El Ministerio de Salud publica registros de casos notificados con variables como departamento, semana epidemiológica, edad, sexo y clasificación de severidad. Este trabajo busca responder:

- ¿Se puede predecir cuántos casos ocurrirán en las siguientes semanas, incluso cuando los brotes superan cualquier registro histórico?
- ¿Permiten estos datos identificar a los pacientes con mayor riesgo de desarrollar dengue grave?
- ¿Existen patrones geográficos que diferencien la dinámica de la enfermedad en el país?

El estudio utiliza únicamente los datos abiertos disponibles, evaluando qué información útil pueden aportar sin incorporar fuentes clínicas o climáticas externas.

## Dataset
- **Fuente:** [Plataforma Nacional de Datos Abiertos – MINSA](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)
- **Período:** 2000 – 2024
- **Registros originales:** >1 millón de casos notificados
- **Variables utilizadas:** año, semana epidemiológica, departamento, provincia, distrito, sexo, edad, tipo de diagnóstico, clasificación de severidad.

---

## Metodología

### Modelo 1: Predicción de incidencia semanal (Regresión / Series temporales)
**Objetivo:** Predecir la cantidad de casos nuevos por semana a nivel nacional.

1. **Agrupación temporal:** Se sumaron los casos por año y semana epidemiológica.
2. **Selección de rezagos:** Mediante la Función de Autocorrelación Parcial (PACF) se identificaron los lags significativos: t-1, t-2, t-3 y t-52 (estacional).
3. **Diferenciación:** Se transformó la serie original a una tasa de cambio intersemanal (yt - yt-1) para lograr estacionariedad y romper el "techo" de predicción de modelos basados en árboles.
4. **Modelos comparados:** Ridge, Lasso, Random Forest, Gradient Boosting.
5. **Validación:** División temporal estricta (entrenamiento hasta 2022, prueba 2023-2024). Métricas: R² y MAE, incluyendo comparación contra un baseline naïve.

*Resultado clave:* La diferenciación permitió a Random Forest pasar de un R² de 0.41 a 0.96 en el período de brote atípico, rompiendo el límite de extrapolación de los árboles y logrando una generalización Out-of-Distribution (OOD) frente a escenarios anómalos.

### Modelo 2: Clasificación de riesgo de dengue grave (Clasificación)
**Objetivo:** Clasificar si un paciente desarrollará dengue grave a partir de datos demográficos y espacio-temporales.

1. **Redefinición del target:** Las tres clases originales (sin signos, con signos, grave) se colapsaron a binaria (No Grave vs Grave) al detectar la "clase sándwich" que impedía la separación espacial de los datos.
2. **Partición temporal:** Train hasta 2021, validación 2022, test 2023-2024, evitando fuga de información del futuro (Data Leakage).
3. **Manejo del desbalance extremo:** Prevalencia real de graves <0.4%. Se aplicó undersampling en train (1 grave por 15 no graves) y calibración bayesiana (Prior Shift de Saerens) para restaurar las probabilidades reales.
4. **Modelo:** XGBoost.
5. **Optimización de umbral:** Se eligió el punto de corte que maximiza el F1-score en validación (τ=0.0076) en lugar de maximizar la sensibilidad, reduciendo drásticamente las falsas alarmas masivas que colapsarían un sistema de triaje real.
6. **Métricas:** Accuracy, Recall, Precision, F1, PR-AUC, matriz de confusión.

*Resultado clave:* El PR-AUC de apenas 0.0056 (cercano al azar) demuestra estadísticamente que las variables disponibles no contienen información suficiente para discriminar la gravedad individual. Las variables más relevantes fueron las geográficas y temporales, no las biológicas.

### Modelo 3: Segmentación geográfica epidemiológica (Clustering)
**Objetivo:** Descubrir perfiles departamentales de transmisión y gravedad del dengue.

1. **Agregación y filtrado:** Se crearon perfiles por departamento con variables como edad media, tasas de severidad y semana pico. Se excluyeron regiones con <100 casos históricos para limpiar el ruido estadístico y administrativo.
2. **Selección de K:** El Método del codo (inercia) y el Coeficiente de Silhouette determinaron K=2 como el hiperparámetro óptimo.
3. **Algoritmos comparados:** K-Means y Clustering Jerárquico, evaluados con Silhouette y el Índice de Davies-Bouldin para garantizar estabilidad estructural.
4. **Visualización:** Análisis de Componentes Principales (PCA) capturando un 70.7% de varianza explicada en 2D, con la identificación topológica de Piura como un outlier extremo.
5. **Caracterización:** Se extrajeron los promedios de las variables originales para cada clúster.

*Resultado clave:* Emergen dos perfiles epidemiológicos nítidos:
- **Clúster 0 - Costa Epidémica:** Alto volumen de casos, baja letalidad, pico en abril (semana 17), pacientes de mayor edad.
- **Clúster 1 - Selva Endémica:** Volumen menor pero con el doble de tasa de gravedad, pico en octubre (semana 39), población más joven afectada.

---

## Resultados consolidados

| Modelo | Técnica principal | Métrica principal | Hallazgo |
|--------|-------------------|-------------------|----------|
| Predicción semanal | Random Forest + diferenciación | R² = 0.960 (en brote OOD) | Se puede predecir la magnitud de brotes, con 1 semana de desfase |
| Clasificación de gravedad | XGBoost + calibración bayesiana | PR-AUC = 0.0056 | Los datos demográficos no predicen la gravedad individual |
| Clustering geográfico | K-Means (K=2) | Silhouette = 0.33 | Existen dos macro-regiones con dinámicas opuestas |

---

## Conclusiones
- **Predicción de brotes:** La diferenciación es una estrategia simple pero poderosa para que los modelos de árboles superen su límite de extrapolación y pronostiquen picos epidémicos inéditos. El sistema funciona como alerta temprana, aunque reacciona con una semana de retraso; la incorporación de predictores climáticos podría eliminar ese desfase.
- **Clasificación de gravedad:** Con las variables abiertas actuales no es posible construir un clasificador clínico útil para dengue grave. Es indispensable incluir datos de laboratorio, serotipo, comorbilidades y signos vitales para trazar fronteras de decisión eficientes.
- **Segmentación regional:** Perú enfrenta dos endemias diferentes. La costa sufre epidemias masivas y explosivas tras el verano; la selva presenta una endemia constante, más severa y con pico en el último trimestre. Las políticas de prevención y asignación de recursos deben diferenciarse geográficamente.
- **Valor de los datos abiertos:** Los datos del MINSA permiten construir sistemas robustos de monitoreo y pronóstico de carga de enfermedad poblacional, pero son limitados para el análisis de riesgo clínico individual. Complementarlos con fuentes climáticas y clínicas potenciará significativamente las herramientas de salud pública.

*Nota: Los datos originales no se incluyen; pueden descargarse directamente desde la fuente oficial.*

## Tecnologías utilizadas
Python, Scikit-learn, XGBoost, Statsmodels, Pandas, Matplotlib, Seaborn.