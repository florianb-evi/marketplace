# Audit UI/UX automatique — UXKIN UI Check

## 1. Dans le dépôt du marketplace (pull requests)
Copier `ui-check.yml` dans `.github/workflows/`. À chaque PR, l'action vérifie les lignes ajoutées
et annote directement le diff : lien `href="#"`, image sans `alt`, champ sans label, `outline:none`,
couleur hors tokens, liste sans états chargement/erreur/vide, dégradé violet, emoji en icône, etc.
`fail-on: warning` bloque la fusion dès un avertissement (recommandé pendant la refonte).

Copier `tokens.css` à la racine du front (ou dans `src/styles/`). Son nom contient « tokens » :
les couleurs qu'il définit sont la charte, tout le reste sera signalé.

## 2. En local, sur n'importe quel fichier (prototypes compris)
```bash
git clone --depth 1 https://github.com/uxkin/ui-check .tools/ui-check
node ci/ui-check-local.mjs --tokens ci/tokens.css prototypes/marketplace-proto-v6.html
```
Code de sortie 1 s'il y a une erreur. `--json` pour un rapport exploitable, `--disable id1,id2` pour ignorer une règle.

## 3. Ce que l'action ne voit pas
C'est une vérification du code, pas du rendu. Elle ne juge ni la hiérarchie visuelle, ni la clarté
des textes, ni le parcours. Garder en complément : les tests Playwright (débordement, erreurs JS,
desktop/mobile), un audit axe-core sur le rendu, et les tests utilisateurs de la spécification (§11).

## État des prototypes au 16 nov. 2026
`marketplace-proto-v6.html` et `marketplace-reference-v5.html` : 0 erreur, 0 avertissement avec `tokens.css`.
