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

# Robots-direktiv. Snippet-/preview-direktiven är kvar även under förlansering —
# de kostar inget och är redan rätt den dag PRELAUNCH slås av. Det enda som
# ändras vid cutover är index/noindex.
ROBOTS_META = ("noindex, nofollow" if PRELAUNCH else "index, follow") + \
              ", max-snippet:-1, max-image-preview:large, max-video-preview:-1"

FONT_B64 = base64.b64encode((ROOT/"fonts/gp-bold.woff2").read_bytes()).decode()
# Officiella varumärkeslockuper (brand-teamets Drive). fill="currentColor" gör
# dem OMFÄRGBARA -> de ärver textfärgen och får rätt kulör per yta automatiskt.
# logo-mark = GP's-symbolen (header), logo-cafe = fulla "Guilty Pleasure Café"-
# lockupen (hero), logo-stacked committas för framtida bruk. Path-datan är
# designens SANNING och rörs aldrig — bara färgmekanismen + viewBox-cropen.
MARK = (ROOT/"logo-mark.svg").read_text(encoding="utf-8")
LOGO = (ROOT/"logo-cafe.svg").read_text(encoding="utf-8").replace("<svg ", '<svg class="gp-logo" ', 1)

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

# Kontraktet mellan designen och WCAG. Varje par som FAKTISKT används i CSS:en
# står här med sitt krav. Bygget failar om någon kombination underskrider det.
#   4.5 = brödtext (normal storlek)
#   3.0 = stor text (>=18,66px fet) och UI-element/ramar
QA_REQUIRED = [
    ("brödtext mossa på grädde",      ratio(MOSSA, GRADDE), 4.5),
    ("brödtext grädde på mossa",      ratio(GRADDE, MOSSA), 4.5),
    ("brödtext mossa på disco",       ratio(MOSSA, DISCO),  4.5),  # hundsektionen
    ("disco på mossa (kicker, pris)", ratio(DISCO, MOSSA),  4.5),
    ("STOR eld på grädde (h1, pris)", ratio(ELD, GRADDE),   3.0),
    ("STOR grädde på eld (ortkort)",  ratio(GRADDE, ELD),   3.0),
]

# ---- A11y-BINDNINGAR: selector -> färgpar -> storlekskrav ---------------------
# Lighthouse-baseline 2026-07-11 hittade eldfärgad LITEN text (3,25:1 < 4,5:1)
# på fyra ställen efter designportningen: dagens rad i öppettiderna, brödsmule-
# länken, footer-rubrikerna och infokorts-/faktakortsrubrikerna (94-95 i a11y,
# skulle vara 100). QA_REQUIRED räckte inte — den mäter abstrakta färgpar men
# band dem aldrig till faktiska textstorlekar. Det är exakt hålet NATTRAPPORT
# beskrev. Bindningarna görs här: grinden failar om (a) den fixade CSS-
# deklarationen försvinner, (b) den gamla regressionen kommer tillbaka, eller
# (c) färgparet inte längre klarar kravet för sin storlek.
def wcag_krav(px, fet):
    """WCAG-tröskel: stor text (>=24px, eller >=18.66px fet) = 3.0:1, annars 4.5:1.
    px=None betyder icke-text (grafik/UI, SC 1.4.11) = 3.0:1."""
    if px is None: return 3.0
    return 3.0 if (px >= 24 or (fet and px >= 18.66)) else 4.5

QA_BOUND = [
    # (namn, css som MÅSTE finnas, css som ALDRIG får återvända, fg, bg, px, fet)
    ("hours dagens rad: fet text i arvsfärg",
     "table.hours tr.today td{font-weight:700}",
     "table.hours tr.today td{color:var(--fire)", MOSSA, GRADDE, 15, True),
    ("hours dagens rad: eld-punkt som GRAFIK (1.4.11)",
     "table.hours tr.today td:first-child::before{background:var(--fire)}",
     None, ELD, GRADDE, None, False),
    ("brödsmulelänk: mossa + understrykning (13px liten text)",
     ".crumbs a{text-decoration:underline;color:var(--moss)}",
     ".crumbs a{text-decoration:none;color:var(--fire)}", MOSSA, GRADDE, 13, True),
    ("footer h3: eld i 19px fet (stor text)",
     "footer h3{font-size:19px;color:var(--fire)}",
     "footer h3{font-size:14px", ELD, GRADDE, 19, True),
    (".infocard h3: eld i 19px fet (stor text)",
     ".infocard h3{font-family:var(--body);font-size:19px;color:var(--fire);",
     ".infocard h3{font-family:var(--body);font-size:15px", ELD, GRADDE, 19, True),
    (".fact h3: eld i 19px fet (stor text)",
     ".fact h3{font-size:19px;color:var(--fire)}",
     ".fact h3{font-size:15px", ELD, GRADDE, 19, True),
]

