# GP's — teknisk & SEO/AEO/GEO-genomgång

> **Vad det här är:** ett komplett underlag att bolla med. Klistra in det i
> ChatGPT eller Claude och be dem hitta hål, ifrågasätta val eller föreslå nästa
> steg. Skrivet för att kunna läsas av någon utan förkunskap om projektet.
>
> **Status:** 2026-07-12. Sajten ligger på `guiltypleasure-se.pages.dev` med
> `noindex` — den är **inte lanserad**. `guiltypleasure.se` drivs fortfarande
> av WordPress.

---

## 1. Vad projektet är

Guilty Pleasure Café — restaurang och bar i **Umeå** (Skolgatan 62) och
**Sundsvall** (Storgatan 12). New York-inspirerad comfort bistro. Brunch,
dinner, disco. Hundvänligt.

Vi bygger om sajten från grunden. Den gamla WordPress-sajten har ett problem
som är värt att förstå, för det formar hela strategin:

**Den gamla sajten var fylld av tunt AI-genererat innehåll** (via en tjänst som
heter trakk.ai). Den producerade flera nästan identiska sidor per sökintention
— `/sv/lunch-umea-sv/`, `/sv/umea-sv/lunch/`, `/sv/lunchrestauranger-i-umea/`
— som konkurrerade med varandra om samma sökord. Det kallas kannibalisering,
och Google straffar det via sin *helpful content*-bedömning. **33 gamla URL:er
kollapsar till ~15 i den nya strukturen.**

Det är därför hela projektet är byggt kring en enda princip: **hellre färre,
sannare, djupare sidor än fler tunna.**

---

## 2. Teknisk arkitektur — och varför

### Egen statisk generator i Python. Inga ramverk. Noll npm-beroenden.

```
build.py           → hubb, stadssidor (Umeå/Sundsvall), 404, all CSS, schema
build_menu.py      → menysidan (101 rätter/drycker)
build_menu_en.py   → engelska menysidan
build_en.py        → engelsk hubb + hreflang
build_en_cities.py → engelska stadssidor
build_intent.py    → intentionssidor (just nu: /umea/brunch/)
og_gen_ci.py       → delningsbilder (OG) genererade ur varumärkets typsnitt
qa_facts.py        → FAKTAGRINDEN (se §5)
build_info.py      → public/build-info.json
```

Output: statisk HTML i `public/`. Deployas på **Cloudflare Pages**. Varje push
till `main` bygger och går live.

**Varför inte Astro/Next/WordPress?**

Det fanns ett Astro-spår. Det är arkiverat. Skälen till att den rena
Python-generatorn vann:

1. **All text finns i levererad HTML.** Ingen JavaScript krävs för att läsa
   innehållet. Det spelar roll för AEO: många AI-crawlers renderar inte JS.
   Googlebot gör det, men GPTBot och andra gör det ofta inte.
2. **Noll beroenden = noll supply chain, noll bygg-drift.** Sajten kommer att
   byggas likadant om två år.
3. **Fullständig kontroll över markupen.** Ingen ramverksgenererad schema.org
   som vi inte förstår.
4. **Prestanda.** Ren HTML + inlinad CSS + två self-hostade woff2-typsnitt.

**Kostnaden:** allt måste skrivas för hand. Det är ett medvetet val.

### Typsnitt

Varumärkets egna typsnitt (Guilty Pleasure Bold + PP Neue Montreal) ligger
**base64-kodade i repot** och avkodas vid bygget. Inga Google Fonts, inga
externa fontanrop — det är både en prestanda- och en integritetsfråga.

---

## 3. Sidstrukturen (IA) — location-first

```
/                      Varumärkeshubb, dirigerar till orterna
/umea/                 Umeå: egen NAP, öppettider, FAQ, Restaurant-schema
/umea/brunch/          Intentionssida: "brunch Umeå"
/sundsvall/            Sundsvall: samma struktur
/meny/                 Hela menyn (delad — menyerna är identiska idag)
/en/...                Engelsk spegel med hreflang
```

**Location-first** betyder att varje ort är en egen liten sajt under sin egen
katalog. Det är den starkaste strukturen för lokal SEO: Google kopplar en
tydlig geografisk entitet till varje katalog, och strukturen skalar till en
tredje stad utan omskrivning.

**Regeln:** EN stark kanonisk sida per (intention × ort × språk). Aldrig två
sidor om samma sak.

### Vad som finns idag (9 sidor)

