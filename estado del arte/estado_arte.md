# Estado del Arte — Predicción de Casos de Dengue con *Machine Learning* y Series Temporales

> **Documento de trabajo (español)** para la Sección 2 (*Related Work*) del artículo SIMBIG 2026:
> *Weekly Dengue Case Forecasting in Peru Using Regression and Time-Series Machine Learning Models (2000–2024)*.
>
> **Criterios del docente:** mínimo ~3 artículos, de los **últimos 3 años** (2023–2026), recalcando las
> **técnicas utilizadas** y la **forma de atacar el problema** (correo 25/06); apoyarse en `pdf-anexo.pdf`,
> que pronostica hasta una **ventana de 60 semanas** (correo 27/06).
>
> Todos los artículos desarrollados abajo son de **2024–2025**. Cada uno se analiza con el mismo esquema
> (Objetivo · Datos · Modelo · Resultados · Relación con nuestro trabajo).

---

## 1. Panorama del campo

El pronóstico de casos de dengue con aprendizaje automático y series temporales es un campo muy activo,
impulsado por la necesidad de **sistemas de alerta temprana**: el dengue es una enfermedad estacional
transmitida por *Aedes aegypti*, sin tratamiento específico, por lo que predecir el número de casos es una de
las principales herramientas de prevención. La literatura reciente se concentra en cuatro patrones que se
verán en los artículos analizados: (i) el **uso casi sistemático de variables exógenas** (clima y, más
recientemente, movilidad humana) como predictores [1, 2, 4, 5]; (ii) el **predominio de LSTM** como modelo
de referencia o ganador en horizontes cortos y medios [2, 4, 5]; (iii) la **superioridad de los ensambles**
(estadístico + *deep learning*, o mecanicista + ML) sobre los modelos aislados [1, 2, 3]; y (iv) la
aparición de **Perú** como sitio de estudio, principalmente por transferencia de modelos entrenados en
Brasil [3]. Nuestro trabajo se posiciona como contraste a esta tendencia (ver §4).

---

## 2. Análisis de los trabajos seleccionados

### 2.1 Lu et al. (2025) — Selangor, Malasia *(artículo anexo)*

**Objetivo.** Construir un marco capaz de **extender el horizonte de pronóstico** del dengue mucho más allá
de las pocas semanas habituales (la mayoría de estudios pronostican de 15 días a 4 meses), incorporando
variables climáticas para anticipar brotes con suficiente antelación.

**Datos.** Casos de dengue y datos meteorológicos de **Selangor** (estado con más casos de Malasia). Variables
climáticas: temperatura media, humedad relativa y precipitación acumulada. La serie se divide en ventana de
entrenamiento (semanas 1–261) y ventana de pronóstico (semanas 262–365, ene-2019 a dic-2020).

**Modelo.** Ensamble de tres modelos encadenados: (1) **Regresión Lineal Múltiple (MLR) con efecto de
interacción** que relaciona el clima con la **tasa de picadura del mosquito** (variable intermedia, no los
casos); (2) **LSTM sobre los residuos** de la MLR, previamente *denoised* con **análisis multiresolución
(transformada wavelet discreta 1-D)** para capturar la parte no lineal; y (3) un **modelo compartimental
SI-SIR** (mosquitos Susceptible-Infectado + humanos Susceptible-Infectado-Recuperado) que, con la tasa de
picadura pronosticada, finalmente estima el número de casos.

**Resultados.** El ensamble propuesto (Approach D) pronostica con buena precisión hasta **~60 semanas**, con
**MAPE = 13.97** antes del confinamiento por COVID-19 (*Movement Control Order*, MCO), y MAPE de 13.12–17.09
en validaciones extendidas. Superó a las tres alternativas: solo MLR (el peor, por su linealidad), solo LSTM
(MAPE 17.53) y MLR+LSTM sin vincular la tasa de picadura al clima (MAPE 20.03). Durante el MCO el error se
dispara (MAPE ≈ 87), porque ningún modelo estadístico anticipa un cambio que rompe los patrones históricos.

**Relación con nuestro trabajo.** Es la referencia central que motivó esta revisión. Demuestra que el
horizonte largo se logra **gracias al clima y a un componente mecanicista**; como nosotros usamos *solo* el
historial de casos, nuestro horizonte corto (H = 1 semana) es coherente, y la vía para ampliarlo es
incorporar variables exógenas (trabajo futuro). Además, su colapso durante el MCO es análogo a la dificultad
de nuestros modelos ante el **brote sin precedentes de 2023–2024**.

