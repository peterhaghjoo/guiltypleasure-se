#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EN-stadssidor (en/umea/, en/sundsvall/) + hreflang per stad.
Körs SIST: python3 build.py && python3 build_en.py && python3 build_menu.py && python3 build_en_cities.py"""
import json, re, pathlib
from build import head, topbar, footer, CITIES, rest_schema, faq_schema, faq_html, fix_amps, breadcrumbs
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
      .replace("Häng med oss","Follow along")
      .replace("Ingen telefon än — maila oss eller skicka DM på Instagram.","No phone yet — email us or send a DM on Instagram.")
      .replace("Drop-in only — bara kom in.","Walk-ins only — just come in.")
      .replace("Boka bord online</a> — eller kom förbi.","Book a table online</a> — or drop by.")
      .replace("· karta</a>","· map</a>").replace('>karta<','>map<'))

def rest_schema_en(city_key):
    s = rest_schema(city_key, f"https://www.guiltypleasure.se/en/{city_key}/", lang="en")
    for a,b in (
        ('"Signaturer ur baren"','"Signatures from the bar"'),
        ('"Gin, viol, citron, ingefäraskum & salt"','"Gin, violet, lemon, ginger foam & salt"'),
        ('"Blodapelsinsorbet, fläder & cava"','"Blood orange sorbet, elderflower & cava"'),
        ('"Tequila, jalapeño & lime"','"Tequila, jalapeño & lime"'),
        ('"Alkoholfri signatur — viol, citron, ingefäraskum & salt"','"Zero-proof signature — violet, lemon, ginger foam & salt"'),
    ): s = s.replace(a,b)
    return s

UMEA_STORY_EN = """
<p class="lead">We opened at Skolgatan 62 in 2021 with one simple idea: Umeå deserved a place where brunch doesn't end just because the clock does.</p>
<p>Since then we've been the city's New York-inspired comfort bistro — the flagship of the Guilty Pleasure family. Our day starts with frozen mimosas and comfort classics, slides into dinner when the afternoon runs out of steam, and ends — on weekends — in something best described as disco. Fridays and Saturdays we keep going until 1 am, and yes, you'll notice.</p>
<p>You'll find us in the middle of central Umeå, at Skolgatan 62. Bringing the dog? Bring the dog. Coming with a big group on a Saturday? Come early. We run walk-ins only, first come, first served, and it's a principle we're proud of: life is too short for empty tables reserved for people who never show up.</p>
<p>The bar is our stage. The signature is called Ghost of Prince — gin, violet, lemon, ginger foam and salt — and if you're not drinking alcohol you won't be parked on some sad substitutes' bench: our whole No Regrets list is built with the same love, from Virgin Prince to zero-proof Coffee Granita in three flavours. The coffee? Obviously. That's why the sign says Café.</p>
<p>Umeå is a city that wakes up late and stays up late on weekends. We're built for exactly that.</p>

<p>What do we mean by comfort food? Think of the food you actually crave — generous, hot, a little indecently good — cooked properly and served without delay. The New York diner is the blueprint: high tempo in the kitchen, low tempo at the tables. You can make it here on your lunch break if you want to, but nobody will look at you sideways if you stay until closing. That's the whole point of the word pleasure in our name — and the word guilty you should take with a pinch of salt. Or a salted rim, like on the margarita.</p>
<p>Weekends are our main event. Brunch rolls from opening — frozen mimosas, coffee that means something, and comfort classics until the afternoon gives up. Then we change costume: the lights drop, the playlist wakes up, and anyone who stays finds out why the third act is called disco. No dress code, no guest list — just a mood that keeps climbing until closing time.</p>
<p>We're part of the Guilty Pleasure family, with a sister in Sundsvall and the same four colours in our soul: fire, disco, moss and cream. But Umeå is where it all began in 2021, and this is where the flag stands. Come by and you'll understand.</p>
"""

SUNDSVALL_STORY_EN = """
<p class="lead">In the middle of Stenstan, at Storgatan 12, we serve finger-licking good food and drinks — all day, everyday.</p>
<p>We're Sundsvall's slice of the Guilty Pleasure family: the same New York-inspired comfort bistro soul as the flagship in Umeå, but with a rhythm of our own. The stone houses of Stenstan and the pulse of Storgatan set the tone — you come here for a long weekend brunch, a dinner in no particular hurry, or a Friday night that grows into something more. Fridays and Saturdays we're open until 1 am.</p>
<p>Unlike our sister up north, we take table bookings — book online and your table is ready when you arrive. But the door is just as open if you're simply passing by: walk-ins are always welcome, and the bar always has room for one more. Dogs? Welcome, always.</p>
<p>The bar works the same magic as in Umeå: Ghost of Prince is the signature, Frozen Blood Orange Mimosa owns the brunches, and the whole No Regrets list is properly alcohol-free — not an afterthought. The menu changes with the seasons, so ask what's new.</p>
<p>Sundsvall has always known how to have a good time. We're just the place where it happens.</p>

