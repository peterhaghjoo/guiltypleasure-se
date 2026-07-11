#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Intentionssidor per ort (BACKLOG 1.2). Körs EFTER build.py och build_menu.py.

Första sidan: /umea/brunch/ — kanonisk sida för "brunch Umeå".

FAKTAKÄLLOR (hitta aldrig på):
- Rätter: docs/menu-content.md, BRUNCH-sektionen. Peter bekräftade 2026-07-11
  att brunchmenyn är IDENTISK i Umeå och Sundsvall (källfilen är Sundsvalls PDF).
- Brunchtider: Peter bekräftade 2026-07-11 — brunch serveras ENDAST lördag och
  söndag. Vardagar är det à la carte.
- Adress/öppettider: CITIES i build.py, som i sin tur kommer ur NAP-källan
  (docs/website-rebuild-design.md §5).

PRISER: tagna ur brunchkällan. Tre rätter saknar pris i källan (Chicken 'n'
Waffle, Green Goddess Toast, Banana Bread Tiramisu) — de listas utan pris tills
Peter fyller i dem (BACKLOG 2.1). Ghost of Prince utelämnad ur dryckeslistan:
brunchkällan säger 159, levande menyn säger 149. Konflikten löses i 2.1.
"""
import json, re, pathlib
from build import head, topbar, footer, CITIES, faq_schema, faq_html, fix_amps, breadcrumbs

ROOT = pathlib.Path(__file__).parent
(ROOT/"umea/brunch").mkdir(parents=True, exist_ok=True)

# (namn, pris, beskrivning) — pris "" = saknas i källan
BRUNCH = [
 ("Bowls", [
  ("Açai Bowl","105","Granola, banan & bär. Innehåller nötter."),
  ("Yoghurt Bowl","119","Bananyoghurt, karamelliserad banan, choklad & granola."),
  ("Tropical Cloud Bowl","129","Jordgubbar, ananas, vattenmelon, blåbär, rostad kokos, mynta, citron & honungsmascarpone."),
  ("Banana Split Bowl","99",""),
 ]),
 ("Sweets", [
  ("French Toast — Banana Biscoff","139","Karamelliserad banan, biscoffsås, vispad grädde, hallon & biscoff crumble."),
  ("French Toast — Dubai Chocolate","125","Dubai pistagekräm, mjukglass, nötellasås, jordgubbar, pistage & kadayif crunch."),
  ("American Pancakes — Strawberry & White Chocolate","119","Jordgubb & vitchokladganache, rostad vitchokladcrunch, jordgubbar. Gör det till en stack +39."),
  ("American Pancakes — Nötella Crunch","119","Nötella, brynt smör, hasselnöts- & cornflakescrunch, jordgubbar. Stack +39."),
  ("Banana Bread Tiramisu","","Bananbröd, kaffe anglaise, mascarponekräm & kakao."),
 ]),
 ("Savoury", [
  ("Chicken 'n' Waffle","","Friterad kyckling, våffla, maple butter, rostad kokos, syltad jalapeño & salladslök."),
  ("Green Goddess Toast","","Levain, smashad avokado, vispad ricotta, tomater, picklad rödlök, chili-lime-fröcrunch & rödbetsgroddar."),
 ]),
 ("House Benedicts — 119", [
  ("Smoked Salmon","119","English muffin, kallrökt lax, krispsallad, pocherat ägg, fluffy hollandaise & gräslök."),
  ("Crispy Bacon","119","English muffin, krispig bacon, krispsallad, pocherat ägg, fluffy hollandaise & gräslök."),
  ("Smashed Avocado","119","English muffin, smashad avokado, krispsallad, pocherat ägg, fluffy hollandaise & gräslök."),
 ]),
 ("Mains", [
  ("Mini Lobster Rolls","199","Brioche, smörstekt hummer, krämig räkröra, skirat smör & gräslök."),
  ("Swedish Räkmacka","239","Räkor, levain, krispsallad, gurka, picklad rödlök, ägg & pepparrotssirap."),
  ("Double Cheeseburger","229","Dubbel smash, cheddar, pickles, svart pepparmajo, karamelliserad lök & fries."),
  ("Caesar Crunch Salad","229","Friterad kyckling, bacon, romansallad, körsbärstomat, rödlök & krisp."),
 ]),
]

# Drycker: bara de vars pris är samstämmigt mellan brunchkällan och levande menyn.
BRUNCH_DRINKS = [
  ("Frozen Blood Orange Mimosa","119","Blodapelsinsorbet, fläder & cava. Brunchens bästa vän."),
  ("Aperol Spritz","129","Aperol, cava & apelsin."),
  ("Bryggkaffe","39","Fri påtår. Kaffe som betyder något."),
]

EXTRAS = "Bacon 49 · Pocherat ägg 39 · Extra lax 99 · Summer truffle fries 75"

def rows(items):
    out = []
    for n, p, d in items:
        price = f'<span class="price">{p}</span>' if p else ""
        body = f"<p>{d}</p>" if d else ""
        out.append(f'<details class="mrow"><summary><b>{n}</b><span class="dots"></span>{price}</summary>{body}</details>')
    return "".join(out)

def cards(groups):
    out = []
    for sek, items in groups:
        out.append(f'<div class="menucard" style="max-width:none;margin-bottom:18px">'
                   f'<div class="mc-head"><span class="tagpill">{sek}</span></div>{rows(items)}</div>')
    return "".join(out)

FAQ = [
  ("När serveras brunch på GP's i Umeå?",
   "Brunchen är en helggrej — lördag och söndag, från öppning klockan 11.30. Vardagar kör jag à la carte i stället."),
  ("Behöver man boka bord för brunch i Umeå?",
   "Nej, jag kör drop-in only på Skolgatan 62 — först till kvarn. Kom tidigt om ni är många; helgförmiddagarna är min paradgren och borden går åt."),
  ("Vad kostar brunchen?",
   "Det finns ingen fast brunchbuffé — du väljer à la carte ur brunchmenyn. Bowls från 99 kronor, House Benedicts 119, pannkakor och french toast 119–139."),
  ("Finns det vegetariskt eller veganskt på brunchen?",
   "Ja. Green Goddess Toast och Smashed Avocado Benedict är vegetariska, och det finns alltid minst ett veganskt alternativ. Fråga mig så löser vi det."),
  ("Får man ta med hunden på brunch?",
   "Ja, hundar är alltid välkomna. Vatten står framme."),
  ("Serverar ni alkoholfritt till brunchen?",
   "Absolut. Hela No Regrets-listan är alkoholfri, och kaffet har fri påtår."),
]

def build():
    c = CITIES["umea"]
    url = "https://www.guiltypleasure.se/umea/brunch/"
    title = "Brunch i Umeå – bowls, pancakes & frozen mimosas | GP's"
    desc = ("Brunch på GP's i Umeå, Skolgatan 62 — lördag & söndag från 11.30. "
            "Bowls, House Benedicts, american pancakes och frozen mimosas. Drop-in only. Hundar välkomna.")

    menu_schema = {"@context":"https://schema.org","@type":"Menu","@id":url+"#menu",
      "name":"GP's brunchmeny — Umeå","inLanguage":"sv",
      "hasMenuSection":[
        {"@type":"MenuSection","name":sek,"hasMenuItem":[
            dict({"@type":"MenuItem","name":n},
                 **({"description":d} if d else {}),
                 **({"offers":{"@type":"Offer","price":p,"priceCurrency":"SEK"}} if p else {}))
            for n,p,d in items]}
        for sek,items in BRUNCH]}

    # Brunchen är ett tidsbegränsat erbjudande — modelleras som en egen
    # OpeningHoursSpecification, inte som ortens generella öppettider.
    event = {"@context":"https://schema.org","@type":"FoodEstablishment",
      "@id":url+"#brunch",
      "name":"Brunch på GP's Umeå",
      "parentOrganization":{"@id":"https://www.guiltypleasure.se/umea/#restaurant"},
      "address":{"@type":"PostalAddress","streetAddress":c["street"],"postalCode":c["postal"],
                 "addressLocality":c["name"],"addressRegion":c["region"],"addressCountry":"SE"},
      "servesCuisine":["Brunch"],
      "acceptsReservations":False,
      "hasMenu":{"@id":url+"#menu"},
      "openingHoursSpecification":[
        {"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday","Sunday"],
         "opens":"11:30","closes":"16:00","name":"Brunch"}],
    }

    schema = ('<script type="application/ld+json">'+json.dumps(menu_schema,ensure_ascii=False)+'</script>'
      + "\n" + '<script type="application/ld+json">'+json.dumps(event,ensure_ascii=False)+'</script>'
      + "\n" + faq_schema(FAQ, url)
      + "\n" + breadcrumbs([("Hem","https://www.guiltypleasure.se/"),
                            ("Umeå","https://www.guiltypleasure.se/umea/"),
                            ("Brunch", url)], url))

    html = head(title, desc, "/umea/brunch/", extra_schema=schema,
                fontpath="../../fonts/", og="og-umea.png") + topbar("../../") + f"""
