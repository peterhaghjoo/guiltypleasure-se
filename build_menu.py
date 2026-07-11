#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Menysidan — hela sommarmenyn 2026 ur GP_Menu_Copy_Final. Körs efter build.py."""
import json, re, pathlib
from build import head, topbar, footer, CITIES, breadcrumbs

ROOT = pathlib.Path(__file__).parent
(ROOT/"meny").mkdir(exist_ok=True)

# (namn, pris, beskrivning, tagg)  — exakt copy från GP_Menu_Copy_Final_2026-07-06
MAT = [
 ("Snacks", [
  ("Löjrom & Chips","139","Löjrom, smetana, rödlök, gräslök & dill.",""),
  ("Tryffelpopcorn","59","",""),("Gröna Oliver","49","",""),("Marconamandlar","45","",""),
 ]),
 ("Small Plates", [
  ("Cream Cheese Garlic Bun","99","Brioche, sötad färskost, vitlökssmör & persilja.",""),
  ("Spicy Feta Dip","109","Feta, hot honey, aleppo & grillat bröd.",""),
  ("Manchego Cornribs","139","Majsribs, manchego, cayennemajo, koriander & lime.",""),
  ("Mini Lobster Rolls","199","Hummer, räka, grönt äpple, skirat smör & gräslök.",""),
  ("Sesame Tuna Taco","169","Tonfisk, krispig gyoza, salladslöksmajo, ananas & furikake.",""),
  ("Crispy Råbiff","169 / 269","Råbiff, risnudlar, pepparmajo, friterad lök & koriander. ½ / hel med pommes.",""),
 ]),
 ("Big Plates", [
  ("Double Cheeseburger","229","2× smash, cheddar, pepparmajo, pickles & pommes.",""),
  ("Truffle Mafaldine","229","Mafaldine, tryffelsås, marconamandlar, parmesan & citron.",""),
  ("Spicy Nduja Moules Frites","269","Blåmusslor, gochujang-gräddsås, nduja, yuzuaioli & pommes.",""),
  ("Scampi Mafaldine","239","Scampi, vongolesås, chili, vitlök, tomat & persilja.",""),
  ("Caesar Crunch Salad","229","Kyckling/räkor, bacon, parmesan & caesardressing.",""),
  ("GP's Räkmacka","239","Handskalade räkor, ägg, dill & pepparrotskräm.",""),
  ("Ponzu Tuna Bowl","229","Tonfisk, limeponzu, glasnudlar, sesam & puffat ris.",""),
  ("Steak 'n Fries","369","Grain-fed ryggbiff, rödvinssås, chimichurrismör & pommes.",""),
 ]),
 ("Pizza", [
  ("Hot Honey Pepperoni","239","Mozzarella, pepperoni, hot honey, jalapeño & parmesan.",""),
  ("Löjromspizza","289","Västerbottensost, smetana, löjrom, chips, rödlök & dill.",""),
  ("Creamy Burrata","229","Mozzarella, burrata, semibakade tomater, basilikaaioli & parmesan.",""),
 ]),
 ("Desserts", [
  ("Tiramisu Cloud","129","Dubbel tiramisu, savoiardi, kaffe, mascarponeskum & kakao.",""),
  ("American Cookie Sundae","129","Varma cookies, mjukglass & cornflakes.",""),
  ("Chocolate Strawberries","99","Jordgubbar & smält belgisk mjölkchoklad.",""),
  ("Blood Orange Sorbet","75","Blodapelsinsorbet & mörk choklad.",""),
 ]),
 ("Dips", [
  ("Tryffel","29","",""),("Cayenne","29","",""),("Yuzuaioli","29","",""),("Pepparmajo","29","",""),("Ketchup","19","",""),
 ]),
]

