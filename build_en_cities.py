#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EN-stadssidor (en/umea/, en/sundsvall/) + hreflang per stad.
Körs SIST: python3 build.py && python3 build_en.py && python3 build_menu.py && python3 build_en_cities.py"""
import json, re, pathlib
from build import head, topbar, footer, CITIES, rest_schema, faq_schema, faq_html, fix_amps
from build_en import MENU_EN, en_hours_table, en_status

ROOT = pathlib.Path(__file__).parent
(ROOT/"en/umea").mkdir(parents=True, exist_ok=True)
(ROOT/"en/sundsvall").mkdir(parents=True, exist_ok=True)

def en_topbar():
    # topbar("../") ger redan rätt relativa mål inne i /en/<stad>/ (../index.html -> /en/)
    t = topbar("../").replace('aria-label="Huvudmeny"','aria-label="Main menu"').replace(">Signaturer<",">Signatures<")
    t = t.replace('<a href="../umea/index.html">Umeå</a>',
                  '<a href="../../meny/index.html">Menu</a>\n      <a href="../umea/index.html">Umeå</a>')
    return t

def en_footer():
    return (footer("../")
      .replace("Häng med mig","Follow along")
      .replace("Telefon? Min AI-värdinna svarar från augusti. Tills dess: maila eller DM:a.","No phone yet — my AI host answers from August. Until then: email or DM.")
      .replace("Drop-in only — bara kom in.","Walk-ins only — just come in.")
      .replace("Boka bord online</a> — eller kom förbi.","Book a table online</a> — or drop by.")
      .replace("· karta</a>","· map</a>").replace('>karta<','>map<'))

def rest_schema_en(city_key):
    s = rest_schema(city_key, f"https://www.guiltypleasure.se/en/{city_key}/")
    for a,b in (
        ('"Signaturer ur baren"','"Signatures from the bar"'),
        ('"Gin, viol, citron, ingefäraskum & salt"','"Gin, violet, lemon, ginger foam & salt"'),
        ('"Blodapelsinsorbet, fläder & cava"','"Blood orange sorbet, elderflower & cava"'),
        ('"Tequila, jalapeño & lime"','"Tequila, jalapeño & lime"'),
        ('"Alkoholfri signatur — viol, citron, ingefäraskum & salt"','"Zero-proof signature — violet, lemon, ginger foam & salt"'),
    ): s = s.replace(a,b)
    return s

UMEA_STORY_EN = """
<p class="lead">I opened at Skolgatan 62 in 2021 with one simple idea: Umeå deserved a place where brunch doesn't end just because the clock does.</p>
<p>Since then I've been the city's New York-inspired comfort bistro — the flagship of the Guilty Pleasure family. My day starts with frozen mimosas and comfort classics, slides into dinner when the afternoon runs out of steam, and ends — on weekends — in something best described as disco. Fridays and Saturdays I keep going until 1 am, and yes, you'll notice.</p>
<p>You'll find me in the middle of central Umeå, a stone's throw from Rådhustorget and a ten-minute walk from Umeå Central station. Bringing the dog? Bring the dog — water's already out. Coming with a big group on a Saturday? Come early. I run walk-ins only, first come, first served, and it's a principle I'm proud of: life is too short for empty tables reserved for people who never show up. Table booking launches this autumn for the planners among you — but spontaneity will always come first here.</p>
<p>The bar is my stage. The signature is called Ghost of Prince — gin, violet, lemon, ginger foam and salt — and if you're not drinking alcohol you won't be parked on some sad substitutes' bench: my whole No Regrets list is built with the same love, from Virgin Prince to zero-proof Coffee Granita in three flavours. The coffee? Obviously. That's why the sign says Café.</p>
<p>Umeå is a city that wakes up late and stays up late on weekends. I'm built for exactly that.</p>

