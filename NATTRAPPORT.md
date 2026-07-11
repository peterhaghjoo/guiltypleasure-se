# NATTRAPPORT — 2026-07-11

## Läs det här först

**Jag kunde inte köra över natten.** Jag finns bara medan en tur körs — det finns
ingen bakgrundsprocess som fortsätter när sessionen tar slut. Uppdraget var
skrivet för en agent som arbetar i tolv timmar; jag arbetade i ett svep och
prioriterade stenhårt. Det som är gjort är gjort ordentligt, byggt, testat och
verifierat i produktion. Det som inte är gjort står ärligt listat längst ned.

**Det viktigaste i uppdraget — faktakaranänen — är klart och deployat.**

Deployad commit: `0926947` · Verifiera själv:
`curl -s https://guiltypleasure-se.pages.dev/build-info.json`

---

## 1. Faktakarantän — KLAR ✅

Den externa granskningen hade rätt. Sajten ljög för sina gäster. Inte
"ungefär" — den påstod saker som helt enkelt inte var sanna, och de hade
uppstått i en byggpipeline utan att någon människa beslutat dem.

### Varje borttaget påstående

| Påstående | Fanns på | Varför det ströks |
|---|---|---|
| **"AI-värdinnan svarar från augusti 2026"** | 5 ställen (footer + FAQ, sv+en) | Tjänsten finns inte. Ett framtidslöfte med exakt datum, uppfunnet av en byggpipeline. |
| **"Bordsbokning lanseras hösten 2026"** | 7 ställen (FAQ, policy, berättelse, sv+en) | Källan säger `Drop-in only (for now)`. "(for now)" är inte ett lanseringsdatum. Både beslutet och tidpunkten var uppfunna. |
| **"tio minuters promenad från Umeå Central"** | 4 ställen | Ingen har mätt. Avstånd är verifierbara — blir de fel motsäger Google oss direkt. |
| **"ett stenkast från Rådhustorget"** | 2 ställen | Ingen källa. |
| **"Vatten står framme" / "Vatten fixar jag"** | 8 ställen | Att hundar är välkomna är belagt. Att det alltid står vatten framme är ett serviceåtagande ingen gett. |
| **"No Regrets 39–89 kr"** | 6 ställen | Menykällan säger 79–99. (39 är priset på läsk.) |
| **"Green Goddess Toast och Smashed Avocado Benedict är vegetariska"** | 1 ställe | **Mitt eget påhitt.** Jag härledde det ur ingredienslistan. Exakt det fel granskningen letade efter, begånget av mig, tre timmar tidigare. |
| **Brunchens `closes: 16:00` i strukturerad data** | JSON-LD | Peter sa när brunchen *börjar*. Aldrig när den slutar. En gäst som kommer 15.30 och får höra att brunchen är slut har blivit lurad av vår markup. Hellre ingen uppgift än en påhittad. |

**Verifierat mot produktion**, inte mot min lokala kopia: alla 14 fraserna
hämtade från de faktiskt levererade sidorna → 0 träffar.

### Faktaregistret — `data/facts/`

| Fil | Innehåll |
|---|---|
| `locations.json` | NAP per ort. Varje fält har `source`, `status`, `verified_at`. |
| `claims.json` | Varje sakpåstående utanför NAP (hundpolicy, alkoholfritt, veganskt). |
| `removed.json` | **Kvittot.** Varje struket påstående, var det stod, varför, och vad du måste besluta. Raderas aldrig. |

Peters besked i chatt räknas som ägargodkänt — **men bara när det är nedskrivet
här med datum.** Muntligt är inte en källa förrän det är en källa.

### Grinden — `qa_facts.py`

Granskar **hela `public/`** (11 sidor, båda språk) och **failar bygget** vid träff.
Kopplad in i `ci_build.sh` som steg 5 av 6.

Den första versionen av grinden satt inne i `build.py` och såg bara sina egna
tre sidor. **Två läckor gömde sig i de andra åtta** — en engelsk hundvattenfras
och ett prisspann. Den fristående grinden hittade dem båda. Det är hela poängen:
en grind som bara granskar det du redan tittat på är ingen grind.

---

## 2. Grafiska manualen — granskad på riktigt ✅

Jag hade byggt designen ur Astro-mockupens `tokens.css` och färgvärdena i
CLAUDE.md — **aldrig ur den faktiska manualen**. Så jag läste den: 27 sidor,
renderade och lästa, sedan granskad av fem oberoende agenter med en skeptiker
per fynd som försökte motbevisa det. 32 verifierade fynd.

### Tre brott mot manualens egna don'ts (s.19)

**Symbolen "GP's" i headern hade en discofärgad prick på den eldfärgade
ordbilden — och pricken blinkade.** Manualen s.19, don't #1: *"Vi blandar inte
flera färger i samma enhet"* — och manualens **eget exempel på just det brottet
är GP's-symbolen i en färg med en prick i en annan.** Don't #3: *"Vi använder
inte glow-effekter, **det gör våra neonskyltar själva**."* Koden kallade den
själv "diskret neonflimmer". Två don'ts i en enda CSS-rad. Borttagen.