BAR = [
 ("Summer Drinks", [
  ("Adult Lemonade Spritz","139","Maker's Mark, lemon curd, citrus & soda.",""),
  ("Strawberry & White","149","Vodka, jordgubbar, vit choklad & digestive.",""),
  ("Rhubarb 3.0","139","Vodka, rabarber ×3, vanilj & kardemumma.",""),
  ("Sour Cherry","139","Gin, körsbär & citrus.",""),
  ("Strawberry Daiquiri","139","Rom, lime, jordgubbar & socker.",""),
  ("Coffee Granita","139","Vodka, kaffelikör & espresso granita. Original / Salted Caramel / Kanelbulle.",""),
  ("Mojito","129 / 179","Rom, lime, mynta, socker & soda. Klassisk / Passion / Jordgubb.",""),
  ("Mojito-Kanna","449","3–6 personer. Klassisk / Passion / Jordgubb.",""),
 ]),
 ("Golden Hits", [
  ("Ghost of Prince","149","Gin, viol, citron, ingefäraskum & salt.","signature"),
  ("Disco Colada","139","Rom, vanilj, apelsin, ananas, lime & kokos.",""),
  ("Spicy Margarita","139","Tequila, lime, jalapeño & tajinsalt.",""),
  ("French Kiss","139","Svartvinbär, moscato, citron, ingefära & marängskum.",""),
  ("Espresso Martini Cloud","159","Vodka, Kahlúa, espresso & salt.",""),
 ]),
 ("Shots", [
  ("Birthday Shot","89","Vodka, jordgubbe & kokosskum.",""),
  ("Cold Shot","79","Galliano, körsbär & glass.",""),
  ("Tequila","89","Tequila, lime & salt.",""),
  ("Äppelpaj","119","Fireball, kanel & äpple.",""),
 ]),
 ("No Regrets — 0.0 %", [
  ("Virgin Prince","79","Viol, citron, ingefäraskum & salt.","no regrets"),
  ("Virgin Disco","79","Ananas, lime, kokos & skum.",""),
  ("Virgin Sour Cherry","89","Syrligt körsbär, citrus & socker.",""),
  ("Virgin Mojito","99","Lime, mynta, socker & soda.",""),
  ("Coffee Granita 0.0 %","89","Espresso granita. Original / Salted Caramel / Kanelbulle.",""),
 ]),
 ("Bar Classics", [
  ("Aperol Spritz","129","Aperol, cava & apelsin.",""),
  ("GP's Hernö G&T","149","Hernö gin, tonic & citron.",""),
  ("Flygplans-GT","119","Gin, tonic & lime.",""),
  ("Negroni","149","Gin, söt vermouth & Campari.",""),
  ("Redbull Vodka","149","Vodka & Red Bull Original / Sugar Free.",""),
 ]),
 ("Vitt vin · glas / karaff / flaska", [
  ("Husets Vita","89 / 149 / 449","Friskt, torrt & lätt.",""),
  ("Riesling 1L","119 / 189 / 779","Scheuermann, DE · äpple, citrus & örter.",""),
  ("Chardonnay","149 / 249 / 739","Joseph Burrier, FR · päron, acacia & citrus.",""),
  ("Anjou Blanc","849","Boudignon, FR · Chenin, sälta & mineral.",""),
  ("Chablis","899","Vocoret, FR · citrus, sälta & mineral.",""),
  ("Pouilly-Fuissé 2013","1199","Beauregard, FR · honung, citrus & rostat.",""),
 ]),
 ("Rött & rosé · glas / karaff / flaska", [
  ("Husets Röda","89 / 149 / 449","Mjukt, bärigt & lättdrucket.",""),
  ("Husets Rosé","89 / 149 / 449","Le Arche, IT · hallon, smultron & blodgrape.",""),
  ("Côte du Rhône","119 / 189 / 549","Trapadis, FR · Grenache, bär & krydda.",""),
  ("Carignan","129 / 219 / 649","Myrko Tépus, FR · örtigt, rödfruktigt & mineral.",""),
  ("Pinot Noir","749","Joseph Burrier, FR · röda bär & silke.",""),
  ("Barolo MGM","1999","Fenocchio, IT · rosor, lakrits & tannin.",""),
 ]),
 ("Bubbel · glas / flaska", [
  ("Husets Bubbel","75","Prosecco, IT · friskt & lätt.",""),
  ("Husets Cava","89 / 449","Jaume Serra, ES · torrt, äpple & kex.",""),
  ("Rosécava","99 / 499","El Mar, ES · jordgubb, persika & blodgrape.",""),
  ("Els Vignerons","595","Pregadéu, ES · Xarel·lo, citrus & sälta.",""),
  ("Husets Champagne","799","Michel Gonet, FR · brioche, citrus & mineral.",""),
 ]),
 ("Öl & cider", [
  ("Carlsberg Export","75 / 139","5,0 % · krispig & lätt maltig · 2,2 L-kanna 399.",""),
  ("Carlsberg Hof","69","4,2 % · ljus & lättdrucken.",""),
  ("Eriksberg Lager","95","5,3 % · rund & maltig.",""),
  ("Bryggverket Lager","79","5,0 % · krispig & lokal.",""),
  ("Hälsingbräu Pilsner","89","4,5 % · torr, frisk & glutenfri.",""),
  ("Bryggverket Lengräddad IPA","89","6,5 % · tropisk, len & grumlig.",""),
  ("To Øl Modern Pale","89","5,5 % · citrus & tropik.",""),
  ("Hammerhead Hazy IPA","109","7,0 % · juicig, tropisk & fyllig.",""),
  ("Thunder Hex IPA","139","8,0 % · intensiv, fruktig & mjuk.",""),
  ("Bryggverket Megasourus","119","8,0 % · syrlig, bärig & vanilj.",""),
  ("Taddy Porter","89","5,0 % · rostad, mörk & chokladig.",""),
  ("Pomsi Apple Cider","89","4,5 % · friskt äpple & citrus.",""),
  ("Somersby Pear","79","4,5 % · söt päronfrisk & lätt.",""),
 ]),
 ("0.0 % öl, vin & bubbel", [
  ("Carlsberg 0.0 %","69","",""),("Somersby Pear 0.0 %","69","",""),
  ("Husets Vita / Röda 0.0 %","89","",""),("Nozeco","89","",""),
 ]),
 ("Läsk & juice", [
  ("Läsk","39","Coca-Cola, Zero, Fanta, Sprite.",""),
  ("Ramlösa","39","Naturell / Citrus.",""),
  ("Red Bull","49","Original / Sugar Free.",""),
  ("Jarritos Mandarin","49","",""),
  ("Juice","29","Äpple / Apelsin.",""),
 ]),
 ("Kaffe & te", [
  ("Bryggkaffe","39","",""),("Cappuccino","49","",""),("Café Latte","49","",""),
  ("Espresso","39","",""),("Rött / Svart Te","39","",""),
 ]),
]

