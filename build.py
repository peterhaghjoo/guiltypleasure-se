#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GP-sajtens generator — en källa, alla sidor. Kör: python3 build.py"""
import base64, json, re, pathlib

ROOT = pathlib.Path(__file__).parent

# ============================================================================
# FÖRLANSERINGSFLAGGA
# ----------------------------------------------------------------------------
# True  = varje sida får <meta name="robots" content="noindex, nofollow">.
#         Sajten ligger på guiltypleasure-se.pages.dev och ska INTE indexeras
#         medan guiltypleasure.se fortfarande drivs av WordPress — annars
#         konkurrerar de två sajterna om samma sökord.
# False = sidorna blir indexerbara. Sätts till False EN gång, vid DNS-cutover
#         (BACKLOG 3.4/3.5) — och bara då.
#
# robots.txt lämnas medvetet öppen (Allow: /): en Disallow skulle hindra Google
# från att över huvud taget läsa noindex-taggen, vilket ger motsatt effekt.
# ============================================================================
PRELAUNCH = True

FONT_B64 = base64.b64encode((ROOT/"fonts/gp-bold.woff2").read_bytes()).decode()
LOGO = (ROOT/"logo.inline.svg").read_text(encoding="utf-8")

# ---------- kontrastberäkning (kvalitetsgrind) ----------
def lum(hexc):
    r,g,b = [int(hexc[i:i+2],16)/255 for i in (1,3,5)]
    f = lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def ratio(a,b):
    la,lb = lum(a),lum(b)
    hi,lo = max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)

MOSSA,GRADDE,DISCO,ELD = "#24270e","#fff8eb","#ff99ff","#ff450a"
QA_CONTRAST = {
    "gradde/mossa": ratio(GRADDE,MOSSA),
    "disco/mossa": ratio(DISCO,MOSSA),
    "eld/mossa": ratio(ELD,MOSSA),
    "gradde/eld": ratio(GRADDE,ELD),
    "mossa/disco": ratio(MOSSA,DISCO),
}

