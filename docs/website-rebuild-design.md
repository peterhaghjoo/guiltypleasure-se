# Guilty Pleasure Café — Website Rebuild Design Spec

**Date:** 2026-07-07
**Owner:** Peter (peter@guiltypleasure.se)
**Status:** Draft for approval
**Note 2026-07-11:** Skrevs för Astro-spåret. Tekniska val i §9 är historiska —
levande sajten är Python-genererad statisk HTML (se CLAUDE.md). Allt övrigt
(brand, IA, NAP, bokning, SEO/AEO-krav, tillgänglighet) gäller.

---

## 1. Goal

Rebuild guiltypleasure.se from the current WordPress site into a fast, modern
site that (a) carries the finished GP's brand design and (b) dramatically
improves SEO, AEO (being cited by AI assistants), and GEO (local/generative
search). Success = all of: more bookings, ranking for local queries
("brunch Umeå", "lunch Sundsvall"), being recommended by ChatGPT/Google AI, and
a brand-worthy look.

## 2. Brand & design system

Taken directly from the approved Claude Design mockup.

**Palette — four colors, never mix two stand-out colors in one element:**
| Token | Hex | Role |
|---|---|---|
| `--gp-eld` (fire) | `#ff450a` | Primary accent, buttons |
| `--gp-disco` (pink) | `#ff99ff` | Disco accent |
| `--gp-mossa` (moss) | `#24270e` | Text — used instead of black |
| `--gp-gradde` (cream) | `#fff8eb` | Background — used instead of white |

Default surface: moss text on cream.

**Type:** Display = "Guilty Pleasure" (licensed, owned); Body = "PP Neue Montreal"
(licensed). Self-host for performance; preload the display face.

**Voice:** Playful Swedish-first. "Your local happy place", "Comfort food deluxe",
"Två platser. Samma vibb.", "Bring your dog." Brand line (from Facebook):
"NEW YORK COMFORT BISTRO. Livet är för kort för tomma bord."

## 3. Information architecture

**Location-first hierarchy** — each location is a self-contained mini-site under
its own folder. Strongest structure for local SEO/GEO/AEO; scales to a 3rd city.

```
/                    → Brand hub, routes to locations
/umea/               → Umeå landing — own NAP, hours, map, FAQ, Restaurant schema
/umea/meny/          → Umeå menu (à la carte / kväll)
/umea/brunch/        → high-intent "brunch Umeå"
/umea/lunch/         → high-intent "lunch Umeå" (seasonal — closed summer)
/umea/after-work/    → high-intent "after work Umeå"
/sundsvall/          → Sundsvall landing
/sundsvall/meny/
/sundsvall/brunch/
/sundsvall/lunch/
/sundsvall/after-work/
/sundsvall/boka/     → Sundsvall booking (WaiterAid)
/om-oss/             → Brand story / about
/jobb/               → Jobs
/en/...              → English mirror (hreflang sv⇄en + x-default)
```

- One folder per location = clear local relevance.
- ONE strong canonical page per intent+location+language — no thin duplicates.
- Breadcrumbs (Hem › Umeå › Meny) + `BreadcrumbList` schema.
- Menus currently identical across locations — share content, surface per
  location; split only when they diverge. Seasonal toggles (lunch closed summer).

## 4. Page sections (from the mockup)

- **Header** — wordmark; nav Meny · Hitta hit · Om oss · Disco; "Boka bord"; mobile burger.
- **Hero** — eyebrow "Brunch · Dinner · Disco"; H1 "Your local happy place."; CTAs.
- **Marquee** — scrolling brand phrases.
- **Menu** — tabs Brunch / Dinner / Disco, items with descriptions + prices.
- **Locations** — "Två platser. Samma vibb." cards with address + hours + directions.
- **Dogs** — "Bring your dog." Dog-friendly, always. (FAQ + AEO material.)
- **Booking** — WaiterAid popup (§7).
- **Footer** — newsletter, social, contact, "Hundvänligt — alltid."

## 5. Locations (source of truth for NAP + schema)

| | Umeå | Sundsvall |
|---|---|---|
| Address | Skolgatan 62, 903 29 Umeå | Storgatan 12, 852 31 Sundsvall |
| Since | 2021 | (newer) |
| Booking | **Drop-in only** (for now) | **Bookable (WaiterAid) + drop-in** |
| Email | umea@guiltypleasure.se | sundsvall@guiltypleasure.se |
| Phone | **TBD — open item** | **TBD — open item** |

Address + hours confirmed by Peter 2026-07-07 (from Google Business Profile).
Per-day hours for `openingHoursSpecification`:
- **Umeå:** Mon 11:30–22:00, Tue–Thu 11:30–00:00, Fri–Sat 11:30–01:00, Sun 11:30–22:00.
- **Sundsvall:** Mon–Tue 11:00–22:00, Wed–Thu 11:00–00:00, Fri–Sat 11:00–01:00, Sun 11:00–22:00.

These differ from the OLD live site's stated hours — the rebuild corrects them.
Keep in sync with GBP going forward.

## 6. Menu

Real menus reconstructed into `docs/menu-content.md` (prices unverified).
Moving menus from the AnyFlip flipbook into real HTML is the single biggest SEO fix:

- Crawlable HTML, not images/PDF/flipbook.
- `Menu`/`MenuItem` schema incl. `offers.price`, `suitableForDiet` (V = vegan
  option; "glutenfritt? fråga oss"), allergen notes ("innehåller nötter").