<p>What do I mean by comfort food? Think of the food you actually crave — generous, hot, a little indecently good — cooked properly and served without delay. The New York diner is the blueprint: high tempo in the kitchen, low tempo at the tables. You can make it here on your lunch break if you want to, but nobody will look at you sideways if you stay until closing. That's the whole point of the word pleasure in my name — and the word guilty you should take with a pinch of salt. Or a salted rim, like on the margarita.</p>
<p>Weekends are my main event. Brunch rolls from opening — frozen mimosas, coffee that means something, and comfort classics until the afternoon gives up. Then I change costume: the lights drop, the playlist wakes up, and anyone who stays finds out why the third act is called disco. No dress code, no guest list — just a mood that keeps climbing until closing time.</p>
<p>I'm part of the Guilty Pleasure family, with a sister in Sundsvall and the same four colours in my soul: fire, disco, moss and cream. But Umeå is where it all began in 2021, and this is where the flag stands. Come by and you'll understand.</p>
"""

SUNDSVALL_STORY_EN = """
<p class="lead">In the middle of Stenstan, at Storgatan 12, I serve finger-licking good food and drinks — all day, everyday.</p>
<p>I'm Sundsvall's slice of the Guilty Pleasure family: the same New York-inspired comfort bistro soul as the flagship in Umeå, but with a rhythm of my own. The stone houses of Stenstan and the pulse of Storgatan set the tone — you come here for a long weekend brunch, a dinner in no particular hurry, or a Friday night that grows into something more. Fridays and Saturdays I'm open until 1 am.</p>
<p>Unlike my sister up north, I take table bookings — book online and your table is ready when you arrive. But the door is just as open if you're simply passing by: walk-ins are always welcome, and the bar always has room for one more. Dogs? Welcome, always. I'll sort the water.</p>
<p>The bar works the same magic as in Umeå: Ghost of Prince is the signature, Frozen Blood Orange Mimosa owns the brunches, and the whole No Regrets list is properly alcohol-free — not an afterthought. The menu changes with the seasons, so ask what's new.</p>
<p>Sundsvall has always known how to have a good time. I'm just the place where it happens.</p>

