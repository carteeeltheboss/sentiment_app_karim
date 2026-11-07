# Semaine 2 : le modèle de sentiment

Le modèle TF-IDF et régression logistique obtient un F1 macro de 0,879 sur 58 avis de test, avec 7 erreurs (2 négatifs classés positifs, 5 positifs classés négatifs), toutes sur des avis mitigés du type « bon début, sauf que ensuite… ».
Un sac de mots compte les mots positifs et négatifs mais ignore leur ordre : il ne voit pas le retournement qui change le sens de l'avis.
Pour corriger, il faudrait un modèle qui garde l'ordre des mots (n-grammes, plongements de phrases ou modèle de langue) et davantage d'avis mitigés à l'entraînement.