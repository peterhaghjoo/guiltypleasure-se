#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EN-version + hreflang. Körs EFTER build.py: python3 build.py && python3 build_en.py"""
import json, re, pathlib
from build import head, topbar, footer, status_js, hours_table, CITIES, LOGO, MENU_ROWS, fix_amps

ROOT = pathlib.Path(__file__).parent
(ROOT/"en").mkdir(exist_ok=True)

MENU_EN = MENU_ROWS.replace("Ur baren","From the bar").replace("Min stolthet — börja här.","My pride and joy — start here.")\
 .replace("Blodapelsinsorbet, fläder &amp; cava. Brunchens bästa vän.","Blood orange sorbet, elderflower &amp; cava. Brunch's best friend.")\
 .replace("Tequila, jalapeño &amp; lime. Den bits — lagom mycket.","Tequila, jalapeño &amp; lime. It bites — just enough.")\
 .replace("Vodka, kaffelikör &amp; espressogranita — välj Original, Salted Caramel eller Kanelbulle.","Vodka, coffee liqueur &amp; espresso granita — Original, Salted Caramel or Cinnamon Bun.")\
 .replace("Gin, viol, citron, ingefäraskum &amp; salt.","Gin, violet, lemon, ginger foam &amp; salt.")\
 .replace("Viol, citron, ingefäraskum &amp; salt. Hela min No Regrets-lista är alkoholfri, 39–89 kr.","Violet, lemon, ginger foam &amp; salt. My whole No Regrets list is zero-proof, 39–89 SEK.")\
 .replace("Tryck på en rad för detaljer. Hela menyn får du på plats — den byter skepnad med säsongen.",'Tap a row for details. <a href="../meny/index.html">See the full menu →</a> It changes with the seasons.')

EN_DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def en_hours_table(city_key):
    c = CITIES[city_key]
    rows = "".join(
        f'<tr data-d="{(i+1)%7}"><td>{EN_DAYS[i]}</td><td>{h.replace("11.30","11:30")}</td></tr>'
        for i,(_,h) in enumerate(c["hours_txt"]))
    return f'<table class="hours" data-city="{city_key}" aria-label="Opening hours GP\'s {c["name"]}">{rows}</table>'

def en_status(cities_js):
    return (status_js(cities_js)
      .replace("'Öppet nu · stänger '","'Open now · closes '")
      .replace("'Stängt just nu'","'Closed right now'"))