CSS = """
  :root{--night:#24270e;--night-2:#2e321a;--cream:#fff8eb;--pink:#ff99ff;--flame:#ff450a;--maxw:1080px}
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:var(--night);color:var(--cream);font:16px/1.6 "PP Neue Montreal","Montreal Fallback","Arial","Helvetica",sans-serif}
  img,svg{max-width:100%;height:auto}
  a{color:inherit;text-decoration:underline;text-decoration-thickness:.08em;text-underline-offset:.18em}
  a:hover{color:var(--pink)}
  .wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}
  .topbar{position:sticky;top:0;z-index:50;background:rgba(36,39,14,.94);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,248,235,.14)}
  .topbar .wrap{display:flex;align-items:center;gap:16px;height:58px}
  .wordmark{font-family:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;font-size:22px;color:var(--pink);text-decoration:none;position:relative}
  .wordmark:hover{color:var(--pink)}
  nav{margin-left:auto;display:flex;gap:18px}
  nav a{text-decoration:none;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;opacity:.9}
  nav a:hover{opacity:1;color:var(--pink)}
  @media(max-width:640px){nav{gap:12px} nav a.hidem{display:none}}
  .hero{padding:52px 0 40px;text-align:center}
  .gp-logo{width:min(380px,68vw);color:var(--cream);display:block;margin:0 auto 6px}
  .eyebrow{font-weight:700;font-size:12.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--pink)}
  h1{font-family:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;font-weight:700;color:var(--pink);font-size:clamp(32px,6.2vw,62px);line-height:1.08;margin:14px auto 12px;max-width:16ch;text-wrap:balance}
  .sub{max-width:54ch;margin:0 auto 26px;font-size:17px;opacity:.92}
  .cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
  .btn{display:inline-block;text-decoration:none;font-weight:700;letter-spacing:.05em;text-transform:uppercase;font-size:14px;padding:14px 24px;border-radius:9999px;min-height:44px}
  .btn-pink{background:var(--pink);color:var(--night)}
  .btn-pink:hover{color:var(--night);background:var(--cream)}
  .btn-line{border:2px solid var(--cream);color:var(--cream)}
  .btn-fire{background:var(--pink);color:var(--night)}
  .btn-fire:hover{color:var(--night);background:var(--cream)}
  .marquee{border-top:2px solid var(--pink);border-bottom:2px solid var(--pink);padding:12px 0;overflow:hidden;white-space:nowrap;margin-top:30px}
  .marquee span{display:inline-block;font-family:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;font-size:21px;color:var(--pink);animation:roll 28s linear infinite}
  @keyframes roll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
  section{padding:56px 0}
  .kicker{font-weight:700;font-size:12.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--pink);margin-bottom:8px}
  h2{font-family:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;font-weight:700;font-size:clamp(27px,4.4vw,40px);color:var(--cream);margin-bottom:20px;text-wrap:balance}
  .amp{font-family:"PP Neue Montreal","Helvetica Neue",Arial,sans-serif;font-weight:700;font-size:.92em}
  h2 .accent{color:var(--pink)}
  h3{font-weight:700;text-transform:uppercase;letter-spacing:.02em;font-size:20px;margin-bottom:10px}
  .acts{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  @media(max-width:760px){.acts{grid-template-columns:1fr}}
  .act{background:var(--night-2);border:1px solid rgba(255,248,235,.16);border-radius:24px;padding:26px 22px;position:relative}
  .tagpill{background:var(--pink);color:var(--night);font-weight:700;font-size:12px;letter-spacing:.1em;text-transform:uppercase;border-radius:9999px;padding:6px 14px}
  .act .tagpill{position:absolute;top:-14px;left:20px}
  .act h3{font-family:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;text-transform:none;font-size:24px;color:var(--pink);margin:8px 0}
  .act p{font-size:15px;opacity:.92}
  .menucard{background:var(--night-2);border:2px solid var(--pink);border-radius:24px;padding:32px 28px;max-width:640px;margin:0 auto}
  .mc-head{text-align:center;margin-bottom:18px}
  .mrow{padding:4px 0}
  .mrow summary{display:flex;align-items:baseline;gap:8px;cursor:pointer;list-style:none;padding:8px 0;min-height:44px}
  .mrow summary::-webkit-details-marker{display:none}
  .mrow b{font-weight:700;font-size:15.5px;text-transform:uppercase;letter-spacing:.02em}
  .sig{color:var(--pink);font-family:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;font-size:12px;text-transform:none;margin-left:6px}
  .dots{flex:1;border-bottom:2px dotted rgba(255,248,235,.4);transform:translateY(-4px);min-width:24px}
  .price{font-weight:700;color:var(--pink);font-size:15.5px}
  .mrow p{font-size:13.5px;opacity:.85;padding:0 0 8px}
  .mc-foot{text-align:center;margin-top:16px;font-size:13.5px;opacity:.8}
  .facts{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  @media(max-width:760px){.facts{grid-template-columns:1fr}}
  .fact{border:1px solid rgba(255,248,235,.16);border-radius:24px;padding:22px;background:var(--night-2)}
  .fact h3{font-size:15px;color:var(--pink)}
  .fact p{font-size:14.5px;opacity:.92}
  .cities{display:grid;grid-template-columns:1fr 1fr;gap:22px}
  @media(max-width:820px){.cities{grid-template-columns:1fr}}
  .city{background:var(--night-2);border:1px solid rgba(255,248,235,.18);border-radius:24px;padding:28px 26px;display:flex;flex-direction:column;gap:10px}
  .city h3{font-family:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;text-transform:none;font-size:26px;color:var(--pink);margin:0}
  .cstatus{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:5px 12px;border-radius:9999px;border:1.5px solid var(--cream);color:var(--cream);white-space:nowrap;display:inline-block}
  .cstatus.open{border-color:var(--pink);color:var(--pink)}
  .cstatus.closed{border-color:var(--flame);color:var(--cream);background:rgba(255,69,10,.18)}
  table.hours{width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0}
  table.hours td{padding:8px 0;border-bottom:1px solid rgba(255,248,235,.12)}
  table.hours td:last-child{text-align:right;font-weight:700}
  table.hours tr.today td{color:var(--pink);font-weight:700}
  table.hours caption{text-align:left;font-weight:700;text-transform:uppercase;font-size:12.5px;letter-spacing:.1em;padding-bottom:6px;color:var(--pink)}
  .faq details{border:1px solid rgba(255,248,235,.16);border-radius:16px;background:var(--night-2);margin-bottom:10px}
  .faq summary{cursor:pointer;font-weight:700;padding:16px 18px;list-style:none;min-height:44px;font-size:15.5px}
  .faq summary::-webkit-details-marker{display:none}
  .faq summary::before{content:"+ ";color:var(--pink);font-weight:700}
  .faq details[open] summary::before{content:"– "}
  .faq div{padding:0 18px 16px;font-size:15px;opacity:.94}
  .story p{max-width:64ch;margin:0 0 16px;font-size:16.5px;line-height:1.65}
  .story .lead{font-size:19px;font-weight:700}
  .crumbs{font-size:13px;opacity:.85;padding:16px 0 0}
  .crumbs a{text-decoration:none}
  .stickycta{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:60;box-shadow:none;display:none}
  @media(max-width:820px){.stickycta{display:inline-block}}
  .igband{text-align:center;background:var(--night-2);border-top:1px solid rgba(255,248,235,.14);border-bottom:1px solid rgba(255,248,235,.14)}
  .igband p{max-width:46ch;margin:8px auto 20px;opacity:.92}
  footer{padding:40px 0 90px;font-size:14.5px}
  .fgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;margin-bottom:22px}
  @media(max-width:760px){.fgrid{grid-template-columns:1fr}}
  footer h3{font-size:14px;color:var(--pink)}
  footer p{opacity:.92;margin-bottom:6px}
  footer .soc a{font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:13px;margin-right:14px}
  .fin{text-align:center;opacity:.7;font-size:13px;margin-top:10px}
  a:focus-visible,.btn:focus-visible,summary:focus-visible{outline:3px solid var(--pink);outline-offset:3px;border-radius:6px}
  @media (prefers-reduced-motion:reduce){.marquee span{animation:none}.wordmark::after{animation:none!important}}
  /* signaturanimation: diskret neonflimmer på wordmark-punkten */
  .wordmark::after{content:"·";color:var(--flame);margin-left:2px;animation:flick 4.5s infinite}
  @keyframes flick{0%,92%,96%,100%{opacity:1}94%,98%{opacity:.25}}
"""

