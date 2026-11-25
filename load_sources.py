"""Charge les sources (articles / vidéos) et leurs mentions dans data/hacks.db.
Rang 1 = meilleur. rank=None => cité sans classement."""
import re
import sqlite3

DB = "data/hacks.db"

ALIASES = {
    "ashgray": "Ash Gray", "ash gray": "Ash Gray",
    "firered rocket edition": "Rocket Edition", "fire red rocket edition": "Rocket Edition",
    "pokemon rocket edition": "Rocket Edition", "team rocket edition": "Rocket Edition",
    "pokemon rocket edition": "Rocket Edition",
    "team rocket edition dragonsden": "Team Rocket Edition: Dragonsden",
    "emerald kaizo": "Emerald Kaizo", "kaizo emerald": "Emerald Kaizo",
    "adventure red chapter": "Adventure Red Chapter", "adventures red chapter": "Adventure Red Chapter",
    "adventure red": "Adventure Red Chapter", "adventures: red chapter": "Adventure Red Chapter",
    "the last firered": "The Last FireRed", "the last fire red": "The Last FireRed",
    "gaia version": "Gaia", "sword and shield ultimate gba": "Sword and Shield GBA",
    "sword and shield ultimate plus gba": "Sword and Shield GBA",
    "sword and shield gba": "Sword and Shield GBA",
    "sun sky & moon galaxy": "Sun Sky and Moon Galaxy", "sun sky and moon galaxy": "Sun Sky and Moon Galaxy",
    "heart & soul": "Heart & Soul", "heart and soul": "Heart & Soul",
    "dark rising": "Dark Rising", "darkcry": "Dark Cry", "dark cry: the legend of giratina": "Dark Cry",
    "blaze black 2 & volt white 2 redux": "Blaze Black 2 & Volt White 2 Redux",
    "blaze black 2 and volt white 2 redux": "Blaze Black 2 & Volt White 2 Redux",
    "firered extended version": "FireRed Extended", "fire red extended": "FireRed Extended",
    "mega power": "Mega Power", "red++": "Red++",
    "emerald seaglass": "Emerald Seaglass", "aesthetic red": "Aesthetic Red",
    "record keepers": "Recordkeepers", "recordkeepers": "Recordkeepers",
    "mega emerald x & y edition": "Theta Emerald EX", "emerald imperium": "Emerald Imperium",
    "emerald rogue": "Emerald Rogue", "hoen's last wish": "Hoen's Last Wish",
    "mono myth": "Monomyth", "ultra shiny gold sigma": "Ultra Shiny Gold Sigma",
    "light platinum": "Light Platinum",
    "amethyst": "Amethyst Version", "soul gold": "SoulGold", "oops! all eevees": "Oops! All Eevees",
    "cawps": "Cawps", "mega emerald x and y edition": "Theta Emerald EX", "wally quest": "Wally's Quest", "darkviolet": "Dark Violet", "flora": "Flora Sky", "ash grey": "Ash Gray",
    "adventure red": "Adventure Red Chapter", "seaglass": "Emerald Seaglass", "rowe": "R.O.W.E", "r.o.w.e.": "R.O.W.E",
    "team rocket edition dragonsden version": "Team Rocket Edition: Dragonsden", "ephemerald": "Ephemerald",
    "fire red rocket edition": "Rocket Edition", "moemon mega firered": "Moemon Mega FireRed",
    "repurpled edition": "Repurpled Edition", "hoen's last wish": "Hoen's Last Wish",
}

# Plateformes connues hors GBA (stockées pour pouvoir les ignorer plus tard)
NON_GBA = {
    "Uranium": "PC", "Insurgence": "PC", "Reborn": "PC", "Revolution Online": "PC",
    "Infinite Fusion": "PC", "Phoenix Rising": "PC", "Lost World: Echoes of Eternity": "PC",
    "Storm Silver": "DS", "Blaze Black 2 & Volt White 2 Redux": "DS", "HeartGold Generations": "DS",
    "Renegade Platinum": "DS", "Prism": "GBC", "Crystal Clear": "GBC", "Polished Crystal": "GBC",
    "Liquid Crystal": "GBC", "Brown": "GBC", "Red++": "GBC", "Blue Kaizo": "GBC", "Crystal Legacy": "GBC",
    "Crystal Advance Redux": "GBA", "Yu-Gi-Oh PokeDuel": "?", "Digimon Nova Red": "GBA",
    "Platinum Kaizo": "DS", "Revolution Online": "PC", "Renegade Platinum": "DS", "Rejuvenation": "PC", "Blaze Black": "DS", "Bloody Platinum": "DS",
    "Origin Heart Gold": "DS", "Special Pikachu Edition": "GBC", "Perfect Crystal": "GBC", "Polished Crystal": "GBC", "Black Hack": "DS", "Insurgence": "PC",
    "Reborn": "PC", "Infinite Fusion": "PC", "Uranium": "PC", "Phoenix Rising": "PC", "Prism": "GBC", "Brown": "GBC", "Red++": "GBC", "Crystal Clear": "GBC",
    "Liquid Crystal": "GBC", "Light Crystal": "GBC", "Dragon Ball Z Team Training": "?", "Origin Heart Gold": "DS", "GS Vitro": "PC", "Repurpled Edition": "GB",
}


