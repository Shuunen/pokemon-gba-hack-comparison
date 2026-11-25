# Contribuer / Contributing

Le plus simple : ouvre une issue avec le modèle « Proposer ou corriger un hack ». Pour modifier les données toi-même, lis la suite. (EN: the easiest way is an issue using the "Propose or fix a hack" template; to edit the data yourself, see below.)

## Règles

- **GBA uniquement**, hacks terminés ou jouables de bout en bout. Les statuts Alpha, Bêta et En cours sont acceptés dans les fiches (colonne `status`), pas masqués : chacun filtre à sa façon.
- **Aucune ROM, aucun patch** dans le dépôt, ni de lien direct vers un fichier ROM. Lie vers la page de l'auteur ou une page de téléchargement qui en dépend.
- **Les notes sont des jugements sourcés** : indique dans `*_text` la phrase ou la source qui justifie la note (0 à 10, plus c'est haut, mieux c'est pour le joueur : plus facile, moins de grind, plus de confort).
- **Captures** : URL d'images lossless d'origine (PokéHarbor, Hackdex, imgur…). Ne retouche ni ne recompresse aucune image.

## Modifier les données

`data/hacks.db` est une base SQLite (schéma dans `data/schema.sql`). Avec le client `sqlite3` ou n'importe quel éditeur SQLite :

```sql
-- corriger une note (0 à 10) et sa justification
UPDATE hacks SET grind_score = 8, grind_text = 'Sources : ...' WHERE name = 'Nom du hack';

-- ajouter un lien (kind : download, hackdex, retroachievements, forum, officiel)
INSERT INTO hack_links (hack_id, kind, url)
  SELECT id, 'forum', 'https://...' FROM hacks WHERE name = 'Nom du hack';
```

Pour ajouter un hack, insère une ligne dans `hacks` (`name`, `platform = 'GBA'`, `enriched_at` non nul pour qu'il s'affiche) puis remplis les colonnes de notes. Colonnes principales : `difficulty_*`, `grind_*`, `comfort_*`, `visual_*`, `stability_*`, `appreciation_*`, `openworld_*`, `maturity_score`, `status`, `hackdex_downloads`.

Les captures vont dans `data/shots.json` :

```json
"Nom du hack": { "world": ["https://.../monde1.png", "https://.../monde2.png"], "battle": "https://.../combat.png" }
```

Les classements (articles, vidéos) se gèrent dans `load_sources.py` (liste `SOURCES`, alias de noms `ALIASES`).

## Vérifier

```
python3 build_site.py     # doit afficher « dist/index.html écrit »
python3 serve.py 8085     # puis regarder la fiche modifiée sur http://localhost:8085/
```

Décris dans ta pull request ce que tu as changé et la source de chaque nouvelle information.
