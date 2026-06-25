# Weekly Dengue Case Forecasting in Peru Using Regression and Time-Series Machine Learning Models (2000–2024)

> **Draft for SIMBIG 2026.** English manuscript derived from `INFORME.md`. Author names,
> affiliations and full bibliographic citations must be completed before submission.

**Authors:** _(names)_ — _(affiliation, email)_

---

## Abstract

Dengue is a recurrent, climate-sensitive epidemic disease and a major public-health burden in
Peru. Anticipating the weekly number of cases enables early-warning systems that help health
authorities allocate resources before outbreaks escalate. Using the Peruvian Ministry of Health
(MINSA) national epidemiological surveillance dataset (1,029,421 individual case records,
2000–2024), we aggregate the data into a continuous weekly case time series (1,305 points) and
frame the task as a regression / time-series forecasting problem. We first justify this framing
empirically by comparing the three canonical problem types on the same data: severity
classification, clustering of departments, and case-count regression. Classification of clinical
severity shows no usable signal (macro-F1 ≈ 0.33, recall of the *Severe* class = 0), and
department clustering yields only a weak structure (silhouette ≈ 0.35), whereas regression is
clearly adequate. We then distinguish two notions of "window": the **input window** `W` (past
weeks used as features, where the error decreases and plateaus) and the **forecast horizon** `H`
(weeks ahead, where the error increases monotonically), selecting `W = 3` and `H = 1` via
elbow-type criteria. We compare six techniques — Ridge, Lasso, Multilayer Perceptron, Random
Forest, Gradient Boosting and an LSTM network. The best model is a regularized linear model
(Ridge, R² = 0.975, RMSE = 671), which outperforms the naïve persistence baseline (R² = 0.959)
and, notably, the LSTM (R² = 0.560). We conclude that, using case history alone and a one-week
horizon, simple linear models are preferable, providing a reproducible early-warning baseline.

**Keywords:** dengue, case forecasting, time series, regression, machine learning, early warning,
public health, Peru.

---

## 1. Introduction

Dengue, transmitted by the *Aedes aegypti* mosquito, causes recurrent epidemics in Peru, with
endemic regions such as Loreto, Piura and Madre de Dios and a marked seasonal pattern. The
2023–2024 period saw an unprecedented surge in reported cases. Accurate short-term forecasts of
weekly case counts support **early-warning systems**: they let public-health authorities
anticipate outbreaks and allocate resources in advance.

A frequent methodological pitfall is choosing the modeling paradigm (classification, regression
or clustering) by intuition rather than by evidence. In this work we **empirically test all three
paradigms** on the same national dataset and use the metrics appropriate to each to decide which
is adequate. We then develop and compare regression / time-series models for one-week-ahead case
forecasting.

**Contributions.** (i) An evidence-based justification of the regression framing for this
dataset; (ii) a clear separation between the *input window* and the *forecast horizon*, which are
often conflated; (iii) a six-technique comparison including LSTM; and (iv) the finding that, using
case history alone at a one-week horizon, regularized linear models outperform the LSTM, yielding
a reproducible early-warning baseline.

## 2. Related Work

Machine-learning and time-series forecasting of dengue is an active field, particularly for
early-warning systems. Three lines are relevant here. First, **weekly case forecasting framed as
a time-series problem** with an explicit surveillance focus; Peru (especially Iquitos) is a
recurrent study site [1]. Second, **deep-learning models (LSTM)**, frequently enhanced with
**climate** and **human-mobility** covariates and often deployed in **ensembles**, which tend to
report state-of-the-art accuracy [2, 4, 5]. A reproducible ensemble originally built for Brazil
has been transferred to Peru, producing one-month-ahead incidence estimates at the state level
[3]. Third, **regional reviews and hybrid statistical/ML early-warning systems** [6, 7].

