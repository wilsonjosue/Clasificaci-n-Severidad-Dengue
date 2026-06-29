# Plan General del Proyecto — Trabajo de Investigación IA (SIMBIG 2026)

> Documento maestro de cómo avanzar. Reemplaza al plan anterior (`avances.md`), que quedó
> obsoleto al cambiar el enfoque de **clasificación** a **regresión / serie temporal**.
> **Deadline SIMBIG 2026: 30 de junio de 2026.**

---

## 1. Información general del proyecto (enunciado del profesor)

**Selección de tema** (fuente: datosabiertos.gob.pe)
- ✅ Dataset con ≥ 10 mil registros → **1,029,421 registros**.
- ✅ ≥ 10 características interesantes (sin nombre/dirección/ubigeo).

**Selección de estrategia**
- Elegir entre **regresión, clasificación o clustering** según el tipo de problema.
- Buscar el **estado del arte**.
- Elegir **5 técnicas** para comparar.
- Realizar **EDA**.
- Comparar con **métricas** según el tipo de problema.
- Generar **insights**.

**Entregable final:** *paper* para **SIMBIG 2026** (inglés) + notebooks + informe.

---

## 2. Dataset y enfoque decidido

| Campo | Valor |
|---|---|
| Dataset | `data/raw/datos_abiertos_vigilancia_dengue_2000_2024.csv` (MINSA) |
| Registros | 1,029,421 (2000–2024, 25 años) |
| **Enfoque principal** | **Regresión / serie temporal**: predecir casos de dengue por semana |
| Variable objetivo | `casos` = nº de casos por semana epidemiológica (conteo agregado real) |
| Experimentos secundarios | Clasificación (severidad) y Clustering (departamentos) — justifican por qué se eligió regresión |

**Por qué regresión:** el dataset es histórico y continuo, con fuerte autocorrelación
(lag-1 = 0.982). Las métricas mostraron que clasificación **no** tiene señal (recall *Grave* = 0)
y que clustering es débil (Silhouette 0.35); **solo regresión es adecuado** (R² = 0.975 a 1 semana).

---

## 3. Observaciones del profesor ya incorporadas

1. **Leakage:** se eliminó `diagnostic` (CIE-10), que era un mapeo 1-a-1 con la severidad.
2. **Cambio de enfoque:** de "clasificar severidad" a "predecir casos por semana".
3. **2.ª revisión (sobre la ventana):** el profesor espera que *"el error crezca con la ventana
   y se elija el codo"*. Ver la **Nota técnica (sección 3.1)**: hay que distinguir dos conceptos
   de ventana; presentamos **ambos** para ser rigurosos.

## 3.1 Nota técnica: la elección de la ventana `W` (verificación crítica)

Existen **dos conceptos distintos de "ventana"** que se comportan de forma **opuesta**. Es clave
no confundirlos (fue el error que cometimos al inicio):

| Concepto | Definición | Comportamiento real (verificado) | Cómo se elige |
|---|---|---|---|
| **Ventana de entrada (lags) `W`** | Nº de semanas pasadas usadas como *features* | El error **baja y se aplana** (RMSE 864→733→671→…→660) | Codo de **rendimientos decrecientes** (~3–5 semanas) |
| **Horizonte de pronóstico `H`** | Nº de semanas hacia el **futuro** que se predicen | El error **sube monótonamente** (RMSE 660→4694) | Mayor `H` con error aceptable (~1–2 semanas) |