CSS = """
  /* ==========================================================================
     GP:s designsystem — portat från den godkända Claude Design-mockupen
     (guilty-pleasure-cafe/src/styles/design.css + tokens.css), 2026-07-11.

     GRUNDYTAN ÄR GRÄDDE, INTE MOSSA. Manualen (CLAUDE.md) säger: Grädde är
     bakgrund, Mossa är text. Sajten körde tvärtom — mörk botten, ljus text.
     Det är rättat här; allt annat i systemet hänger på den vändningen.

     KONTRASTREGLER (verifieras av QA_CONTRAST i bygget):
     - Brödtext: Mossa på Grädde (14,49:1) eller Grädde på Mossa (14,49:1).
     - Eld på Grädde = 3,25:1 → ENDAST stor text (>=18,66px fet) och UI-element.
       Aldrig löptext. Därför är .price satt till 19px fet — då kvalar den som
       stor text och får bära Eld.
     - Disco på Mossa = 8,20:1 → fritt fram, även liten text.
     - Aldrig två starka färger (Eld + Disco) i samma element.
     ========================================================================== */
  :root{
    --moss:#24270e;--cream:#fff8eb;--disco:#ff99ff;--fire:#ff450a;
    --line:rgba(36,39,14,.18);--line-cream:rgba(255,248,235,.22);--maxw:1080px;
    --display:"Guilty Pleasure","GP Fallback A","GP Fallback B","Arial Black",sans-serif;
    --body:"PP Neue Montreal","Montreal Fallback","Arial","Helvetica",sans-serif;
    /* Tracking-tokens = manualens typ-tabell (§3). Adobe-tracking / 1000 = em:
       Headline 0 · Alternativ rubrik 20 · Underrubrik/Ingress 40 · Brödtext 40.
       Används konsekvent nedan — inga letter-spacing utanför {0,.02em,.04em}. */
    --track-display:0;--track-alt:.02em;--track-ingress:.04em;--track-body:.04em;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
    /* Manualen s.13: BRÖDTEXT = PP Neue Montreal Medium, Tracking 40.
     Tracking 40 i Adobe-enheter = 0.04em i CSS. Låg på 0 — nu rättat. */
  body{background:var(--cream);color:var(--moss);font:500 16px/1.65 var(--body);
    letter-spacing:var(--track-body);overflow-x:hidden}
  /* Display-rubriker ska ha Tracking 0 (manualen s.13) — neutralisera arvet. */
  h1,h2,.marquee span,.act h3,.city h3{letter-spacing:var(--track-display)}
  img,svg{max-width:100%;height:auto}
  a{color:inherit;text-decoration:underline;text-decoration-thickness:.08em;text-underline-offset:.18em}
  a:hover{color:var(--fire)}

  /* ---- Helbreddsytor -------------------------------------------------------
     box-shadow + clip-path målar färgen ut till skärmkanten utan att röra
     layouten och utan att skapa horisontell scroll. Sektionerna är .wrap
     (max 1080px) — de behöver alltså inte struktureras om. */
  .surf-moss,.surf-disco{position:relative}
  .surf-moss{background:var(--moss);color:var(--cream);
    box-shadow:0 0 0 100vmax var(--moss);clip-path:inset(0 -100vmax)}
  .surf-disco{background:var(--disco);color:var(--moss);
    box-shadow:0 0 0 100vmax var(--disco);clip-path:inset(0 -100vmax)}

  .wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}

  /* ---- Header -------------------------------------------------------------- */
  .topbar{position:sticky;top:0;z-index:50;background:rgba(255,248,235,.94);
    backdrop-filter:blur(8px);border-bottom:1.5px solid var(--line)}
  .topbar .wrap{display:flex;align-items:center;gap:16px;height:62px}
  /* Header: officiella GP's-MÄRKET (logo-mark.svg) inline, ~34px, eld på grädde
     via currentColor. Ersätter den gamla textbaserade .wordmark. */
  .brandmark{display:inline-flex;align-items:center;color:var(--fire);
    text-decoration:none;line-height:0}
  .brandmark svg{height:34px;width:auto;display:block}
  .brandmark:hover{color:var(--moss)}
  nav{margin-left:auto;display:flex;gap:20px}
  nav a{text-decoration:none;font-weight:700;font-size:13px;letter-spacing:var(--track-alt);
    text-transform:uppercase;color:var(--moss)}
  nav a:hover{color:var(--fire)}
  @media(max-width:640px){nav{gap:12px} nav a.hidem{display:none}}

  /* ---- Hero + display-typografi -------------------------------------------
     Astro-mockupen kör h1 upp till 128px. Det är hela känslan. */
  .hero{padding:64px 0 44px;text-align:center}
  /* Hero: fulla "Guilty Pleasure Café"-lockupen (logo-cafe.svg), eld på grädde
     via currentColor, responsiv bredd. margin ger clearspace (~⅓ logohöjd luft
     under, manualen §5); hero-paddingen ger luften ovanför. */
  .gp-logo{width:min(440px,74vw);color:var(--fire);display:block;margin:0 auto 20px}
  /* 19px FET = "stor text" enligt WCAG -> 3,0:1-tröskeln gäller -> Eld (3,25:1) OK.
     På 12,5px hade den krävt 4,5:1 och fallit. Storleken är inte kosmetik, den är kravet. */
  .eyebrow{font-weight:700;font-size:19px;letter-spacing:var(--track-ingress);text-transform:uppercase;
    color:var(--fire)}
  h1{font-family:var(--display);font-weight:700;color:var(--fire);
    font-size:clamp(42px,9vw,120px);line-height:1.02;margin:16px auto 16px;
    max-width:15ch;text-wrap:balance}
  .sub{max-width:56ch;margin:0 auto 28px;font-size:17.5px;color:var(--moss)}
  .surf-moss .sub,.surf-moss p{color:var(--cream)}

  /* ---- Knappar ------------------------------------------------------------- */
  .cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
  /* 19px FET -> stor text -> 3,0:1 gäller -> Grädde på Eld (3,25:1) OK.
     På 14px krävdes 4,5:1 och knapparna föll. Ger dessutom bättre tryckyta på mobil. */
  .btn{display:inline-block;text-decoration:none;font-weight:700;letter-spacing:.04em;
    text-transform:uppercase;font-size:19px;padding:15px 28px;border-radius:9999px;
    min-height:44px;border:2px solid transparent;
    transition:background .18s ease,color .18s ease,border-color .18s ease}
  .btn-fire{background:var(--fire);color:var(--cream);border-color:var(--fire)}
  .btn-fire:hover{background:var(--moss);border-color:var(--moss);color:var(--cream)}
  .btn-pink{background:var(--disco);color:var(--moss);border-color:var(--disco)}
  .btn-pink:hover{background:var(--moss);border-color:var(--moss);color:var(--cream)}
  .btn-line{background:transparent;color:var(--moss);border-color:var(--moss)}
  .btn-line:hover{background:var(--moss);color:var(--cream)}
  .surf-moss .btn-line{color:var(--cream);border-color:var(--cream)}
  .surf-moss .btn-line:hover{background:var(--cream);color:var(--moss)}
  .surf-disco .btn-line{color:var(--moss);border-color:var(--moss)}

  /* ---- Marquee: eldband ---------------------------------------------------- */
  .marquee{background:var(--fire);color:var(--cream);padding:14px 0;overflow:hidden;
    white-space:nowrap;margin:34px 0 0}
  .marquee span{display:inline-block;font-family:var(--display);font-size:24px;
    color:var(--cream);animation:roll 28s linear infinite}
  @keyframes roll{from{transform:translateX(0)}to{transform:translateX(-50%)}}

  /* ---- Sektioner -----------------------------------------------------------
     OBS specificitet: sektionerna har class="wrap surf-moss", och .wrap sätter
     padding:0 22px — en klass slår elementselektorn `section`, så vertikal-
     paddingen försvann. Med bakgrundsfärg blir det direkt synligt (kickers
     klistrade mot fältkanten). Därför sätts paddingen explicit på section.wrap. */
  section{padding:64px 0}
  section.wrap{padding:64px 22px}
  .hero.wrap{padding:64px 22px 44px}
  /* Samma skäl som .eyebrow: Eld kräver stor text. 19px fet. */
  .kicker{font-weight:700;font-size:19px;letter-spacing:var(--track-ingress);text-transform:uppercase;
    color:var(--fire);margin-bottom:12px}
  .surf-moss .kicker{color:var(--disco)}
  .surf-disco .kicker{color:var(--moss)}
  h2{font-family:var(--display);font-weight:700;font-size:clamp(32px,5.4vw,64px);
    color:var(--moss);margin-bottom:24px;line-height:1.05;text-wrap:balance}
  .surf-moss h2{color:var(--cream)}
  .amp{font-family:var(--body);font-weight:700;font-size:.92em}
  h2 .accent{color:var(--fire)}
  .surf-moss h2 .accent{color:var(--disco)}
  .surf-disco h2,.surf-disco h2 .accent{color:var(--moss)}
  h3{font-weight:700;text-transform:uppercase;letter-spacing:var(--track-alt);font-size:20px;
    margin-bottom:10px}

  /* ---- Kort ---------------------------------------------------------------- */
  .acts{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
  @media(max-width:760px){.acts{grid-template-columns:1fr}}
  .act{background:var(--cream);border:2px solid var(--moss);border-radius:26px;
    padding:30px 24px;position:relative}
  .tagpill{background:var(--moss);color:var(--cream);font-weight:700;font-size:12px;
    letter-spacing:var(--track-alt);text-transform:uppercase;border-radius:9999px;padding:7px 15px;
    display:inline-block}
  .act .tagpill{position:absolute;top:-15px;left:22px}
  .act h3{font-family:var(--display);text-transform:none;font-size:30px;color:var(--fire);
    margin:10px 0}
  .act p{font-size:15.5px}

  /* ---- Menykort ------------------------------------------------------------ */
  .menucard{background:var(--cream);border:2px solid var(--moss);border-radius:26px;
    padding:34px 30px;max-width:640px;margin:0 auto}
  .surf-moss .menucard{background:var(--moss);border-color:var(--disco);color:var(--cream)}
  .mc-head{text-align:center;margin-bottom:20px}
  .mrow{padding:4px 0}
  .mrow summary{display:flex;align-items:baseline;gap:8px;cursor:pointer;list-style:none;
    padding:9px 0;min-height:44px}
  .mrow summary::-webkit-details-marker{display:none}
  .mrow b{font-weight:700;font-size:15.5px;text-transform:uppercase;letter-spacing:var(--track-alt)}
  .sig{color:var(--fire);font-family:var(--display);font-size:13px;text-transform:none;
    margin-left:6px}
  .surf-moss .sig{color:var(--disco)}
  .dots{flex:1;border-bottom:2px dotted var(--line);transform:translateY(-4px);min-width:24px}
  .surf-moss .dots{border-color:var(--line-cream)}
  /* 19px fet = "stor text" enligt WCAG -> Eld (3,25:1) är tillåtet här. */
  .price{font-weight:700;color:var(--fire);font-size:19px}
  .surf-moss .price{color:var(--disco)}
  .mrow p{font-size:14px;padding:0 0 10px;color:var(--moss)}
  .surf-moss .mrow p{color:var(--cream)}
  .mc-foot{text-align:center;margin-top:18px;font-size:13.5px}

  /* ---- Faktakort ----------------------------------------------------------- */
  .facts{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
  @media(max-width:760px){.facts{grid-template-columns:1fr}}
  .fact{border:2px solid var(--moss);border-radius:26px;padding:24px;background:var(--cream)}
  .fact h3{font-size:19px;color:var(--fire)}  /* 19px fet = stor text -> eld OK */
  .fact p{font-size:15px}

  /* ---- Ortkort: eldblock med stadsnamnet i displaytypsnitt ------------------
     Fyllt eldblock + gräddvit display-text = 3,25:1, godkänt för stor text.
     Statuspillret (.cstatus) är gräddvitt med mossatext (14,49:1) så det håller
     även som liten text ovanpå elden. */
  .cities{display:grid;grid-template-columns:1fr 1fr;gap:24px}
  @media(max-width:820px){.cities{grid-template-columns:1fr}}
  .city{background:var(--cream);border:2px solid var(--moss);border-radius:28px;
    overflow:hidden;display:flex;flex-direction:column}
  .city h3{font-family:var(--display);text-transform:none;
    font-size:clamp(34px,4.6vw,54px);line-height:1.05;
    background:var(--fire);color:var(--cream);margin:0;padding:26px 26px 22px;
    display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
  .city > :not(h3){margin-left:26px;margin-right:26px}
  .city > p{margin-top:20px;font-size:15.5px}
  .city .cta-row{justify-content:flex-start;margin:14px 0 26px}
  .cstatus{font-family:var(--body);font-size:12px;font-weight:700;letter-spacing:var(--track-alt);
    text-transform:uppercase;padding:6px 13px;border-radius:9999px;
    background:var(--cream);color:var(--moss);white-space:nowrap;display:inline-block}
  .cstatus.closed{background:var(--moss);color:var(--cream)}

  /* ---- Infokort (stadssidans "Praktiskt": adress + öppettider) --------------
     Egen klass, INTE .city — där är h3 ett stort eldblock med stadsnamnet,
     och en gatuadress i 54px displaytypsnitt vore bara löjligt. */
  .infocard{background:var(--cream);border:2px solid var(--moss);border-radius:26px;
    padding:28px 26px}
  /* 19px fet = stor text -> eld (3,25:1) klarar 3,0:1-kravet. På 15px föll den. */
  .infocard h3{font-family:var(--body);font-size:19px;color:var(--fire);
    text-transform:uppercase;letter-spacing:var(--track-alt);margin-bottom:14px}
  .infocard p{font-size:15.5px;margin-bottom:8px}

  /* ---- Öppettider ---------------------------------------------------------- */
  table.hours{width:100%;border-collapse:collapse;font-size:15px;margin:14px 0}
  table.hours td{padding:9px 0;border-bottom:1px solid var(--line)}
  table.hours td:last-child{text-align:right;font-weight:700}
  /* Dagens rad: FET text i ytans arvsfärg + eld-PUNKT (grafik, inte text).
     Eld på grädde är 3,25:1 och får INTE bära liten text (kravet är 4,5:1) —
     det var Lighthouse-regressionen 2026-07-11. Punkten är icke-text: SC 1.4.11
     kräver 3,0:1, och 3,25:1 klarar det. Fetstilen gör att signalen inte hänger
     på färg ensam (SC 1.4.1). En osynlig punkt reserveras på ALLA rader så att
     .today (sätts av JS efter load) inte knuffar layouten — noll CLS. */
  table.hours td:first-child::before{content:"";display:inline-block;width:8px;height:8px;
    border-radius:50%;background:transparent;margin-right:8px;vertical-align:1px}
  table.hours tr.today td{font-weight:700}
  table.hours tr.today td:first-child::before{background:var(--fire)}
  .surf-moss table.hours td{border-color:var(--line-cream)}
  .surf-moss table.hours tr.today td{color:var(--disco)}

  /* ---- FAQ ----------------------------------------------------------------- */
  .faq details{border:2px solid var(--moss);border-radius:18px;background:var(--cream);
    margin-bottom:12px}
  .faq summary{cursor:pointer;font-weight:700;padding:17px 20px;list-style:none;
    min-height:44px;font-size:15.5px;text-transform:uppercase;letter-spacing:var(--track-alt)}
  .faq summary::-webkit-details-marker{display:none}
  .faq summary::before{content:"▸ ";color:var(--fire);font-weight:700}
  .faq details[open] summary::before{content:"▾ "}
  .faq div{padding:0 20px 18px;font-size:15.5px}

  /* ---- Övrigt -------------------------------------------------------------- */
  .story p{max-width:64ch;margin:0 0 18px;font-size:17px;line-height:1.7}
  .story .lead{font-size:20px;font-weight:700}
  .crumbs{font-size:13px;padding:18px 0 0;text-transform:uppercase;letter-spacing:var(--track-alt);
    font-weight:700}
  /* Länkkonvention i stället för eldfärg: 13px är liten text, och eld på
     grädde (3,25:1) faller under 4,5:1-kravet. Mossa + understrykning — även
     vid hover, eftersom hover-tillstånd inte undantas av WCAG. */
  .crumbs a{text-decoration:underline;color:var(--moss)}
  .crumbs a:hover{color:var(--moss)}
  .stickycta{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:60;
    display:none}
  @media(max-width:820px){.stickycta{display:inline-block}}
  .igband{text-align:center}
  .igband p{max-width:46ch;margin:8px auto 22px}

  /* ---- Hundsektion: disco-yta, mossatext (8,20:1) --------------------------- */
  .dogs{text-align:left}
  .dogs .chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
  .dogs .chip{background:var(--moss);color:var(--cream);font-weight:700;font-size:12.5px;
    letter-spacing:var(--track-alt);text-transform:uppercase;border-radius:9999px;padding:9px 16px}
  .dogs p{max-width:52ch;font-size:17px}

  /* ---- Footer -------------------------------------------------------------- */
  footer{padding:52px 0 90px;font-size:15px;border-top:2px solid var(--moss);
    margin-top:0}
  .fgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;margin-bottom:26px}
  @media(max-width:760px){.fgrid{grid-template-columns:1fr}}
  /* 19px fet = stor text -> 3,0:1 gäller -> eld (3,25:1) OK. På 14px föll den. */
  footer h3{font-size:19px;color:var(--fire)}
  footer p{margin-bottom:6px}
  footer .soc a{font-weight:700;text-transform:uppercase;letter-spacing:var(--track-alt);font-size:13px;
    margin-right:14px}
  .fin{text-align:center;font-size:13px;margin-top:14px;color:var(--moss)}

  a:focus-visible,.btn:focus-visible,summary:focus-visible{outline:3px solid var(--fire);
    outline-offset:3px;border-radius:6px}
  @media (prefers-reduced-motion:reduce){
    .marquee span{animation:none}
    .btn{transition:none}
  }
  /* Ingen prick, ingen animation på symbolen.
     Grafisk manual s.19, don't #1: "Vi blandar inte flera färger i samma enhet"
     — manualens EGET exempel är GP's-symbolen i en färg med en prick i en annan.
     Don't #3: "Vi använder inte glow-effekter, det gör våra neonskyltar själva."
     Sajten hade en discofärgad prick som BLINKADE på den eldfärgade symbolen.
     Två don'ts i en enda CSS-rad. Borttagen 2026-07-11. Lägg aldrig tillbaka den. */
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
    hero_sub="Vi är flaggskeppet. Mitt i stan, på Skolgatan 62 — där cravings möter good vibes.",
  ),
  "sundsvall": dict(
    name="Sundsvall", street="Storgatan 12", postal="852 31", email="sundsvall@guiltypleasure.se",
    maps="https://maps.google.com/?q=Guilty+Pleasure+Caf%C3%A9+Storgatan+12+Sundsvall",
    reviews="https://www.google.com/search?q=Guilty+Pleasure+Caf%C3%A9+Sundsvall+recensioner",
    region="Västernorrlands län", booking="https://www.bokabord.se/restaurang/guilty-pleasure-cafe-sundsvall",
    hours_txt=[("Måndag","11–22"),("Tisdag","11–22"),("Onsdag","11–00"),("Torsdag","11–00"),("Fredag","11–01"),("Lördag","11–01"),("Söndag","11–22")],
    hours_js="{1:[660,1320],2:[660,1320],3:[660,1440],4:[660,1440],5:[660,1500],6:[660,1500],0:[660,1320]}",
    hours_schema=[["Monday","Tuesday","11:00","22:00"],["Wednesday","Thursday","11:00","00:00"],["Friday","Saturday","11:00","01:00"],["Sunday","Sunday","11:00","22:00"]],
    hero_h1="Finger-licking good — mitt i Stenstan",
    hero_sub="Vi är GP's i Sundsvall. Storgatan 12 — food and drinks, all day, everyday.",
  ),
}

MENU_ROWS = """
      <div class="mc-head"><span class="tagpill">Ur baren</span></div>
      <details class="mrow"><summary><b>Ghost of Prince</b><span class="sig">signature</span><span class="dots"></span><span class="price">149</span></summary><p>Gin, viol, citron, ingefäraskum &amp; salt. Vår stolthet — börja här.</p></details>
      <details class="mrow"><summary><b>Frozen Blood Orange Mimosa</b><span class="dots"></span><span class="price">119</span></summary><p>Blodapelsinsorbet, fläder &amp; cava. Brunchens bästa vän.</p></details>
      <details class="mrow"><summary><b>Spicy Margarita</b><span class="dots"></span><span class="price">139</span></summary><p>Tequila, jalapeño &amp; lime. Den bits — lagom mycket.</p></details>
      <details class="mrow"><summary><b>Coffee Granita</b><span class="dots"></span><span class="price">139</span></summary><p>Vodka, kaffelikör &amp; espressogranita — välj Original, Salted Caramel eller Kanelbulle.</p></details>
      <details class="mrow"><summary><b>Virgin Prince 0.0</b><span class="sig">no regrets</span><span class="dots"></span><span class="price">79</span></summary><p>Viol, citron, ingefäraskum &amp; salt. Hela vår No Regrets-lista är alkoholfri.</p></details>
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
<meta name="robots" content="{ROBOTS_META}">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="restaurant">
<meta property="og:site_name" content="GP's — Guilty Pleasure Café">
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
    <a class="brandmark" href="{base}index.html" aria-label="GP's — startsida">{MARK}</a>
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
        <p><a href="{CITIES['sundsvall']["booking"]}" rel="noopener">Boka bord online</a> — eller kom förbi.</p>
      </div>
      <div>
        <h3>Häng med oss</h3>
        <p class="soc"><a href="https://www.instagram.com/guiltypleasure.se/" rel="noopener">Instagram</a><a href="https://www.tiktok.com/@guiltypleasure.se" rel="noopener">TikTok</a><a href="https://www.facebook.com/gpsumea/" rel="noopener">Facebook</a></p>
        <p>Ingen telefon än — maila oss eller skicka DM på Instagram.</p>
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

