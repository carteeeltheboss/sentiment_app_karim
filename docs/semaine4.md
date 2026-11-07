# Semaine 4 : tests approfondis et qualité

## 1. Point de départ

Première mesure : 1 failed (jeu d'or vide). ruff signalait des remarques (B904, I001, F401, B905, E741). mypy ne disait rien, parce que predict() renvoyait un dict.

## 2. Les défauts trouvés et le test qui les a trouvés

| Défaut | Test | Correction |
|---|---|---|
| Un texte d'espaces recevait un 422 dont detail est une chaîne ; hypothesis trouve aussi le caractère x85 | tests/test_limites.py | field_validator dans api/schemas.py, même règle que predict() |
| Des mots inventés reçoivent NEGATIVE avec une confiance de 0,5162 (seule l'ordonnée à l'origine joue) | courbe du seuil, tests/test_jeu_or.py | abstention INDETERMINE sous 0,60 dans api/model.py |
| Une panne ValueError renvoyait un 422 avec le message interne | tests/test_integration.py | toute panne répond 500 sans message interne |

## 3. Courbe du seuil

    Jeu de test : 58 avis (demo)
    
     seuil  répond à   part  exactitude  erreurs  vers un humain
      0.50        58   100%       0.879        7               0
      0.55        47    81%       0.915        4              11
      0.60        42    72%       0.952        2              16
      0.65        41    71%       0.976        1              17
      0.70        37    64%       1.000        0              21
      0.75        29    50%       1.000        0              29
      0.80        13    22%       1.000        0              45
      0.85         6    10%       1.000        0              52
      0.90         0     0%           -        0              58
      0.95         0     0%           -        0              58

Le seuil de 0,60 est un compromis : plus il monte, plus d'avis partent vers un humain ; plus il descend, plus le modèle répond à tout et se trompe sur les avis incertains.

## 4. Jeu d'or

    abstention               INDETERMINE  0.52  attendu POSITIVE  Commande reçue en deux jours, emballage soigné
    juste                    POSITIVE     0.82  attendu POSITIVE  Très bon rapport qualité prix, je recommande
    juste                    POSITIVE     0.74  attendu POSITIVE  Produit conforme à la description, rien à redire
    erreur franche déclarée  NEGATIVE     0.62  attendu POSITIVE  Service client réactif et aimable
    abstention               INDETERMINE  0.58  attendu POSITIVE  Qualité au rendez-vous, livraison rapide
    abstention               INDETERMINE  0.55  attendu NEGATIVE  Article défectueux dès le déballage
    abstention               INDETERMINE  0.59  attendu NEGATIVE  Remboursement jamais reçu, service injoignable
    erreur franche déclarée  POSITIVE     0.70  attendu NEGATIVE  Très déçu, la qualité est médiocre
    juste                    NEGATIVE     0.69  attendu NEGATIVE  Colis perdu et aucune réponse du vendeur
    juste                    NEGATIVE     0.70  attendu NEGATIVE  Matériau fragile, cassé après deux jours
    juste                    POSITIVE     0.62  attendu POSITIVE  Pas déçu du tout, je recommande
    abstention               INDETERMINE  0.52  attendu POSITIVE  Rien à reprocher à ce produit
    abstention               INDETERMINE  0.55  attendu POSITIVE  Ce n'est vraiment pas mauvais pour le prix
    juste                    NEGATIVE     0.63  attendu NEGATIVE  Arrivé cassé, bravo le transporteur
    erreur franche déclarée  POSITIVE     0.65  attendu NEGATIVE  Super, encore un colis en retard, merci beaucoup
    juste                    NEGATIVE     0.79  attendu NEGATIVE  Livraison rapide mais produit cassé à l'arrivée
    abstention               INDETERMINE  0.59  attendu POSITIVE  Un peu cher au début, mais finalement je l'adore
    juste                    POSITIVE     0.60  attendu POSITIVE  Le film est long mais les acteurs sont formidables
    erreur franche déclarée  POSITIVE     0.61  attendu NEGATIVE  Scénario creux et mise en scène ennuyeuse
    juste                    POSITIVE     0.64  attendu POSITIVE  Un restaurant où l'on mange très bien et le service est
    
    Bilan sur 20 avis : abstention 7, erreur franche déclarée 4, juste 9

Les erreurs franches restantes sont déclarées en xfail(strict=True) avec leur raison : le sac de mots ne voit pas le contexte (ironie, vocabulaire d'un autre domaine).

## 5. Couverture, ruff, mypy

    ................................................sss...............x...x. [ 74%]
    .....x...x...............                                                [100%]
    ============================== warnings summary ===============================
    .venv\Lib\site-packages\starlette\testclient.py:37
      C:\Users\Karim\Documents\tpIADEV\sentiment_app_karim\.venv\Lib\site-packages\starlette\testclient.py:37: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
        _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =============================== tests coverage ================================
    _______________ coverage: platform win32, python 3.11.9-final-0 _______________
    
    Name             Stmts   Miss  Cover   Missing
    ----------------------------------------------
    api\main.py         38      0   100%
    api\model.py        28      0   100%
    api\schemas.py      18      0   100%
    ----------------------------------------------
    TOTAL               84      0   100%
    
    1 empty file skipped.
    Required test coverage of 95% reached. Total coverage: 100.00%
    =========================== short test summary info ===========================
    SKIPPED [1] tests\test_git_history.py:29: aucun commit
    SKIPPED [1] tests\test_git_history.py:33: aucun commit
    SKIPPED [1] tests\test_git_history.py:41: aucun commit
    XFAIL tests/test_jeu_or.py::test_pas_d_erreur_franche[ligne-5] - mot positif ou négatif dominant, le sac de mots ne voit pas le contexte
    XFAIL tests/test_jeu_or.py::test_pas_d_erreur_franche[ligne-9] - mot positif ou négatif dominant, le sac de mots ne voit pas le contexte
    XFAIL tests/test_jeu_or.py::test_pas_d_erreur_franche[ligne-16] - mot positif ou négatif dominant, le sac de mots ne voit pas le contexte
    XFAIL tests/test_jeu_or.py::test_pas_d_erreur_franche[ligne-20] - mot positif ou négatif dominant, le sac de mots ne voit pas le contexte
    90 passed, 3 skipped, 4 xfailed, 1 warning in 6.63s

ruff et mypy sont muets. Le bloc __main__ de api/main.py est exclu de la couverture, car il ne peut pas s'exécuter sous pytest.