def canon(name: str) -> str:
    n = re.sub(r"^pok[eé]mon\s+", "", name.strip(), flags=re.I).strip()
    n = n.replace("’", "'")
    return ALIASES.get(n.lower(), n)


SOURCES = [
    # (kind, title, url, site, published, list_size, [(rank|None, name), ...])
    ("article", "22 Best Pokemon GBA ROM Hacks for 2026", "https://www.pokemoncoders.com/best-pokemon-gba-rom-hacks/", "PokeCoders", "2025-05-25", 22,
     list(enumerate(["Unbound", "Radical Red", "Glazed", "FireRed Rocket Edition", "Light Platinum", "Gaia", "Emerald Kaizo", "AshGray", "Clover", "Heart & Soul", "Dreamstone Mysteries", "The Last FireRed", "GS Chronicles", "Adventure Red Chapter", "Liquid Crystal", "Orange Islands", "Ultra Shiny Gold Sigma", "FireRed Extended Version", "Sun Sky & Moon Galaxy", "Emerald Rogue", "Saiph", "Dark Rising"], 1))),
    ("article", "5 Best Pokemon ROM Hacks to Play in 2026", "https://comicbook.com/gaming/list/5-best-pokemon-rom-hacks-to-play-in-2026/", "ComicBook.com", "2026-01-21", 5,
     list(enumerate(["Unbound", "Odyssey", "Lazarus", "Super Mariomon", "Pisces"], 1))),
    ("article", "Best Pokemon GBA Rom Hacks: Our Top 10", "https://thatvideogameblog.com/best-pokemon-gba-rom-hacks/", "That Video Game Blog", "2026-03", 10,
     list(enumerate(["Unbound", "Emerald Rogue", "Radical Red", "Rocket Edition", "Gaia", "GS Chronicles", "Glazed", "Orange Islands", "Kaizo Emerald", "Light Platinum"], 1))),
    ("article", "The best Pokemon GBA ROM hacks that you can get right now", "https://win.gg/the-best-pokemon-gba-rom-hacks-that-you-can-get-right-now/", "Win.gg", None, 5,
     [(None, n) for n in ["Unbound", "Ash Gray", "Radical Red", "Elite Redux", "Sword and Shield Ultimate GBA"]]),
    ("article", "20 best Pokemon ROM Hacks of all time, ranked", "https://sportskeeda.com/pokemon/best-pokemon-rom-hacks-time-ranked", "Sportskeeda", None, 20,
     list(enumerate(["Unbound", "Uranium", "Radical Red", "Emerald Rogue", "Prism", "AshGray", "Gaia", "Adventures Red Chapter", "Dark Rising", "Glazed", "Phoenix Rising", "Blaze Black 2 & Volt White 2 Redux", "Infinite Fusion", "Emerald Imperium", "Fire Red Rocket Edition", "Emerald Kaizo", "PokeSouls", "Dark Cry: The Legend of Giratina", "Iridium Version", "Lost World: Echoes of Eternity"], 1))),
    ("article", "Best Pokémon ROM Hacks And Fan Games", "https://www.timeextension.com/guides/best-pokemon-rom-hacks-and-fan-games", "Time Extension", None, 10,
     [(None, n) for n in ["Prism", "Uranium", "Unbound", "Dark Rising", "Phoenix Rising", "Gaia", "Rocket Edition", "Sword and Shield GBA", "Omega Red", "Insurgence"]]),
    ("article", "Top 10 Best Pokemon GBA ROM Hack Games (vote)", "https://www.thetoptens.com/pokemon/pokemon-gba-hack-games/", "TheTopTens", None, 20,
     list(enumerate(["Light Platinum", "Cawps", "Glazed", "Dark Rising", "Korosu", "Adventures Red Chapter", "XYZ", "Ash Gray", "Omega Ruby (GBA)", "Outlaw", "Rocket Edition", "Noon", "Dark Rising 2", "DarkCry", "Eclipse", "Liquid Crystal", "Dark Violet", "Shiny Gold", "Snakewood"], 1))),
    ("article", "Top 10 Best Pokemon GBA ROM Hacks", "https://www.game.guide/best-pokemon-gba-rom-hacks", "Game.Guide", None, 10,
     [(None, n) for n in ["Brown", "Flora Sky", "Liquid Crystal", "Vega", "Gaia", "Prism", "Crystal Clear", "Glazed", "Radical Red", "Unbound"]]),
    ("article", "10 Best Pokemon ROM hacks and fan-made games", "https://dexerto.com/pokemon/10-best-pokemon-rom-hacks-and-fan-made-games-1565547", "Dexerto", "2021-05-03", 10,
     [(None, n) for n in ["Gaia", "Insurgence", "Phoenix Rising", "Revolution Online", "Renegade Platinum", "Prism", "Glazed", "Ash Gray", "Light Platinum", "Adventure Red Chapter"]]),
    ("article", "The Best Pokemon Rom Hacks", "https://www.escapistmagazine.com/the-best-pokemon-rom-hacks/", "The Escapist", None, 5,
     list(enumerate(["Unbound", "Polished Crystal", "Emerald Rogue", "Red++", "Adventure Red"], 1))),
    ("article", "10 best Pokémon ROM hacks for 2023, ranked", "https://dotesports.com/pokemon/news/10-best-pokemon-rom-hacks-ranked", "Dot Esports", "2023", 10,
     list(enumerate(["Unbound", "GS Chronicles", "Crystal Legacy", "Phoenix Rising", "SORS", "Rocket Edition", "Gaia", "Dark Rising", "DarkFire", "Flora Sky"], 1))),
    ("article", "The Top 10 Best Pokemon ROM Hacks", "https://thenerdstash.com/the-top-10-best-pokemon-rom-hacks", "The Nerd Stash", "2022", 10,
     list(enumerate(["Glazed", "Prism", "Emerald Kaizo", "Blue Kaizo", "Renegade Platinum", "Gaia Version", "Radical Red", "Infinite Fusion", "Unbound", "Quetzal"], 1))),
    ("article", "10 Best Pokemon ROM Hacks of All Time", "https://www.pokemoncoders.com/best-pokemon-rom-hacks-of-all-time/", "PokeCoders", None, 10,
     list(enumerate(["Unbound", "Radical Red", "Gaia", "Glazed", "FireRed Rocket Edition", "Liquid Crystal", "Adventure Red Chapter", "Light Platinum", "Ash Gray", "Prism"], 1))),
    ("article", "20 Best Pokemon FireRed ROM Hacks for 2026", "https://www.pokemoncoders.com/best-pokemon-firered-rom-hacks", "PokeCoders", "2026", 20,
     list(enumerate(["Unbound", "Radical Red", "Odyssey", "Dark Violet", "Liquid Crystal", "Dark Rising", "FireRed Rocket Edition", "SORS", "The Last Fire Red", "AshGray", "Gaia", "Adventure Red Chapter", "Sword and Shield Ultimate GBA", "Ultra Violet", "Clover", "Outlaw", "Nameless", "AlteRed", "Aesthetic Red", "Fakemon FireRed"], 1))),
    ("article", "Die besten Pokémon-Rom-Hacks aller Zeiten", "https://www.vodafone.de/featured/article/die-besten-pokemon-rom-hacks-208701", "Vodafone.de", "2026", 5,
     [(None, n) for n in ["Light Platinum", "Gaia", "Glazed", "Dark Rising", "AshGray"]]),
    ("article", "12 meilleurs hacks de ROM Pokémon", "https://www.tenorshare.fr/change-location/meilleurs-pokemon-hacks-rom.html", "Tenorshare.fr", "2025", 11,
     list(enumerate(["Unbound", "Radical Red", "Gaia", "Flora Sky", "Eclipse", "Saffron", "Infinity (RPG Maker)", "Dreams", "Clover", "Dark Rising", "Mega Power"], 1))),
    ("article", "Thousands Vote For The Greatest Pokémon ROM Hacks Ever Made", "https://retrododo.com/thousands-vote-for-the-greatest-pokemon-rom-hacks-ever-made/", "Retro Dodo", "2026-05-11", None,
     [(None, n) for n in ["Lazarus", "Pisces", "Odyssey", "Dreamstone Mysteries", "Aesthetic Red", "Recordkeepers", "Super Mariomon", "Emerald Imperium", "Royal Sapphire", "Ghost Grey", "Heart & Soul"]]),
    ("article", "Les 5 meilleures Rom Hack Pokémon en 2025", "https://www.justgeek.fr/?p=107965", "JustGeek.fr", "2025", 5,
     list(enumerate(["Uranium", "Storm Silver", "AshGray", "Revolution Online", "Reborn"], 1))),
    ("article", "Pokémon Émeraude : les 5 ROM hacks incontournables", "https://booster-breakerz.fr/pokemon-emeraude-les-5-rom-hacks-incontournables-pour-les-fans-de-hoenn", "Booster Breakerz", "2026", 5,
     [(None, n) for n in ["Emerald Legacy", "Elite Redux", "Parallel Emerald", "Emerald Kaizo", "Theta Emerald EX"]]),
    ("article", "50 Best Pokemon ROM Hacks for 2026", "https://www.pokemoncoders.com/best-pokemon-rom-hacks/", "PokeCoders", "2026", 50,
     list(enumerate(["Unbound", "SoulGold", "Quetzal", "Super Mariomon", "Heart & Soul", "Amethyst Version", "Radical Red", "Odyssey", "Emerald Imperium", "Modern Emerald", "HeartGold Generations", "Ghost Grey", "R.O.W.E", "Emerald Seaglass", "Emerald Rogue", "Blaze Black 2 & Volt White 2 Redux", "Sword and Shield Ultimate Plus GBA", "Scorched Silver", "Team Rocket Edition Dragonsden", "Too Many Types 2", "Fakemon FireRed", "Delta Emerald", "Aesthetic Red", "Ambrosia", "Yu-Gi-Oh PokeDuel", "Gaia", "Glazed", "Light Platinum", "Adventures Red Chapter", "Sun Sky and Moon Galaxy", "AshGray", "DarkFire", "Liquid Crystal", "Moon Emerald", "Emerald Horizons", "Sovereign of the Skies", "GS Chronicles", "Fused Dimensions", "Mega Power", "Inclement Emerald", "Polished Crystal", "Prism", "Blazed Glazed", "Gold and Silver 97: Reforged", "Rocket Edition", "FireRed Reignited", "Ultra Shiny Gold Sigma", "Kanlara Ultimate", "Digimon Nova Red", "Sienna"], 1))),
    # --- Vidéos (YouTube) ---
    ("video", 'Official TOP 10 Best Pokemon ROM Hacks of 2026', "https://www.youtube.com/watch?v=Lc_cC7OoYL8", 'YouTube / SacredAlmighty', '2026', 10, [(10, 'Amethyst Version'), (9, 'Homestead'), (8, 'Super Dark Worship'), (5, 'Light Platinum'), (3, 'Origin Heart Gold'), (2, 'Monomyth'), (1, 'Ghost Grey'), (None, 'SoulGold'), (None, 'Platinum Kaizo'), (None, 'GS Vitro')]),
    ("video", 'The 10 BEST Pokemon ROM Hacks You NEED to Play (2026)', "https://www.youtube.com/watch?v=aowpsIPXDDE", 'YouTube / SacredAlmighty', '2026', 10, [(10, 'Heart & Soul'), (8, 'Royal Sapphire'), (5, 'Dreamstone Mysteries'), (4, 'Emerald Imperium'), (3, 'Lazarus'), (2, 'Pisces'), (1, 'Odyssey'), (None, 'Termain'), (None, 'Platinum Redux')]),
    ("video", 'Tier List of 70+ ROM Hacks & Fan Games (tier list)', "https://www.youtube.com/watch?v=x0ACanbSIfw", 'YouTube / SacredAlmighty', '2026', None, []),
    ("video", 'Top 10 COMPLETED GBA Rom Hacks (October 2026)', "https://www.youtube.com/watch?v=jqqB0hjdDr8", 'YouTube / Invincible Greninja', '2026-10', 10, [(None, 'Super Dark Worship'), (None, 'Rhythm'), (None, "Let's Go Pikachu and Eevee"), (None, 'Hyper Emerald Lost Artifacts'), (None, 'World Stadium'), (None, 'Origin Heart Gold')]),
    ("video", 'Top 10 COMPLETED GBA Rom Hacks To Play In 2026', "https://www.youtube.com/watch?v=aLzeSagyMs8", 'YouTube / Invincible Greninja', '2026', 10, [(10, 'Amethyst Version'), (9, 'Valiant'), (8, 'Hyper Emerald Lost Artifacts'), (7, 'Lazarus'), (6, 'Blue Stars 4'), (5, 'R.O.W.E'), (4, 'World Stadium'), (3, 'Fire of Sky'), (2, 'Remnants of War'), (1, 'SoulGold')]),
    ("video", 'TOP 5 BEST POKEMON GBA ROM HACKS (MAY 2026)', "https://www.youtube.com/watch?v=auowDavlWwQ", 'YouTube / Invincible Greninja', '2026-05', 5, [(5, 'Ultra Heart Gold'), (4, 'Xenon'), (3, 'Eirias Chronicles'), (2, "Hoen's Last Wish"), (1, 'Amethyst Version')]),
    ("video", 'Top 5 NEW GBA Rom Hacks & Fangames (Legends Z-A Megas)', "https://www.youtube.com/watch?v=FTT2Jg7v9HM", 'YouTube / Invincible Greninja', '2026', 5, [(1, 'Legends Delta'), (3, 'Synthesis'), (4, 'Unbound'), (None, 'GS Vitro'), (None, 'River Teal')]),
    ("video", 'Top 5 BEST Pokémon GBA ROM Hacks Of September 2026', "https://www.youtube.com/watch?v=193xhZ4BmXc", "YouTube / Gohan's Tips", '2026-09', 5, [(3, 'Wishes of Tomorrow'), (1, 'Hyper Emerald Lost Artifacts'), (None, 'Wild Indigo'), (None, 'Solstice'), (None, 'Azul Agua')]),
    ("video", 'The Actual Best Completed Pokemon ROM Hacks to Play In 2026', "https://www.youtube.com/watch?v=81UK1ExDyFY", 'YouTube / Ayrei', '2026', None, [(None, 'Heart & Soul'), (None, 'Lazarus'), (None, 'Odyssey'), (None, 'Glazed'), (None, 'Gaia'), (None, 'Unbound')]),
    ("video", 'The Top 10 Completed Pokemon ROM Hacks of 2025', "https://www.youtube.com/watch?v=oaaWmbR-jpY", 'YouTube / Ayrei', '2025', 10, [(9, 'HeartGold Generations'), (8, 'Crystal Advance Redux'), (7, 'Dreamstone Mysteries'), (6, 'Royal Sapphire'), (5, 'Pisces'), (4, 'Heart & Soul'), (None, 'Lazarus'), (None, 'Emerald Seaglass'), (None, 'Recordkeepers')]),
    ("video", 'What Is The Best Pokemon ROM Hack For EVERY Generation', "https://www.youtube.com/watch?v=U-uCldX9Ujk", 'YouTube / Ayrei', '2025', None, [(None, 'Odyssey'), (None, 'Unbound'), (None, 'Prism')]),
    ("video", 'The Best Pokemon ROM Hack of 2026, Possibly Ever', "https://www.youtube.com/watch?v=KBnvY1iJD54", 'YouTube / Ayrei', '2026', 1, [(1, 'Monomyth')]),
    ("video", "Ranking Every Completed Pokemon ROM Hack I've Ever Played (tier list)", "https://www.youtube.com/watch?v=PYCxlP3jkr8", 'YouTube / Ayrei', '2025', None, [(None, 'Adventure Red Chapter'), (None, 'Ash Gray'), (None, 'Crystal Clear'), (None, 'Dark Violet'), (None, 'Elite Redux'), (None, 'Emerald Rogue'), (None, 'Emerald Seaglass'), (None, 'FireRed Extended'), (None, 'Flora Sky'), (None, 'Gaia'), (None, 'Glazed'), (None, 'Light Platinum'), (None, 'Liquid Crystal')]),
    ("video", 'Ranking Every Pokemon ROM Hack I Played In 2025 (tier list)', "https://www.youtube.com/watch?v=v1loCOZMzuw", 'YouTube / Ayrei', '2025', None, [(None, 'Lazarus'), (None, 'Odyssey'), (None, 'Pisces'), (None, 'Recordkeepers'), (None, 'Dreamstone Mysteries'), (None, 'Valiant')]),
    ("video", 'The Best Pokemon Fan Games and ROM Hacks of August 2026', "https://www.youtube.com/watch?v=3rLhXViaWhc", 'YouTube / Ayrei', '2026-08', None, []),
    ("video", 'Top 10 BEST Pokemon Rom Hacks to Play In November 2026', "https://www.youtube.com/watch?v=1k9acZE_vRA", 'YouTube / HDvee Plays', '2026-11', 10, [(None, 'Monomyth'), (None, 'Oops! All Eevees'), (None, 'Wishes of Tomorrow'), (None, 'Rhythm'), (None, 'River Teal'), (None, 'Repurpled Edition'), (None, 'GS Vitro'), (None, "Let's Go Pikachu and Eevee"), (None, 'Bug Lime'), (None, 'Emerald Rush')]),
    ("video", 'Top 10 BEST Pokemon Rom Hacks To Play Of All Time', "https://www.youtube.com/watch?v=AaylsHsFBmY", 'YouTube / HDvee Plays', '2023', 10, [(None, 'Prism'), (None, 'Light Platinum'), (None, 'Radical Red'), (None, 'Crystal Clear'), (None, 'Gaia'), (None, 'Ash Gray'), (None, 'Unbound'), (None, 'Uranium'), (None, 'Glazed'), (None, 'Team Rocket Edition')]),
    ("video", 'The Best COMPLETED Pokemon ROM Hacks of November 2026', "https://www.youtube.com/watch?v=G_W6P8Nrp5Y", 'YouTube / A Start Gaming', '2026-11', None, [(None, 'Amethyst Version'), (None, 'Valiant'), (None, 'Nameless'), (None, 'Lazarus'), (None, 'Elysium'), (None, 'Quetzal'), (None, 'Super Dark Worship'), (None, 'Rhythm')]),
    ("video", 'Top 10 Best Pokemon GBA Rom Hacks (April 2026)', "https://www.youtube.com/watch?v=sb1v46tFFsE", 'YouTube / A Start Gaming', '2026-04', 10, [(None, 'Omega Ruby Origins'), (None, 'Kanto Eternal'), (None, 'Duality'), (None, 'Dark Worship'), (None, 'Xenon'), (None, "Hoen's Last Wish"), (None, 'Legends Delta')]),
    ("video", 'Top 10 Must Play Pokemon GBA Rom Hacks (July 2026)', "https://www.youtube.com/watch?v=i-4GK5CHcOo", 'YouTube / A Start Gaming', '2026-07', 10, [(None, 'Quetzal'), (None, 'Mystique')]),
    ("video", 'Top 10 Best Completed Pokemon GBA Rom Hacks (June 2026)', "https://www.youtube.com/watch?v=JIN1F5P1UpE", 'YouTube / A Start Gaming', '2026-06', 10, [(None, 'Heart & Soul'), (None, 'Amethyst Version'), (None, 'Lazarus'), (None, 'Emerald Seaglass'), (None, 'Emerald Rogue'), (None, "Wally's Quest")]),
    ("video", 'LES 10 MEILLEURS ROM HACKS POKEMON DE 2025 (FR)', "https://www.youtube.com/watch?v=DLacRhqe2zA", 'YouTube / Romash', '2025', 10, [(None, 'Pisces'), (None, 'Royal Sapphire')]),
    ("video", 'LES 16 MEILLEURS FAN GAMES POKEMON EN FRANÇAIS DE 2026 (FR)', "https://www.youtube.com/watch?v=lc-mGF2cBBQ", 'YouTube / Romash', '2026', 16, [(None, 'SoulGold'), (None, 'Unbound'), (None, 'Radical Red'), (None, 'Light Platinum')]),
    ("video", 'Tier List of EVERY Fan-Made Pokemon Game (tier list)', "https://www.youtube.com/watch?v=gg3x_MFuU58", 'YouTube / Genosii', None, None, []),
    ("video", 'MA TIERLIST COMPLÈTE DES FANGAMES POKÉMON (tier list FR)', "https://www.youtube.com/watch?v=VamKB5ZEluw", 'YouTube / Fildrong', None, None, []),
    ("video", 'Pro Nuzlocker Ranks The Best Pokemon ROM Hacks', "https://www.youtube.com/watch?v=YUxcXAlrYgo", 'YouTube / pChal', None, None, []),
    ("video", 'Pokemon Rom Hacks Tier List! - Rank The World', "https://www.youtube.com/watch?v=ldJeI9fveWA", 'YouTube / Man Ham Productions', None, None, []),
    ("video", "These are the BEST Pokemon ROM Hacks. Here's Why", "https://www.youtube.com/watch?v=2hRSMkOEWT4", 'YouTube / RetroNC', None, 5, [(None, 'Lazarus'), (None, 'Emerald Seaglass')]),
    ("video", 'I Ranked EVERY Pokemon Rom Hack', "https://www.youtube.com/watch?v=xKEn_8NOebw", 'YouTube / ?', None, 35, []),
    # --- lot 2 (2026-11-25): 20 articles supplémentaires ---
    ("article", "10 Best Pokemon GBA ROM Hacks (2024)", "https://whatifgaming.com/?p=130691", "WhatIfGaming", "2024-01", 10,
     [(None, n) for n in ["Emerald Crest", "Radical Red", "Saiph", "SORS", "GS Chronicles", "Gaia", "Blazed Glazed", "Blazing FireRed", "Stranded", "Elysium"]]),
    ("article", "8 Best Pokemon Emerald ROM Hacks (2023)", "https://whatifgaming.com/?p=126396", "WhatIfGaming", "2023-12", 8,
     [(None, n) for n in ["R.O.W.E", "Blazing Emerald", "Wally Quest", "Inclement Emerald", "Emerald Horizons", "Altered Emerald", "Theta Emerald Renev", "Elite Redux"]]),
    ("article", "8 Best Pokemon FireRed ROM Hacks (2024)", "https://whatifgaming.com/?p=129812", "WhatIfGaming", "2024-02", 8,
     [(None, n) for n in ["DarkViolet", "Mirage Of Tales", "Unbound", "Vega", "Adventures Red Chapter", "Shiny Gold Sigma", "FireRed Rocket Edition", "Liquid Crystal"]]),
    ("article", "10 Best Pokemon ROM Hacks You Can Download for Free", "https://www.hackernoon.com/10-best-pokemon-rom-hacks-you-can-download-for-free-lv2c37hz", "HackerNoon", "2021-07", 10,
     [(None, n) for n in ["Turquoise Version", "The Last FireRed", "Rocket Edition", "Advanced Adventures", "Shiny Gold", "Unbound", "Dreams", "Adventure Red Chapter", "Light Platinum", "Clover"]]),
    ("article", "The 10 Best Pokémon ROM Hacks of All Time", "https://gaminggorilla.com/best-pokemon-rom-hacks", "Gaming Gorilla", "2023-06", 10,
     list(enumerate(["Revolution Online", "Phoenix Rising", "Unbound", "Uranium", "Light Platinum", "Radical Red", "Gaia", "Godra", "Prism", "Brown"], 1))),
    ("article", "10 Best Pokemon ROM Hacks of 2025, Ranked", "https://thegameslayer.com/lists/best-pokemon-rom-hacks-of-2025-ranked/", "The Game Slayer", "2025-12", 10,
     list(enumerate(["Odyssey", "Lazarus", "Super Mariomon", "Heart & Soul", "Dreamstone Mysteries", "Recordkeepers", "Pisces", "Spirits of the Storm", "Hearth", "Valiant"], 1))),
    ("article", "Best Pokémon GBA Gen III ROM Hacks & Fan Games", "https://www.fandomspot.com/best-pokemon-gen3-rom-hacks/", "FandomSpot", "2022-06", 10,
     list(enumerate(["Orange Islands", "Adventure Red", "Saffron", "Rocket Edition", "Gaia", "Nameless", "Glazed", "Clover", "Unbound", "Kaizo Emerald"], 1))),
    ("article", "Top 7 Pokemon Emerald ROM Hacks You Have to Try", "https://thatvideogameblog.com/pokemon-emerald-rom-hacks/", "That Video Game Blog", "2023-12", 7,
     [(1, "Glazed"), (2, "R.O.W.E"), (3, "Inclement Emerald"), (3, "Emerald Kaizo"), (4, "Theta Emerald Renev"), (5, "Emerald Rogue"), (6, "Victory Fire"), (7, "CAWPS")]),
    ("article", "Best Pokémon GBA ROM Hacks of 2024 (Updated List)", "https://goombastomp.com/?p=391585", "Goomba Stomp", "2025-11", 15,
     list(enumerate(["Flora Sky", "Mega Power", "Unbound", "Prism", "Blazed Glazed", "Dark Rising", "Light Crystal", "Light Platinum", "Dark Cry", "Gaia", "Liquid Crystal", "Sword and Shield GBA", "Emerald Rogue", "Ultra Shiny Gold Sigma", "Ash Grey"], 1))),
    ("article", "10 Best Pokémon ROM Hacks For Beginners", "https://thegameslayer.com/lists/best-pokemon-rom-hacks-for-beginners/", "The Game Slayer", "2026-02", 10,
     list(enumerate(["SORS", "Dreamstone Mysteries", "Rocket Edition", "Exceeded", "Gaia", "Blazed Glazed", "Heart & Soul", "Dreams", "Unbound", "Lazarus"], 1))),
    ("article", "20 Best Pokemon Emerald ROM Hacks to Try in 2026", "https://www.pokemoncoders.com/best-pokemon-emerald-rom-hacks/", "PokeCoders", "2026-07", 20,
     list(enumerate(["Glazed", "Heart & Soul", "Mega Power", "Pisces", "Resolute", "R.O.W.E", "Dreamstone Mysteries", "Lazarus", "Emerald Imperium", "Super Mariomon", "Seaglass", "Too Many Types", "Team Rocket Edition Dragonsden Version", "Emerald Rogue", "Emerald Crest", "Mega Emerald X and Y Edition", "Ephemerald", "Theta Emerald EX", "Blazing Emerald", "Emerald Kaizo"], 1))),
    ("article", "30 Best Pokémon ROM Hacks in 2023", "https://progameguides.com/pokemon/30-best-pokemon-rom-hacks/", "Pro Game Guides", "2023-07", 30,
     list(enumerate(["Renegade Platinum", "Insurgence", "Radical Red", "Infinite Fusion", "Rejuvenation", "Unbound", "Blaze Black", "Reborn", "GS Chronicles", "Emerald Kaizo", "Soulstones", "Emerald Trash Lock", "Inclement Emerald", "Team Rocket Edition", "Flora Sky", "SORS", "Liquid Crystal", "Uranium", "Fused Dimensions", "Glazed", "Eclipse", "Vega", "Fool's Gold", "Prism", "Phoenix Rising", "Fire Omega", "Bloody Platinum", "Rising Ruby", "Neo X", "Dark Rising"], 1))),
    ("article", "10 Best Pokemon GBA ROM Hacks", "https://attackofthefanboy.com/articles/best-pokemon-gba-rom-hacks/", "Attack of the Fanboy", "2023-01", 10,
     [(1, "GS Chronicles"), (2, "Dark Rising"), (3, "Flora Sky"), (4, "Unbound"), (5, "Radical Red"), (6, "Orange Islands"), (8, "Gaia"), (9, "Moemon Mega FireRed"), (10, "Rocket Edition")]),
    ("article", "14 Best Pokémon ROM Hacks Of 2026 [All Tested]", "https://retrododo.com/best-pokemon-rom-hacks", "Retro Dodo", "2026-11", 14,
     [(None, n) for n in ["Lazarus", "Origin Heart Gold", "Unbound", "Prism", "Radical Red", "Glazed", "Monomyth", "Special Pikachu Edition", "Crystal Clear", "Dark Energy", "Bronze", "Perfect Crystal", "Light Platinum", "Gaia"]]),
    ("article", "17 Best GBA ROM Hacks To Download Today", "https://retrododo.com/best-gba-rom-hacks/", "Retro Dodo", "2025-07", 17,
     [(2, "Ash Gray"), (4, "Unbound"), (6, "Snakewood"), (8, "Gaia"), (11, "GS Chronicles"), (15, "Sword and Shield GBA"), (17, "Glazed")]),
    ("article", "Top 10 Best Pokémon Rom Hacks of All Time 2026", "https://nerdbear.com/best-pokemon-rom-hacks", "NerdBear", "2026-10", 10,
     list(enumerate(["Flora Sky", "Gaia", "Adventures Red Chapter", "Ash Gray", "Ultra Shiny Gold Sigma", "Liquid Crystal", "Blazed Glazed", "Glazed", "Light Platinum", "Theta Emerald EX"], 1))),
    ("article", "19 Best Pokémon ROM Hacks of ALL TIME", "https://thatvideogameblog.com/best-pokemon-rom-hacks/", "That Video Game Blog", "2023-12", 19,
     [(None, n) for n in ["Dark Rising", "Gaia", "Glazed", "Blazed Glazed", "Brown", "Prism", "Light Platinum", "Dark Cry", "Phoenix Rising", "Omega Red", "Ash Gray", "Insurgence", "Team Rocket Edition", "Mega Emerald X and Y Edition", "Unbound", "Clover", "Mega Power", "Saffron", "Adventure Red"]]),
    ("article", "The 10 Best Pokémon GBA ROM Hacks", "https://gaminggorilla.com/best-pokemon-gba-rom-hacks", "Gaming Gorilla", "2023-07", 10,
     list(enumerate(["Unbound", "Radical Red", "Mega Power", "Light Platinum", "Dark Rising", "Gaia", "Emerald Rogue", "Ultra Shiny Gold Sigma", "Glazed", "Liquid Crystal"], 1))),
    ("article", "10 Hacks de Pokémon Que Todo Fã Deveria Jogar", "https://criticalhits.com.br/games/10-hacks-de-pokemon-que-todo-fa-deveria-jogar/", "Critical Hits", "2026-11", 10,
     [(None, n) for n in ["Unbound", "Super Mariomon", "Lazarus", "Rocket Edition", "Emerald Rogue", "Dragon Ball Z Team Training", "Adventures Red Chapter", "Light Platinum", "Recordkeepers", "Pisces"]]),
    ("article", "The Easiest Pokémon ROM Hacks For Beginners", "https://www.fandomspot.com/easiest-pokemon-rom-hacks/", "FandomSpot", "2022-06", 10,
     list(enumerate(["Dreams", "Gaia", "Crystal Clear", "Polished Crystal", "Red++", "Light Platinum", "Blazed Glazed", "Orange Islands", "Black Hack", "Flora Sky"], 1))),
]


