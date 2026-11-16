# Tests

`test_marketplace.py` parcourt le prototype complet : accueil → fiche (quantité 10 → 25) → catégories → panier (avertissements) → paiement (blocages) → confirmation → commandes → devis → recherche, à 1440 et 390 px. Il affiche les erreurs JS, les débordements horizontaux et les résultats clés.

`test_comparateur.py` vérifie l'écran de référence : bascule du classement selon la quantité, tri, HT/TTC.

Prérequis : `pip install playwright && playwright install chromium`. Lancer depuis la racine du dépôt.