- Per-location menus may differ — model per location, share where identical.
- Seasonal toggles (lunch closed over summer).
- Price variants (89/149/449) and add-ons ("stack +39", "Lobster +50").

## 7. Booking

- **Sundsvall — WaiterAid popup widget** (confirmed by WaiterAid):
  - Script: `https://app.bokabord.se/widget-popup/widget.min.js` — load only on
    Sundsvall pages, deferred.
  - Button: `class="waiteraid-widget" data-hash="<restaurant code>"` — wire the
    design's "Boka bord" button. Restaurant code finns i WaiterAid-kontot.
  - English pages: `data-lang="en"` (confirm English enabled on the account).
  - Optional `data-mealid` to pre-select sitting (brunch page → brunch sitting).
  - Schema `acceptsReservations`: point at the booking URL.
- **Umeå:** drop-in → "Hör av dig / droppa in" CTA; structure booking-ready.

## 8. SEO / AEO / GEO requirements

- **Schema:** per-location `Restaurant` (address, geo, `openingHoursSpecification`,
  `telephone` when available, `servesCuisine`, `priceRange` `$$`,
  `acceptsReservations`, `menu`, `sameAs`); `Menu`; `FAQPage`; `Organization` + `WebSite`.
- **NAP consistency** across site, GBP, Facebook, directories. Category "Kafé", `$$`.
- **hreflang** reciprocal sv⇄en + `x-default`.
- **Metadata:** unique titles (brand + location + intent), single `<h1>` per page.
- **Content quality:** real, specific copy — NOT AI-filler.
- **Crawlable menu**; alt text on photos.
- **Performance:** strong Core Web Vitals.
- **Measurement:** GA4 + Search Console; baseline before launch.
- **GBP:** claim/verify both locations; hours, photos, menu + booking links.
- **URL migration:** all 33 old URLs 301 per `docs/redirect-map.md`. Keep 301s
  permanently; submit new sitemap at launch; watch Coverage for drops.

## 9. Tech stack (HISTORISK — se CLAUDE.md)

Ursprungligen Astro + git-baserad CMS. Levande sajten är Python-genererad
statisk HTML på Cloudflare Pages. CMS-frågan (personalredigerbara menyer/tider)
är ett öppet framtidsbeslut.

## 10. Integrations

- **WaiterAid** — Sundsvall booking.
- **Newsletter** — provider TBD.
- **Social (unified `@guiltypleasure.se`):** Instagram
  instagram.com/guiltypleasure.se, TikTok tiktok.com/@guiltypleasure.se,
  Facebook facebook.com/gpsumea. No Spotify.
- **Maps** per location.

## 11. Open items (do not block build)

- ☐ Phone numbers per location (build telephone-ready). Possible AI phone — decide separately.
- ☑ WaiterAid booking — RESOLVED: popup widget. Remaining: confirm English on
  account; optionally sitting meal-IDs; booking URL for schema.
- ☐ Menu prices/items verification + which menu per location + lunch menu after summer.
- ☐ Real photography (hero, menu, interior).
- ☐ Google Business Profile access for both locations.
- ☐ Newsletter provider.

**Decommission trakk.ai (important):** old site's thin/duplicate pages were
produced by trakk.ai and likely triggered a helpful-content demotion. Actions:
deactivate + delete Trakk WP plugin, remove trakk user, revoke API access.
Final cleanup via 301 map at cutover. Disable NOW to start recovery.

## 12. Out of scope / later

- Custom booking modal via WaiterAid API; booking for Umeå.
- AI phone service.
- Online ordering / takeaway.

## 13. Success metrics

Bookings from site, rankings for target local queries, AI-assistant citations,
Core Web Vitals, review volume/rating, organic traffic to per-location pages.

---

# Optimization layers (top-1%)

## 14. Accessibility & legal

- **WCAG 2.2 AA:** semantic HTML, keyboard nav, focus states, alt text, labels,
  `prefers-reduced-motion`. Verify contrast — fire/pink on cream only for large
  text/UI; moss-on-cream for body.
- **EU Accessibility Act / tillgänglighetsdirektivet:** build to AA + publish
  accessibility statement.
- **GDPR:** consent banner (decline non-essential by default) gating GA4;
  privacy-friendly analytics (Plausible/Fathom) as primary; privacy policy.

## 15. Reviews & local presence

- Surface real reviews; `aggregateRating` only from genuine on-page ratings.
- Review loop: QR at table/receipt → per-location Google review link.
- NAP consistency: hitta.se, eniro, TheFork/Tripadvisor, Visit Umeå,
  Destination Sundsvall, Google Business, Apple Maps, Bing Places.
- GBP cadence: weekly posts, fresh photos, menu links, reply to every review.

## 16. Content strategy (AEO)

- **Journal/guide section** — "Bästa brunchen i Umeå", "Hundvänliga ställen";
  quality over quantity, GP's voice. Antidote to trakk's thin pages.
- **`llms.txt`** at root.
- **FAQ per location** → `FAQPage` schema.
- **AI-citation monitoring:** periodically ask AI assistants local questions,
  log whether GP's is cited — the real GEO KPI. Automatable.

## 17. Engagement & polish

- **Event schema** for disco/after-work/live nights + events section.
- **"Öppet nu"** — compute open/closed + current mode from hours + time.
- **Instagram feed** — lightweight/self-hosted embed.
- **Per-page branded OG images.**
- **Edge hosting, HTTP/3, Brotli, AVIF/WebP, security headers (CSP).**
- **CWV targets:** LCP < 2.0s, INP < 200ms, CLS < 0.1; Lighthouse ≥ 95.
