"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de sentiment_app.predict, qui charge le modèle une seule fois.
"""
from typing import Literal, TypedDict

from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as _predict

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
    """Construit le classifier (le cache est dans sentiment_app.predict)."""
    return SentimentClassifier()