# Multi-typad entitet. NightClub är MEDVETET bortvald: GP's kör klubbkvällar men
# har inget dansgolv (bekräftat av Peter 2026-07-11), och NightClub vore ett
# påstående om en verksamhet som inte finns. Tagg-researchen föreslog den — vi
# avviker med flit. Se BACKLOG 1.4.
GP_TYPES = ["Restaurant", "CafeOrCoffeeShop", "BarOrPub"]

# amenityFeature — bara det sajten faktiskt påstår.
# Hundvänligt: står i FAQ:n ("hundar är alltid välkomna").
# Veganskt: bekräftat av Peter 2026-07-11 (alltid minst ett veganskt alternativ).
# Dansgolv: INTE uppmärkt — finns inte.
AMENITIES = {
  "sv": [("Hundvänligt", True), ("Veganska alternativ", True), ("Alkoholfria cocktails", True)],
  "en": [("Dog friendly", True), ("Vegan options", True), ("Zero-proof cocktails", True)],
}
CUISINE = {
  "sv": ["Comfort food", "Amerikanskt", "Brunch", "Cocktails"],
  "en": ["Comfort food", "American", "Brunch", "Cocktails"],
}

def rest_schema(city_key, page_url, lang="sv"):
    c = CITIES[city_key]
    node = {
      "@context":"https://schema.org","@type":GP_TYPES,
      "@id":f"https://www.guiltypleasure.se/{city_key}/#restaurant",
      "name":f"GP's — Guilty Pleasure Café {c['name']}",
      "servesCuisine":CUISINE[lang],
      "priceRange":"$$",
      "address":{"@type":"PostalAddress","streetAddress":c["street"],"postalCode":c["postal"],"addressLocality":c["name"],"addressRegion":c["region"],"addressCountry":"SE"},
      "email":c["email"],"url":f"https://www.guiltypleasure.se/{city_key}/",
      "acceptsReservations": (c["booking"] if c["booking"] else False),
      "amenityFeature":[{"@type":"LocationFeatureSpecification","name":n,"value":v} for n,v in AMENITIES[lang]],
      "hasMap":c["maps"],
      "sameAs":["https://www.instagram.com/guiltypleasure.se/","https://www.facebook.com/gpsumea/","https://www.tiktok.com/@guiltypleasure.se"],
      "hasMenu":{"@type":"Menu","name":"Signaturer ur baren","hasMenuSection":[{"@type":"MenuSection","name":"Cocktails","hasMenuItem":[
          {"@type":"MenuItem","name":"Ghost of Prince","description":"Gin, viol, citron, ingefäraskum & salt","offers":{"@type":"Offer","price":"149","priceCurrency":"SEK"}},
          {"@type":"MenuItem","name":"Frozen Blood Orange Mimosa","description":"Blodapelsinsorbet, fläder & cava","offers":{"@type":"Offer","price":"119","priceCurrency":"SEK"}},
          {"@type":"MenuItem","name":"Spicy Margarita","description":"Tequila, jalapeño & lime","offers":{"@type":"Offer","price":"139","priceCurrency":"SEK"}},
          {"@type":"MenuItem","name":"Virgin Prince 0.0","description":"Alkoholfri signatur — viol, citron, ingefäraskum & salt","offers":{"@type":"Offer","price":"79","priceCurrency":"SEK"}}]}]},
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":day_range(d1,d2),"opens":o,"closes":cl} for d1,d2,o,cl in c["hours_schema"]],
    }
    # ReserveAction endast där bokning faktiskt finns. Umeå är drop-in only —
    # där säger acceptsReservations: false, och ingen ReserveAction sätts.
    if c["booking"]:
        node["potentialAction"] = {
          "@type":"ReserveAction",
          "target":{"@type":"EntryPoint","urlTemplate":c["booking"],
                    "inLanguage":"sv-SE" if lang=="sv" else "en-GB",
                    "actionPlatform":["https://schema.org/DesktopWebPlatform","https://schema.org/MobileWebPlatform"]},
          "result":{"@type":"FoodEstablishmentReservation","name":f"Boka bord på GP's {c['name']}" if lang=="sv" else f"Book a table at GP's {c['name']}"},
        }
    return '<script type="application/ld+json">'+json.dumps(node,ensure_ascii=False)+'</script>'

