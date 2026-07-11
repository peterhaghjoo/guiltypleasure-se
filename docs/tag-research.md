# Tagg-research: svenska restaurang/café/klubb-sajter (2026-07-07)

Tre parallella analyser: Umeå-konkurrenter (9 sajter), Sundsvall-konkurrenter
(6 sajter), nationella toppsajter + aggregatorer (15+ sajter).

## Huvudinsikt
Sveriges venue-sajter vinner på varumärke + GBP + nyckelordsexakta titlar — deras
schema är nästan bara ramverks-defaults (Yoast @graph). Den riktiga markupen
finns hos AGGREGATORERNA (Thatsup, Bokabord) som äger "bästa X"-SERP:arna.
Slutsats: lägg aggregator-klassens markup på egen domän → förbi hela fältet.

## Vad ingen konkurrent gör (och vi nu gör)
- **Multi-typad entitet** `["Restaurant","CafeOrCoffeeShop","BarOrPub","NightClub"]` — ingen i Sverige
- **amenityFeature** (hundvänligt/veganskt/dansgolv) — bara ett litet Umeå-café
- **acceptsReservations som URL + ReserveAction** — ingen (alla länkar bara ut)
- **Event-schema för klubbkvällar** — INGEN → öppen mål när vi har riktiga event
- FAQPage på egen domän — vi har det redan
- llms.txt — bara TAK i hela landet — vi har det redan

## Titel-formler som bevisat funkar
- **Golden Hits-mönstret** (multi-service): implementerat som "Guilty Pleasure Café Umeå – Café, Restaurang, Brunch & Disco"
- **Tornhuset-mönstret** (nyckelord-först + specifika detaljer): implementerat som "Brunch i Umeå – bowls, pancakes & bubbel | GP's"
- **q.bar-mönstret** (fakta i description) + **GB-mönstret** (betyg i description-text) → implementerat i ort-descriptions
- Bokabord: årtal i guide-titlar ("…10 bästa bruncher 2026") → använd i journal-artiklar

## Implementerat 2026-07-07 (i Astro-spåret — VERIFIERA mot levande sajten)
Multi-typing, amenityFeature, keywords, svensk servesCuisine, bookingUrl
(bokabord.se/restaurang/guilty-pleasure-cafe-sundsvall) som acceptsReservations +
ReserveAction, explicit acceptsReservations:false för Umeå (drop-in), og:locale
sv_SE/en_GB + og:site_name, robots max-snippet/-image/-video, nya titlar +
betygsfakta i meta-descriptions.

## Medvetet INTE gjort (och varför)
- **aggregateRating i schema** — Googles policy kräver att betygen syns på sidan.
  Betyg i description-TEXT är ok → gjort.
- **Event-schema** — inga riktiga event publicerade än. När klubbkvällar/brunch-event
  finns: MusicEvent/Event med startDate+tz, location → @id, performer (DJ), offers.
  Helt ocontested i hela Sverige — prioritera när eventdata finns.
- meta keywords / geo.position/ICBM — legacy-brus.
- noai-taggar — skulle skada AEO.

## Kvar att göra (innehåll, ej taggar)
- Nattklubb/fest-intentionssida per ort (rankar för "nattklubb sundsvall")
- Journal-guider med årtal i titeln ("Bästa brunchen i Umeå 2026")
- Event-sektion + Event-schema när klubbkvällar publiceras