FONTFACE = f"""<script>
/* Brandfonten laddas SYNKRONT ur ArrayBuffer -> finns före första paint -> noll swap, noll CLS */
try{{document.fonts.add(new FontFace("Guilty Pleasure",Uint8Array.from(atob("{FONT_B64}"),c=>c.charCodeAt(0)).buffer,{{weight:"700"}}));}}catch(e){{}}
</script>
<style>
@font-face{{font-family:"PP Neue Montreal";src:url("{{{{FONTPATH}}}}pp-medium.woff2") format("woff2");font-weight:500;font-style:normal;font-display:optional}}
@font-face{{font-family:"PP Neue Montreal";src:url("{{{{FONTPATH}}}}pp-bold.woff2") format("woff2");font-weight:700;font-style:normal;font-display:optional}}
@font-face{{font-family:"Montreal Fallback";src:local("Arial"),local("Liberation Sans");size-adjust:99.3%;ascent-override:95.8%;descent-override:24.2%;line-gap-override:0%}}
@font-face{{font-family:"GP Fallback A";src:local("Arial Black");font-weight:700;size-adjust:71.6%}}
@font-face{{font-family:"GP Fallback B";src:local("Liberation Sans Bold"),local("DejaVu Sans Bold");font-weight:700;size-adjust:76.9%}}
</style>"""

CITIES = {
  "umea": dict(
    name="Umeå", street="Skolgatan 62", postal="903 29", email="umea@guiltypleasure.se",
    maps="https://maps.google.com/?q=Guilty+Pleasure+Caf%C3%A9+Skolgatan+62+Ume%C3%A5",
    reviews="https://www.google.com/search?q=Guilty+Pleasure+Caf%C3%A9+Ume%C3%A5+recensioner",
    region="Västerbottens län", booking=None,
    hours_txt=[("Måndag","11.30–22"),("Tisdag","11.30–00"),("Onsdag","11.30–00"),("Torsdag","11.30–00"),("Fredag","11.30–01"),("Lördag","11.30–01"),("Söndag","11.30–22")],
    hours_js="{1:[690,1320],2:[690,1440],3:[690,1440],4:[690,1440],5:[690,1500],6:[690,1500],0:[690,1320]}",
    hours_schema=[["Monday","Monday","11:30","22:00"],["Tuesday","Thursday","11:30","00:00"],["Friday","Saturday","11:30","01:00"],["Sunday","Sunday","11:30","22:00"]],
    hero_h1="Umeås guilty pleasure sedan 2021",
    hero_sub="Jag är flaggskeppet. Mitt i stan, på Skolgatan 62 — där cravings möter good vibes.",
  ),
  "sundsvall": dict(
    name="Sundsvall", street="Storgatan 12", postal="852 31", email="sundsvall@guiltypleasure.se",
    maps="https://maps.google.com/?q=Guilty+Pleasure+Caf%C3%A9+Storgatan+12+Sundsvall",
    reviews="https://www.google.com/search?q=Guilty+Pleasure+Caf%C3%A9+Sundsvall+recensioner",
    region="Västernorrlands län", booking="https://app.bokabord.se",
    hours_txt=[("Måndag","11–22"),("Tisdag","11–22"),("Onsdag","11–00"),("Torsdag","11–00"),("Fredag","11–01"),("Lördag","11–01"),("Söndag","11–22")],
    hours_js="{1:[660,1320],2:[660,1320],3:[660,1440],4:[660,1440],5:[660,1500],6:[660,1500],0:[660,1320]}",
    hours_schema=[["Monday","Tuesday","11:00","22:00"],["Wednesday","Thursday","11:00","00:00"],["Friday","Saturday","11:00","01:00"],["Sunday","Sunday","11:00","22:00"]],
    hero_h1="Finger-licking good — mitt i Stenstan",
    hero_sub="Jag är GP's i Sundsvall. Storgatan 12 — food and drinks, all day, everyday.",
  ),
}

MENU_ROWS = """
      <div class="mc-head"><span class="tagpill">Ur baren</span></div>
      <details class="mrow"><summary><b>Ghost of Prince</b><span class="sig">signature</span><span class="dots"></span><span class="price">149</span></summary><p>Gin, viol, citron, ingefäraskum &amp; salt. Min stolthet — börja här.</p></details>
      <details class="mrow"><summary><b>Frozen Blood Orange Mimosa</b><span class="dots"></span><span class="price">119</span></summary><p>Blodapelsinsorbet, fläder &amp; cava. Brunchens bästa vän.</p></details>
      <details class="mrow"><summary><b>Spicy Margarita</b><span class="dots"></span><span class="price">139</span></summary><p>Tequila, jalapeño &amp; lime. Den bits — lagom mycket.</p></details>
      <details class="mrow"><summary><b>Coffee Granita</b><span class="dots"></span><span class="price">139</span></summary><p>Vodka, kaffelikör &amp; espressogranita — välj Original, Salted Caramel eller Kanelbulle.</p></details>
      <details class="mrow"><summary><b>Virgin Prince 0.0</b><span class="sig">no regrets</span><span class="dots"></span><span class="price">79</span></summary><p>Viol, citron, ingefäraskum &amp; salt. Hela min No Regrets-lista är alkoholfri, 39–89 kr.</p></details>
      <div class="mc-foot">Tryck på en rad för detaljer. Hela menyn får du på plats — den byter skepnad med säsongen.</div>
"""

