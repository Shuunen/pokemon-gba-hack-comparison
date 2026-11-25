"""Génère dist/index.html (données embarquées) à partir de data/hacks.db.
Le calcul du score est fait en JavaScript pour que les poids soient réglables en direct;
la même formule est reproduite en Python (score_py) pour vérification en ligne de commande."""
import json
import math
import os
import sqlite3
from datetime import date

DB = "data/hacks.db"
TODAY = date.today()


def load():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    weights = {r["criterion"]: r["points"] for r in c.execute("select * from weights")}
    hacks = [dict(r) for r in c.execute("select * from hacks where enriched_at is not null and platform in ('GBA','GBA?')")]
    srcs = {r["id"]: dict(r) for r in c.execute("select * from sources")}
    ments = {}
    for r in c.execute("select hack_id, source_id, rank from mentions"):
        ments.setdefault(r["hack_id"], []).append([r["source_id"], r["rank"]])
    return weights, hacks, srcs, ments


def age_factor(published):
    """1.0 si source < 18 mois, 0.5 si plus ancienne, 0.75 si date inconnue."""
    if not published:
        return 0.75
    parts = [int(x) for x in published.split("-")]
    d = date(parts[0], parts[1] if len(parts) > 1 else 6, 1)
    return 1.0 if (TODAY - d).days <= 548 else 0.5


def raw_source_points(ments, srcs):
    tot = 0.0
    for sid, rank in ments:
        s = srcs[sid]
        n = s["list_size"]
        pts = (n - rank + 1) / n if (rank and n) else 0.3
        tot += pts * age_factor(s["published"])
    return tot


def score_py(weights, hacks, srcs, ments):
    allraw = {}
    c = sqlite3.connect(DB)
    for (hid,) in c.execute("select id from hacks"):
        allraw[hid] = math.sqrt(raw_source_points(ments.get(hid, []), srcs))
    mx = max(allraw.values()) or 1
    out = []
    for h in hacks:
        src10 = 10 * allraw[h["id"]] / mx
        parts = {
            "sources": src10, "grind": h["grind_score"], "difficulty": h["difficulty_score"],
            "comfort": h["comfort_score"], "visual": h["visual_user_score"] if h.get("visual_user_rated") and h.get("visual_user_score") is not None else h["visual_score"], "maturity": h["maturity_score"], "stability": h["stability_score"], "appreciation": h["appreciation_score"], "hackdex": h["hackdex_score"], "openworld": h["openworld_score"],
        }
        tot = 100 * sum(weights[k] * (5 if parts[k] is None else parts[k]) / 10 for k in weights) / (sum(weights.values()) or 1)
        out.append((round(tot, 1), h["name"]))
    return sorted(out, reverse=True)


def main():
    weights, hacks, srcs, ments = load()
    c = sqlite3.connect(DB)
    # source brute pour TOUS les hacks (le maximum sert de référence 10/10)
    allraw = {hid: math.sqrt(raw_source_points(ments.get(hid, []), srcs)) for (hid,) in c.execute("select id from hacks")}
    mx = max(allraw.values()) or 1
    for h in hacks:
        h["src10"] = round(10 * allraw[h["id"]] / mx, 2)
        h["nb_sources"] = len(ments.get(h["id"], []))
        h["nb_articles"] = sum(1 for sid, _ in ments.get(h["id"], []) if srcs[sid]["kind"] == "article")
        h["nb_videos"] = h["nb_sources"] - h["nb_articles"]
        h["best_rank"] = min([r for _, r in ments.get(h["id"], []) if r] or [None]) if any(r for _, r in ments.get(h["id"], [])) else None
        h["mentions"] = sorted(
            [{"t": srcs[sid]["title"], "site": srcs[sid]["site"], "u": srcs[sid]["url"], "pub": srcs[sid]["published"], "kind": srcs[sid]["kind"],
              "rank": rank, "n": srcs[sid]["list_size"],
              "pts": round(((srcs[sid]["list_size"] - rank + 1) / srcs[sid]["list_size"] if (rank and srcs[sid]["list_size"]) else 0.3) * age_factor(srcs[sid]["published"]), 2),
              "age": age_factor(srcs[sid]["published"])}
             for sid, rank in ments.get(h["id"], [])],
            key=lambda m: (m["rank"] is None, m["rank"] or 0, -(m["n"] or 0), m["t"]))   # classés par rang (à rang égal: plus grande liste d'abord), puis les « cités »
        h["verified"] = bool(h["verified"])
        h["excluded"] = bool(h.get("excluded"))
        # note « visuel » : la note perso remplace la note par défaut quand l'utilisateur l'a renseignée
        h["visual_rated"] = bool(h.get("visual_user_rated"))
        h["visual_default"] = h["visual_score"]
        if h["visual_rated"] and h.get("visual_user_score") is not None:
            h["visual_score"] = h["visual_user_score"]
    links = {}
    for hid, kind, url in c.execute("select hack_id, kind, url from hack_links order by hack_id, kind, url"):
        links.setdefault(hid, []).append({"kind": kind, "url": url})
    for h in hacks:
        h["links"] = links.get(h["id"], [])
    shots = json.load(open("data/shots.json", encoding="utf-8"))
    for h in hacks:
        s = shots.get(h["name"]) or {}
        h["world"] = s.get("world", [])                       # captures du monde ouvert (colonne de gauche)
        h["shots"] = [h["world"][0] if h["world"] else None, s.get("battle")]
    keep = ["id", "name", "shots", "platform", "base_game", "difficulty_text", "difficulty_score", "visual_text", "visual_score",
            "grind_text", "grind_score", "comfort_text", "comfort_score", "weak_point", "maturity_score",
            "duration_hours", "modern_rules", "gimmicks", "verified", "sources_read", "src10", "nb_sources",
            "nb_articles", "nb_videos", "best_rank", "excluded", "excluded_reason", "stability_score", "stability_text", "stability_verified", "appreciation_score", "appreciation_pct", "appreciation_votes", "appreciation_text", "status", "status_detail", "hackdex_downloads", "hackdex_score", "openworld_score", "openworld_text", "links", "mentions", "visual_rated", "visual_default", "world"]
    hacks = [{k: h.get(k) for k in keep} for h in hacks]
    data = {"weights": weights, "hacks": hacks,
            "stats": {"sources": len(srcs), "articles": sum(1 for s in srcs.values() if s["kind"] == "article"),
                      "videos": sum(1 for s in srcs.values() if s["kind"] == "video"),
                      "total_hacks": c.execute("select count(*) from hacks").fetchone()[0],
                      "fiched": len(hacks)}}
    os.makedirs("dist", exist_ok=True)
    html = open("site_template.html", encoding="utf-8").read().replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))
    open("dist/index.html", "w", encoding="utf-8").write(html)
    print("dist/index.html écrit,", len(hacks), "hacks")
    for i, (s, n) in enumerate(score_py(weights, load()[1], srcs, ments)[:10], 1):
        print(i, s, n)


if __name__ == "__main__":
    main()
