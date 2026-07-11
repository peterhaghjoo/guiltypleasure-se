# Redirect map (301) — current WordPress URLs → new URLs

> Built from live sitemap (guiltypleasure.se/page-sitemap.xml, 33 URLs, fetched
> 2026-07-07). Purpose: preserve rankings + backlinks through the rebuild. Every
> old URL must 301 → its best new equivalent. New structure: Swedish at clean
> root (no `/sv/`), English under `/en/`. Verify against Google Search Console
> "top pages" so the highest-traffic URLs are mapped most carefully.

## Key finding: heavy duplication to collapse
The current site targets each intent with multiple thin URLs that cannibalize
each other. The rebuild collapses each cluster to ONE canonical page:

| Intent | Current URLs (to collapse) | New canonical |
|---|---|---|
| Umeå landing | /sv/umea-sv/, /sv/umea-restaurang/, /sv/restaurang-umea-sv/, /en/restaurant-umea/ | /umea/ (+ /en/umea/) |
| Umeå brunch | /sv/brunch-umea-sv/, /en/brunch-umea/ | /umea/brunch/ |
| Umeå lunch | /sv/lunch-umea-sv/, /sv/umea-sv/lunch/, /sv/lunchrestauranger-i-umea/, /en/lunch-umea/ | /umea/lunch/ |
| Umeå after work | /sv/aw-umea/, /sv/after-work-umea-fredag/ | /umea/after-work/ |
| Umeå bar/disco | /sv/bar-umea/ | /umea/ (disco section) |
| Sundsvall landing | /sv/sundsvall-sv/, /sv/restaurang-sundsvall-sv/, /sv/krog-sundsvall/, /en/restaurant-sundsvall/ | /sundsvall/ (+ /en/sundsvall/) |
| Sundsvall brunch | /sv/brunch-sundsvall-sv/, /en/brunch-sundsvall/ | /sundsvall/brunch/ |
| Sundsvall lunch | /sv/lunch-sundsvall-sv/, /sv/sundsvall-sv/lunch/, /en/lunch-sundsvall/ | /sundsvall/lunch/ |
| Sundsvall after work | /sv/after-work-sundsvall/, /sv/aw-sundsvall/ | /sundsvall/after-work/ |
| Sundsvall bar/disco | /sv/bar-sundsvall-sv/, /en/bar-sundsvall/ | /sundsvall/ (disco section) |
| Concept / about | /sv/koncept/ | /om-oss/ |
| Takeaway | /en/take-away-umea/, /en/take-away-sundsvall/ | 301 → location page (takeaway not offered) |

## Full 301 map

| Old URL | → New URL (301) |
|---|---|
| /sv/ | / |
| /en/ | /en/ |
| /sv/koncept/ | /om-oss/ |
| /sv/umea-sv/ | /umea/ |
| /sv/umea-restaurang/ | /umea/ |
| /sv/restaurang-umea-sv/ | /umea/ |
| /en/restaurant-umea/ | /en/umea/ |
| /en/umea/ | /en/umea/ *(keep)* |
| /sv/brunch-umea-sv/ | /umea/brunch/ |
| /en/brunch-umea/ | /en/umea/brunch/ |
| /sv/lunch-umea-sv/ | /umea/lunch/ |
| /sv/umea-sv/lunch/ | /umea/lunch/ |
| /sv/lunchrestauranger-i-umea/ | /umea/lunch/ |
| /en/lunch-umea/ | /en/umea/lunch/ |
| /sv/aw-umea/ | /umea/after-work/ |
| /sv/after-work-umea-fredag/ | /umea/after-work/ |
| /sv/bar-umea/ | /umea/ |
| /en/take-away-umea/ | /en/umea/ |
| /sv/sundsvall-sv/ | /sundsvall/ |
| /sv/restaurang-sundsvall-sv/ | /sundsvall/ |
| /sv/krog-sundsvall/ | /sundsvall/ |
| /en/restaurant-sundsvall/ | /en/sundsvall/ |
| /en/sundsvall/ | /en/sundsvall/ *(keep)* |
| /sv/brunch-sundsvall-sv/ | /sundsvall/brunch/ |
| /en/brunch-sundsvall/ | /en/sundsvall/brunch/ |
| /sv/lunch-sundsvall-sv/ | /sundsvall/lunch/ |
| /sv/sundsvall-sv/lunch/ | /sundsvall/lunch/ |
| /en/lunch-sundsvall/ | /en/sundsvall/lunch/ |
| /sv/after-work-sundsvall/ | /sundsvall/after-work/ |
| /sv/aw-sundsvall/ | /sundsvall/after-work/ |
| /sv/bar-sundsvall-sv/ | /sundsvall/ |
| /en/bar-sundsvall/ | /en/sundsvall/ |
| /en/take-away-sundsvall/ | /en/sundsvall/ |

## Notes / decisions needed
- **Takeaway:** confirmed NOT offered — old takeaway URLs 301 to the location
  page (as above). Takeaway stays out of scope.
- **After-work & lunch pages** are worth keeping as dedicated per-location pages
  (real search intent) — added to the IA alongside brunch.
- **Bar/disco** folds into the location page's disco section rather than its
  own thin page.
- Post-launch: submit new sitemap in Search Console, keep 301s permanently,
  monitor Coverage + top queries for drops.