def head(title, desc, canon_path, lang="sv", extra_schema="", fontpath="fonts/", og="og.png"):
    ff = FONTFACE.replace("{{FONTPATH}}", fontpath)
    base = fontpath.replace("fonts/", "")
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{'<meta name="robots" content="noindex, nofollow">' if PRELAUNCH else ''}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="restaurant">
<meta property="og:locale" content="{'sv_SE' if lang=='sv' else 'en_GB'}">
<meta property="og:image" content="https://www.guiltypleasure.se/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<!-- FOTO: og-bilden är typografisk (brandsystemet) — byt till riktigt foto (1200x630) när Peters bilder finns -->
<meta name="theme-color" content="#24270e">
<link rel="preload" href="{fontpath}pp-medium.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{fontpath}pp-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" type="image/svg+xml" href="{base}favicon.svg">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
<link rel="canonical" href="https://www.guiltypleasure.se{canon_path}">
{ff}
{extra_schema}
<style>{CSS}</style>
</head>
<body>"""

def fix_amps(html):
    """&-tecknet saknas i brandfonten — sätt Montreal medvetet i brandfont-element (h1/h2/marquee)."""
    def wrap(m):
        seg = m.group(0)
        return seg if 'class="amp"' in seg else seg.replace("&amp;", '<span class="amp">&amp;</span>')
    html = re.sub(r'<h1[^>]*>.*?</h1>', wrap, html, flags=re.S)
    html = re.sub(r'<h2[^>]*>.*?</h2>', wrap, html, flags=re.S)
    html = re.sub(r'<div class="marquee"[^>]*><span>.*?</span></div>', wrap, html, flags=re.S)
    return html

def topbar(base=""):
    return f"""
<header class="topbar">
  <div class="wrap">
    <a class="wordmark" href="{base}index.html">GP's</a>
    <nav aria-label="Huvudmeny">
      <a href="{base}index.html#signaturer" class="hidem">Signaturer</a>
      <a href="{base}umea/index.html">Umeå</a>
      <a href="{base}sundsvall/index.html">Sundsvall</a>
    </nav>
  </div>
</header>"""

def footer(base=""):
    return f"""
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <h3>GP's Umeå</h3>
        <p>Skolgatan 62 · <a href="{CITIES['umea']['maps']}" rel="noopener">karta</a></p>
        <p><a href="mailto:umea@guiltypleasure.se">umea@guiltypleasure.se</a></p>
        <p>Drop-in only — bara kom in.</p>
      </div>
      <div>
        <h3>GP's Sundsvall</h3>
        <p>Storgatan 12 · <a href="{CITIES['sundsvall']['maps']}" rel="noopener">karta</a></p>
        <p><a href="mailto:sundsvall@guiltypleasure.se">sundsvall@guiltypleasure.se</a></p>
        <p><a href="https://app.bokabord.se" rel="noopener">Boka bord online</a> — eller kom förbi.</p>
      </div>
      <div>
        <h3>Häng med mig</h3>
        <p class="soc"><a href="https://www.instagram.com/guiltypleasure.se/" rel="noopener">Instagram</a><a href="https://www.tiktok.com/@guiltypleasure.se" rel="noopener">TikTok</a><a href="https://www.facebook.com/gpsumea/" rel="noopener">Facebook</a></p>
        <p>Telefon? Min AI-värdinna svarar från augusti. Tills dess: maila eller DM:a.</p>
      </div>
    </div>
    <p class="fin">See you at GP's for a delicious time, friend. 💚 · © 2026 Guilty Pleasure</p>
  </div>
</footer>
</body>
</html>"""

def status_js(cities_js, closes=True):
    return f"""