### 2.2 Comparación de métodos en Río de Janeiro, Brasil (2025)

**Objetivo.** Comparar de forma sistemática **modelos estadísticos clásicos vs. técnicas de ML** para el
pronóstico semanal de dengue, e identificar si los ensambles aportan mejoras.

**Datos.** Casos semanales de dengue de **Río de Janeiro** (sistema *InfoDengue*), 8 años (semanas
epidemiológicas de 2016 a 2023), junto con temperatura y humedad. Promedio ≈ 295 casos/semana (rango 0–3,127).

**Modelo.** Amplio banco de modelos: estadísticos (AR, MA, **ARIMA**, ETS, VAR, **SARIMAX**) y de ML (SVM,
Random Forest, XGBoost, **LSTM**, Prophet), además de **ensambles** que combinan los mejores.

**Resultados.** A 1 semana, el **LSTM con covariables climáticas** fue el más preciso entre los individuales
(MAE 71.35, RMSE 101.53), y el **ensamble LSTM-SARIMAX** mejoró aún más (MAE 65.24, MAPE 15.82 %, RMSE
103.52) frente a ARIMA (MAE 78.26) y SARIMAX (MAE 79.24). Prophet con covariables destacó a 12 semanas. Los
ensambles mostraron "mejoras sustanciales" sobre los modelos aislados.

**Relación con nuestro trabajo.** Es el trabajo más cercano a nuestro diseño experimental: **compara LSTM
contra modelos clásicos** con métricas equivalentes (MAE/RMSE/MAPE). La diferencia clave es que su mejor
desempeño depende de **incorporar clima**; en nuestro caso, sin variables exógenas y a 1 semana, los modelos
lineales superan al LSTM. Sustenta nuestra afirmación de que clima y ensambles son los que elevan el techo.

### 2.3 Ensamble reproducible Brasil → Perú (2024)

**Objetivo.** Proponer un sistema de pronóstico **reproducible y transferible** de la incidencia de dengue a
nivel estatal, con énfasis en escalabilidad operativa y en contextos con escasez de datos.

**Datos.** **Brasil** 2001–2019 (19 años, **27 unidades federativas**, agregación mensual, población total y
grupo 0–19 años) y **Perú** 2010–2019 (10 años, departamentos seleccionados). Covariables: temperatura,
precipitación, humedad, viento, NDVI, elevación, pérdida/cobertura forestal y 31 variables socioeconómicas.

**Modelo.** Ensamble de **CatBoost (gradient boosting) + SVM + LSTM**, combinados mediante un **Random
Forest** meta-aprendiz.

**Resultados.** Pronóstico a **un mes vista**. En Brasil, RMSE normalizado de 0.041–0.857 entre unidades
federativas (mejor en Distrito Federal, 0.041), con menor incertidumbre que los modelos individuales. La
**transferencia a Perú** (con *fine-tuning*) dio RMSE normalizado de 0.117–0.294 en seis departamentos,
mostrando "buena capacidad de generalización" pese al dataset más pequeño.

**Relación con nuestro trabajo.** Es la referencia que **valida explícitamente el dengue en Perú** con ML, y
refuerza el enfoque de alerta temprana. Su predicción mensual a **nivel departamental** marca dos extensiones
naturales de nuestro trabajo (desagregación espacial y agregación mensual). Confirma además que los ensambles
con muchas covariables son el estándar de alto desempeño.

### 2.4 LSTM con movilidad y clima en Brasil (2025)

**Objetivo.** Mejorar el pronóstico y la **detección de brotes** de dengue integrando **movilidad humana**
además del clima, y cuantificar la incertidumbre de las predicciones.

**Datos.** **10 ciudades** brasileñas (Manaus, Belém, Fortaleza, São Paulo, Río, etc.), 2016–2023. Variables:
casos semanales, temperatura, humedad y **flujos de movilidad intermunicipal** (aéreo, fluvial, terrestre),
con cálculo de "casos importados ajustados por movilidad" (datos de *InfoDengue* y Oliveira et al., 2024).

