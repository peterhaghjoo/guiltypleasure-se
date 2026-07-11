# Guilty Pleasure Café Website — Implementation Plan (HISTORISK)

> **Note 2026-07-11:** Detta var genomförandeplanen för Astro-spåret
> (`guilty-pleasure-cafe`, arkiverad föregångare). Levande sajten byggdes i
> stället som Python-genererad statisk HTML (se CLAUDE.md). Planens Astro-steg
> är historiska — men FASSTRUKTUREN, KVALITETSMÅLEN, VERIFIERINGARNA och de
> ÖPPNA PUNKTERNA gäller fortfarande och ska avräknas mot den levande sajten.

**Goal:** Rebuild guiltypleasure.se as a fast, accessible, SEO/AEO/GEO-optimized
site with a location-first IA and a top-1% feature set.

## Global Constraints (gäller fortfarande)

- **Brand palette (verbatim):** fire `#ff450a`, disco pink `#ff99ff`, moss `#24270e`,
  cream `#fff8eb`. Never combine two stand-out colors in one element. Body text =
  moss on cream; bright colors only for large text/UI (contrast).
- **Fonts:** display "Guilty Pleasure", body "PP Neue Montreal" — licensed, self-hosted.
- **Languages:** Swedish default (clean root), English under `/en/`, reciprocal
  hreflang + x-default.
- **Accessibility:** WCAG 2.2 AA on every page.
- **Performance targets:** LCP < 2.0s, INP < 200ms, CLS < 0.1, Lighthouse ≥ 95.
- **NAP source of truth:** Umeå — Skolgatan 62, 903 29 Umeå, umea@guiltypleasure.se;
  Sundsvall — Storgatan 12, 852 31 Sundsvall, sundsvall@guiltypleasure.se.
  Phone = pending (build telephone-ready).
- **No thin/AI-filler content** (the trakk.ai mistake). Real, specific copy only.
- **Commit frequently**, one logical change per commit.

## Milestone roadmap (avräknas mot levande sajten)

| Phase | Deliverable | Verified by |
|---|---|---|
| 1. Foundation | Design system + base layout + Umeå page live with schema | Lighthouse ≥95, Rich Results test |
| 2. Full IA | All location + intent pages (brunch/lunch/AW), sv+en, hreflang | Sitemap, hreflang validator, crawl |
| 3. Content | Menus/hours/copy complete, seasonal toggles | Menu schema, crawlable HTML |
| 4. Booking + integrations | WaiterAid widget, GA4+GSC, consent, privacy analytics | Booking flow, consent gate, GSC verify |
| 5. Migration | 301 redirects, cutover, old-site retirement | Redirect tests, GSC coverage |
| 6. Top-1% layers | Reviews, events, "open now", IG, OG, llms.txt, journal | Schema validators, CWV, a11y sweep |
| 7. Launch & monitor | Go-live, submit sitemap, AI-citation baseline | Post-launch checklist |

## Fas 4 — Booking & integrations

- WaiterAid popup on Sundsvall pages only: load widget.min.js deferred; wire
  "Boka bord" button (hash i WaiterAid-kontot); `data-lang="en"` on English pages;
  optional `data-mealid` on brunch/lunch buttons.
- `acceptsReservations` URL into Sundsvall schema.
- Consent-mode cookie banner (decline non-essential by default) gating GA4.
- Privacy-friendly analytics (Plausible/Fathom) as primary; GA4 behind consent.
- Connect Google Search Console; submit sitemap; baseline current metrics.

## Fas 5 — Migration (301 + cutover)

- Implement all 301s from `docs/redirect-map.md` (`_redirects` on Cloudflare Pages).
- Redirect tests: every old URL returns 301 → correct new URL.
- Point the domain to Cloudflare (Peter controls DNS). Keep 301s permanent.
- Retire WordPress + remove trakk.ai plugin/user.
- Verify: curl each old URL for 301 + Location; GSC coverage after cutover.

## Fas 6 — Top-1% layers

- Accessibility sweep (WCAG 2.2 AA); accessibility statement page.
- Reviews: surface real reviews; per-location QR → Google review link; GBP cadence.
- Local citations: NAP checklist (hitta.se, eniro, TheFork, Tripadvisor,
  Visit Umeå, Destination Sundsvall, Apple/Bing).
- Content journal (/journal/) with 2–3 real seed articles; llms.txt; FAQ expansion.
- Events + Event schema (disco/AW nights).
- "Öppet nu" component from hours + time.
- Instagram feed + per-page branded OG images.
- AI-citation monitoring: scheduled routine querying AI assistants for local
  intents, logging whether GP's is cited.

## Fas 7 — Launch & monitor

- Pre-launch checklist: 404, security headers/CSP, forms, mobile pass.
- Go live; submit sitemap; request indexing of key pages.
- Monitoring: uptime, CWV (CrUX/PSI), rank tracking, AI-citation log.
- Post-launch review at 2 + 6 weeks.

## Open items (slot in when ready)

- Phone numbers per location (add to schema when available).
- Final menu prices + which menu per location + lunch menu after summer.
- Real photography (hero, menu, interior).
- Google Business Profile access for both locations.
- Newsletter provider choice.
- Confirm English enabled on WaiterAid account.
- Verify Umeå geo coordinates for Skolgatan 62.