<script>
(function(){{
  var H = {cities_js};
  var now=new Date(), d=now.getDay(), m=now.getHours()*60+now.getMinutes();
  Object.keys(H).forEach(function(c){{
    var s=H[c][d], y=H[c][(d+6)%7];
    var spill=(y[1]>1440 && m < y[1]-1440);
    var open=(m>=s[0]&&m<Math.min(s[1],1440))||spill;
    var cm=spill?y[1]:s[1];
    var lbl=cm>=1440?String(Math.floor((cm-1440)/60)).padStart(2,'0'):String(Math.floor(cm/60)).padStart(2,'0');
    var t = open ? ('Öppet nu · stänger '+lbl) : 'Stängt just nu';
    document.querySelectorAll('.cstatus[data-city="'+c+'"]').forEach(function(el){{
      el.textContent=t; el.className='cstatus '+(open?'open':'closed');
    }});
    var row=document.querySelector('table.hours[data-city="'+c+'"] tr[data-d="'+d+'"]');
    if(row){{row.classList.add('today');}}
  }});
}})();
</script>"""

def hours_table(city_key):
    c = CITIES[city_key]
    rows = "".join(f'<tr data-d="{(i+1)%7}"><td>{d}</td><td>{h}</td></tr>' for i,(d,h) in enumerate(c["hours_txt"]))
    return f'<table class="hours" data-city="{city_key}" aria-label="Öppettider GP\'s {c["name"]}">{rows}</table>'

WEEK = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def day_range(d1, d2):
    """Alla dagar i spannet d1–d2, inklusive ändpunkterna.

    hours_schema lagrar spann som ["Tuesday","Thursday",...]. Tidigare togs bara
    ändpunkterna med, så onsdagen försvann ur schemat och Google läste Umeå som
    stängt på onsdagar. Se BACKLOG 1.1b.
    """
    i, j = WEEK.index(d1), WEEK.index(d2)
    return WEEK[i:j+1] if i <= j else WEEK[i:] + WEEK[:j+1]

def rest_schema(city_key, page_url):
    c = CITIES[city_key]
    node = {
      "@context":"https://schema.org","@type":"Restaurant",
      "@id":f"https://www.guiltypleasure.se/{city_key}/#restaurant",
      "name":f"GP's — Guilty Pleasure Café {c['name']}",
      "servesCuisine":["Comfort food","Brunch","Cocktails"],
      "priceRange":"$$",
      "address":{"@type":"PostalAddress","streetAddress":c["street"],"postalCode":c["postal"],"addressLocality":c["name"],"addressRegion":c["region"],"addressCountry":"SE"},
      "email":c["email"],"url":f"https://www.guiltypleasure.se/{city_key}/",
      "acceptsReservations": (c["booking"] if c["booking"] else "False"),
      "hasMap":c["maps"],
      "sameAs":["https://www.instagram.com/guiltypleasure.se/","https://www.facebook.com/gpsumea/","https://www.tiktok.com/@guiltypleasure.se"],
      "hasMenu":{"@type":"Menu","name":"Signaturer ur baren","hasMenuSection":[{"@type":"MenuSection","name":"Cocktails","hasMenuItem":[
          {"@type":"MenuItem","name":"Ghost of Prince","description":"Gin, viol, citron, ingefäraskum & salt","offers":{"@type":"Offer","price":"149","priceCurrency":"SEK"}},
          {"@type":"MenuItem","name":"Frozen Blood Orange Mimosa","description":"Blodapelsinsorbet, fläder & cava","offers":{"@type":"Offer","price":"119","priceCurrency":"SEK"}},
          {"@type":"MenuItem","name":"Spicy Margarita","description":"Tequila, jalapeño & lime","offers":{"@type":"Offer","price":"139","priceCurrency":"SEK"}},
          {"@type":"MenuItem","name":"Virgin Prince 0.0","description":"Alkoholfri signatur — viol, citron, ingefäraskum & salt","offers":{"@type":"Offer","price":"79","priceCurrency":"SEK"}}]}]},
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":day_range(d1,d2),"opens":o,"closes":cl} for d1,d2,o,cl in c["hours_schema"]],
    }
    return '<script type="application/ld+json">'+json.dumps(node,ensure_ascii=False)+'</script>'

def faq_schema(qas, url):
    node={"@context":"https://schema.org","@type":"FAQPage","@id":url+"#faq",
      "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
    return '<script type="application/ld+json">'+json.dumps(node,ensure_ascii=False)+'</script>'

def faq_html(qas):
    items="".join(f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q,a in qas)
    return f'<div class="faq">{items}</div>'

# ---------------- STADSSIDOR ----------------
UMEA_STORY = """
<p class="lead">Jag öppnade på Skolgatan 62 år 2021 med en enkel idé: Umeå förtjänade ett ställe där brunchen inte tar slut bara för att klockan gör det.</p>
<p>Sedan dess har jag varit stans New York-inspirerade comfort bistro — flaggskeppet i Guilty Pleasure-familjen. Hos mig börjar dagen med frozen mimosas och comfort-klassiker, glider över i middag när eftermiddagen tröttnat, och slutar på helgerna i något som bäst beskrivs som disco. Fredagar och lördagar håller jag igång till klockan ett, och ja — det märks.</p>
<p>Du hittar mig mitt i centrala Umeå, ett stenkast från Rådhustorget och tio minuters promenad från Umeå Central. Kommer du med hunden? Ta med den in, vatten står framme. Kommer du med ett stort gäng en lördag? Kom tidigt — jag kör drop-in only, först till kvarn, och det är en princip jag är stolt över: livet är för kort för tomma bord som väntar på folk som inte dyker upp. Bordsbokning lanserar jag till hösten för er som vill planera — men spontaniteten kommer alltid ha förtur här.</p>
<p>Baren är min scen. Signaturen heter Ghost of Prince — gin, viol, citron, ingefäraskum och salt — och den som inte dricker alkohol får ingen tråkig avbytarbänk: hela min No Regrets-lista är byggd med samma kärlek, från Virgin Prince till alkoholfri Coffee Granita i tre smaker. Kaffet? Självklart. Det är därför det står Café på skylten.</p>
<p>Umeå är en stad som vaknar sent och lägger sig sent på helgen. Jag är byggd för exakt det.</p>

<p>Vad menar jag med comfort food? Tänk maten du egentligen längtar efter — generös, het, lite oanständigt god — lagad på riktigt och serverad utan dröjsmål. New York-dinern är förebilden: högt tempo i köket, lågt tempo vid borden. Du ska hinna hit på lunchrasten om du vill, men ingen kommer titta konstigt på dig om du blir kvar till stängning. Det är hela poängen med ordet pleasure i mitt namn — och ordet guilty tar du med en nypa salt. Eller som saltkanten på margaritan.</p>
<p>Helgerna är min paradgren. Brunchen rullar från öppning — frozen mimosas, kaffe som betyder något och comfort-klassiker tills eftermiddagen ger upp. Sen byter jag skepnad: ljuset sjunker, spellistan vaknar, och den som stannar kvar märker varför tredje akten heter disco. Ingen dresscode, ingen gästlista — bara stämning som stiger med timmarna fram till stängning.</p>
<p>Jag är en del av Guilty Pleasure-familjen, med en syster i Sundsvall och samma fyra färger i själen: eld, disco, mossa och grädde. Men Umeå är där allt började 2021, och det är här flaggan står. Kom förbi så förstår du.</p>
"""

SUNDSVALL_STORY = """
<p class="lead">Mitt i Stenstan, på Storgatan 12, serverar jag finger-licking good food and drinks — all day, everyday.</p>
<p>Jag är Sundsvalls del av Guilty Pleasure-familjen: samma New York-inspirerade comfort bistro-själ som flaggskeppet i Umeå, men med min egen rytm. Stenstans stenhus och Storgatans puls sätter tonen — hit kommer du för en lång brunch i helgen, en middag som inte har bråttom, eller en fredagskväll som växer till något mer. Fredag och lördag håller jag öppet till klockan ett.</p>
<p>Till skillnad från min syster i norr tar jag emot bordsbokningar — boka online så står bordet redo när du kommer. Men dörren är lika öppen för dig som bara svänger förbi: drop-in är alltid välkommet, och baren har alltid plats för en till. Hundar? Välkomna, alltid. Vatten fixar jag.</p>
<p>Ur baren händer samma magi som i Umeå: Ghost of Prince är signaturen, Frozen Blood Orange Mimosa äger bruncherna, och hela No Regrets-listan är alkoholfri på riktigt — inte en eftertanke. Menyn byter skepnad med säsongen, så fråga vad som är nytt.</p>
<p>Sundsvall har alltid vetat hur man har trevligt. Jag är bara stället där det händer.</p>

