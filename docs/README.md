# Docs — projektdokumentation

Dessa dokument migrerades 2026-07-11 från det tidigare sajtrepot
`guilty-pleasure-cafe` (Astro-spåret, numera arkiverat föregångare).
De skrevs för Astro-bygget men gäller i allt väsentligt även den
levande Python-genererade sajten: URL-struktur, redirects, innehåll,
SEO/AEO-strategi och affärsbeslut är teknikoberoende.

## Innehåll

- `redirect-map.md` — **kritisk vid lansering.** Komplett 301-karta från
  gamla WordPress-sajtens 33 URL:er till nya strukturen. Implementeras
  som `_redirects` på Cloudflare Pages när guiltypleasure.se pekas om.
- `website-rebuild-design.md` — designspec: brand, IA, sidsektioner,
  NAP/öppettider (källa: GBP, bekräftat 2026-07-07), WaiterAid-bokning,
  SEO/AEO-krav, tillgänglighet, top-1%-lager.
- `website-rebuild-plan.md` — ursprunglig genomförandeplan (Astro-faserna
  är historiska; kvalitetsmål, verifieringar och öppna punkter gäller).
- `menu-content.md` — menyinnehåll extraherat ur PDF:er. ⚠️ Priser
  overifierade — stäm av mot original innan publicering.
- `tag-research.md` — konkurrentanalys av schema-markup på svenska
  venue-sajter + vad som implementerats och medvetet utelämnats.

## Vid avvikelse

Vid konflikt mellan dessa dokument och CLAUDE.md gäller CLAUDE.md
(arkitektur) — dessa dokument är facit för INNEHÅLL och LANSERING.
