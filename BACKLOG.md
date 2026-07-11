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

- [ ] **1.1 Gap-analys: levande sajten vs docs.** Inventera vilka sidor
      byggskripten faktiskt genererar och jämför mot IA:n i
      website-rebuild-design.md §3. Lista saknade sidor och saknad markup.
      Verifiera särskilt tagg-researchens punkter (multi-typning,
      amenityFeature, llms.txt, FAQPage, ReserveAction) mot genererad HTML.
      Leverans: rapport + uppdaterad detaljlista under 1.2–1.4.
- [ ] **1.2 Intentionssidor per stad:** /umea/brunch/, /umea/lunch/,
      /umea/after-work/ + Sundsvall-motsvarigheter (+ /en/-speglar med
      hreflang). En stark kanonisk sida per intent — riktigt innehåll i
      GP's röst, inte tunt fyllnadsmaterial. Lunch = säsongsmarkerad
      (stängd sommar).
- [ ] **1.3 Kompletterande sidor:** /om-oss/, /jobb/, /sundsvall/boka/
      (WaiterAid-widget endast på Sundsvall-sidor, deferred; kod i
      WaiterAid-kontot).
- [ ] **1.4 Schema-komplettering** enligt gap-analysen: per-location
      Restaurant med openingHoursSpecification från NAP-källan
      (docs/website-rebuild-design.md §5), Menu/MenuItem med
      suitableForDiet + allergener, FAQPage, BreadcrumbList,
      Organization + WebSite.

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
      aktiv skadar den Google-profilen. PETER gör detta i wp-admin
      (Claude Code kan guida).
- [ ] **3.2 301-redirects:** implementera hela docs/redirect-map.md som
      _redirects-fil för Cloudflare Pages. Testa att varje gammal URL
      ger 301 → rätt mål (curl-loop).
- [ ] **3.3 Search Console:** verifiera nya sajten, baseline nuvarande
      toppsidor/queries FÖRE cutover.
- [ ] **3.4 Pre-launch-checklista:** 404, security headers/CSP, mobil-
      genomgång, Lighthouse ≥ 95, WCAG-stickprov, noindex BORT från
      produktionsbygget vid cutover (och bara då).
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

- [ ] git pull lokalt (nya commits 2026-07-11: docs + CLAUDE.md + BACKLOG)
- [ ] Stäng öppen PR + 7 branches i guilty-pleasure-cafe, arkivera sedan
      repot (Settings → Archive)
- [ ] Besluta: guiltypleasure-se publikt eller privat (rekommendation: privat)
- [ ] Skapa seo-granskare-subagenten (om skills/agent-genomlysningen
      bekräftar att den saknas)
- [ ] Windows aktiva timmar (efter serverrapporten)
- [ ] OneDrive-kvot kollad; Drive-flytten av GP-arkiv + brand-delta klar

## Idéer / senare (medvetet parkerade)

- Nattklubb/fest-intentionssida per ort (tagg-researchen: "nattklubb
  sundsvall" är svagt försvarad SERP)
- CMS för personalredigerade menyer/öppettider (öppet arkitekturbeslut)
- Bokning för Umeå; AI-telefonsvar
- Nyhetsbrevsleverantör
- Tredje stad (/uppsala/?) — IA:n skalar redan
