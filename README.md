# guiltypleasure.se

GP's Guilty Pleasure Café — Umeå & Sundsvall. Statisk sajt, byggd av `build*.py` vid varje push.

## Cloudflare Pages-inställningar (engångs)

- Build command: `bash ci_build.sh`
- Build output directory: `public`
- Framework preset: None

Vid varje push till `main` byggs och deployas hela sajten automatiskt.

## Struktur

- `build.py` — svenska sidor (hubb, umeå, sundsvall, 404), CSS, schema, kvalitetsgrindar
- `build_en.py` — engelsk hubb + hreflang
- `build_menu.py` — menysidan (hela menyn med priser)
- `build_en_cities.py` — engelska stadssidor
- `og_gen_ci.py` — delningsbilder + appleikon ur webbfonten
- `fonts/*.b64` — subsettade webbfonter (base64-text; dekodas i bygget)

Ändra i källan → pusha → live. Fullständig dokumentation i koncernens docs-arkiv.