| Sida | Språkspegel |
|---|---|
| `/` | `/en/` |
| `/umea/` | `/en/umea/` |
| `/sundsvall/` | `/en/sundsvall/` |
| `/meny/` | `/en/meny/` |
| `/umea/brunch/` | **saknas** ← enda hålet i hreflang-paren |

### Vad som saknas (planerat)

`/umea/lunch/`, `/umea/after-work/`, `/sundsvall/brunch/`, `/sundsvall/lunch/`,
`/sundsvall/after-work/`, `/om-oss/`, `/jobb/`, `/sundsvall/boka/` + engelska
speglar.

**Konsekvens:** av 33 gamla WordPress-URL:er har ~15 fortfarande inget mål att
301:a till. Redirect-kartan kan inte implementeras förrän sidorna finns.

---

## 4. SEO — det klassiska lagret

### Teknisk grund

- **Canonical** på varje sida, absolut URL, pekar på `www.guiltypleasure.se`
- **hreflang** bidirektionellt sv⇄en + `x-default` → sv. Verifierat: 8 av 9
  sidor har kompletta par (brunchsidan saknar sin EN-spegel)
- **Sitemap** med alla 9 URL:er
- **robots.txt** — medvetet **öppen** (`Allow: /`), se nedan
- **En enda `<h1>` per sida.** Verifierat i test.
- **Semantisk HTML**, inga div-soppor
- **`noindex` på allt** tills lansering (`PRELAUNCH = True` i `build.py`)

**Varför robots.txt är öppen trots att sajten är noindex:** en `Disallow` hindrar
Google från att *hämta* sidan — och då kan den aldrig se `noindex`-taggen. Sidan
kan då ändå hamna i indexet (via länkar), och du kan inte få bort den. Rätt
kombination är: **öppen robots.txt + noindex i metataggen.** Det är ett vanligt
misstag som är värt att kunna.

### Titel-mönster

Från en konkurrentanalys av 30+ svenska restaurangsajter:

- **Nyckelord först, sedan specifika detaljer.**
  `"Brunch i Umeå – bowls, pancakes & frozen mimosas | GP's"`
- Inte: `"GP's | Brunch"` (varumärke först slösar bort de dyraste tecknen)

### Menyn i HTML — den enskilt största SEO-fixen

Den gamla sajten hade menyn i en **AnyFlip-flipbook** (i praktiken bilder).
Google kunde inte läsa en enda rätt. Nu ligger 101 rätter och drycker som
crawlbar HTML med `Menu`/`MenuItem`/`Offer`-schema och priser.

Det betyder att sökningar som "löjromspizza Umeå" eller "espresso martini
Sundsvall" plötsligt kan hitta oss.

---

## 5. Faktaregistret — projektets viktigaste idé

Det här är det jag mest vill att du bollar med någon.

### Problemet

En extern granskning hittade **påhittade uppgifter live på sajten**:

- *"AI-värdinnan svarar från augusti 2026"* — tjänsten finns inte
- *"Bordsbokning lanseras hösten 2026"* — beslutet var aldrig fattat
- *"tio minuters promenad från Umeå Central"* — ingen har mätt
- *"Vatten står framme"* (om hundar) — inget sådant löfte fanns
- *"Green Goddess Toast är vegetarisk"* — härlett ur en ingredienslista

Ingen av dem hade en källa. **De uppstod i en AI-driven byggpipeline och gick
rakt ut till gästerna.** Det är samma sjukdom som trakk.ai — bara i finare kläder.

### Lösningen: `data/facts/`

Varje uppgift på sajten måste finnas i ett register, med källa:

```json
"umea": {
  "street":    { "value": "Skolgatan 62", "status": "verified",
                 "source": "docs/website-rebuild-design.md §5", "verified_at": "2026-07-07" },
  "telephone": { "value": null, "status": "verified",
                 "note": "DET FINNS INGET TELEFONNUMMER. Sajten får inte antyda att ett är på väg." },
  "booking":   { "value": "drop-in", "status": "verified",
                 "note": "Källan säger 'Drop-in only (for now)'. '(for now)' är INTE ett lanseringslöfte." }
}
```

Status kan vara `verified` · `draft` · `expired` · `conflicting`.
**Bara `verified` får publiceras.**

Källhierarki: ägargodkända dokument > bokningsleverantör > egen verifierad
social profil > extern verifierbar källa.

`removed.json` är **kvittot** — varje struket påstående, var det stod, varför,
och vad ägaren måste besluta. Raderas aldrig.

