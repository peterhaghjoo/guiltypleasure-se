# Faktaregistret — sanningskällan för allt som påstås på sajten

> **Regeln:** ingen uppgift får publiceras på sajten om den inte finns här med
> `status: verified`. Ingen text, ingen JSON-LD, ingen metadata, ingen llms.txt.
> Saknas källa → uppgiften finns inte. Punkt.

Bakgrunden: en extern granskning hittade **påhittade uppgifter live** — en
"AI-värdinna" som skulle svara i telefon från augusti 2026, en bordsbokning i
Umeå som skulle lanseras hösten 2026, promenadavstånd till Umeå Central, och
dietpåståenden om enskilda rätter. Inget av det hade en källa. Framtidslöften
är dessutom **ägarbeslut, inte agentbeslut** — de får aldrig uppstå i en
byggpipeline.

## Källhierarki (högst först)

1. `docs/` — ägargodkänt material (t.ex. `website-rebuild-design.md` §5 = NAP)
2. Bokningsleverantör (WaiterAid / bokabord)
3. Verifierad egen social profil
4. Extern verifierbar källa

Peters direkta besked i chatt räknas som **ägargodkänt**, men måste skrivas in
här med datum för att gälla. Muntligt är inte en källa förrän det är nedskrivet.

## Status

| Status | Betydelse | Får publiceras? |
|---|---|---|
| `verified` | Källa finns och är kontrollerad | **Ja** |
| `draft` | Sannolikt sant men obekräftat | Nej — sidan blockeras |
| `expired` | Hade en källa, giltighetstiden gick ut | Nej |
| `conflicting` | Källor säger emot varandra | Nej — utelämnas och loggas |

## Filer

- `locations.json` — adresser, öppettider, e-post, bokningsläge per ort
- `menu.json` — menyns status (priser är **overifierade**, se BACKLOG 2.1)
- `socials.json` — sociala profiler
- `booking.json` — bokningskanaler
- `claims.json` — övriga sakpåståenden (hundpolicy, alkoholfritt, diet)
- `removed.json` — **allt som sanerats bort**, med skäl. Raderas aldrig.

## Vad som INTE finns här (och därför inte får sägas)

- Telefonnummer. Det finns inget. Sajten får inte antyda att ett är på väg.
- Bordsbokning i Umeå. Umeå är drop-in. Inget löfte om framtida bokning.
- Avstånd/promenadtider till hållplatser eller torg.
- Vilka enskilda rätter som är vegetariska eller veganska.