**OG-bilderna hade samma konstruktion** — eldprick bredvid den gräddvita
ordbilden. Det är sajtens avsändarbild i varje delning på Facebook, LinkedIn
och Slack. Borttagen.

**`--moss-2` (#424d1b) var en femte färg.** Manualen s.17: *"EXAKT dessa fyra."*
Borttagen.

### Två WCAG-brott — mina egna

| Element | Var | Kravet | Fix |
|---|---|---|---|
| `.kicker` / `.eyebrow` | Eld på Grädde, 12,5 px | 3,25:1 mot krav **4,5:1** ❌ | 19 px fet → kvalar som stor text → 3,0:1 gäller ✅ |
| `.btn` | Grädde på Eld, 14 px | 3,25:1 mot krav **4,5:1** ❌ | 19 px fet → samma ✅ (och bättre tryckyta på mobil) |

Min kontrastgrind kontrollerade abstrakta färgpar men **band dem aldrig till
faktiska textstorlekar**. Det var hålet, och det var jag som lämnade det.

### Typografi

Manualen s.13: brödtext = PP Neue Montreal **Medium**, **Tracking 40** (= 0.04em).
Låg på 0. Rättat — med Tracking 0 bevarat på display-rubrikerna, som manualen
kräver.

---

## 3. Verifiering

```
faktagrind:     11 sidor, 19 förbjudna påståenden, 0 träffar
kontrastgrind:  6 färgpar, alla över sitt WCAG-krav
JSON-LD:        22 block, 0 trasiga
Playwright:     5 sidor × mobil + desktop, alla 200, en h1/sida
horisontell scroll: ingen
build-info.json live: 0926947 (= pushad commit)
noindex live:   noindex, nofollow, max-snippet:-1, ...
```

---

## ÖPPNA FRÅGOR TILL DIG

Sajten är nu **tystare** än den var. Den påstår mindre. Varje sak nedan kan
komma tillbaka så fort du bekräftar den — men inte innan.

1. **Telefon.** Ska en telefonlinje nämnas alls? AI eller människa? När?
2. **Bordsbokning i Umeå.** Kommer den? När?
3. **Hundvatten.** Står det vatten framme? Isåfall får det stå på sajten igen.
4. **Menypriser** (BACKLOG 2.1) — blockerar `suitableForDiet` och priserna på
   brunchsidan. Tre rätter saknar helt pris i källan.
5. **Vilka rätter är veganska/vegetariska?** Verksamhetsnivå är verifierat
   ("det finns alltid minst ett"); per rätt är okänt.
6. **När slutar brunchen?** Du sa när den börjar.
7. **Serveras brunch i Sundsvall, och vilka dagar?** Du bekräftade att *menyn*
   är identisk — inte dagarna.
8. **Avstånd/vägbeskrivning.** Vill du ha det? Då mäter vi och skriver in det.

---

## HANN INTE MED — ärligt

Uppdraget var skrivet för tolv timmars arbete. Det här är vad som står kvar,
i den ordning jag hade tagit det:

| # | Uppgift | Status |
|---|---|---|
| **1** | **Berättarrösten "jag" → "vi"** | **Inte gjord.** Berättelserna och FAQ:erna är skrivna i första person singular ("Jag öppnade på Skolgatan 62..."). Du kräver "vi"/"GP's". Det är ~1 800 ord × 2 orter × 2 språk. Jag började (brunchsidan är omskriven) men vägrade göra resten hastigt — en halvgjord röstväxling läser värre än ingen. |
| 2 | `data/routes.yaml` (route-manifest) | Inte gjord |
| 3 | WaiterAid-widget + CSP-flöde | Inte gjord |
| 4 | `/en/meny/` (språkläckan) + `/om-oss/` | Inte gjord |
| 5 | 301-kartan som `_redirects` | Inte gjord — och den **kan inte** göras än: 15 av 33 mål saknas fortfarande |
| 6 | Lighthouse-baseline | Inte gjord |
| 7 | Intentionssidor (P2) | Bara `/umea/brunch/` finns |
| 8 | Illustrationerna ur manualen (s.15) | Inte gjorda. Alla sex finns i `brand-package/assets/illustrations/` — **noll används.** Manualen namnger dem uttryckligen som ett kärnelement. Största kvarvarande designgapet. |
| 9 | Allt i P3 och P4 | Inte gjort |

### Det jag är minst nöjd med

Att jag själv hittade på ett dietpåstående, tre timmar innan jag fick i uppdrag
att städa bort påhittade dietpåståenden. Grinden finns nu, och den hade fångat
mig. Men den fanns inte då, och jag skrev det ändå.

---

## Nästa session börjar här

```bash
git log --oneline -3          # 0926947 = faktakarantänen
cat data/facts/removed.json   # vad som ströks och varför
.venv/Scripts/python.exe qa_facts.py   # grinden
```

Säkerhetstagg: `safepoint-natt-2026-07-11` → `464fc3c` (läget före natten).
Rollback = `git revert`, aldrig `reset --hard`.
