"""Definición de los 5 modelos a comparar.

Pendiente de completar en el Avance 2. Cada función debe devolver un estimador
(idealmente dentro de un Pipeline con el preprocesamiento) listo para entrenar.
Mantener la misma interfaz para que la comparación sea justa.
"""
from __future__ import annotations


def modelos_a_comparar():
    """Devuelve un dict {nombre: estimador} con los 5 modelos.

    Sugerencia de implementación (Avance 2):
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.svm import SVC
        from sklearn.neural_network import MLPClassifier
        from xgboost import XGBClassifier
    Usar class_weight='balanced' o SMOTE (imblearn) por el desbalance de clases.
    """
    raise NotImplementedError("Definir los 5 modelos en el Avance 2")
