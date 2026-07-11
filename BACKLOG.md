# BACKLOG — guiltypleasure.se

> Prioriterad bygglista. Arbeta uppifrån och ner om inget annat sägs.
> Regler: jobba i feature-branch → PR → preview → Peters OK → merge till main.
> Vid varje avklarad punkt: bocka av här och committa. Vid nya idéer: lägg
> dem under "Idéer/senare" — inte mitt i prioritetsordningen.
>
> Skapad 2026-07-11. Källor: docs/website-rebuild-plan.md,
> docs/website-rebuild-design.md, docs/redirect-map.md, docs/tag-research.md.

---

## FAS 1 — Gap-analys & komplettering (NU)

- [x] **1.1 Gap-analys: levande sajten vs docs.** KLAR 2026-07-11.
      Sajten genererar 7 sidor + 404: `/`, `/umea/`, `/sundsvall/`, `/meny/`,
      `/en/`, `/en/umea/`, `/en/sundsvall/`. Mål-IA:n (§3) har 15 sidor.
      **16 av 33 gamla URL:er i redirect-kartan skulle idag landa på 404.**
      Detaljer inarbetade i 1.1b och 1.2–1.4 nedan.

- [x] **1.1b ÖPPETTIDSBUGG I SCHEMA — FIXAD i PR #1 (2026-07-11, aa520ee).**
      `build.py` expanderade dagsintervall till bara ändpunkterna, så onsdagen
      försvann ur Umeås `openingHoursSpecification` — Google läste Umeå som
      stängt på onsdagar. `day_range()` fyller nu hela spannet. Verifierat:
      båda orter 7/7 dagar mot NAP-källan i §5. Samma PR: PRELAUNCH-noindex
      på alla sidor + UTF-8-encoding i byggskripten.

- [ ] **1.2 Intentionssidor per stad** — SAKNAS HELT (10 sidor).
      SV: `/umea/brunch/`, `/umea/lunch/`, `/umea/after-work/` +
      `/sundsvall/brunch/`, `/sundsvall/lunch/`, `/sundsvall/after-work/`.
      EN-speglar: `/en/umea/brunch/`, `/en/umea/lunch/`,
      `/en/sundsvall/brunch/`, `/en/sundsvall/lunch/` (hreflang-par).
      Dessa är mål för **13 av de 16 trasiga redirectsen** — högst SEO-värde.
      En stark kanonisk sida per intent, riktigt innehåll i GP's röst.
      Lunch = säsongsmarkerad (stängd sommar).
      Titelmönster enligt tagg-researchen (Tornhuset: nyckelord först).
      ARBETSSÄTT: Peter + Claude (chatten) skriver /umea/brunch/ som mall
      först; övriga nio produceras efter mallen, en PR per batch.

- [ ] **1.3 Kompletterande sidor** — SAKNAS HELT (4 sidor).
      `/om-oss/` (mål för 301 från /sv/koncept/ — trasig redirect),
      `/jobb/`, `/sundsvall/boka/` (WaiterAid-widget, endast Sundsvall,
      deferred; kod i WaiterAid-kontot), samt **`/en/meny/`** —
      idag länkar engelska hubben till den SVENSKA menysidan, vilket
      bryter språkregeln i CLAUDE.md. `/meny/` saknar dessutom hreflang helt.

- [ ] **1.4 Schema & taggar** — verifierat mot genererad HTML 2026-07-11.
      FINNS: FAQPage, openingHoursSpecification (fixad, se 1.1b), servesCuisine,
      priceRange `$$`, hasMenu + Menu/MenuItem med priser, Organization,
      sameAs, acceptsReservations, og:locale, korrekt hreflang på 6 av 7 sidor.
      SAKNAS:
      - Multi-typning `["Restaurant","CafeOrCoffeeShop","BarOrPub","NightClub"]`
        (tagg-researchens främsta konkurrensfördel — ingen i Sverige har den)
      - `amenityFeature` (hundvänligt / veganskt / dansgolv)
      - `ReserveAction` + riktig boknings-URL. Idag pekar Sundsvalls
        `acceptsReservations` på generiska `https://app.bokabord.se` i stället
        för `bokabord.se/restaurang/guilty-pleasure-cafe-sundsvall`
      - `BreadcrumbList` (IA:n kräver brödsmulor)
      - `WebSite`-entitet, `og:site_name`
      - `robots`-direktiv (max-snippet / max-image-preview / max-video-preview)
        — kombineras med PRELAUNCH-noindexen tills cutover
      - `suitableForDiet` + allergener på MenuItem
      - `llms.txt` — finns inte i `public/` (tagg-researchen påstår att den
        finns; det gällde Astro-spåret)
      - `servesCuisine` är på engelska ("Comfort food") på svenska sidor

## FAS 2 — Innehållsskuld (kräver Peter)

- [ ] **2.1 Menypriser verifieras** mot originalmenyer — docs/menu-content.md
      är märkt overifierad. PETER: stäm av priserna.
