# Fiche modèle : sentiment-app

## Identité du modèle

Paquet sentiment-app 0.6.0 ; pipeline TF-IDF de mots et bigrammes suivi d'une
régression logistique équilibrée, scikit-learn 1.5.2, graine 42. Le modèle a été
recréé le 13 novembre 2026 ; les métriques versionnées de référence datent du
7 novembre 2026 et sont reproduites à l'identique.

## Usage prévu

Prototype pédagogique de tri des avis clients en français, dans le domaine des
produits, livraisons et services. Il aide à préparer une revue des avis ; les
sorties sont POSITIVE, NEGATIVE ou INDETERMINE selon la confiance.

## Usages exclus

Ne pas prendre de décision automatique sur un client, un salarié ou un droit.
Ne pas utiliser pour un diagnostic médical ou une décision juridique, ni pour
prétendre mesurer les émotions d'une personne. Les autres langues et domaines
ne sont pas validés par ce jeu de démonstration.

## Données d'entraînement

Jeu synthétique français généré par `src/make_demo.py` : 290 avis, 145 par classe,
dont 100 mitigés et 30 neutres rattachés à une classe. Découpage stratifié avant
vectorisation : 232 avis d'entraînement et 58 de test. Ce petit vocabulaire
répétitif ne représente ni la diversité des clients ni de vrais avis collectés.

## Performances mesurées

`models/metrics.json` : F1 macro 0.879, exactitude 0.8793, rappel des négatifs
0.931. Sur les 58 avis de test, 7 erreurs sans abstention. Au seuil API de 0.60,
42 avis sont traités (72.4 %), 16 sont envoyés à un humain et 2 erreurs restent
parmi les avis traités. Sur les 20 avis du jeu d'or : 9 justes, 7 abstentions et
4 erreurs franches déjà déclarées. Ces mesures ne valident pas un usage réel.

## Limites connues

Le modèle ne comprend pas la conclusion d'un retournement ni l'ironie. Exemple
du jeu d'or : « Super, encore un colis en retard, merci beaucoup » est classé
POSITIVE à 0.65 malgré le sentiment négatif attendu. Les négations, formulations
inédites et changements de domaine nécessitent une revue humaine.

## Biais mesurés

Mesures du script de biais du kit, sur le même découpage : avis directs,
41 exemples, exactitude 1.000 ; avec retournement, 17 exemples, exactitude
0.588, 7 erreurs, 15 abstentions et 2 erreurs restantes. Avis courts (9 mots ou
moins) : 31 exemples, exactitude 1.000 ; longs : 27, exactitude 0.741. Il s'agit
de groupes linguistiques, sans mesure de biais démographique disponible.

## Explicabilité

Le script SHAP du kit a été exécuté sur le modèle local. Coefficients positifs :
« je » +0.771, « service impeccable » +0.677 ; négatifs : « cassé » -0.923.
Sur l'avis mitigé par défaut du kit, la classe brute est négative à 0.5335 :
base -0.0114, contributions et base donnent -0.1343, exactement le score
logarithmique du modèle. L'API s'abstient sur cet exemple. Les poids décrivent
des associations apprises et non une compréhension du contexte.

## Conditions d'usage

Un humain examine chaque abstention et les avis ironiques ou mitigés, et contrôle
un échantillon des réponses confiantes. Aucune sanction, suppression de plainte
ou décision sur une personne ne doit dépendre de ce seul score. La confiance
affichée n'est pas une garantie de justesse.

## Maintenance

Réentraîner et réévaluer sur des données représentatives en cas de changement
de domaine, de vocabulaire ou de hausse des erreurs. Garder scikit-learn 1.5.2
pour reproduire ce modèle ; valider explicitement toute migration de version.
Fournir le modèle via `SENTIMENT_MODELE`, rejouer les tests, puis actualiser cette
fiche et les métriques à chaque nouvel entraînement.
