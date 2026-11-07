"""Tests d'intégration : l'API telle qu'elle tourne (TP4, étape D)."""
import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import model as api_model
from api.main import app

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle absent : python src/train.py")

AVIS = {"text": "Livraison rapide, produit conforme, très satisfait"}


@pytest.fixture
def predict_mod():
    mod = importlib.import_module("predict")
    mod.charger_modele.cache_clear()
    yield mod
    mod.charger_modele.cache_clear()


def test_demarrage_reel():
    with TestClient(app) as c:
        sante = c.get("/health")
        assert sante.status_code == 200
        assert sante.json()["status"] == "OK"
        assert c.post("/predict", json=AVIS).status_code == 200


def test_refus_de_demarrer_sans_modele(monkeypatch, tmp_path, predict_mod):
    monkeypatch.setattr(predict_mod, "MODELE", tmp_path / "absent.joblib")
    predict_mod.charger_modele.cache_clear()
    with pytest.raises(FileNotFoundError), TestClient(app):
        pass


def test_503_quand_le_modele_est_retire(monkeypatch):
    with TestClient(app) as c:
        monkeypatch.setattr(app.state, "classifier", None)
        assert c.post("/predict", json=AVIS).status_code == 503
        assert c.get("/health").status_code == 503


@pytest.mark.parametrize("erreur", [RuntimeError("panne"), ValueError("bug interne")])
def test_500_sans_message_interne(monkeypatch, erreur):
    with TestClient(app) as c:
        def en_panne(texte):
            raise erreur

        monkeypatch.setattr(app.state.classifier, "predict", en_panne)
        r = c.post("/predict", json=AVIS)
        assert r.status_code == 500
        assert r.json()["detail"] == "Erreur interne du serveur"
        assert str(erreur) not in r.text


def test_refus_d_un_modele_aux_etiquettes_inconnues(monkeypatch):
    clf = api_model.SentimentClassifier()
    monkeypatch.setattr(api_model, "_predict", lambda texte: {"label": "neutral", "score": 0.9})
    with pytest.raises(RuntimeError):
        clf.predict("texte quelconque")