<p>Ett praktiskt ord på vägen: helgkvällar är det klokt att boka — Stenstan fylls snabbt och mina bord är populära. Vardagsluncher och eftermiddagar funkar drop-in nästan alltid. Kommer ni som större sällskap, maila mig på sundsvall@guiltypleasure.se så löser vi det tillsammans. Och följ @guiltypleasure.se på Instagram — där droppar nyheterna först, nästan varje dag.</p>

<p>Comfort food på mitt vis betyder mat utan krusiduller men med full effekt — New York-diner i själen, Norrland i hjärtat. Kom på lunchen, kom på middagen, kom bara. Tempot i köket är högt så att tempot vid ditt bord kan vara precis så lågt du vill. Och kaffet tar jag på största allvar; det är därför det står Café på skylten.</p>
<p>Helgerna har tre akter även här. Brunchen öppnar spelet, middagen bygger vidare, och när fredags- och lördagskvällarna närmar sig midnatt har tredje akten — disco — tagit över rummet. Stenstan utanför fönstren har sett det mesta sedan 1800-talet, men jag vågar påstå att den sett få ställen med den här kombinationen av frozen mimosas och discokänsla.</p>
<p>Jag är Sundsvallsdelen av Guilty Pleasure-familjen — flaggskeppet ligger i Umeå, men själen är densamma: fyra färger, en attityd, och övertygelsen att livet är för kort för trista ställen. Välkommen in.</p>
"""

UMEA_FAQ = [
  ("Kan man boka bord på GP's i Umeå?","Nej — jag kör drop-in only, först till kvarn. Det är en princip: livet är för kort för tomma bord. Bordsbokning lanseras under hösten 2026; tills dess är det bara att komma in på Skolgatan 62."),
  ("Vilka öppettider har GP's i Umeå?","Måndag 11.30–22, tisdag–torsdag 11.30–00, fredag–lördag 11.30–01 och söndag 11.30–22. Fredagar och lördagar är det öppet till klockan ett."),
  ("Var i Umeå ligger GP's?","På Skolgatan 62, mitt i centrala Umeå — nära Rådhustorget och cirka tio minuters promenad från Umeå Central."),
  ("Är hundar välkomna på GP's Umeå?","Ja, hundar är alltid välkomna. Vatten står framme."),
  ("Finns alkoholfria drinkar på GP's?","Ja — hela No Regrets-listan är alkoholfri, från Virgin Prince 0.0 (79 kr) till alkoholfri Coffee Granita. Priserna ligger på 39–89 kr."),
  ("Hur kontaktar jag GP's i Umeå?","Maila umea@guiltypleasure.se eller skicka DM på Instagram @guiltypleasure.se. Telefon är på väg — AI-värdinnan svarar från augusti 2026."),
]

SUNDSVALL_FAQ = [
  ("Kan man boka bord på GP's i Sundsvall?","Ja — boka online via bokabord, så står bordet redo. Drop-in funkar lika bra: dörren på Storgatan 12 är öppen och baren har alltid plats för en till."),
  ("Vilka öppettider har GP's i Sundsvall?","Måndag–tisdag 11–22, onsdag–torsdag 11–00, fredag–lördag 11–01 och söndag 11–22. Helgkvällarna går till klockan ett."),
  ("Var i Sundsvall ligger GP's?","På Storgatan 12, mitt i Stenstan — Sundsvalls stenstadskärna, nära Stora torget."),
  ("Är hundar välkomna på GP's Sundsvall?","Ja, alltid. Vatten fixar jag."),
  ("Hur kontaktar jag GP's i Sundsvall?","Maila sundsvall@guiltypleasure.se eller DM:a @guiltypleasure.se på Instagram. Telefon kommer i augusti 2026 — då svarar AI-värdinnan."),
]

def city_page(key):
    c = CITIES[key]
    faqs = UMEA_FAQ if key=="umea" else SUNDSVALL_FAQ
    story = UMEA_STORY if key=="umea" else SUNDSVALL_STORY
    url=f"https://www.guiltypleasure.se/{key}/"
    title = f"Restaurang & bar i {c['name']} — GP's Guilty Pleasure Café, {c['street']}"
    desc = (f"New York-inspirerad comfort bistro på {c['street']}, {c['name']}. Brunch, dinner & disco. "
            + ("Drop-in only, hundar välkomna. Öppet till 01 fre–lör." if key=="umea" else "Boka bord online eller kom förbi — hundar välkomna. Öppet till 01 fre–lör."))
    schema = rest_schema(key,url) + "\n" + faq_schema(faqs,url)
    cta = (f'<a class="btn btn-fire stickycta" href="{c["booking"]}" rel="noopener">Boka bord</a>' if c["booking"]
           else f'<a class="btn btn-fire stickycta" href="{c["maps"]}" rel="noopener">Hitta hit</a>')
    booking_row = (f'<a class="btn btn-pink" href="{c["booking"]}" rel="noopener">Boka bord</a>' if c["booking"] else "")
    html = head(title,desc,f"/{key}/",extra_schema=schema,fontpath="../fonts/",og=f"og-{key}.png") + topbar("../") + f"""
