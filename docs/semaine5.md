# Semaine 5 : l'interface Streamlit

**Pourquoi l'interface n'importe-t-elle jamais le modèle ?**
L'interface est un client de l'API, comme n'importe quel programme. Si elle chargeait le fichier .joblib, elle dupliquerait la logique (seuil d'abstention, validation) et il faudrait la modifier à chaque réentraînement ou déplacement du modèle. En passant par l'API, un modèle réentraîné ne demande aucun changement de la page.

**Que montre-t-elle quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?**
Elle affiche « Je ne sais pas » avec la confiance (par exemple 52 % pour des mots inventés) et indique qu'un humain doit trancher. Un verdict forcé aurait affiché « Avis négatif » avec une fausse assurance, alors que le modèle n'avait aucune information.

**Que voit l'utilisateur quand l'API tombe ?**
Un message d'erreur en haut de la page, « API injoignable : lancez d'abord uvicorn api.main:app », dès le rechargement, car la santé de l'API est revérifiée à chaque exécution du script. Le client traduit l'erreur de connexion, la page n'affiche jamais de trace Python.