def rows(items):
    out=[]
    for namn,pris,desc,tag in items:
        sig = f'<span class="sig">{tag}</span>' if tag else ""
        p = f"<p>{desc}</p>" if desc else ""
        if desc:
            out.append(f'<details class="mrow"><summary><b>{namn}</b>{sig}<span class="dots"></span><span class="price">{pris}</span></summary>{p}</details>')
        else:
            out.append(f'<div class="mrow"><summary style="display:flex;align-items:baseline;gap:8px;padding:8px 0"><b>{namn}</b>{sig}<span class="dots"></span><span class="price">{pris}</span></summary></div>')
    return "\n".join(out)

def section_cards(data):
    cards=[]
    for rubrik,items in data:
        cards.append(f'<div class="menucard" style="max-width:none;margin:0 0 22px"><div class="mc-head"><span class="tagpill">{rubrik}</span></div>{rows(items)}</div>')
    return "\n".join(cards)

url="https://www.guiltypleasure.se/meny/"
title="Meny — GP's Guilty Pleasure Café | Mat, cocktails, vin & öl"
desc="Hela GP's sommarmeny 2026: comfort food, pizza, cocktails, No Regrets 0.0 %, vinlista och öl. Samma meny hela dagen — brunch, dinner & disco."

menu_schema = {"@context":"https://schema.org","@type":"Menu","@id":url+"#menu",
  "name":"GP's meny — Sommar 2026","inLanguage":"sv",
  "hasMenuSection":[
    {"@type":"MenuSection","name":sek,"hasMenuItem":[
        {"@type":"MenuItem","name":n,"description":d,"offers":{"@type":"Offer","price":p.split(" / ")[0],"priceCurrency":"SEK"}}
        for n,p,d,_ in items]}
    for sek,items in (MAT+BAR)]}
schema=('<script type="application/ld+json">'+json.dumps(menu_schema,ensure_ascii=False)+'</script>'
        + "\n" + breadcrumbs([("Hem","https://www.guiltypleasure.se/"),("Meny",url)], url))