def hub_en():
    url="https://www.guiltypleasure.se/en/"
    title="GP's — Guilty Pleasure Café | Restaurant & bar in Umeå and Sundsvall, Sweden"
    desc="New York-inspired comfort bistro in Umeå (Skolgatan 62) and Sundsvall (Storgatan 12), Sweden. Brunch, dinner & disco — where cravings meet good vibes."
    org = {"@context":"https://schema.org","@type":"Organization","@id":url+"#org",
      "name":"Guilty Pleasure Café","url":"https://www.guiltypleasure.se/",
      "sameAs":["https://www.instagram.com/guiltypleasure.se/","https://www.facebook.com/gpsumea/","https://www.tiktok.com/@guiltypleasure.se"]}
    schema='<script type="application/ld+json">'+json.dumps(org,ensure_ascii=False)+'</script>'
    h = head(title,desc,"/en/",lang="en",extra_schema=schema,fontpath="../fonts/")
    body = (topbar("../").replace('href="../index.html"','href="index.html"',1)
            .replace(">Signaturer<",">Signatures<").replace('aria-label="Huvudmeny"','aria-label="Main menu"')) + f"""
<main id="top">
  <section class="hero wrap">
    {LOGO}
    <div class="eyebrow">New York-inspired comfort bistro · Umeå &amp; Sundsvall, Sweden</div>
    <h1>Where cravings meet good vibes</h1>
    <p class="sub">I serve good mood comfort food, fast — with a cheeky attitude. Brunch, dinner &amp; disco in two cities up north. Life's too short for empty tables.</p>
    <div class="cta-row">
      <a class="btn btn-pink" href="../umea/index.html">GP's Umeå</a>
      <a class="btn btn-pink" href="../sundsvall/index.html">GP's Sundsvall</a>
    </div>
  </section>
  <div class="marquee" aria-hidden="true"><span>BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · </span></div>
  <section class="wrap">
    <div class="kicker">Three acts, every week</div>
    <h2>A day at <span class="accent">GP's</span></h2>
    <div class="acts">
      <article class="act"><span class="tagpill">Act 1</span><h3>Brunch</h3><p>Long mornings, frozen mimosas and comfort classics. Arrive hungry, leave happy.</p></article>
      <article class="act"><span class="tagpill">Act 2</span><h3>Dinner</h3><p>New York bistro meets northern Swedish hospitality. Food comes fast — company stays late.</p></article>
      <article class="act"><span class="tagpill">Act 3</span><h3>Disco</h3><p>When darkness falls, I turn it up. Fridays and Saturdays open till 1 am.</p></article>
    </div>
  </section>
  <section class="wrap" id="signaturer">
    <div class="kicker">From the bar</div>
    <h2>Signatures <span class="accent">&amp; guilty pleasures</span></h2>
    <div class="menucard">{MENU_EN}</div>
  </section>
  <section class="wrap">
    <div class="kicker">Two cities, one soul</div>
    <h2>Pick your <span class="accent">GP's</span></h2>
    <div class="cities">
      <div class="city">
        <h3>Umeå <span class="cstatus" data-city="umea" aria-live="polite">…</span></h3>
        <p>The flagship since 2021. Skolgatan 62, city centre. Walk-ins only — first come, first served. Dogs welcome.</p>
        {en_hours_table("umea")}
        <div class="cta-row" style="justify-content:flex-start"><a class="btn btn-line" href="{CITIES['umea']['maps']}" rel="noopener">Directions</a><a class="btn btn-line" href="mailto:umea@guiltypleasure.se">umea@guiltypleasure.se</a></div>
      </div>
      <div class="city">
        <h3>Sundsvall <span class="cstatus" data-city="sundsvall" aria-live="polite">…</span></h3>
        <p>In the heart of Stenstan at Storgatan 12. Finger-licking good — all day, everyday. Book online or drop by.</p>
        {en_hours_table("sundsvall")}
        <div class="cta-row" style="justify-content:flex-start"><a class="btn btn-fire" href="https://app.bokabord.se" rel="noopener">Book a table</a><a class="btn btn-line" href="{CITIES['sundsvall']['maps']}" rel="noopener">Directions</a></div>
      </div>
    </div>
  </section>
  <section class="igband">
    <div class="wrap" style="padding-top:52px;padding-bottom:52px">
      <div class="kicker">Almost daily</div>
      <h2>Follow <span class="accent">@guiltypleasure.se</span></h2>
      <p>Today's special, new drinks and everything that happens after dark — it drops on Instagram first.</p>
      <a class="btn btn-pink" href="https://www.instagram.com/guiltypleasure.se/" rel="noopener">Follow on Instagram</a>
    </div>
  </section>
</main>
""" + footer("../").replace("Häng med mig","Follow along").replace("Telefon? Min AI-värdinna svarar från augusti. Tills dess: maila eller DM:a.","No phone yet — my AI host answers from August. Until then: email or DM.").replace("Drop-in only — bara kom in.","Walk-ins only — just come in.").replace("Boka bord online</a> — eller kom förbi.","Book a table online</a> — or drop by.").replace("· karta</a>","· map</a>").replace('>karta<','>map<')
    html = h + body
    html = html.replace("</body>", en_status('{"umea":'+CITIES["umea"]["hours_js"]+',"sundsvall":'+CITIES["sundsvall"]["hours_js"]+"}") + "\n</body>")
    return fix_amps(html)

def main():
    (ROOT/"en/index.html").write_text(hub_en(), encoding="utf-8")

    # hreflang: bidirektionell hubb sv<->en + x-default, självrefererande på stadssidor
    HREF_SV = '<link rel="alternate" hreflang="sv" href="https://www.guiltypleasure.se/">\n<link rel="alternate" hreflang="en" href="https://www.guiltypleasure.se/en/">\n<link rel="alternate" hreflang="x-default" href="https://www.guiltypleasure.se/">'
    for f,tag in (("index.html",HREF_SV),("en/index.html",HREF_SV)):
        p=(ROOT/f); s=p.read_text(encoding="utf-8")
        if 'hreflang' not in s:
            s=s.replace('<link rel="canonical"', tag+'\n<link rel="canonical"')
            p.write_text(s, encoding="utf-8")

    # sitemap + verifiering
    sm=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
    if "/en/" not in sm:
        sm=sm.replace("</urlset>",'  <url><loc>https://www.guiltypleasure.se/en/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>\n</urlset>')
        (ROOT/"sitemap.xml").write_text(sm, encoding="utf-8")

    s=(ROOT/"en/index.html").read_text(encoding="utf-8")
    blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    for b in blocks: json.loads(b)
    assert 'lang="en"' in s and "tel:" not in s and "hreflang" in s
    assert "hreflang" in (ROOT/"index.html").read_text(encoding="utf-8")
    print(f"en/index.html: {len(s)//1024} KB, {len(blocks)} schema OK, hreflang OK, sitemap: {'/en/' in sm}")

if __name__ == "__main__":
    main()
