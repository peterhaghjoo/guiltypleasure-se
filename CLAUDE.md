# CLAUDE.md — guiltypleasure.se

Läs den här filen vid varje sessionsstart. Den är facit för hur projektet fungerar och vilka regler som gäller. Vid konflikt mellan denna fil och en enskild prompt: fråga innan du avviker.

## Vad projektet är

Statisk restaurangsajt för GP's Guilty Pleasure Café (Umeå & Sundsvall), byggd för SEO/AEO. Ägare: Guilty Pleasure Group AB. Svenska är primärspråk, engelska sekundärt under /en/.

Live: https://guiltypleasure-se.pages.dev (domänen guiltypleasure.se pekas om vid lansering).

**Detta är det ENDA levande sajtrepot.** Repot `guilty-pleasure-cafe` (Astro-spåret) är en arkiverad föregångare — bygg aldrig vidare där. Dess dokumentation är migrerad hit till `docs/`: redirect-karta (kritisk vid lansering), designspec, plan, menyinnehåll och tagg-research. Läs `docs/README.md` för översikt.

## Arkitektur — RÖR INTE utan uttryckligt beslut

Egen statisk sajtgenerator i Python. Inga ramverk. Inga npm-beroenden. Ingen JavaScript-beroende text.

- `build.py` — svenska sidor (hubb, Umeå, Sundsvall, 404), CSS, schema.org, kvalitetsgrindar
- `build_menu.py` — menysidan med hela menyn och priser
- `build_en.py` — engelsk hubb + hreflang
- `build_en_cities.py` — engelska stadssidor
- `og_gen_ci.py` — delningsbilder (OG) + appleikon ur webbfonten
- `fonts/*.b64` — subsettade webbfonter som base64, dekodas i bygget
- Output: `public/` — committas ALDRIG, byggs alltid från källa

Föreslå inte migrering till Astro/Next/annat ramverk. Arkitekturvalet är medvetet: enkelhet och noll beroenden.

## Deploy

Cloudflare Pages. Varje push till `main` kör `bash ci_build.sh` → bygger → live.
Det betyder: **allt som pushas till main går live.** Vid osäkerhet eller större ändringar: jobba i en feature-branch och skapa PR i stället.

## Brand — exakta värden, aldrig avvikelser

Färger:
- Grädde `#fff8eb` (bakgrund)
- Eld `#ff450a` (accent/CTA)
- Mossa `#24270e` (text/mörk)
- Disco `#ff99ff` (lekfull accent)

Regel: kombinera aldrig två starka färger (Eld/Disco) i samma element. Brödtext = Mossa på Grädde; starka färger endast för stor text/UI (kontrast).

Typsnitt: GuiltyPleasure-Bold (rubriker), PPNeueMontreal-Bold/Medium (övrigt). Self-hostade som woff2 med `font-display: swap`. Inga Google Fonts, inga externa fontanrop.

## Språkregler

- Svensk sida = svensk title, meta, innehåll. Aldrig blandspråk.
- Engelska endast under /en/ med korrekta hreflang-taggar (sv, en, x-default → sv).
- Korrekt svensk stavning och grammatik i allt innehåll. Tonalitet: varm, lekfull, självsäker — GP's röst.

## Kvalitetskrav (kravspec)

- All text ska finnas i levererad HTML — verifiera med curl, aldrig lita på webbläsarrendering
- LCP < 2,0 s mobil, CLS < 0,1
- Bilder: AVIF/WebP med fallback, srcset, lazy loading under fold
- Valid schema.org-markup (Restaurant/LocalBusiness per enhet)
- Sitemap uppdateras vid nya/ändrade sidor
- Inget tunt AI-fyllnadsinnehåll — verkligt, specifikt innehåll (trakk.ai-misstaget upprepas aldrig)

## Faktakällor (NAP)

Sanningskälla för adresser och öppettider: `docs/website-rebuild-design.md` §5 (bekräftat mot Google Business Profile 2026-07-07). Hitta aldrig på öppettider eller kontaktuppgifter — vid osäkerhet, fråga Peter.

## Säkerhet

- Repot är publikt: ALDRIG API-nycklar, lösenord, tokens eller interna uppgifter i kod eller kommentarer
- Hemligheter ligger i `.env` (gitignored) eller Cloudflare Pages miljövariabler
- Kör secrets-koll före push om något känsligt hanterats i sessionen

## Arbetsflöde med ägaren

Peter är inte utvecklare. Han granskar diffar och godkänner — Claude Code skriver koden. Det innebär:
- Förklara ändringar kort på svenska innan de görs
- Visa diff före commit vid innehålls- eller designändringar
- Sammanfatta efter push: vad ändrades, var syns det, hur verifierar man
- Fråga hellre en gång för mycket vid destruktiva ändringar (radera filer, ändra CI, byta struktur)

## Verifiering efter bygge

1. Kör byggskripten lokalt utan fel
2. Kontrollera att `public/` innehåller förväntade sidor
3. Stickprov med curl att texten finns i HTML:en
4. Efter push: bekräfta att Cloudflare Pages-deployen gick igenom