<p>A practical word of advice: on weekend evenings it's smart to book — Stenstan fills up fast and my tables are popular. Weekday lunches and afternoons, walk-ins almost always work. Coming as a bigger group? Email me at sundsvall@guiltypleasure.se and we'll sort it out together. And follow @guiltypleasure.se on Instagram — that's where the news drops first, almost every day.</p>
<p>Comfort food my way means food without fuss but with full effect — New York diner in the soul, northern Sweden in the heart. Come for lunch, come for dinner, just come. The tempo in the kitchen is high so the tempo at your table can be exactly as low as you like. And I take coffee very seriously; that's why the sign says Café.</p>
<p>Weekends run in three acts here too. Brunch opens the game, dinner builds on it, and as Friday and Saturday nights approach midnight the third act — disco — has taken over the room. Stenstan outside the windows has seen most things since the 1800s, but I'd argue it has seen few places with this combination of frozen mimosas and disco feeling.</p>
<p>The flagship is in Umeå, but the soul here is the same: four colours, one attitude, and the conviction that life is too short for boring places. Welcome in.</p>
"""

UMEA_FAQ_EN = [
  ("Can you book a table at GP's in Umeå?","No — I run walk-ins only, first come, first served. It's a principle: life is too short for empty tables. Table booking launches in autumn 2026; until then, just come by Skolgatan 62."),
  ("What are the opening hours at GP's in Umeå?","Monday 11:30–22, Tuesday–Thursday 11:30–midnight, Friday–Saturday 11:30–01 and Sunday 11:30–22. Fridays and Saturdays run until 1 am."),
  ("Where in Umeå is GP's?","At Skolgatan 62, in central Umeå — near Rådhustorget and about a ten-minute walk from Umeå Central station."),
  ("Are dogs welcome at GP's Umeå?","Yes, dogs are always welcome. Water's already out."),
  ("Are there alcohol-free drinks at GP's?","Yes — the whole No Regrets list is zero-proof, from Virgin Prince 0.0 (79 SEK) to alcohol-free Coffee Granita. Prices range 39–89 SEK."),
  ("How do I contact GP's in Umeå?","Email umea@guiltypleasure.se or send a DM to @guiltypleasure.se on Instagram. A phone line is on its way — the AI host answers from August 2026."),
]

SUNDSVALL_FAQ_EN = [
  ("Can you book a table at GP's in Sundsvall?","Yes — book online via bokabord and your table will be ready. Walk-ins work just as well: the door at Storgatan 12 is open and the bar always has room for one more."),
  ("What are the opening hours at GP's in Sundsvall?","Monday–Tuesday 11–22, Wednesday–Thursday 11–midnight, Friday–Saturday 11–01 and Sunday 11–22. Weekend nights run until 1 am."),
  ("Where in Sundsvall is GP's?","At Storgatan 12, in the middle of Stenstan — Sundsvall's historic stone-town centre, near Stora torget."),
  ("Are dogs welcome at GP's Sundsvall?","Yes, always. I'll sort the water."),
  ("How do I contact GP's in Sundsvall?","Email sundsvall@guiltypleasure.se or DM @guiltypleasure.se on Instagram. A phone line arrives in August 2026 — the AI host will answer."),
]

def city_page_en(key):
    c = CITIES[key]
    faqs  = UMEA_FAQ_EN if key=="umea" else SUNDSVALL_FAQ_EN
    story = UMEA_STORY_EN if key=="umea" else SUNDSVALL_STORY_EN
    url = f"https://www.guiltypleasure.se/en/{key}/"
    title = f"Restaurant & bar in {c['name']}, Sweden — GP's Guilty Pleasure Café, {c['street']}"
    desc = (f"New York-inspired comfort bistro at {c['street']}, {c['name']}, Sweden. Brunch, dinner & disco. "
            + ("Walk-ins only, dogs welcome. Open till 1 am Fri–Sat." if key=="umea"
               else "Book online or walk in — dogs welcome. Open till 1 am Fri–Sat."))
    hero_h1 = "Umeå's guilty pleasure since 2021" if key=="umea" else "Finger-licking good — in the heart of Stenstan"
    hero_sub = ("I'm the flagship. Right in the city centre, at Skolgatan 62 — where cravings meet good vibes." if key=="umea"
                else "I'm GP's in Sundsvall. Storgatan 12 — food and drinks, all day, everyday.")
    schema = rest_schema_en(key) + "\n" + faq_schema(faqs,url)
    cta = (f'<a class="btn btn-fire stickycta" href="{c["booking"]}" rel="noopener">Book a table</a>' if c["booking"]
           else f'<a class="btn btn-fire stickycta" href="{c["maps"]}" rel="noopener">Find us</a>')
    booking_row = (f'<a class="btn btn-pink" href="{c["booking"]}" rel="noopener">Book a table</a>' if c["booking"] else "")
    policy = ("Walk-ins only — come as you are. Table booking launches in autumn 2026." if key=="umea"
              else "Book online or drop by — both work just as well.")
    menu_rows = MENU_EN.replace('href="../meny/index.html"','href="../../meny/index.html"')
    html = head(title,desc,f"/en/{key}/",lang="en",extra_schema=schema,fontpath="../../fonts/",og=f"og-{key}.png") + en_topbar() + f"""