> **Valoración honesta:** la frase del profesor *"el error sube cuanto mayor es la ventana"*
> **es correcta para el horizonte `H`, pero NO para la ventana de entrada `W`** (más historia
> normalmente ayuda, no perjudica). En su descripción original ("tomamos 3 registros y predecimos
> el siguiente") se refería a la ventana de **entrada**, donde el error en realidad **decrece**.
> La intuición de "error creciente + codo" probablemente viene del método del codo de K-means
> (donde el SSE siempre baja), pero aquí el sentido es el inverso.

**Decisión metodológica:** presentar **los dos análisis** en `03_Regresion`:
1. **Ventana de entrada `W`** vs. error → elegir por el codo donde el error se aplana.
2. **Horizonte `H`** vs. error → curva creciente; elegir el mayor `H` confiable (alerta temprana).

Así el trabajo es técnicamente correcto **y** muestra la curva creciente que el profesor espera,
explicando la diferencia entre ambos conceptos.

---

## 4. Estado actual (al 25 de junio de 2026)

| Componente | Estado |
|---|---|
| `01_EDA_Dengue.ipynb` | ✅ EDA general ejecutado |
| `03_Regresion.ipynb` (principal) | ✅ Validado: doble ventana (W=3, H=1) + 6 técnicas con LSTM |
| `02_Clasificacion.ipynb` | ✅ Reformulado como experimento secundario y validado |
| `04_Clustering.ipynb` | ✅ Reconstruido (outliers corregidos, Silhouette 0.35) |
| `INFORME.md` | ✅ Completo y coherente (Secciones 1–6 + estado del arte) |
| Estado del arte (Sección 2) | ✅ 7 referencias reales (faltan citas completas) |
| LSTM (técnica de referencia) | ✅ Integrado (TensorFlow instalado) |
| `PAPER.md` (inglés, SIMBIG) | ✅ Borrador completo |
| Entorno (`.venv` + kernel `dengue-ia`) | ✅ Listo |
| **Pendiente** | Citas completas, plantilla SIMBIG, nombres de autores, figuras |

---

## 5. Metodología que seguimos (para regresión / serie temporal)

1. **Agregación** del CSV a serie semanal (`GROUP BY año, semana` + `COUNT`) — target real verificado.
2. **EDA temporal:** tendencia, estacionalidad (semana pico) y autocorrelación.
3. **Doble análisis de ventana** (ver §3.1):
   - **`W` de entrada** vs. error → codo de rendimientos decrecientes (cuánta historia usar).
   - **`H` horizonte** vs. error → curva creciente → mayor horizonte confiable (alerta temprana).
4. **5 técnicas** comparadas con la misma evaluación (split temporal pasado→futuro), fijando
   el `W` y el `H` elegidos.
5. **Métricas:** R², RMSE, MAE + comparación con **baseline ingenuo** (persistencia).
6. **Insights** y conclusiones (alerta temprana).

---

## 6. Plan de avance por fases (orden de prioridad)

> Las 4 opciones, ordenadas según prioridad y dependencias. **De aquí arrancamos.**

### 🟥 FASE 1 — Añadir LSTM (completar las 5 técnicas)
- **Qué:** incorporar **LSTM** (red recurrente) al `03_Regresion`, que el profesor llamó
  *"la mejor técnica"* para series temporales.
- **Por qué primero:** deja la **tabla de comparación definitiva**; así el INFORME se actualiza
  una sola vez con todas las técnicas.
- **Observación:** requiere **instalar TensorFlow** (descarga pesada, varios minutos). Si la
  instalación falla, se documenta LSTM como *trabajo futuro* y se continúa sin bloquear.

### 🟧 FASE 2 — Actualizar el INFORME con los resultados corregidos
- **Qué:** volcar al `INFORME.md` la metodología de horizonte, la curva error vs. ventana, la
  tabla de las 5 (o 6) técnicas y la comparación con el baseline.
- **Por qué segundo:** consolida el **núcleo del entregable** una vez cerradas las técnicas.
- **Observación:** la Sección 4 ya tiene una primera versión; hay que reemplazar con los números
  finales y alinear las Secciones 3 y 4.

### 🟨 FASE 3 — Estado del arte (Sección 2)
- **Qué:** buscar y documentar **6–8 referencias** de *forecasting* de dengue / brotes con ML.
- **Por qué tercero:** es **requisito explícito** del enunciado y la sección *Related Work* del
  paper; no depende de los experimentos.
- **Observación:** buscar en Google Scholar/PubMed/Scopus; revisar papers previos de SIMBIG para
  alinear el estilo.

### 🟩 FASE 4 — Corregir clustering y clasificación (experimentos secundarios)
- **Qué:** en `04_Clustering` quitar el outlier (MOQUEGUA, 1 caso) y/o usar escala log; dejar
  `02_Clasificacion` limpio como evidencia de que el dataset **no** sirve para clasificar.
- **Por qué último:** son experimentos de **apoyo** que justifican elegir regresión; aportan
  completitud pero no son el resultado central.
- **Observación:** no invertir demasiado tiempo; basta con que ilustren el contraste de métricas.

---

## 7. Cronograma sugerido (hacia el 30 de junio)

| Día | Foco |
|---|---|
| 25–26 jun | Fase 1 (LSTM) + Fase 2 (INFORME) |
| 27–28 jun | Fase 3 (estado del arte) + Fase 4 (clustering/clasificación) |
| 29 jun | Redacción/traducción del *paper* al inglés (formato SIMBIG) |
| 30 jun | Revisión final y envío |

---

## 8. Checklist del enunciado

- [x] Tema con ≥ 10 mil registros
- [x] ≥ 10 características interesantes
- [x] Tipo de problema definido (regresión / serie temporal)
- [x] EDA (general + temporal)
- [x] 5 técnicas comparadas (Ridge, Lasso, Perceptrón, Random Forest, Gradient Boosting)
- [ ] LSTM (técnica de referencia) — *Fase 1*
- [ ] Estado del arte documentado — *Fase 3*
- [x] Comparación con métricas (R², RMSE, MAE + baseline)
- [~] Insights (en el notebook; pasar al informe con valores finales)
- [ ] Informe consolidado con resultados corregidos — *Fase 2*
- [ ] Paper en inglés (formato SIMBIG)