### Grinden: `qa_facts.py`

Kör sist i bygget, granskar **hela `public/`** och **failar bygget** om ett
förbjudet påstående dyker upp igen — oavsett vem eller vad som skrev det.

Den fångade två läckor som människan (och AI:n) hade missat.

**Lärdomen som är värd att bolla om:** den *första* versionen av grinden satt
inne i generatorn och granskade bara de tre sidor generatorn själv kände till.
Den missade läckorna i de andra sex. **En grind som bara tittar där du redan
tittat är ingen grind.** Den måste granska slutprodukten.

---

## 6. AEO — att bli citerad av AI-assistenter

AEO = *Answer Engine Optimization*. Målet: när någon frågar ChatGPT eller
Google AI "var äter jag bra brunch i Umeå?" ska GP's nämnas.

### Vad vi gör

**1. Strukturerad data som faktiskt beskriver entiteten.**
Multi-typning: `["Restaurant", "CafeOrCoffeeShop", "BarOrPub"]`.
En analys av 30+ svenska restaurangsajter visade att **ingen** gör detta — de
kör Yoast-defaults. Aggregatorerna (Thatsup, Bokabord) har den vassa markupen,
och det är därför de äger "bästa X i Y"-sökningarna. **Idén: lägg
aggregator-klassens markup på egen domän.**

> **Notera:** `NightClub` föreslogs av analysen men **valdes bort** — GP's har
> inget dansgolv. Att märka upp det vore ett falskt påstående i data som AI
> läser som sanning. Det här är principen i praktiken.

**2. `amenityFeature`** — hundvänligt, veganska alternativ, alkoholfria
cocktails. Nästan ingen konkurrent har det. Det är exakt den typ av fakta en
AI-assistent behöver för att svara "hundvänlig brunch i Umeå".

**3. `FAQPage`-schema** med riktiga frågor per ort. AI-assistenter älskar
fråga–svar-par; de är direkt citerbara.

**4. `llms.txt`** i roten — en kort, faktabaserad sammanfattning riktad till
AI-crawlers. Inga superlativ, bara verifierbara uppgifter och länkar till
nyckelsidor. Enligt analysen har **en enda** svensk restaurangsajt detta.

**5. robots.txt välkomnar AI-crawlers explicit** — GPTBot, ClaudeBot,
PerplexityBot, Google-Extended.

**6. All text i HTML.** Ingen JS-beroende text. Många AI-crawlers renderar inte
JavaScript.

**7. Sanningen som konkurrensfördel.** Det här är det icke-uppenbara: en
AI-assistent som citerar dig och har fel skadar dig. En sajt vars fakta stämmer
blir en sajt som är trygg att citera. **Faktaregistret är inte bara etik — det
är AEO-strategi.**

---

## 7. GEO — lokal och generativ sökning

- **NAP-konsistens** (Name, Address, Phone) — samma uppgifter överallt.
  Sanningskällan är Google Business Profile, bekräftad 2026-07-07.
- **`openingHoursSpecification` per ort**, alla sju dagar.

  > Här fanns en **allvarlig bugg**: koden expanderade dagsintervall till bara
  > ändpunkterna, så Umeås `Tuesday–Thursday` blev `["Tuesday","Thursday"]` —
  > **onsdagen försvann.** Google och AI-assistenter läste GP's Umeå som
  > **stängt på onsdagar**. Den låg live. Fixad.

- **`acceptsReservations`** som URL för Sundsvall (bokabord.se) + `ReserveAction`.
  Umeå: `false` (drop-in). Analysen: ingen konkurrent gör detta — alla länkar
  bara ut.
- **`BreadcrumbList`** på alla undersidor.
- **`Organization` + `WebSite`** på hubbarna, med `subOrganization` till de två
  restaurangerna. Ger AI en tydlig entitetsgraf.

### Kvar att göra på GEO

- Google Business Profile: hävda och verifiera båda enheterna, länka sajten
- NAP-citations: hitta.se, eniro, Tripadvisor, Visit Umeå, Destination Sundsvall
- Recensionsloop (QR → Google-recension per enhet)

---

## 8. Kvalitetsgrindar — bygget vägrar leverera skräp

Bygget **failar** vid:

