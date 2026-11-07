# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Repérer automatiquement les avis clients négatifs pour les traiter en priorité.



## Utilisateur final (obligatoire)

L'équipe du service client.



## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Machine learning : (a) des milliers d'avis étiquetés sont disponibles, par exemple le jeu Allociné et les avis du site ; (c) le coût par requête d'un modèle TF-IDF est très faible ; (d) une erreur est peu grave, un avis mal classé est simplement relu.



## Données nécessaires et leur origine (obligatoire)

Des avis clients étiquetés positif ou négatif, issus du site et du jeu public Allociné pour l'entraînement.



## Métrique de succès et seuil d'acceptation (obligatoire)

F1 macro d'au moins 0,85 sur un jeu de test tenu à part avant l'entraînement.



## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif manqué est traité plus tard : sous le seuil de confiance, le modèle s'abstient et un humain relit l'avis.



## Risques éthiques ou de confidentialité (obligatoire)

Les avis peuvent contenir des noms ou des coordonnées : les anonymiser avant l'entraînement et ne pas les publier.



## Approche écartée et pourquoi (facultatif)

