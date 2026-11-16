# Marketplace Evidentall — refonte UI/UX

Prototypes, audit, spécification et outillage qualité de la refonte du marketplace comparateur de prix Evidentall.

## Contenu

| Dossier | Contenu |
|---|---|
| `prototypes/marketplace.html` | **Prototype complet** (v8) : accueil, rayons, fiche « 1 produit, N offres » par quantité, panier → livraison → paiement, listes de réassort, alertes, commandes, devis labo, comparateur matériel, page partenaire. Un seul fichier, aucune dépendance. |
| `prototypes/comparateur-reference.html` | L'écran de référence isolé : le comparateur par quantité avec les trois réponses. |
| `prototypes/archive/` | Les versions intermédiaires (v1 → v7), pour l'historique des décisions. |
| `docs/audit/` | Audit UI/UX du marketplace en production (16 nov. 2026) avec captures. |
| `docs/spec/` | Spécification développeurs : principes, design system, composants, modèle de données, règles de calcul R1–R9, URLs, accessibilité, prérequis données, tests utilisateurs, plan en 4 lots. |
| `assets/logo/` | Logos Evidentall avec et **sans baseline** (dans l'interface : toujours sans). |
| `ci/` | `tokens.css` (charte, source de vérité des couleurs), lanceur local UXKIN UI Check, mode d'emploi. |
| `.github/workflows/ui-check.yml` | Audit UI automatique sur chaque pull request (UXKIN UI Check). |
| `tests/` | Tests Playwright (desktop 1440 / mobile 390) : erreurs JS, débordements, parcours complets. |

## Ouvrir le prototype

Ouvrir `prototypes/marketplace.html` dans un navigateur. Liens profonds utiles :

- `#accueil` · `#categorie-conso` · `#categorie-ster` · `#categorie-chir`
- `#produit-gants-jet-100` (déplacez la quantité de 10 à 25) · `#produit-masque-3p` · `#produit-pgcl`
- `#panier` (deux avertissements à résoudre) · `#livraison` · `#paiement` (choisir « Virement » pour voir l'erreur)
- `#mes-listes` (onglets Listes · Alertes · Commandes · Devis) · `#devis-travaux` · `#comparer-autoclaves` · `#partenaire-elite-ceram`

Les photos produit sont chargées depuis `https://evidentall.fr/api/marketplace/products/{id}/image` ; hors ligne, les icônes prennent le relais.

## Vérifier

```bash
# Règles UXKIN en local (cloner l'action une fois)
git clone --depth 1 https://github.com/uxkin/ui-check .tools/ui-check
node ci/ui-check-local.mjs --tokens ci/tokens.css prototypes/marketplace.html

# Parcours complets desktop + mobile (Python 3 + playwright + chromium)
pip install playwright && playwright install chromium
python tests/test_marketplace.py
python tests/test_comparateur.py
```

## Charte

Principale `#0077fd` · Accompagnante `#50c3ff` · Secondaire `#032444` · gris froids · Montserrat. Voir `ci/tokens.css` et `docs/spec/` §2–3.
