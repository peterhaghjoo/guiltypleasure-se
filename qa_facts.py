#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAKTAGRIND — körs SIST i bygget, mot hela public/.

Varför den finns
----------------
En extern granskning hittade PÅHITTADE uppgifter live på sajten:

  · "AI-värdinnan svarar från augusti 2026"      — en tjänst som inte finns
  · "Bordsbokning lanseras hösten 2026"          — ett beslut ingen fattat
  · "tio minuters promenad från Umeå Central"    — ett avstånd ingen mätt
  · "Vatten står framme"                         — ett löfte ingen gett
  · "Green Goddess Toast är vegetarisk"          — en härledning, inte ett faktum

Ingen av dem hade en källa. De uppstod i en byggpipeline och gick rakt ut.
Sanerade 2026-07-11 — varje borttaget påstående finns kvitterat i
data/facts/removed.json.

Den här grinden ser till att de aldrig kommer tillbaka. Den granskar VARJE
byggd sida — svenska, engelska, meny, intentionssidor, 404 — och FAILAR bygget
vid träff. Byggets inbyggda grind i build.py räcker inte: den ser bara sina
egna tre sidor, och läckorna hittades i de andra fem.

Regeln
------
Vill du lägga tillbaka ett påstående: skriv först in det i data/facts/ med
källa, status och datum. Sedan — och bara då — får det stå på sajten.
Ett framtidslöfte är ALDRIG ett agentbeslut. Fråga Peter.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
PUBLIC = ROOT / "public"

# (fras, skäl) — matchas skiftlägesokänsligt mot all genererad HTML + llms.txt
FORBJUDET = [
    ("AI-värdinna",         "påhittad tjänst — ingen källa, ingen sådan tjänst finns"),
    ("AI host",             "påhittad tjänst (EN)"),
    ("AI-värdinnan",        "påhittad tjänst"),
    ("augusti 2026",        "påhittat framtidsdatum för telefon"),
    ("August 2026",         "påhittat framtidsdatum (EN)"),
    ("hösten 2026",         "påhittat lanseringsdatum för bordsbokning i Umeå"),
    ("autumn 2026",         "påhittat lanseringsdatum (EN)"),
    ("minuters promenad",   "avståndspåstående utan källa"),
    ("minute walk",         "avståndspåstående utan källa (EN)"),
    ("stenkast",            "avståndspåstående utan källa"),
    ("stone's throw",       "avståndspåstående utan källa (EN)"),
    ("Vatten står framme",  "serviceåtagande utan källa"),
    ("Vatten fixar",        "serviceåtagande utan källa"),
    ("water's already out", "serviceåtagande utan källa (EN)"),
    ("water waiting",       "serviceåtagande utan källa (EN)"),
    ("sort the water",      "serviceåtagande utan källa (EN) — hundvattenfrasen i vi-form, läcka från röstväxlingsarbetet (PR #7)"),
    ("är vegetariska",      "dietmärkning per rätt utan källa — se BACKLOG 2.1"),
    ("are vegetarian",      "dietmärkning per rätt utan källa (EN)"),
    ("39–89",               "prisspann som motsägs av menykällan (No Regrets är 79–99)"),
    ("39-89",               "prisspann som motsägs av menykällan"),
]

# Telefonnummer finns inte. Ingen sida får låtsas annat.
TEL_MONSTER = re.compile(r'tel:|href="tel|\+46\s?\d{2}')


def main():
    if not PUBLIC.exists():
        print("FAKTAGRIND: public/ saknas — kör bygget först.")
        return 1

    sidor = sorted(list(PUBLIC.rglob("*.html")) + list(PUBLIC.glob("*.txt")))
    trafffar = []

    for sida in sidor:
        text = sida.read_text(encoding="utf-8")
        lag = text.lower()
        for fras, skal in FORBJUDET:
            if fras.lower() in lag:
                trafffar.append((sida.relative_to(PUBLIC), fras, skal))
        if TEL_MONSTER.search(text):
            trafffar.append((sida.relative_to(PUBLIC), "telefonnummer", "det finns inget telefonnummer"))

    if trafffar:
        print("\n" + "=" * 70)
        print("FAKTAGRINDEN STOPPADE BYGGET")
        print("=" * 70)
        for sida, fras, skal in trafffar:
            print(f"  {sida}")
            print(f"    '{fras}' — {skal}")
        print("\nSe data/facts/removed.json. Ett påstående utan källa får inte")
        print("publiceras. Skriv in det i faktaregistret först, eller ta bort det.\n")
        return 1

    print(f"faktagrind: {len(sidor)} sidor, {len(FORBJUDET)} förbjudna påståenden, 0 träffar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
