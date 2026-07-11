#!/bin/bash
# Cloudflare Pages-bygge för guiltypleasure.se
# Build command:  bash ci_build.sh
# Build output:   public
set -e

echo "== 1/4 Dekodar fonter (b64 -> woff2) =="
for f in fonts/*.b64; do base64 -d "$f" > "${f%.b64}"; done
ls -la fonts/

echo "== 2/4 Installerar byggberoenden =="
pip install --quiet fonttools brotli pillow

echo "== 3/4 Bygger alla sidor =="
python3 build.py
python3 build_en.py
python3 build_menu.py
python3 build_en_cities.py
python3 build_intent.py
python3 og_gen_ci.py

echo "== 4/6 Paketerar public/ =="
rm -rf public
mkdir -p public/fonts
cp index.html 404.html sitemap.xml robots.txt llms.txt favicon.svg apple-touch-icon.png og.png og-umea.png og-sundsvall.png og-meny.png public/
cp -r umea sundsvall en meny public/
cp fonts/pp-medium.woff2 fonts/pp-bold.woff2 public/fonts/

echo "== 5/6 FAKTAGRIND =="
# Failar bygget om ett påhittat påstående smugit sig tillbaka in.
# Se qa_facts.py och data/facts/removed.json. Deployar hellre ingenting
# än en sajt som ljuger för gästerna.
python3 qa_facts.py

echo "== 6/6 build-info.json =="
# Så att deployad version alltid kan spåras till en commit:
#   curl -s https://guiltypleasure-se.pages.dev/build-info.json
python3 build_info.py

echo "KLART:"
find public -type f | sort