<main id="top">
  <div class="wrap crumbs"><a href="../index.html">GP's</a> / {c['name']}</div>
  <section class="hero wrap" style="padding-top:34px">
    <div class="eyebrow">Guilty Pleasure Café · {c['name']}, Sweden</div>
    <h1>{hero_h1}</h1>
    <p class="sub">{hero_sub} <span class="cstatus" data-city="{key}" aria-live="polite">…</span></p>
    <div class="cta-row">
      {booking_row}
      <a class="btn btn-line" href="{c['maps']}" rel="noopener">Directions</a>
      <a class="btn btn-line" href="{c['reviews']}" rel="noopener">Google reviews</a>
    </div>
  </section>
  <div class="marquee" aria-hidden="true"><span>BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · </span></div>
  <section class="wrap story">
    <div class="kicker">My story</div>
    <h2>This is <span class="accent">GP's {c['name']}</span></h2>
    {story}
  </section>
  <section class="wrap">
    <div class="kicker">From the bar</div>
    <h2>Signatures <span class="accent">&amp; guilty pleasures</span></h2>
    <div class="menucard">{menu_rows}</div>
  </section>
  <section class="wrap">
    <div class="kicker">The practical bits</div>
    <h2>Find us <span class="accent">&amp; opening hours</span></h2>
    <div class="cities">
      <div class="city">
        <h3>{c['street']}, {c['postal']} {c['name']}</h3>
        <p>GP's — Guilty Pleasure Café is at {c['street']} in central {c['name']}. <a href="{c['maps']}" rel="noopener">Open directions in maps</a>.</p>
        <p><a href="mailto:{c['email']}">{c['email']}</a></p>
        <p style="font-size:14px;opacity:.85">{policy}</p>
      </div>
      <div class="city">{en_hours_table(key)}</div>
    </div>
  </section>
  <section class="wrap">
    <div class="kicker">Quick answers</div>
    <h2>Questions <span class="accent">&amp; answers</span></h2>
    {faq_html(faqs)}
  </section>
</main>
{cta}
""" + en_footer()
    html = html.replace("</body>", en_status("{"+f'"{key}":{c["hours_js"]}'+"}") + "\n</body>")
    return fix_amps(html)

for key in ("umea","sundsvall"):
    (ROOT/f"en/{key}/index.html").write_text(city_page_en(key), encoding="utf-8")

# --- hreflang: bidirektionella par per stad + x-default -> sv ---
for key in ("umea","sundsvall"):
    tag = (f'<link rel="alternate" hreflang="sv" href="https://www.guiltypleasure.se/{key}/">\n'
           f'<link rel="alternate" hreflang="en" href="https://www.guiltypleasure.se/en/{key}/">\n'
           f'<link rel="alternate" hreflang="x-default" href="https://www.guiltypleasure.se/{key}/">')
    for f in (f"{key}/index.html", f"en/{key}/index.html"):
        p=(ROOT/f); s=p.read_text(encoding="utf-8")
        if 'hreflang' not in s:
            p.write_text(s.replace('<link rel="canonical"', tag+'\n<link rel="canonical"'), encoding="utf-8")

# --- EN-hubben ska peka på EN-städerna (nav + CTA-knappar) ---
p=(ROOT/"en/index.html"); s=p.read_text(encoding="utf-8")
if 'href="umea/index.html"' not in s:
    s=s.replace('href="../umea/index.html"','href="umea/index.html"').replace('href="../sundsvall/index.html"','href="sundsvall/index.html"')
    p.write_text(s, encoding="utf-8")

# --- sitemap ---
sm=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
for key in ("umea","sundsvall"):
    if f"/en/{key}/" not in sm:
        sm=sm.replace("</urlset>",f'  <url><loc>https://www.guiltypleasure.se/en/{key}/</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>\n</urlset>')
(ROOT/"sitemap.xml").write_text(sm, encoding="utf-8")

# --- verifiering ---
for key in ("umea","sundsvall"):
    s=(ROOT/f"en/{key}/index.html").read_text(encoding="utf-8")
    blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    for b in blocks: json.loads(b)
    words=len(re.sub(r'<[^>]+>',' ', (UMEA_STORY_EN if key=="umea" else SUNDSVALL_STORY_EN)).split())
    assert 'lang="en"' in s and "tel:" not in s and "hreflang" in s and "Öppet nu" not in s
    assert '../../meny/index.html' in s and 'stickycta' in s
    assert words>=350, f"story {key}: {words} ord"
    sv=(ROOT/f"{key}/index.html").read_text(encoding="utf-8")
    assert f'hreflang="en" href="https://www.guiltypleasure.se/en/{key}/"' in sv
    print(f"en/{key}/index.html: {len(s)//1024} KB · {len(blocks)} schema OK · story {words} ord · hreflang par OK")
print("sitemap-URL:er:", sm.count("<loc>"), "· EN-hubb -> EN-städer:", 'href="umea/index.html"' in (ROOT/"en/index.html").read_text(encoding="utf-8"))