| Grind | Kollar |
|---|---|
| **Faktagrind** | 20 förbjudna påståenden mot hela `public/`. Även: inga telefonnummer (det finns inget). |
| **Kontrastgrind** | Varje färgpar som används mot sitt WCAG-krav. |
| **Schema-grind** | Varje JSON-LD-block måste parsa. |
| **Språkgrind** | Ingen svensk UI-text på engelska sidor. (Den fångade en AI som råkade skriva "Öppet nu" i en CSS-kommentar — CSS:en bakas in i varje sida.) |
| **hreflang-grind** | Bidirektionella par. |
| **Route-manifest** | `data/routes.yaml` — facit över vilka sidor som ska finnas. |

Plus `build-info.json` på sajten, så man alltid kan verifiera vilken commit som
faktiskt ligger live:

```bash
curl -s https://guiltypleasure-se.pages.dev/build-info.json
```

---

## 9. Design & varumärke

Färgerna kommer ur den grafiska manualen (v1.0, 27 sidor):
**Grädde `#fff8eb`** (bakgrund) · **Eld `#ff450a`** (accent) ·
**Mossa `#24270e`** (text) · **Disco `#ff99ff`**.

Manualen har sex uttryckliga *don'ts* om logotypen: inga skuggor, ingen glow,
inga gradienter, **aldrig flera färger i samma enhet**.

> Sajten bröt mot två av dem samtidigt: symbolen "GP's" hade en **discofärgad
> prick** på den eldfärgade ordbilden — och pricken **blinkade**. Manualen säger
> ordagrant: *"Vi använder inte glow-effekter — det gör våra neonskyltar
> själva."* Fixat.

**Tillgänglighet:** WCAG 2.2 AA. Eld på Grädde är bara **3,25:1** — det räcker
för stor text (≥18,66px fet) men **inte** för brödtext. Kickers och knappar låg
på 12,5px respektive 14px och föll. De är höjda till 19px fet, vilket både
klarar kravet och ger bättre tryckytor på mobil. Lighthouse a11y: **100**.

---

## 10. Öppna frågor — det som blockerar

Sajten påstår idag **mindre** än den gjorde. Varje punkt kan komma tillbaka så
fort den är bekräftad:

1. **Telefon.** Finns inget nummer. Ska ett nämnas alls?
2. **Bordsbokning i Umeå.** Kommer den? När?
3. **Menypriserna är overifierade.** Blockerar `suitableForDiet` i schemat.
4. **Vilka rätter är veganska/vegetariska?** Verksamhetsnivå är bekräftat
   ("det finns alltid minst ett") — per rätt är okänt. Två menykällor säger
   emot varandra, och den ena märker **Löjromspizza som vegansk** (den innehåller
   löjrom och smetana). Därför är dietmärkning per rätt **blockerad**.
5. **När slutar brunchen?** Vi vet när den börjar.
6. **Serveras brunch i Sundsvall, vilka dagar?**
7. **Riktig fotografering.** Sajten har **noll bilder**. Manualen namnger sex
   illustrationer som kärnelement — noll används.
8. **trakk.ai ligger kvar på WordPress** och skadar Google-profilen varje dag.

---

## 11. Bra frågor att bolla med en AI

Klistra in det här dokumentet och prova:

- *"Vilka hål ser du i AEO-strategin? Vad gör konkurrenter som vi missar?"*
- *"Faktaregistret — är det överarbetat, eller är det rätt svar på
  AI-genererat innehåll? Vad skulle du göra annorlunda?"*
- *"Location-first IA med en kanonisk sida per intention × ort × språk — vilka
  risker ser du när vi skalar till en tredje stad?"*
- *"Vi har noll bilder. Hur mycket kostar det oss i SEO/AEO, och vad är
  minimum för att vara trovärdig?"*
- *"15 av 33 gamla URL:er saknar redirect-mål. Vad är den billigaste vägen till
  en säker cutover?"*
- *"Är det rimligt att vägra publicera dietmärkningar per rätt, eller är vi för
  försiktiga? Vad är risken åt andra hållet?"*
- *"Multi-typning `["Restaurant","CafeOrCoffeeShop","BarOrPub"]` — finns det en
  risk att Google tolkar det som spam?"*

---

## 12. Länkar

- Förlanseringssajt: https://guiltypleasure-se.pages.dev (noindex)
- Nuvarande live: https://guiltypleasure.se (WordPress, ska ersättas)
- Repo: `peterhaghjoo/guiltypleasure-se`
- Arbetsordning: `BACKLOG.md`
- Regler & arkitektur: `CLAUDE.md`
- Faktaregister: `data/facts/`