<main id="top">
  <div class="wrap crumbs"><a href="../index.html">GP's</a> / {c['name']}</div>
  <section class="hero wrap" style="padding-top:34px">
    <div class="eyebrow">Guilty Pleasure Café · {c['name']}</div>
    <h1>{c['hero_h1']}</h1>
    <p class="sub">{c['hero_sub']} <span class="cstatus" data-city="{key}" aria-live="polite">…</span></p>
    <div class="cta-row">
      {booking_row}
      <a class="btn btn-line" href="{c['maps']}" rel="noopener">Vägbeskrivning</a>
      <a class="btn btn-line" href="{c['reviews']}" rel="noopener">Google-recensioner</a>
    </div>
  </section>
  <div class="marquee" aria-hidden="true"><span>BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · </span></div>
  <section class="wrap story">
    <div class="kicker">Min historia</div>
    <h2>Det här är <span class="accent">GP's {c['name']}</span></h2>
    {story}
  </section>
  <section class="wrap">
    <div class="kicker">Ur baren</div>
    <h2>Signaturer <span class="accent">&amp; guilty pleasures</span></h2>
    <div class="menucard">{MENU_ROWS}</div>
  </section>
  <section class="wrap">
    <div class="kicker">Praktiskt</div>
    <h2>Hitta hit <span class="accent">&amp; öppettider</span></h2>
    <div class="cities">
      <div class="city">
        <h3>{c['street']}, {c['postal']} {c['name']}</h3>
        <p>GP's — Guilty Pleasure Café ligger på {c['street']} i centrala {c['name']}. <a href="{c['maps']}" rel="noopener">Öppna vägbeskrivning i kartor</a>.</p>
        <p><a href="mailto:{c['email']}">{c['email']}</a></p>
        <p style="font-size:14px;opacity:.85">{"Drop-in only — kom som du är. Bordsbokning lanseras hösten 2026." if key=="umea" else "Boka online eller kom förbi — båda funkar lika bra."}</p>
      </div>
      <div class="city">{hours_table(key)}</div>
    </div>
  </section>
  <section class="wrap">
    <div class="kicker">Snabba svar</div>
    <h2>Frågor <span class="accent">&amp; svar</span></h2>
    {faq_html(faqs)}
  </section>
</main>
{cta}
""" + footer("../")
    html = html.replace("</body>", status_js("{"+f'"{key}":{c["hours_js"]}'+"}") + "\n</body>")
    return fix_amps(html)

# ---------------- HUBB ----------------
def hub():
    url="https://www.guiltypleasure.se/"
    title="GP's — Guilty Pleasure Café | Restaurang & bar i Umeå och Sundsvall"
    desc="New York-inspirerad comfort bistro i Umeå (Skolgatan 62) och Sundsvall (Storgatan 12). Brunch, dinner & disco — where cravings meet good vibes."
    org = {"@context":"https://schema.org","@type":"Organization","@id":url+"#org",
      "name":"Guilty Pleasure Café","url":url,
      "sameAs":["https://www.instagram.com/guiltypleasure.se/","https://www.facebook.com/gpsumea/","https://www.tiktok.com/@guiltypleasure.se"],
      "subOrganization":[{"@type":"Restaurant","@id":"https://www.guiltypleasure.se/umea/#restaurant"},{"@type":"Restaurant","@id":"https://www.guiltypleasure.se/sundsvall/#restaurant"}]}
    schema='<script type="application/ld+json">'+json.dumps(org,ensure_ascii=False)+'</script>'
    html = head(title,desc,"/",extra_schema=schema,fontpath="fonts/") + topbar("") + f"""
<main id="top">
  <section class="hero wrap">
    {LOGO}
    <div class="eyebrow">New York-inspirerad comfort bistro · Umeå &amp; Sundsvall</div>
    <h1>Where cravings meet good vibes</h1>
    <p class="sub">Jag serverar good mood comfort food, snabbt — med en cheeky attityd. Brunch, dinner &amp; disco i två städer. Välj din.</p>
    <div class="cta-row">
      <a class="btn btn-pink" href="umea/index.html">GP's Umeå</a>
      <a class="btn btn-pink" href="sundsvall/index.html">GP's Sundsvall</a>
      <a class="btn btn-line" href="#signaturer">Se signaturerna</a>
    </div>
  </section>
  <div class="marquee" aria-hidden="true"><span>BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · BRUNCH · DINNER · DISCO · </span></div>
  <section class="wrap">
    <div class="kicker">Tre akter, varje vecka</div>
    <h2>Dagen på <span class="accent">GP's</span></h2>
    <div class="acts">
      <article class="act"><span class="tagpill">Akt 1</span><h3>Brunch</h3><p>Långa förmiddagar, frozen mimosas och comfort-klassiker. Kom hungrig, gå lycklig.</p></article>
      <article class="act"><span class="tagpill">Akt 2</span><h3>Dinner</h3><p>New York-bistro möter norrländsk gästvänlighet. Maten kommer snabbt — sällskapet stannar länge.</p></article>
      <article class="act"><span class="tagpill">Akt 3</span><h3>Disco</h3><p>När mörkret faller vrider jag upp volymen. Fredagar och lördagar öppet till ett.</p></article>
    </div>
  </section>
  <section class="wrap" id="signaturer">
    <div class="kicker">Ur baren</div>
    <h2>Signaturer <span class="accent">&amp; guilty pleasures</span></h2>
    <div class="menucard">{MENU_ROWS}</div>
  </section>
  <section class="wrap">
    <div class="kicker">Två städer, en själ</div>
    <h2>Välj din <span class="accent">GP's</span></h2>
    <div class="cities">
      <div class="city">
        <h3>Umeå <span class="cstatus" data-city="umea" aria-live="polite">…</span></h3>
        <p>Flaggskeppet sedan 2021. Skolgatan 62, mitt i stan. Drop-in only — livet är för kort för tomma bord.</p>
        {hours_table("umea")}
        <div class="cta-row" style="justify-content:flex-start"><a class="btn btn-pink" href="umea/index.html">Till Umeå-sidan</a></div>
      </div>
      <div class="city">
        <h3>Sundsvall <span class="cstatus" data-city="sundsvall" aria-live="polite">…</span></h3>
        <p>Mitt i Stenstan på Storgatan 12. Finger-licking good — all day, everyday. Boka bord eller kom förbi.</p>
        {hours_table("sundsvall")}
        <div class="cta-row" style="justify-content:flex-start"><a class="btn btn-pink" href="sundsvall/index.html">Till Sundsvall-sidan</a><a class="btn btn-fire" href="https://app.bokabord.se" rel="noopener">Boka bord</a></div>
      </div>
    </div>
  </section>
  <section class="igband">
    <div class="wrap" style="padding-top:52px;padding-bottom:52px">
      <div class="kicker">Nästan dagligen i flödet</div>
      <h2>Följ <span class="accent">@guiltypleasure.se</span></h2>
      <p>Dagens rätt, nya drinkar och allt som händer efter mörkrets inbrott — det droppar först på Instagram.</p>
      <a class="btn btn-pink" href="https://www.instagram.com/guiltypleasure.se/" rel="noopener">Följ mig på Instagram</a>
    </div>
  </section>
