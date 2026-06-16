"""Métricas y gráficos de evaluación (clasificación multiclase con desbalance).

Pendiente de completar en el Avance 2. Por el desbalance NO usar solo accuracy:
priorizar F1-macro, balanced accuracy y el recall de la clase 'Grave'.
"""
from __future__ import annotations


def resumen_metricas(y_true, y_pred):
    """Devuelve un dict con accuracy, balanced_accuracy, f1_macro y kappa.

    Sugerencia de implementación (Avance 2):
        from sklearn.metrics import (accuracy_score, balanced_accuracy_score,
                                      f1_score, cohen_kappa_score, classification_report)
    """
    raise NotImplementedError("Definir las métricas en el Avance 2")
