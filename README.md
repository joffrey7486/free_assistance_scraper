# Free Assistance Scraper

Ce script Python explore automatiquement les pages d’articles de l’assistance Free, extrait les titres valides et génère un PDF récapitulatif.

## Installation

Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

Lancez le script :

```bash
python scraper.py
```

Le script parcourt les pages https://assistance.free.fr/articles/1 à .../2000, extrait les titres valides, puis génère un fichier PDF `free_assistance_articles.pdf` contenant la liste paginée des articles avec titre en gras et lien cliquable.

## Exemple de sortie PDF

```
1. Résilier son abonnement Freebox
   https://assistance.free.fr/articles/52

2. Activer l'option TV
   https://assistance.free.fr/articles/84

... jusqu’à la dernière page trouvée
```

## Bonnes pratiques
- Respecte le serveur avec un délai de 1 seconde entre chaque requête
- Gère les erreurs réseau et les pages inexistantes
- Code modulaire et documenté

---
