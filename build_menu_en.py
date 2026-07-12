#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Engelska menysidan /en/meny/ — verkstans backlogpunkt "språkläckan".

Körs EFTER build_menu.py (svenska menysidan måste finnas för hreflang-paret)
och FÖRE build_en_cities.py: se kedjan i ci_build.sh.

FAKTADISCIPLIN (samma regler som allt annat, se data/facts/):
- Rättnamn och priser är IDENTISKA med svenska menyn — de importeras rakt av
  ur build_menu.py (MAT/BAR) och kan inte glida isär. Verifieras dessutom
  mot den byggda svenska sidan längst ned: exakt samma (namn, pris)-lista.
- Endast beskrivningar och sektionsrubriker översätts, till naturlig engelska
  i vi-form. INGA nya påståenden, inget ur data/facts/removed.json.
- Ghost of Prince = 149 (som svenska menyn; brunchkällans 159 är en känd
  konflikt som löses i BACKLOG 2.1 — inte här).
"""
import json, re, pathlib
from build import head, topbar, footer, breadcrumbs, fix_amps
from build_menu import MAT, BAR, section_cards

ROOT = pathlib.Path(__file__).parent
(ROOT/"en/meny").mkdir(parents=True, exist_ok=True)

# --- sektionsrubriker: svensk rubrik -> engelsk (identitet där källan redan är engelsk)
SECTION_EN = {
 "Snacks":"Snacks",
 "Small Plates":"Small Plates",
 "Big Plates":"Big Plates",
 "Pizza":"Pizza",
 "Desserts":"Desserts",
 "Dips":"Dips",
 "Summer Drinks":"Summer Drinks",
 "Golden Hits":"Golden Hits",
 "Shots":"Shots",
 "No Regrets — 0.0 %":"No Regrets — 0.0 %",
 "Bar Classics":"Bar Classics",
 "Vitt vin · glas / karaff / flaska":"White wine · glass / carafe / bottle",
 "Rött & rosé · glas / karaff / flaska":"Red & rosé · glass / carafe / bottle",
 "Bubbel · glas / flaska":"Bubbles · glass / bottle",
 "Öl & cider":"Beer & cider",
 "0.0 % öl, vin & bubbel":"0.0 % beer, wine & bubbles",
 "Läsk & juice":"Soft drinks & juice",
 "Kaffe & te":"Coffee & tea",
}

# --- beskrivningar: exakt svensk källsträng -> naturlig engelska.
# Identitet där källan redan är engelska (produktnamn/varianter behålls).
# Varje rätt med beskrivning MÅSTE ha en nyckel här — bygget failar annars,
# så ingen svenska kan läcka ut på EN-sidan i tysthet.
DESC_EN = {
 # Snacks
 "Löjrom, smetana, rödlök, gräslök & dill.":"Vendace roe, smetana, red onion, chives & dill.",
 # Small Plates
 "Brioche, sötad färskost, vitlökssmör & persilja.":"Brioche, sweetened cream cheese, garlic butter & parsley.",
 "Feta, hot honey, aleppo & grillat bröd.":"Feta, hot honey, aleppo & grilled bread.",
 "Majsribs, manchego, cayennemajo, koriander & lime.":"Corn ribs, manchego, cayenne mayo, coriander & lime.",
 "Hummer, räka, grönt äpple, skirat smör & gräslök.":"Lobster, shrimp, green apple, clarified butter & chives.",
 "Tonfisk, krispig gyoza, salladslöksmajo, ananas & furikake.":"Tuna, crispy gyoza, spring onion mayo, pineapple & furikake.",
 "Råbiff, risnudlar, pepparmajo, friterad lök & koriander. ½ / hel med pommes.":"Beef tartare, rice noodles, pepper mayo, fried onions & coriander. ½ / whole with fries.",
 # Big Plates
 "2× smash, cheddar, pepparmajo, pickles & pommes.":"2× smash patties, cheddar, pepper mayo, pickles & fries.",
 "Mafaldine, tryffelsås, marconamandlar, parmesan & citron.":"Mafaldine, truffle sauce, marcona almonds, parmesan & lemon.",
 "Blåmusslor, gochujang-gräddsås, nduja, yuzuaioli & pommes.":"Blue mussels, gochujang cream sauce, nduja, yuzu aioli & fries.",
 "Scampi, vongolesås, chili, vitlök, tomat & persilja.":"Scampi, vongole sauce, chilli, garlic, tomato & parsley.",
 "Kyckling/räkor, bacon, parmesan & caesardressing.":"Chicken/shrimp, bacon, parmesan & caesar dressing.",
 "Handskalade räkor, ägg, dill & pepparrotskräm.":"Hand-peeled shrimp, egg, dill & horseradish cream.",
 "Tonfisk, limeponzu, glasnudlar, sesam & puffat ris.":"Tuna, lime ponzu, glass noodles, sesame & puffed rice.",
 "Grain-fed ryggbiff, rödvinssås, chimichurrismör & pommes.":"Grain-fed sirloin, red wine sauce, chimichurri butter & fries.",
 # Pizza
 "Mozzarella, pepperoni, hot honey, jalapeño & parmesan.":"Mozzarella, pepperoni, hot honey, jalapeño & parmesan.",
 "Västerbottensost, smetana, löjrom, chips, rödlök & dill.":"Västerbotten cheese, smetana, vendace roe, chips, red onion & dill.",
 "Mozzarella, burrata, semibakade tomater, basilikaaioli & parmesan.":"Mozzarella, burrata, semi-dried tomatoes, basil aioli & parmesan.",
 # Desserts
 "Dubbel tiramisu, savoiardi, kaffe, mascarponeskum & kakao.":"Double tiramisu, savoiardi, coffee, mascarpone foam & cocoa.",
 "Varma cookies, mjukglass & cornflakes.":"Warm cookies, soft serve & cornflakes.",
 "Jordgubbar & smält belgisk mjölkchoklad.":"Strawberries & melted Belgian milk chocolate.",
 "Blodapelsinsorbet & mörk choklad.":"Blood orange sorbet & dark chocolate.",
 # Summer Drinks
 "Maker's Mark, lemon curd, citrus & soda.":"Maker's Mark, lemon curd, citrus & soda.",
 "Vodka, jordgubbar, vit choklad & digestive.":"Vodka, strawberries, white chocolate & digestive.",
 "Vodka, rabarber ×3, vanilj & kardemumma.":"Vodka, rhubarb ×3, vanilla & cardamom.",
 "Gin, körsbär & citrus.":"Gin, cherry & citrus.",
 "Rom, lime, jordgubbar & socker.":"Rum, lime, strawberries & sugar.",
 "Vodka, kaffelikör & espresso granita. Original / Salted Caramel / Kanelbulle.":"Vodka, coffee liqueur & espresso granita. Original / Salted Caramel / Cinnamon Bun.",
 "Rom, lime, mynta, socker & soda. Klassisk / Passion / Jordgubb.":"Rum, lime, mint, sugar & soda. Classic / Passion / Strawberry.",
 "3–6 personer. Klassisk / Passion / Jordgubb.":"3–6 people. Classic / Passion / Strawberry.",
 # Golden Hits — Ghost of Prince följer EN-konventionen från build_en.py
 "Gin, viol, citron, ingefäraskum & salt.":"Gin, violet, lemon, ginger foam & salt.",
 "Rom, vanilj, apelsin, ananas, lime & kokos.":"Rum, vanilla, orange, pineapple, lime & coconut.",
 "Tequila, lime, jalapeño & tajinsalt.":"Tequila, lime, jalapeño & tajín salt.",
 "Svartvinbär, moscato, citron, ingefära & marängskum.":"Blackcurrant, moscato, lemon, ginger & meringue foam.",
 "Vodka, Kahlúa, espresso & salt.":"Vodka, Kahlúa, espresso & salt.",
 # Shots
 "Vodka, jordgubbe & kokosskum.":"Vodka, strawberry & coconut foam.",
 "Galliano, körsbär & glass.":"Galliano, cherry & ice cream.",
 "Tequila, lime & salt.":"Tequila, lime & salt.",
 "Fireball, kanel & äpple.":"Fireball, cinnamon & apple.",
 # No Regrets
 "Viol, citron, ingefäraskum & salt.":"Violet, lemon, ginger foam & salt.",
 "Ananas, lime, kokos & skum.":"Pineapple, lime, coconut & foam.",
 "Syrligt körsbär, citrus & socker.":"Tart cherry, citrus & sugar.",
 "Lime, mynta, socker & soda.":"Lime, mint, sugar & soda.",
 "Espresso granita. Original / Salted Caramel / Kanelbulle.":"Espresso granita. Original / Salted Caramel / Cinnamon Bun.",
 # Bar Classics
 "Aperol, cava & apelsin.":"Aperol, cava & orange.",
 "Hernö gin, tonic & citron.":"Hernö gin, tonic & lemon.",
 "Gin, tonic & lime.":"Gin, tonic & lime.",
 "Gin, söt vermouth & Campari.":"Gin, sweet vermouth & Campari.",
 "Vodka & Red Bull Original / Sugar Free.":"Vodka & Red Bull Original / Sugar Free.",
 # Vitt vin
 "Friskt, torrt & lätt.":"Fresh, dry & light.",
 "Scheuermann, DE · äpple, citrus & örter.":"Scheuermann, DE · apple, citrus & herbs.",
 "Joseph Burrier, FR · päron, acacia & citrus.":"Joseph Burrier, FR · pear, acacia & citrus.",
 "Boudignon, FR · Chenin, sälta & mineral.":"Boudignon, FR · Chenin, salinity & minerality.",
 "Vocoret, FR · citrus, sälta & mineral.":"Vocoret, FR · citrus, salinity & minerality.",
 "Beauregard, FR · honung, citrus & rostat.":"Beauregard, FR · honey, citrus & toast.",
 # Rött & rosé
 "Mjukt, bärigt & lättdrucket.":"Soft, berry-forward & easy-drinking.",
 "Le Arche, IT · hallon, smultron & blodgrape.":"Le Arche, IT · raspberry, wild strawberry & blood grapefruit.",
 "Trapadis, FR · Grenache, bär & krydda.":"Trapadis, FR · Grenache, berries & spice.",
 "Myrko Tépus, FR · örtigt, rödfruktigt & mineral.":"Myrko Tépus, FR · herbal, red-fruited & mineral.",
 "Joseph Burrier, FR · röda bär & silke.":"Joseph Burrier, FR · red berries & silk.",
 "Fenocchio, IT · rosor, lakrits & tannin.":"Fenocchio, IT · roses, liquorice & tannin.",
 # Bubbel
 "Prosecco, IT · friskt & lätt.":"Prosecco, IT · fresh & light.",
 "Jaume Serra, ES · torrt, äpple & kex.":"Jaume Serra, ES · dry, apple & biscuit.",
 "El Mar, ES · jordgubb, persika & blodgrape.":"El Mar, ES · strawberry, peach & blood grapefruit.",
 "Pregadéu, ES · Xarel·lo, citrus & sälta.":"Pregadéu, ES · Xarel·lo, citrus & salinity.",
 "Michel Gonet, FR · brioche, citrus & mineral.":"Michel Gonet, FR · brioche, citrus & minerality.",
 # Öl & cider (decimalkomma -> punkt är konvention, inte faktabyte)
 "5,0 % · krispig & lätt maltig · 2,2 L-kanna 399.":"5.0% · crisp & lightly malty · 2.2 L pitcher 399.",
 "4,2 % · ljus & lättdrucken.":"4.2% · pale & easy-drinking.",
 "5,3 % · rund & maltig.":"5.3% · round & malty.",
 "5,0 % · krispig & lokal.":"5.0% · crisp & local.",
 "4,5 % · torr, frisk & glutenfri.":"4.5% · dry, fresh & gluten-free.",
 "6,5 % · tropisk, len & grumlig.":"6.5% · tropical, smooth & hazy.",
 "5,5 % · citrus & tropik.":"5.5% · citrus & tropics.",
 "7,0 % · juicig, tropisk & fyllig.":"7.0% · juicy, tropical & full-bodied.",
 "8,0 % · intensiv, fruktig & mjuk.":"8.0% · intense, fruity & smooth.",
 "8,0 % · syrlig, bärig & vanilj.":"8.0% · sour, berry-forward & vanilla.",
 "5,0 % · rostad, mörk & chokladig.":"5.0% · roasted, dark & chocolatey.",
 "4,5 % · friskt äpple & citrus.":"4.5% · fresh apple & citrus.",
 "4,5 % · söt päronfrisk & lätt.":"4.5% · sweet pear freshness & light.",
 # Läsk & juice
 "Coca-Cola, Zero, Fanta, Sprite.":"Coca-Cola, Zero, Fanta, Sprite.",
 "Naturell / Citrus.":"Naturell / Citrus.",
 "Original / Sugar Free.":"Original / Sugar Free.",
 "Äpple / Apelsin.":"Apple / Orange.",
}

def translate(data):
    """Samma struktur som MAT/BAR men engelska rubriker och beskrivningar.
    Namn och priser rörs INTE — de går rakt igenom, identiska per definition."""
    out=[]
    for sek,items in data:
        assert sek in SECTION_EN, f"saknad sektionsöversättning: {sek!r}"
        rader=[]
        for namn,pris,desc,tag in items:
            if desc:
                assert desc in DESC_EN, f"saknad beskrivningsöversättning ({namn}): {desc!r}"
            rader.append((namn,pris,DESC_EN[desc] if desc else "",tag))
        out.append((SECTION_EN[sek],rader))
    return out

MAT_EN = translate(MAT)
BAR_EN = translate(BAR)

def en_topbar():
    # Speglar svenska menysidans topbar (build_menu.py: topbar("../"), ingen
    # meny-självlänk) — men alla mål blir EN-sidor eftersom vi står i /en/meny/:
    # ../index.html -> /en/, ../umea/index.html -> /en/umea/ osv.
    return (topbar("../")
      .replace('aria-label="Huvudmeny"','aria-label="Main menu"')
      .replace(">Signaturer<",">Signatures<")
      .replace("GP's — startsida","GP's — home"))

def en_footer():
    # Samma översättningar som build_en_cities.py använder.
    return (footer("../")
      .replace("Häng med oss","Follow along")
      .replace("Ingen telefon än — maila oss eller skicka DM på Instagram.","No phone yet — email us or send a DM on Instagram.")
      .replace("Drop-in only — bara kom in.","Walk-ins only — just come in.")
      .replace("Boka bord online</a> — eller kom förbi.","Book a table online</a> — or drop by.")
      .replace("· karta</a>","· map</a>").replace('>karta<','>map<'))

def main():
    # Day & Night Deal-kortet: samma tokenfix som svenska menysidan (se
    # build_menu.py) — riktiga tokens --fire/--moss/--disco, aldrig två starka
    # färger i samma element. Speglar SV-sidan exakt.
    url="https://www.guiltypleasure.se/en/meny/"
    title="Menu — GP's Guilty Pleasure Café | Food, cocktails, wine & beer"
    desc="GP's full summer menu 2026: comfort food, pizza, cocktails, the zero-proof No Regrets list, wine and beer. Same menu all day — brunch, dinner & disco."

    menu_schema = {"@context":"https://schema.org","@type":"Menu","@id":url+"#menu",
      "name":"GP's menu — Summer 2026","inLanguage":"en",
      "hasMenuSection":[
        {"@type":"MenuSection","name":sek,"hasMenuItem":[
            {"@type":"MenuItem","name":n,"description":d,"offers":{"@type":"Offer","price":p.split(" / ")[0],"priceCurrency":"SEK"}}
            for n,p,d,_ in items]}
        for sek,items in (MAT_EN+BAR_EN)]}
    schema=('<script type="application/ld+json">'+json.dumps(menu_schema,ensure_ascii=False)+'</script>'
            + "\n" + breadcrumbs([("Home","https://www.guiltypleasure.se/en/"),("Menu",url)], url))

    html = head(title,desc,"/en/meny/",lang="en",extra_schema=schema,fontpath="../../fonts/",og="og-meny.png") + en_topbar() + f"""
