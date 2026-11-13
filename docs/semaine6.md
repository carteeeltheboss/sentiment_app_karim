# Semaine 6 : le paquet, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi le modèle n'est-il pas dans la roue ? Comment le paquet le trouve-t-il ?

Le modèle est un artefact entraîné, avec un cycle de vie distinct du code : on peut
le remplacer sans reconstruire la roue. La roue vérifiée contient uniquement
`api`, `sentiment_app`, `ui` et les métadonnées. `SENTIMENT_MODELE` indique le
chemin du fichier joblib ; en développement, le défaut est
`models/sentiment.joblib` à la racine du dépôt.

## 2. Qu'est-ce qui a changé dans api/model.py quand predict() est entré dans le paquet, et pourquoi est-ce mieux ?

L'API importe `charger_modele` et `predict` depuis `sentiment_app.predict`, sans
modifier `sys.path`. Les imports fonctionnent aussi après installation hors du
dépôt. `src/predict.py` reste un module de compatibilité : il délègue au même
objet Python, ce qui conserve les scripts TP2 et les tests existants.

## 3. La roue installée hors du dépôt : qu'a-t-il fallu lui fournir, et pourquoi scikit-learn est-il épinglé dans pyproject.toml ?

Dans `/tmp/sentiment-tp6-wheel-env`, la roue a installé ses dépendances dans un
environnement neuf. Sans `SENTIMENT_MODELE`, `sentiment predict` termine avec le
code 1 et un message donnant le chemin manquant et les deux remèdes. Avec le
chemin absolu du modèle : `POSITIVE`, score 0.777. Les mots inventés donnent
`INDETERMINE`, score 0.5162. scikit-learn est limité à la série 1.5 dans le paquet
et la CI, car la sérialisation joblib des estimateurs n'est pas garantie entre
versions ; le modèle local et celui de la roue sont utilisés avec 1.5.2.

## Contrôles effectués sur macOS

T35 : les deux échecs attendus du kit ont été observés avant migration.
T37 : tests sans échec, Ruff et mypy passent ; aucune modification de `sys.path`
dans `api/`. T38 : commandes version, prédiction, API et interface vérifiées.
T39 : roue `dist/sentiment_app-0.6.0-py3-none-any.whl` construite et contenu
inspecté : aucun test, donnée, modèle ou répertoire `src`.
T40 : installation et prédictions vérifiées hors du dépôt, sans puis avec modèle.
T41a : fiche modèle complétée à partir des mesures locales, avec ses 14 tests.

Résultat final : 113 passed, 4 xfailed (erreurs connues du jeu d'or), couverture
API 100 %, Ruff et mypy sans erreur. `sentiment serve` et `sentiment ui` ont
chacun répondu HTTP 200 sur leur point de santé. Le workflow GitHub est mis à
jour ; son exécution distante et la publication d'une étiquette Git ne sont pas
effectuées dans cette livraison locale de la roue.