<main id="top">
  <div class="wrap crumbs"><a href="../../index.html">GP's</a> / <a href="../index.html">Umeå</a> / Brunch</div>
  <section class="hero wrap" style="padding-top:34px;padding-bottom:20px">
    <div class="eyebrow">Brunch i Umeå · Lördag &amp; söndag från 11.30 · Skolgatan 62</div>
    <h1>Brunchen tar inte slut bara för att klockan gör det</h1>
    <p class="sub">Helgerna är min paradgren. Inga sittningar, ingen buffé, ingen stress — du beställer det du vill ha, när du vill ha det, och stannar så länge sällskapet är kul.</p>
    <div class="cta-row">
      <a class="btn btn-pink" href="#brunchmenyn">Brunchmenyn</a>
      <a class="btn btn-line" href="{c['maps']}" rel="noopener">Vägbeskrivning</a>
    </div>
  </section>
  <div class="marquee" aria-hidden="true"><span>LÖRDAG &amp; SÖNDAG · FROZEN MIMOSAS · FRI PÅTÅR · HUNDAR VÄLKOMNA · LÖRDAG &amp; SÖNDAG · FROZEN MIMOSAS · FRI PÅTÅR · HUNDAR VÄLKOMNA · </span></div>

  <section class="wrap">
    <div class="kicker">Så funkar det</div>
    <h2>Brunch <span class="accent">på mitt sätt</span></h2>
    <p class="sub" style="margin:0 0 18px;max-width:62ch">Jag öppnade på Skolgatan 62 år 2021 med en enkel idé: Umeå förtjänade ett ställe där brunchen inte tar slut bara för att klockan gör det. Ingen buffé där maten stått framme sedan tio. Ingen sittning som slutar när du precis kommit igång. Du får din tallrik lagad när du beställer den, och kaffet har fri påtår så länge du sitter kvar.</p>
    <p class="sub" style="margin:0 0 18px;max-width:62ch">Brunchen kör lördag och söndag, från öppning klockan 11.30. Vardagar är det à la carte som gäller — samma kök, andra rätter.</p>
    <div class="facts">
      <div class="fact"><h3>Drop-in only</h3><p>Ingen bordsbokning i Umeå. Först till kvarn — kom tidigt om ni är många.</p></div>
      <div class="fact"><h3>Hundvänligt</h3><p>Hundar är alltid välkomna. Vatten står framme.</p></div>
      <div class="fact"><h3>Frozen mimosas</h3><p>Blodapelsinsorbet, fläder &amp; cava. Brunchens bästa vän — även 0.0 %.</p></div>
    </div>
  </section>

  <section class="wrap surf-moss" id="brunchmenyn">
    <div class="kicker">Lördag &amp; söndag</div>
    <h2>Brunchmenyn <span class="accent">— à la carte</span></h2>
    <p class="sub" style="margin:0 0 22px">Priser i kronor. Lägg till extra: {EXTRAS}. Allergier eller veganskt? Fråga mig, jag hjälper dig.</p>
    {cards(BRUNCH)}
    <div class="menucard" style="max-width:none">
      <div class="mc-head"><span class="tagpill">Till brunchen</span></div>
      {rows(BRUNCH_DRINKS)}
      <div class="mc-foot">Hela drinklistan, vinerna och ölen hittar du på <a href="../../meny/index.html">menysidan →</a></div>
    </div>
  </section>

  <section class="wrap">
    <div class="kicker">Bra att veta</div>
    <h2>Vanliga frågor <span class="accent">om brunchen</span></h2>
    {faq_html(FAQ)}
    <div class="cta-row" style="justify-content:flex-start;margin-top:26px">
      <a class="btn btn-pink" href="../index.html">Allt om GP's Umeå</a>
      <a class="btn btn-line" href="../../meny/index.html">Hela menyn</a>
    </div>
  </section>