html = head(title,desc,"/meny/",extra_schema=schema,fontpath="../fonts/",og="og-meny.png") + topbar("../") + f"""
<main id="top">
  <div class="wrap crumbs"><a href="../index.html">GP's</a> / Meny</div>
  <section class="hero wrap" style="padding-top:34px;padding-bottom:20px">
    <div class="eyebrow">All day — samma meny hela dagen · Sommar 2026 · Mån–Sön</div>
    <h1>Drypande god mat &amp; drinkar som håller historierna vid liv</h1>
    <p class="sub">Min meny byter skepnad med säsongen — det här är sommaren. Priser i kronor. Allergier eller veganskt? Fråga mig, jag hjälper dig.</p>
    <div class="cta-row"><a class="btn btn-pink" href="#mat">Maten</a><a class="btn btn-line" href="#bar">Baren</a></div>
  </section>
  <div class="marquee" aria-hidden="true"><span>DAY &amp; NIGHT DEAL · 1 SMALL + 1 BIG = 299 · LOBSTER +50 · STEAK +100 · DAY &amp; NIGHT DEAL · 1 SMALL + 1 BIG = 299 · LOBSTER +50 · STEAK +100 · </span></div>
  <section class="wrap" id="mat">
    <div class="kicker">Sida 1</div>
    <h2>Maten <span class="accent">— drypande god</span></h2>
    {section_cards(MAT)}
    <div class="menucard" style="max-width:none;border-color:var(--flame)">
      <div class="mc-head"><span class="tagpill" style="background:var(--night);color:var(--pink);border:1.5px solid var(--flame)">Day &amp; Night Deal</span></div>
      <details class="mrow"><summary><b>1 Small Plate + 1 Big Plate</b><span class="dots"></span><span class="price">299</span></summary><p>Gäller hela dagen, hela kvällen. Lobster +50 · Steak +100.</p></details>
    </div>
  </section>
  <section class="wrap surf-moss" id="bar">
    <div class="kicker">Sida 2 · Skål!</div>
    <h2>Baren <span class="accent">— cocktails, vin &amp; öl</span></h2>
    <p class="sub" style="margin:0 0 22px">Drinkpaket: Bubbel + Öl/Vin + Kaffe 149 · Alkoholfritt paket 119.</p>
    {section_cards(BAR)}
  </section>
</main>
""" + footer("../")
from build import fix_amps
(ROOT/"meny/index.html").write_text(fix_amps(html), encoding="utf-8")

# --- patcha övriga sidor: nav-länk till menyn + rätta signaturpriser ---
def patch(p, repl):
    f=(ROOT/p); s=f.read_text(encoding="utf-8"); changed=False
    for a,b in repl:
        if a in s: s=s.replace(a,b); changed=True
    f.write_text(s, encoding="utf-8"); return changed

price_fix = [
  ('Hela menyn får du på plats — den byter skepnad med säsongen.',
   '<a href="MENYPATH">Se hela menyn →</a> Den byter skepnad med säsongen.'),
]
for p,menypath,navlabel in (("index.html","meny/index.html","Meny"),
                            ("umea/index.html","../meny/index.html","Meny"),
                            ("sundsvall/index.html","../meny/index.html","Meny"),
                            ("en/index.html","../meny/index.html","Menu")):
    pfx = "" if p=="index.html" else "../"
    nav_add = [('<a href="{0}umea/index.html">Umeå</a>'.format(pfx),
                '<a href="{1}">{2}</a>\n      <a href="{0}umea/index.html">Umeå</a>'.format(pfx, menypath, navlabel))]
    patch(p, nav_add + [(a, b.replace("MENYPATH",menypath)) for a,b in price_fix])

# sitemap + verifiering
sm=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
if "/meny/" not in sm:
    sm=sm.replace("</urlset>",'  <url><loc>https://www.guiltypleasure.se/meny/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>\n</urlset>')
    (ROOT/"sitemap.xml").write_text(sm, encoding="utf-8")

s=(ROOT/"meny/index.html").read_text(encoding="utf-8")
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(b)
assert "Ghost of Prince" in s and "Barolo" in s and "tel:" not in s
n_items = sum(len(i) for _,i in MAT+BAR)
print(f"meny/index.html: {len(s)//1024} KB · {n_items} rätter/drycker · schema OK · sitemap {'/meny/' in sm}")
for p in ("index.html","umea/index.html","sundsvall/index.html","en/index.html"):
    t=(ROOT/p).read_text(encoding="utf-8")
    ok_nav = "meny/index.html" in t
    ok_price = 'price">149' in t and '159' not in t
    ok_foot = ("Se hela menyn" in t) or ("See the full menu" in t)
    assert ok_nav and ok_price, f"{p}: nav={ok_nav} price={ok_price}"
    print(p, "meny-länk:", ok_nav, "· Ghost 149:", ok_price, "· meny-foot:", ok_foot)
