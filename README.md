# Comparatif des hacks Pokémon GBA / Pokémon GBA ROM hack comparison

![logo](logo.svg)

[![Project license](https://img.shields.io/github/license/Shuunen/pokemon-gba-hack-comparison.svg?color=informational)](https://github.com/Shuunen/pokemon-gba-hack-comparison/blob/master/LICENSE)
[![Visitors](https://hits.sh/github.com/Shuunen/pokemon-gba-hack-comparison.svg?label=visitors&color=informational)](https://hits.sh/github.com/Shuunen/pokemon-gba-hack-comparison/)

**FR** · [English below](#english)

Un site de comparaison de plus de 100 hacks Pokémon jouables sur GBA : recommandations des classements en ligne, difficulté, grind, confort, visuel, stabilité, appréciation des joueurs, popularité sur Hackdex et monde ouvert. Tout est filtrable par plages de notes et le score est pondéré selon tes priorités.

- **Tes choix restent chez toi** : poids, filtres, exclusions et notes de visuel sont enregistrés dans le `localStorage` de ton navigateur. Le site n'a ni compte ni serveur.
- **Filtres partageables** : le bouton « Copier le lien des filtres » met tes filtres dans l'adresse de la page.
- **Aucune ROM n'est hébergée.** Le site ne fait que lier vers les pages de leurs auteurs.

## Lancer en local

Python 3 suffit, aucune dépendance.

```
python3 serve.py 8085      # puis ouvrir http://localhost:8085/
```

Le serveur reconstruit la page et recharge l'onglet quand la base, le template ou `data/shots.json` changent. Pour générer seulement le site : `python3 build_site.py` (résultat dans `dist/`).

## Déployer

`netlify.toml` configure Netlify : commande `python3 build_site.py`, dossier publié `dist`. N'importe quel hébergeur statique convient : il suffit de publier `dist/`.

## Structure

| Chemin | Rôle |
|---|---|
| `build_site.py` | Génère `dist/index.html` à partir de la base |
| `site_template.html` | Interface (cartes, filtres, poids, notes) |
| `serve.py` | Serveur local en lecture seule avec rechargement automatique |
| `load_sources.py` | Recharge les sources (articles, vidéos) et leurs classements dans la base |
| `data/hacks.db` | Source de vérité : fiches, notes, liens, sources |
| `data/schema.sql` | Schéma de la base et poids par défaut |
| `data/shots.json` | Captures de chaque hack (URL) : monde ouvert et combat |
| `dist/` | Généré, non versionné |

## Comment le score est calculé

Chaque critère est noté de 0 à 10 (une info manquante vaut 5). Le score est la moyenne pondérée de ces notes, ramenée sur 100, avec des poids de 0 à 10 réglables dans l'interface. Les « Recommandations » comptent les mentions dans les classements : plus le rang est haut, plus la mention vaut de points, avec un bonus pour les sources récentes.

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md) : ajouter ou corriger un hack, une source, une capture.

## Mentions

Projet de fans, sans lien avec Nintendo, Game Freak, The Pokémon Company ni les créateurs des hacks. Les captures d'écran appartiennent à leurs auteurs. Le code est sous la licence du fichier `LICENSE` ; les données et images restent soumises aux droits de leurs sources (voir [Thanks](#thanks)). Une erreur ou une demande de retrait : ouvre une issue.

---

## English

A comparison site for 100+ Pokémon ROM hacks playable on GBA: recommendations from online rankings, difficulty, grind, comfort, visuals, stability, player appreciation, Hackdex popularity and open-world feel. Everything can be filtered by score ranges, and the overall score is weighted by your own priorities.

- **Your choices stay with you**: weights, filters, exclusions and visual ratings live in your browser's `localStorage`. There is no account and no backend.
- **Shareable filters**: the "Copy filter link" button puts your filters in the page URL.
- **No ROMs are hosted.** The site only links to the authors' pages.

### Run locally

Python 3 is enough, no dependencies.

```
python3 serve.py 8085      # then open http://localhost:8085/
```

To only build the site: `python3 build_site.py` (output in `dist/`).

### Deploy

`netlify.toml` is provided (build command `python3 build_site.py`, publish directory `dist`). Any static host works: publish `dist/`.

### How the score works

Each criterion is rated 0–10 (missing data counts as 5). The score is the weighted average of those ratings, scaled to 100, with 0–10 weights you can change in the UI. "Recommendations" counts mentions in online rankings: the higher the rank, the more points, with a bonus for recent sources.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

### Notices

Fan project, not affiliated with Nintendo, Game Freak, The Pokémon Company or the hack authors. Screenshots belong to their authors. Code is under the `LICENSE` file; data and images remain subject to their sources' rights (see [Thanks](#thanks)). For a mistake or a takedown request, open an issue.

## Thanks

- [Boxy Svg](https://boxy-svg.com) : simple & effective svg editor
- [Claude Code](https://claude.com/claude-code) : pair programming and data collection help
- [GameBrew](https://gamebrew.org) : hack pages and screenshots
- [Github](https://github.com) : for all their great work year after year, pushing OSS forward
- [Hackdex](https://www.hackdex.app) : download counts, tags and screenshots of the hacks
- [Hits.sh](https://hits.sh) : for the visitors badge on top of this readme
- [Imgur](https://imgur.com) : screenshot hosting
- [Netlify](https://netlify.com) : awesome company that offers free CI & hosting for OSS projects
- [Pokécommunity](https://www.pokecommunity.com) and [PokéCoders](https://www.pokemoncoders.com) : hack release threads, official screenshots and the community behind the hacks
- [PokéHarbor](https://www.pokeharbor.com) : hack pages, downloads, screenshots and player reactions
- [Python](https://www.python.org) and [SQLite](https://www.sqlite.org) : the whole data pipeline with zero dependency
- [RetroAchievements](https://retroachievements.org) : game pages and in-game screenshots
- [Shields.io](https://shields.io) : for the nice badges on top of this readme
- [Svg Omg](https://jakearchibald.github.io/svgomg/) : the great king of svg file size reduction
- The ROM hackers : every hack compared here is the work of passionate authors, and the ranking articles and videos listed on the site