</main>
""" + footer("../../")
    return fix_amps(html)

if __name__ == "__main__":
    (ROOT/"umea/brunch/index.html").write_text(build(), encoding="utf-8")

    # Länka in sidan från Umeå-sidan (intern länkning — Google följer den)
    p = ROOT/"umea/index.html"
    s = p.read_text(encoding="utf-8")
    link = '<a class="btn btn-pink" href="brunch/index.html">Brunch lör &amp; sön</a>\n      '
    if 'href="brunch/index.html"' not in s:
        s = s.replace('      <a class="btn btn-line" href="' + CITIES["umea"]["maps"] + '"',
                      '      ' + link + '<a class="btn btn-line" href="' + CITIES["umea"]["maps"] + '"', 1)
        p.write_text(s, encoding="utf-8")

    # sitemap
    sm = (ROOT/"sitemap.xml").read_text(encoding="utf-8")
    if "/umea/brunch/" not in sm:
        sm = sm.replace("</urlset>",
          '  <url><loc>https://www.guiltypleasure.se/umea/brunch/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n</urlset>')
        (ROOT/"sitemap.xml").write_text(sm, encoding="utf-8")

    # ---- kvalitetsgrindar ----
    t = (ROOT/"umea/brunch/index.html").read_text(encoding="utf-8")
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        json.loads(b)
    assert t.count("<h1") == 1, "exakt en h1"
    assert "Skolgatan 62" in t and "11.30" in t
    assert "tel:" not in t, "inget telefonnummer finns än"
    u = (ROOT/"umea/index.html").read_text(encoding="utf-8")
    assert 'href="brunch/index.html"' in u, "Umeå-sidan måste länka till brunchsidan"
    n = sum(len(i) for _, i in BRUNCH)
    utan_pris = [x[0] for _, items in BRUNCH for x in items if not x[1]]
    ord_count = len(re.sub(r"<[^>]+>", " ", t).split())
    print(f"umea/brunch/index.html: {len(t)//1024} KB · {n} rätter · {ord_count} ord · "
          f"4 schema-block OK · sitemap {'/umea/brunch/' in sm}")
    print(f"  Umeå-sidan länkar hit: True")
    if utan_pris:
        print(f"  SAKNAR PRIS (BACKLOG 2.1): {', '.join(utan_pris)}")