**Modelo.** Red **LSTM** (1,000 unidades ocultas, optimizador Adam, 2,500 épocas) con **predicción conforme
adaptativa** para cuantificar incertidumbre y un clasificador por umbral para detectar brotes.

**Resultados.** Horizonte de **4 semanas**. El modelo con movilidad superó a tres *baselines* en las 10
ciudades; p. ej. en São Paulo: MAE 1,102.75 (vs. 1,230.09 del baseline), MAPE 22.18 % (vs. 24.84 %) y **F1 de
detección de brotes 0.9485** (vs. 0.9149).

**Relación con nuestro trabajo.** Muestra que **añadir variables exógenas (movilidad)** sobre el clima mejora
tanto la predicción como la detección de brotes, y que LSTM es la técnica dominante cuando hay covariables
ricas. Confirma nuestra hipótesis de que la complejidad del LSTM rinde **al disponer de señales externas**,
de las que carecemos al usar solo el historial de casos.

### 2.5 *Deep learning* con clima complejo en Jaipur, India (2025)

**Objetivo.** Predecir el número de pacientes con dengue en una región de clima complejo, comparando varias
arquitecturas de *deep learning*.

**Datos.** Datos mensuales de vigilancia de dengue y meteorológicos de **Jaipur (Rajastán, India), 2015–2019**.

**Modelo.** Comparación de **redes neuronales artificiales (ANN), convolucionales (CNN) y LSTM**, con un
motor de recomendación basado en CNN para interpretar las variables meteorológicas.

**Resultados.** Los modelos de *deep learning* (LSTM en particular) capturan adecuadamente la dinámica de
casos bajo condiciones climáticas variables; estudios análogos de LSTM en India reportan exactitudes > 89 %
para infección. El estudio confirma el valor del *deep learning* combinado con datos meteorológicos.

**Relación con nuestro trabajo.** Aporta diversidad geográfica (Asia) y de arquitecturas (ANN/CNN/LSTM),
reforzando que el *deep learning* es la familia preferida en la literatura **cuando el clima es un predictor
disponible**. Contrasta con nuestro hallazgo de que, sin clima y a 1 semana, los modelos lineales bastan.

---

## 3. Síntesis comparativa

| Ref. | Año | País / sitio | Datos | Técnicas | Variables exógenas | Horizonte | Métrica destacada |
|---|---|---|---|---|---|---|---|
| [1] Lu et al. (anexo) | 2025 | Selangor (Malasia) | Casos + clima, sem. 1–365 | MLR + LSTM + SI-SIR + wavelets | Clima | **~60 semanas** | MAPE 13.97 |
| [2] Río de Janeiro | 2025 | Brasil | 2016–2023, semanal | ARIMA/SARIMAX, SVM, RF, XGBoost, **LSTM**, ensambles | Clima | 1–12 semanas | MAE 65.24 (ensamble) |
| [3] Ensamble reproducible | 2024 | Brasil → **Perú** | 2001–2019 (BR), 2010–2019 (PE), 27 UF, mensual | CatBoost + SVM + LSTM (vía RF) | Clima + socioecon. + satélite | 1 mes | RMSE norm. 0.04–0.86 |
| [4] Movilidad + clima | 2025 | Brasil (10 ciudades) | 2016–2023, semanal | **LSTM** + conformal | Clima + **movilidad** | 4 semanas | F1 brote 0.95 |
| [5] Jaipur | 2025 | India | 2015–2019, mensual | ANN, CNN, **LSTM** | Clima | mensual | Exactitud > 89 % (análogos) |

**Afirmaciones sustentadas en la literatura:**

- **Las variables exógenas son el motor del desempeño:** el clima es predictor central en [1], [2], [3] y [5],
  y la movilidad humana añade mejora medible en [4] (MAE y F1 de brote).
- **LSTM tiende a ser la técnica más fuerte (con covariables):** es el mejor modelo individual en [2], la red
  base en [4] y [5], y componente del ensamble en [1] y [3].
- **Los ensambles superan a los modelos aislados:** ensamble LSTM-SARIMAX en [2], ensamble CatBoost+SVM+LSTM
  en [3], y ensamble MLR+LSTM+SI-SIR en [1].
- **Limitación común:** todos degradan ante eventos que rompen los patrones históricos (MCO/COVID en [1]).

---

## 4. Brecha y posicionamiento (resumen)

