"""Ingeniería de variables y codificación para el modelado.

Pendiente de completar en el Avance 2. Aquí van los encoders (One-Hot / Ordinal),
el escalado y la construcción de la matriz de features X y el objetivo y.

NOTA: no incluir 'diagnostic' (CIE-10) como feature -> es fuga de información (leakage),
codifica casi lo mismo que la severidad.
"""
from __future__ import annotations
import pandas as pd

# Variables candidatas a feature (sin identificadores ni leakage)
FEATURES_NUMERICAS = ["ano", "semana", "edad_anios"]
FEATURES_CATEGORICAS = ["sexo", "departamento", "provincia"]
OBJETIVO = "severidad"


def separar_X_y(df: pd.DataFrame):
    """Devuelve (X, y) usando las columnas definidas arriba."""
    X = df[FEATURES_NUMERICAS + FEATURES_CATEGORICAS].copy()
    y = df[OBJETIVO].copy()
    return X, y
