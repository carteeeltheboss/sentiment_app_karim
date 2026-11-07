# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Détecter automatiquement les ordonnances incomplètes (champs obligatoires manquants) avant la délivrance en pharmacie.



## Utilisateur final (obligatoire)

Le pharmacien et le préparateur au comptoir, qui reçoivent l'ordonnance.



## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Règles métier : (b) vérifiabilité totale, chaque refus s'explique par une règle précise ; (d) une erreur sur une ordonnance a des conséquences sanitaires, il faut un comportement déterministe. De plus (a) aucune donnée étiquetée n'est nécessaire et (c) le coût par requête est quasi nul.



## Données nécessaires et leur origine (obligatoire)

Les ordonnances numérisées ou saisies (patient, médecin, date, médicament, posologie), fournies par la pharmacie, et la liste officielle des champs obligatoires.



## Métrique de succès et seuil d'acceptation (obligatoire)

Détection d'au moins 99 % des ordonnances volontairement incomplètes d'un jeu de test, sans aucun oubli toléré sur la posologie et l'identité du patient.



## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un oubli peut provoquer une erreur de dosage : le pharmacien valide toujours l'ordonnance avant la délivrance, l'outil ne fait que signaler.



## Risques éthiques ou de confidentialité (obligatoire)

Ce sont des données de santé personnelles : pas de stockage des ordonnances, traitement en local, accès limité au personnel, conformité RGPD.



## Approche écartée et pourquoi (facultatif)