- [ ] **2.2 Telefonnummer** per enhet — PETER: leverera när de finns;
      sajten är byggd telephone-ready.
- [ ] **2.3 Riktig fotografering** (hero, mat, interiör) — PETER: beställ/
      leverera. Platshållare tills dess.
- [ ] **2.4 WaiterAid:** bekräfta att engelska är aktiverat på kontot;
      hämta ev. meal-IDs för sittningar — PETER.

## FAS 3 — Lanseringskedjan

- [ ] **3.1 Avveckla trakk.ai på gamla WordPress-sajten (BRÅDSKANDE —
      görs oberoende av övriga fasen):** avaktivera + radera plugin,
      ta bort trakk-användare, återkalla API-åtkomst. Varje dag den är
      aktiv skadar den Google-profilen. Trakk-sidorna ligger LIVE just nu
      (t.ex. /en/disco-umea/, /en/restaurant-umea/ — tunt AI-fyllnadsinnehåll
      med upprepade stycken). PETER gör detta i wp-admin (Claude Code guidar).
- [ ] **3.2 301-redirects:** implementera hela docs/redirect-map.md som
      _redirects-fil för Cloudflare Pages. Testa att varje gammal URL
      ger 301 → rätt mål (curl-loop).
- [ ] **3.3 Search Console:** verifiera nya sajten, baseline nuvarande
      toppsidor/queries FÖRE cutover.
- [ ] **3.4 Pre-launch-checklista:** 404, security headers/CSP, mobil-
      genomgång, Lighthouse ≥ 95, WCAG-stickprov, sätt `PRELAUNCH = False`
      i build.py vid cutover (och bara då).
- [ ] **3.5 DNS-cutover:** peka guiltypleasure.se till Cloudflare Pages.
      Direkt efter: skicka in ny sitemap, begär omindexering av
      nyckelsidor, bevaka Coverage. Behåll 301:orna permanent.
- [ ] **3.6 Pensionera WordPress** när cutover är verifierad och GSC ser
      stabil ut (2 veckor).

## FAS 4 — Efter lansering (top-1%)

- [ ] **4.1 Journal:** /journal/ med 2–3 riktiga artiklar ("Bästa brunchen
      i Umeå 2026" — årtal i titeln enligt tagg-researchen).
- [ ] **4.2 Event-schema + eventsektion** när klubbkvällar/event publiceras —
      helt ocontested i Sverige enligt researchen; prioritera när eventdata finns.
- [ ] **4.3 Recensionsloop:** QR per enhet → Google-recensionslänk;
      GBP-rutin (veckoposter, foton, svara på allt).
- [ ] **4.4 NAP-citations:** hitta.se, eniro, Tripadvisor/TheFork,
      Visit Umeå, Destination Sundsvall, Apple Maps, Bing Places.
- [ ] **4.5 "Öppet nu"-logik** på stadssidorna (beräknas ur öppettider).
- [ ] **4.6 AI-citation-bevakning:** återkommande koll om GP's citeras av
      AI-assistenter för lokala frågor — logga baseline + utveckling.
- [ ] **4.7 Uppföljning 2 + 6 veckor:** GSC coverage, rankningar, bokningar.

## Verkstad — småpunkter (tas löpande)

- [x] git pull lokalt (nya commits 2026-07-11: docs + CLAUDE.md + BACKLOG)
- [x] `write_text()`/`read_text()` utan encoding — FIXAT i PR #1 (aa520ee).
      Bygget är nu plattformsoberoende, ingen PYTHONUTF8 behövs.
- [ ] Verifiera live efter PR #1-deployen: curl mot pages.dev — noindex på
      alla sidor, Umeås openingHoursSpecification 7/7 dagar
- [ ] Cloudflare Pages: slå på Preview deployments för brancher (PETER i
      dashboarden — PR #1 hade noll statuscheckar, ingen preview skapas idag)
- [ ] Stäng öppen PR + 7 branches i guilty-pleasure-cafe, arkivera sedan
      repot (Settings → Archive)
- [ ] Besluta: guiltypleasure-se publikt eller privat (rekommendation: privat)
- [ ] Skapa seo-granskare-subagenten (om skills/agent-genomlysningen
      bekräftar att den saknas)
- [ ] Windows aktiva timmar (efter serverrapporten)
- [ ] OneDrive-kvot kollad; Drive-flytten av GP-arkiv + brand-delta klar
- [ ] GDPR: begränsa åtkomsten till HR-mappen i delade enheten (PETER,
      Drive → Dela → begränsa)

## Idéer / senare (medvetet parkerade)

- Nattklubb/fest-intentionssida per ort (tagg-researchen: "nattklubb
  sundsvall" är svagt försvarad SERP)
- CMS för personalredigerade menyer/öppettider (öppet arkitekturbeslut)
- Bokning för Umeå; AI-telefonsvar
- Nyhetsbrevsleverantör
- Tredje stad (/uppsala/?) — IA:n skalar redan