<main id="top">
  <div class="wrap crumbs"><a href="../index.html">GP's</a> / Menu</div>
  <section class="hero wrap" style="padding-top:34px;padding-bottom:20px">
    <div class="eyebrow">All day — the same menu all day · Summer 2026 · Mon–Sun</div>
    <h1>Dripping good food &amp; drinks that keep the stories alive</h1>
    <p class="sub">Our menu changes with the seasons — this is summer. Prices in Swedish kronor. Allergies or vegan? Ask us, we'll help you.</p>
    <div class="cta-row"><a class="btn btn-pink" href="#mat">The food</a><a class="btn btn-line" href="#bar">The bar</a></div>
  </section>
  <div class="marquee" aria-hidden="true"><span>DAY &amp; NIGHT DEAL · 1 SMALL + 1 BIG = 299 · LOBSTER +50 · STEAK +100 · DAY &amp; NIGHT DEAL · 1 SMALL + 1 BIG = 299 · LOBSTER +50 · STEAK +100 · </span></div>
  <section class="wrap" id="mat">
    <div class="kicker">Page 1</div>
    <h2>The food <span class="accent">— dripping good</span></h2>
    {section_cards(MAT_EN)}
    <div class="menucard" style="max-width:none;border-color:var(--fire)">
      <div class="mc-head"><span class="tagpill" style="background:var(--moss);color:var(--disco)">Day &amp; Night Deal</span></div>
      <details class="mrow"><summary><b>1 Small Plate + 1 Big Plate</b><span class="dots"></span><span class="price">299</span></summary><p>Valid all day, all night. Lobster +50 · Steak +100.</p></details>
    </div>
  </section>
  <section class="wrap surf-moss" id="bar">
    <div class="kicker">Page 2 · Cheers!</div>
    <h2>The bar <span class="accent">— cocktails, wine &amp; beer</span></h2>
    <p class="sub" style="margin:0 0 22px">Drink packages: Bubbles + Beer/Wine + Coffee 149 · Zero-proof package 119.</p>
    {section_cards(BAR_EN)}
  </section>