def breadcrumbs(trail, url):
    """BreadcrumbList. trail = [(namn, absolut URL), ...] från Hem och nedåt."""
    node={"@context":"https://schema.org","@type":"BreadcrumbList","@id":url+"#breadcrumbs",
      "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(trail)]}
    return '<script type="application/ld+json">'+json.dumps(node,ensure_ascii=False)+'</script>'

def website_schema(lang="sv"):
    """WebSite-entiteten — bara på hubbarna, en per språk."""
    home = "https://www.guiltypleasure.se/" + ("" if lang=="sv" else "en/")
    node={"@context":"https://schema.org","@type":"WebSite","@id":home+"#website",
      "url":home,"name":"GP's — Guilty Pleasure Café",
      "inLanguage":"sv-SE" if lang=="sv" else "en-GB",
      "publisher":{"@id":"https://www.guiltypleasure.se/#org"}}
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
<p class="lead">Vi öppnade på Skolgatan 62 år 2021 med en enkel idé: Umeå förtjänade ett ställe där brunchen inte tar slut bara för att klockan gör det.</p>
<p>Sedan dess har vi varit stans New York-inspirerade comfort bistro — flaggskeppet i Guilty Pleasure-familjen. Hos oss börjar dagen med frozen mimosas och comfort-klassiker, glider över i middag när eftermiddagen tröttnat, och slutar på helgerna i något som bäst beskrivs som disco. Fredagar och lördagar håller vi igång till klockan ett, och ja — det märks.</p>
<p>Du hittar oss mitt i centrala Umeå, på Skolgatan 62. Kommer du med hunden? Ta med den in. Kommer du med ett stort gäng en lördag? Kom tidigt — vi kör drop-in only, först till kvarn, och det är en princip vi är stolta över: livet är för kort för tomma bord som väntar på folk som inte dyker upp.</p>
<p>Baren är vår scen. Signaturen heter Ghost of Prince — gin, viol, citron, ingefäraskum och salt — och den som inte dricker alkohol får ingen tråkig avbytarbänk: hela vår No Regrets-lista är byggd med samma kärlek, från Virgin Prince till alkoholfri Coffee Granita i tre smaker. Kaffet? Självklart. Det är därför det står Café på skylten.</p>
<p>Umeå är en stad som vaknar sent och lägger sig sent på helgen. Vi är byggda för exakt det.</p>

<p>Vad menar vi med comfort food? Tänk maten du egentligen längtar efter — generivs äh nej. </p>
<p>Helgerna är vår paradgren.</p>
<p>Vi är en del av Guilty Pleasure-familjen, med en syster i Sundsvall och samma fyra färger i själen: eld, disco, mossa och grädde. Men Umeå är där allt började 2021, och det är här flaggan står. Kom förbi så förstår du.</p>
"""
print("__PLACEHOLDER__")
