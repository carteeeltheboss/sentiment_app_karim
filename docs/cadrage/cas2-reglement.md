# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Répondre aux questions des collaborateurs sur le règlement intérieur en citant l'article concerné.



## Utilisateur final (obligatoire)

Les salariés de l'entreprise et le service des ressources humaines.



## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

RAG : (b) vérifiabilité, chaque réponse cite le passage source du règlement ; (a) il n'existe pas de données étiquetées pour entraîner un modèle, alors que le texte du règlement existe ; (c) le coût par requête reste modéré.



## Données nécessaires et leur origine (obligatoire)

Le texte du règlement intérieur fourni par les RH, découpé en passages indexés, mis à jour à chaque révision du règlement.



## Métrique de succès et seuil d'acceptation (obligatoire)

Au moins 90 % de réponses correctes avec la bonne source citée, mesurées sur 30 questions de test rédigées avec les RH.



## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une mauvaise réponse peut induire une erreur sur un droit ou une obligation : sans source trouvée, l'outil renvoie vers les RH, qui valident les cas sensibles.



## Risques éthiques ou de confidentialité (obligatoire)

Les questions peuvent révéler des situations personnelles : ne pas journaliser le nom de l'employé avec sa question, hébergement interne.



## Approche écartée et pourquoi (facultatif)