</main>
""" + en_footer()
    (ROOT/"en/meny/index.html").write_text(fix_amps(html), encoding="utf-8")

    # --- hreflang: bidirektionellt par /meny/ <-> /en/meny/ + x-default -> sv ---
    # Samma mönster som build_en_cities.py använder för stadsparen.
    tag = ('<link rel="alternate" hreflang="sv" href="https://www.guiltypleasure.se/meny/">\n'
           '<link rel="alternate" hreflang="en" href="https://www.guiltypleasure.se/en/meny/">\n'
           '<link rel="alternate" hreflang="x-default" href="https://www.guiltypleasure.se/meny/">')
    for f in ("meny/index.html","en/meny/index.html"):
        p=(ROOT/f); s=p.read_text(encoding="utf-8")
        if 'hreflang' not in s:
            p.write_text(s.replace('<link rel="canonical"', tag+'\n<link rel="canonical"'), encoding="utf-8")

    # --- sitemap ---
    sm=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
    if "/en/meny/" not in sm:
        sm=sm.replace("</urlset>",'  <url><loc>https://www.guiltypleasure.se/en/meny/</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>\n</urlset>')
        (ROOT/"sitemap.xml").write_text(sm, encoding="utf-8")

    # --- verifiering ---
    s=(ROOT/"en/meny/index.html").read_text(encoding="utf-8")
    blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    for b in blocks: json.loads(b)
    assert 'lang="en"' in s and "tel:" not in s and "hreflang" in s
    assert '<link rel="canonical" href="https://www.guiltypleasure.se/en/meny/">' in s
    assert '../../fonts/' in s and 'og-meny.png' in s
    sv=(ROOT/"meny/index.html").read_text(encoding="utf-8")
    assert 'hreflang="en" href="https://www.guiltypleasure.se/en/meny/"' in sv, "svenska menyn saknar hreflang till EN"
    assert 'hreflang="sv" href="https://www.guiltypleasure.se/meny/"' in s, "EN-menyn saknar hreflang till sv"
    # Namn + priser EXAKT identiska med den byggda svenska sidan (ordning och allt)
    par = re.compile(r'<b>(.*?)</b>.*?<span class="price">(.*?)</span>')
    assert par.findall(s) == par.findall(sv), "namn/priser skiljer sig från svenska menyn"
    assert ("Ghost of Prince","149") in par.findall(s), "Ghost of Prince ska vara 149"
    # Ingen svensk beskrivning får ha läckt igenom (identitetsöversättningar undantagna)
    for _,items in MAT+BAR:
        for _,_,d,_ in items:
            if d and DESC_EN[d] != d:
                assert d not in s, f"svensk beskrivning läckte till EN-sidan: {d!r}"
    n_items = sum(len(i) for _,i in MAT_EN+BAR_EN)
    print(f"en/meny/index.html: {len(s)//1024} KB · {n_items} rätter/drycker · {len(blocks)} schema OK · "
          f"namn/priser identiska med sv · hreflang-par OK · sitemap {'/en/meny/' in sm}")

if __name__ == "__main__":
    main()
