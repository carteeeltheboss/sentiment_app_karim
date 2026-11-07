"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
import sys
from pathlib import Path
from typing import Literal, TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from predict import charger_modele  # noqa: E402  (fonctions du TP2)
from predict import predict as _predict  # noqa: E402

SEUIL_ABSTENTION = 0.60

Etiquette = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class Prediction(TypedDict):
    """Contrat de sortie du classifier."""

    label: Etiquette
    score: float
    text: str


_ETIQUETTES: dict[str, Etiquette] = {"positive": "POSITIVE", "negative": "NEGATIVE"}


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        charger_modele()  # échoue immédiatement si le joblib manque : on ne démarre pas sans modèle

    def predict(self, text: str) -> Prediction:
        """Renvoie le verdict ; sous SEUIL_ABSTENTION l'étiquette devient INDETERMINE."""
        r = _predict(text)  # lève ValueError si le texte est vide
        brut = str(r["label"]).lower()
        if brut not in _ETIQUETTES:
            raise RuntimeError(f"étiquette inconnue renvoyée par le modèle : {brut!r}")
        score = float(r["score"])
        label: Etiquette = "INDETERMINE" if score < SEUIL_ABSTENTION else _ETIQUETTES[brut]
        return {"label": label, "score": score, "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