def main():
    c = sqlite3.connect(DB)
    c.execute("PRAGMA foreign_keys = ON")
    c.execute("DELETE FROM mentions")
    c.execute("DELETE FROM sources")
    for kind, title, url, site, pub, size, ments in SOURCES:
        cur = c.execute("INSERT INTO sources(kind,title,url,site,published,list_size) VALUES(?,?,?,?,?,?)",
                        (kind, title, url, site, pub, size))
        sid = cur.lastrowid
        for rank, raw in ments:
            name = canon(raw)
            plat = NON_GBA.get(name, "GBA?")
            c.execute("INSERT OR IGNORE INTO hacks(name, platform) VALUES(?,?)", (name, plat))
            hid = c.execute("SELECT id FROM hacks WHERE name=?", (name,)).fetchone()[0]
            c.execute("INSERT OR IGNORE INTO mentions VALUES(?,?,?)", (hid, sid, rank))
    c.commit()
    print("sources:", c.execute("select kind,count(*) from sources group by kind").fetchall())
    print("hacks:", c.execute("select count(*) from hacks").fetchone()[0])
    print("top mentions:", c.execute("""select h.name,h.platform,count(*) n from hacks h join mentions m on m.hack_id=h.id
        group by h.id order by n desc limit 12""").fetchall())


if __name__ == "__main__":
    main()
