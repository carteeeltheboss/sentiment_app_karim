"""Tests aux limites du contrat d'entrée de POST /predict (TP4, étape B)."""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from api.main import app

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle absent : python src/train.py")

ETIQUETTES = {"POSITIVE", "NEGATIVE", "INDETERMINE"}


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


CAS = [
    pytest.param({"json": {"text": ""}}, 422, id="vide"),
    pytest.param({"json": {"text": "   "}}, 422, id="espaces"),
    pytest.param({"json": {"text": "a"}}, 200, id="un-caractere"),
    pytest.param({"json": {"text": "a" * 2000}}, 200, id="2000"),
    pytest.param({"json": {"text": "a" * 2001}}, 422, id="2001"),
    pytest.param({"json": {}}, 422, id="champ-absent"),
    pytest.param({"json": {"text": 42}}, 422, id="nombre"),
    pytest.param(
        {"content": b"ceci n'est pas du json", "headers": {"Content-Type": "application/json"}},
        422,
        id="pas-du-json",
    ),
]


@pytest.mark.parametrize(("requete", "attendu"), CAS)
def test_contrat_entree(client, requete, attendu):
    r = client.post("/predict", **requete)
    assert r.status_code == attendu
    if attendu == 422:
        detail = r.json()["detail"]
        assert isinstance(detail, list), "un 422 doit avoir la forme FastAPI : detail est une liste"
        assert detail[0]["loc"]
    else:
        assert r.json()["label"] in ETIQUETTES


@settings(max_examples=50, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(texte=st.text(min_size=1, max_size=2000).filter(lambda t: t.strip()))
def test_propriete_texte_valide(client, texte):
    r = client.post("/predict", json={"text": texte})
    assert r.status_code == 200
    corps = r.json()
    assert corps["label"] in ETIQUETTES
    assert 0 <= corps["score"] <= 1


@settings(max_examples=50, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(texte=st.text(alphabet=" \t\n\r\x0b\x0c\x85\u00a0\u2003", min_size=1, max_size=50))
def test_propriete_blancs_refuses(client, texte):
    r = client.post("/predict", json={"text": texte})
    assert r.status_code == 422
    assert isinstance(r.json()["detail"], list)