</main>
""" + footer("")
    html = html.replace("</body>", status_js('{"umea":'+CITIES["umea"]["hours_js"]+',"sundsvall":'+CITIES["sundsvall"]["hours_js"]+"}") + "\n</body>")
    return fix_amps(html)

# ---------------- SITEMAP + ROBOTS ----------------
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.guiltypleasure.se/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://www.guiltypleasure.se/umea/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://www.guiltypleasure.se/sundsvall/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>
</urlset>
"""
ROBOTS = """User-agent: *
Allow: /

# AI-crawlers uttryckligen välkomna (AEO)
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: https://www.guiltypleasure.se/sitemap.xml
"""

# ---------------- BYGG + VERIFIERA ----------------
if __name__ == "__main__":
    (ROOT/"umea").mkdir(exist_ok=True); (ROOT/"sundsvall").mkdir(exist_ok=True)
    pages = {"index.html":hub(),"umea/index.html":city_page("umea"),"sundsvall/index.html":city_page("sundsvall")}
    for p,contents in pages.items(): (ROOT/p).write_text(contents, encoding="utf-8")
    (ROOT/"sitemap.xml").write_text(SITEMAP, encoding="utf-8"); (ROOT/"robots.txt").write_text(ROBOTS, encoding="utf-8")

    # 404 — Cloudflare Pages serverar 404.html automatiskt (tvåspråkig, noindex)
    nf = head("Sidan finns inte — GP's Guilty Pleasure Café","Oops — den här sidan finns inte. Men menyn gör det.","/404.html") + topbar("") + """
<main id="top">
  <section class="hero wrap">
    <div class="eyebrow">404 · Page not found</div>
    <h1>Oops — den här sidan finns inte</h1>
    <p class="sub">Men lugn: maten, drinkarna och discot finns kvar. This page doesn't exist — but the good vibes do.</p>
    <div class="cta-row">
      <a class="btn btn-pink" href="/">Till startsidan</a>
      <a class="btn btn-pink" href="/meny/">Se menyn</a>
      <a class="btn btn-line" href="/en/">In English</a>
    </div>
  </section>
</main>
""" + footer("")
    # 404 ska aldrig indexeras och ska inte ha canonical. Under PRELAUNCH sätter
    # head() redan noindex på alla sidor — undvik då en dubblerad robots-tagg.
    nf = fix_amps(nf.replace('<link rel="canonical" href="https://www.guiltypleasure.se/404.html">',
                             '' if PRELAUNCH else '<meta name="robots" content="noindex">'))
    # 404 serveras på godtyckligt URL-djup -> absoluta stigar
    for a,b in (('href="index.html','href="/index.html'),('href="umea/index.html"','href="/umea/"'),
                ('href="sundsvall/index.html"','href="/sundsvall/"'),('url("fonts/','url("/fonts/'),
                ('href="favicon.svg"','href="/favicon.svg"'),('href="apple-touch-icon.png"','href="/apple-touch-icon.png"')):
        nf = nf.replace(a,b)
    nf = nf.replace('href="/index.html#signaturer"','href="/#signaturer"').replace('href="/index.html"','href="/"')
    (ROOT/"404.html").write_text(nf, encoding="utf-8")

    # KVALITETSGRINDAR
    report=[]
    for p,contents in pages.items():
        blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>', contents, re.S)
        for b in blocks: json.loads(b)  # kastar vid fel
        assert "tel:" not in contents, p
        assert 'lang="sv"' in contents, p
        report.append(f"{p}: {len(contents)//1024} KB, {len(blocks)} schema-block OK")
    for k,v in QA_CONTRAST.items(): report.append(f"kontrast {k}: {v:.2f}:1")
    # ordräkning stadstexter
    import html as h
    for key,story in (("umea",UMEA_STORY),("sundsvall",SUNDSVALL_STORY)):
        words=len(re.sub(r"<[^>]+>"," ",story).split()); report.append(f"story {key}: {words} ord")
    print("\n".join(report))