A diferencia de los trabajos anteriores —que dependen de **variables exógenas** (clima, movilidad) y donde
**LSTM o los ensambles** suelen ganar [1–5]—, nuestro trabajo estudia qué desempeño se obtiene usando
**únicamente el historial de casos** del dataset nacional del MINSA (Perú, 2000–2024, ~1M registros), y hace
explícita la distinción entre **ventana de entrada** y **horizonte de pronóstico**, rara vez separada en la
literatura. En ese escenario y a 1 semana, mostramos que los modelos lineales simples superan al LSTM por la
fuerte autocorrelación de la serie.

> **Nota:** el desarrollo detallado de *nuestro* método y sus resultados (Ridge R² = 0.975 > baseline > LSTM)
> **no va en el Estado del Arte**, sino en la *Introducción* (contribuciones) y en la *Discusión*. Aquí solo
> se enuncia la brecha en uno o dos párrafos, como cierre de la sección.

---

## 5. Referencias

> Formato **SIMBIG / Springer (estilo LNCS-CCIS)**: `Apellido, I.I.: Título. Revista volumen(número),
> páginas (año). DOI`. Todas son de **2024–2025** (dentro de los últimos 3 años). Se descartaron, por
> antigüedad, una revisión de 2022 y el reto de pronóstico de Iquitos (~2020) de borradores previos; Perú
> queda cubierto por [3]. Listas de autores verificadas en la fuente (PMC/Crossref).

1. Lu, X., Teh, S.Y., Tay, C.J., Abu Kassim, N.F., Fam, P.S., Soewono, E.: Application of multiple linear
   regression model and long short-term memory with compartmental model to forecast dengue cases in Selangor,
   Malaysia based on climate variables. Infectious Disease Modelling 10(1), 240–256 (2025).
   https://doi.org/10.1016/j.idm.2024.10.007
2. Chen, X., Moraga, P.: Assessing dengue forecasting methods: a comparative study of statistical models and
   machine learning techniques in Rio de Janeiro, Brazil. Tropical Medicine and Health 53, 52 (2025).
   https://doi.org/10.1186/s41182-025-00723-7
3. Sebastianelli, A., Spiller, D., Carmo, R., Wheeler, J., Nowakowski, A., Jacobson, L.V., Kim, D., Barlevi,
   H., El Raiss Cordero, Z., Colón-González, F.J., Lowe, R., Ullo, S.L., Schneider, R.: A reproducible
   ensemble machine learning approach to forecast dengue outbreaks. Scientific Reports 14, 3807 (2024).
   https://doi.org/10.1038/s41598-024-52796-9
4. Chen, X., Moraga, P.: Dengue forecasting and outbreak detection in Brazil using LSTM: integrating human
   mobility and climate factors. Infectious Disease Modelling 11(1), 338–354 (2025).
   https://doi.org/10.1016/j.idm.2025.11.002
5. Dhaked, D.K., Sharma, O., Gopal, Y., Gopal, R.: Prediction of dengue patients using deep learning methods
   amid complex weather conditions in Jaipur, India. Discover Public Health 22(1), 58 (2025).
   https://doi.org/10.1186/s12982-025-00448-2

---

## 6. Párrafo listo para el *paper* (versión EN, *Related Work*)

> Recent dengue forecasting work shares three traits relevant to ours. First, **exogenous covariates drive
> performance**: climate is central in [1,2,3,5] and human mobility adds measurable gains in [4]. Second,
> **LSTM is typically the strongest learner** when such covariates are available — best individual model in
> Rio de Janeiro [2], the backbone in [4,5], and a component of the ensembles in [1,3]. Third, **ensembles
> beat single models**: an LSTM-SARIMAX ensemble in [2], a CatBoost+SVM+LSTM ensemble (combined via random
> forest) transferred from Brazil to Peru in [3], and an MLR+LSTM+SI-SIR ensemble that forecasts up to ~60
> weeks ahead (MAPE 13.97) in [1]. All degrade under regime shifts that break historical patterns (the
> COVID-19 movement-control order in [1]). **Unlike these works**, we use only the case history of the MINSA
> national dataset (Peru, 2000–2024) and explicitly separate the input window from the forecast horizon; at a
> one-week horizon, simple regularized linear models surpass the LSTM owing to very high short-term
> autocorrelation, providing a transparent, reproducible baseline and suggesting that deep models and long
> horizons pay off mainly once exogenous signals are added.
