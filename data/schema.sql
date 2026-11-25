PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS hacks (
  id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, aliases TEXT,
  platform TEXT NOT NULL DEFAULT 'GBA', base_game TEXT, content TEXT,
  difficulty_text TEXT, difficulty_score REAL,
  visual_text TEXT, visual_score REAL,
  grind_text TEXT, grind_score REAL,
  comfort_text TEXT, comfort_score REAL,
  weak_point TEXT, maturity_text TEXT, maturity_score REAL,
  languages TEXT, has_french INTEGER DEFAULT 0,
  duration_hours TEXT, modern_rules TEXT, gimmicks TEXT, emulator_notes TEXT,
  url TEXT, verified INTEGER DEFAULT 0, notes TEXT,
  enriched_at TEXT, sources_read TEXT,
  excluded INTEGER DEFAULT 0, excluded_reason TEXT, excluded_at TEXT,
  stability_score REAL, stability_text TEXT, stability_verified INTEGER DEFAULT 0,
  status TEXT, status_detail TEXT,
  hackdex_downloads INTEGER, hackdex_score REAL, openworld_score REAL, openworld_text TEXT, visual_user_score REAL, visual_user_rated INTEGER NOT NULL DEFAULT 0,
  appreciation_pct REAL, appreciation_votes INTEGER, appreciation_score REAL, appreciation_text TEXT
);
CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY, kind TEXT NOT NULL CHECK(kind IN ('article','video')),
  title TEXT, url TEXT UNIQUE NOT NULL, site TEXT, published TEXT, list_size INTEGER
);
CREATE TABLE IF NOT EXISTS mentions (
  hack_id INTEGER NOT NULL REFERENCES hacks(id), source_id INTEGER NOT NULL REFERENCES sources(id),
  rank INTEGER, PRIMARY KEY (hack_id, source_id)
);
CREATE TABLE IF NOT EXISTS weights (criterion TEXT PRIMARY KEY, points REAL NOT NULL);
INSERT OR REPLACE INTO weights VALUES ('sources',10),('grind',9),('difficulty',9),('comfort',9),('visual',6),('stability',7),('appreciation',5),('hackdex',3),('maturity',2),('openworld',4);

CREATE TABLE IF NOT EXISTS hack_links (hack_id INTEGER NOT NULL REFERENCES hacks(id), kind TEXT NOT NULL, url TEXT NOT NULL, PRIMARY KEY (hack_id, url));