Across this literature, exogenous variables (climate, mobility) are commonly the key driver of
performance, and LSTM frequently emerges as the strongest model. **Our work differs** by using
only the case history of the MINSA national dataset (2000–2024). In this setting and at a
one-week horizon, we show that simple linear models surpass the LSTM because of the very high
short-term autocorrelation of the series. This positions our model as a transparent, reproducible
baseline and suggests that the additional complexity of deep models is justified mainly when
exogenous signals are added.

## 3. Materials and Methods

### 3.1 Dataset

We use the MINSA national dengue epidemiological surveillance dataset (Datos Abiertos, Peru),
covering 2000–2024 with 1,029,421 individual case records and 14 columns (department, province,
district, locality, disease type, year, epidemiological week, ICD-10 code, health directorate,
geocode, age, age unit, sex). Identifier fields (geocode, locality code) are discarded. The
ICD-10 `diagnostic` field is **excluded to prevent data leakage**, as it maps one-to-one with the
clinical severity label.

### 3.2 Target construction and validation

For regression we aggregate the individual records into a **weekly case-count series** by grouping
on (year, epidemiological week) and counting cases, yielding 1,305 continuous weekly observations.
The target is a **direct count of real records**, not a synthetic or imputed value: the sum of the
series equals the number of source records (1,029,421), there are no missing weeks, and manual
spot checks match exactly.

### 3.3 Two notions of "window"

We explicitly distinguish two concepts that behave oppositely:
- **Input window `W`**: number of past weeks used as features. The error **decreases and
  plateaus** as `W` grows (diminishing returns); we select `W` at the elbow.
- **Forecast horizon `H`**: number of weeks ahead predicted. The error **increases
  monotonically** with `H`; we select the largest `H` whose error remains acceptable.

This separation is important: the "error grows with the window" behavior holds for the horizon,
not for the input window. We report both analyses.

### 3.4 Models and evaluation

A supervised dataset is built as `X = [casos_{t-W}, …, casos_{t-1}] → y = casos_{t+H-1}`. We use a
**temporal split** (train on the past, test on the most recent ≈20%), avoiding random splits that
would leak future information. We compare six techniques: Ridge (L2), Lasso (L1), a Multilayer
Perceptron, Random Forest, Gradient Boosting, and an LSTM recurrent network (with standardized
inputs). Performance is measured with **R², RMSE and MAE**, and compared against a **naïve
persistence baseline** (`casos_{t+H} = casos_t`).

### 3.5 Secondary experiments (paradigm comparison)

To justify the regression framing, we also run: (i) **severity classification** (3 classes,
excluding `diagnostic`, with class weighting/SMOTE and macro-F1 / balanced accuracy / per-class
recall), and (ii) **clustering of departments** by epidemiological profile (KMeans/Agglomerative,
evaluated with silhouette and Davies–Bouldin, with PCA visualization), excluding cold Andean
departments with near-zero cases.

## 4. Experiments and Results

### 4.1 Exploratory analysis

The series exhibits a strong upward trend driven by the 2023–2024 outbreak (annual cases rising
from ~63k in 2022 to ~257k and ~272k in 2023–2024), a seasonal profile peaking around
epidemiological week 16, and very high short-term autocorrelation (lag-1 = 0.982).

### 4.2 Window selection

The **input window** error decreases and flattens (RMSE 864 → 671 → 660), giving an elbow at
**W = 3 weeks**. The **forecast horizon** error increases monotonically (RMSE 671 → 1150 → … →
4664; R² turning negative beyond ~8 weeks), giving a reliable horizon of **H = 1 week**.

### 4.3 Model comparison (W = 3, H = 1)

| Model | R² | RMSE | MAE | Beats baseline? |
|---|---|---|---|---|
| **Ridge (L2)** | **0.975** | 671 | 278 | Yes |
| Lasso (L1) | 0.975 | 671 | 278 | Yes |
| MLP (perceptron) | 0.972 | 708 | 297 | Yes |
| LSTM | 0.560 | 2817 | 915 | No |
| Random Forest | 0.444 | 3167 | 1054 | No |
| Gradient Boosting | 0.374 | 3359 | 1128 | No |