<p>A practical word of advice: on weekend evenings it's smart to book — Stenstan fills up fast and our tables are popular. Weekday lunches and afternoons, walk-ins almost always work. Coming as a bigger group? Email us at sundsvall@guiltypleasure.se and we'll sort it out together. And follow @guiltypleasure.se on Instagram — that's where the news drops first, almost every day.</p>
<p>Comfort food our way means food without fuss but with full effect — New York diner in the soul, northern Sweden in the heart. Come for lunch, come for dinner, just come. The tempo in the kitchen is high so the tempo at your table can be exactly as low as you like. And we take coffee very seriously; that's why the sign says Café.</p>
<p>Weekends run in three acts here too. Brunch opens the game, dinner builds on it, and as Friday and Saturday nights approach midnight the third act — disco — has taken over the room. Stenstan outside the windows has seen most things since the 1800s, but we'd argue it has seen few places with this combination of frozen mimosas and disco feeling.</p>
<p>The flagship is in Umeå, but the soul here is the same: four colours, one attitude, and the conviction that life is too short for boring places. Welcome in.</p>
"""

UMEA_FAQ_EN = [
  ("Can you book a table at GP's in Umeå?","No — we run walk-ins only, first come, first served. It's a principle: life is too short for empty tables. Just come by Skolgatan 62."),
  ("What are the opening hours at GP's in Umeå?","Monday 11:30–22, Tuesday–Thursday 11:30–midnight, Friday–Saturday 11:30–01 and Sunday 11:30–22. Fridays and Saturdays run until 1 am."),
  ("Where in Umeå is GP's?","At Skolgatan 62, in central Umeå."),
  ("Are dogs welcome at GP's Umeå?","Yes, dogs are always welcome."),
  ("Are there alcohol-free drinks at GP's?","Yes — the whole No Regrets list is zero-proof, from Virgin Prince 0.0 to alcohol-free Coffee Granita."),
  ("How do I contact GP's in Umeå?","Email umea@guiltypleasure.se or send a DM to @guiltypleasure.se on Instagram."),
]

SUNDSVALL_FAQ_EN = [
  ("Can you book a table at GP's in Sundsvall?","Yes — book online via bokabord and your table will be ready. Walk-ins work just as well: the door at Storgatan 12 is open and the bar always has room for one more."),
  ("What are the opening hours at GP's in Sundsvall?","Monday–Tuesday 11–22, Wednesday–Thursday 11–midnight, Friday–Saturday 11–01 and Sunday 11–22. Weekend nights run until 1 am."),
  ("Where in Sundsvall is GP's?","At Storgatan 12, in the middle of Stenstan — Sundsvall's historic stone-town centre, near Stora torget."),
  ("Are dogs welcome at GP's Sundsvall?","Yes, always. Dogs are welcome at GP's Sundsvall."),
  ("How do I contact GP's in Sundsvall?","Email sundsvall@guiltypleasure.se or DM @guiltypleasure.se on Instagram."),
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
    hero_sub = ("We're the flagship. Right in the city centre, at Skolgatan 62 — where cravings meet good vibes." if key=="umea"
                else "We're GP's in Sundsvall. Storgatan 12 — food and drinks, all day, everyday.")
    crumbs = breadcrumbs([("Home","https://www.guiltypleasure.se/en/"),
                          (c["name"], url)], url)
    schema = rest_schema_en(key) + "\n" + faq_schema(faqs,url) + "\n" + crumbs
    cta = (f'<a class="btn btn-fire stickycta" href="{c["booking"]}" rel="noopener">Book a table</a>' if c["booking"]
           else f'<a class="btn btn-fire stickycta" href="{c["maps"]}" rel="noopener">Find us</a>')
    booking_row = (f'<a class="btn btn-pink" href="{c["booking"]}" rel="noopener">Book a table</a>' if c["booking"] else "")
    policy = ("Walk-ins only — come as you are." if key=="umea"
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
    <div class="kicker">Our story</div>
    <h2>This is <span class="accent">GP's {c['name']}</span></h2>
    {story}
  </section>
  <section class="wrap surf-moss">
    <div class="kicker">From the bar</div>
    <h2>Signatures <span class="accent">&amp; guilty pleasures</span></h2>
    <div class="menucard">{menu_rows}</div>
  </section>
  <section class="wrap">
    <div class="kicker">The practical bits</div>
    <h2>Find us <span class="accent">&amp; opening hours</span></h2>
    <div class="cities">
      <div class="infocard">
        <h3>{c['street']}, {c['postal']} {c['name']}</h3>
        <p>GP's — Guilty Pleasure Café is at {c['street']} in central {c['name']}. <a href="{c['maps']}" rel="noopener">Open directions in maps</a>.</p>
        <p><a href="mailto:{c['email']}">{c['email']}</a></p>
        <p style="font-size:14px">{policy}</p>
      </div>
      <div class="infocard"><h3>Opening hours</h3>{en_hours_table(key)}</div>
    </div>
  </section>
  <section class="wrap surf-disco dogs">
    <div class="kicker">The dog is welcome</div>
    <h2>Bring your dog.</h2>
    <p>It's not just you who's welcome — your four-legged best friend too. Dogs are always welcome. Dog friendly, always.</p>
    <div class="chips"><span class="chip">Dogs inside</span><span class="chip">Always welcome</span></div>
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
