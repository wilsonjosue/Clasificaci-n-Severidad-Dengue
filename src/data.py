"""Carga y limpieza del dataset de vigilancia de dengue.

Centraliza las rutas y la lógica de limpieza para reutilizarlas desde los notebooks.
Uso desde un notebook en notebooks/:

    import sys; sys.path.append('../src')
    from data import cargar_crudo, normalizar_edad
"""
from pathlib import Path
import pandas as pd

# Raíz del proyecto (un nivel arriba de src/)
RAIZ = Path(__file__).resolve().parents[1]
RUTA_RAW = RAIZ / "data" / "raw" / "datos_abiertos_vigilancia_dengue_2000_2024.csv"
RUTA_PROCESSED = RAIZ / "data" / "processed" / "dengue_limpio_avance1.csv"

# Severidad ordenada (objetivo de clasificación)
ORDEN_SEVERIDAD = {
    "DENGUE SIN SIGNOS DE ALARMA": 0,
    "DENGUE CON SIGNOS DE ALARMA": 1,
    "DENGUE GRAVE": 2,
}
FACTOR_EDAD = {"A": 1.0, "M": 1 / 12, "D": 1 / 365}  # Años, Meses, Días -> años


def cargar_crudo(ruta: Path = RUTA_RAW) -> pd.DataFrame:
    """Carga el CSV original (separador ';', BOM en la cabecera)."""
    return pd.read_csv(ruta, sep=";", encoding="utf-8-sig", dtype=str)


def normalizar_edad(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte 'edad' + 'tipo_edad' a una columna 'edad_anios' en años."""
    df = df.copy()
    df["edad"] = pd.to_numeric(df["edad"], errors="coerce")
    df["edad_anios"] = df["edad"] * df["tipo_edad"].map(FACTOR_EDAD)
    return df


def cargar_procesado(ruta: Path = RUTA_PROCESSED) -> pd.DataFrame:
    """Carga el dataset limpio generado por el notebook de EDA."""
    return pd.read_csv(ruta)
