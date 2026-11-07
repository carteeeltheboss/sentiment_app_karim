# Semaine 3 : l'API

**Pourquoi l'API refuse-t-elle de démarrer sans modèle plutôt que de répondre 503 ?**
Sans modèle, aucune requête ne peut réussir : le service serait vivant mais inutile. Un échec franc au démarrage (FileNotFoundError, puis Application startup failed) se voit tout de suite dans les journaux et empêche de déployer une API cassée, alors qu'un 503 permanent passerait inaperçu.

**Un texte vide est refusé deux fois, par Pydantic puis par predict() : est-ce redondant ?**
Pas vraiment : les deux protections ont des rôles différents. Pydantic protège l'entrée de l'API et produit le 422 normalisé, predict() protège la fonction du TP2, qui peut être appelée sans l'API (notebook, autre programme). Au TP3, un texte fait d'espaces passait Pydantic et n'était refusé que par predict(), avec un 422 de forme différente : au TP4 la règle est reprise dans le schéma.