*Naïve persistence baseline: R² = 0.959, RMSE = 862, MAE = 383.*

The regularized linear models (Ridge/Lasso) are best and clearly beat the baseline. Tree-based
models fail because they cannot extrapolate beyond the training range during the outbreak. The
LSTM underperforms the linear models at this one-week horizon.

### 4.4 Paradigm comparison

| Paradigm | Main metric | Result | Verdict |
|---|---|---|---|
| Classification (severity) | macro-F1 / recall *Severe* | 0.33 / 0.00 | Not adequate |
| **Regression (time series)** | R² | **0.975** | **Adequate** |
| Clustering (departments) | Silhouette | 0.35 | Weak / not adequate |

Classification provides no usable signal (models predict the majority class; *Severe* recall = 0),
and clustering is weak after removing outlier departments. Regression is the only clearly adequate
paradigm.

## 5. Discussion

Several insights emerge. **(i) Evidence over intuition:** testing the three paradigms with their
own metrics demonstrates, rather than assumes, what the dataset supports. **(ii) Autocorrelation
drives predictability:** the best one-week predictor of cases is the recent case history.
**(iii) The outbreak explains model behavior:** tree-based models fail to extrapolate the
2023–2024 surge while linear autoregressive models follow it. **(iv) Complexity is not always
better:** despite being the reference technique for time series, the LSTM does not beat simple
linear models here, partly because of the unprecedented test-period magnitudes and the absence of
exogenous covariates. **(v) Window semantics matter:** conflating the input window with the
forecast horizon leads to wrong conclusions.

**Limitations.** Counts depend on MINSA passive surveillance (possible underreporting); the
severity classes are extremely imbalanced; and clustering structure is weak even after cleaning.

## 6. Conclusions and Future Work

Using the MINSA national dataset, the data are adequate for **regression / time-series
forecasting** (Ridge, R² = 0.975, beating the naïve baseline), but not for severity classification
(recall of *Severe* = 0) nor clustering (silhouette = 0.35). The best model is a simple,
interpretable regularized linear model, which even surpasses the LSTM at a one-week horizon. The
resulting model can serve as an **early-warning baseline** for dengue outbreaks. Future work
includes providing richer context to the LSTM (longer sequences, more epochs), incorporating
**exogenous variables** (temperature, rainfall, mobility), and producing **department-level**
forecasts.

## References

1. *Weekly dengue forecasts in Iquitos, Peru; San Juan, Puerto Rico; and Singapore.* PMC7567393.
   https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567393/
2. *Assessing dengue forecasting methods: a comparative study of statistical models and machine
   learning techniques in Rio de Janeiro, Brazil.* PMC11984044.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11984044/
3. *A reproducible ensemble machine learning approach to forecast dengue outbreaks.* Scientific
   Reports (2024). https://www.nature.com/articles/s41598-024-52796-9
4. *Dengue forecasting and outbreak detection in Brazil using LSTM: integrating human mobility and
   climate factors.* PMC12657288. https://pmc.ncbi.nlm.nih.gov/articles/PMC12657288/
5. *Prediction of dengue patients using deep learning methods amid complex weather conditions in
   Jaipur, India.* Discover Public Health, Springer (2025).
   https://link.springer.com/article/10.1186/s12982-025-00448-2
6. *Dengue Prediction in Latin America Using Machine Learning and the One Health Perspective: A
   Literature Review.* PMC9611387. https://pmc.ncbi.nlm.nih.gov/articles/PMC9611387/
7. *Bayesian hybrid statistical and machine learning models for dengue forecasting in Bangladesh.*
   medRxiv (2025). https://www.medrxiv.org/content/10.1101/2025.09.14.25335716
