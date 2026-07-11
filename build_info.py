#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""public/build-info.json — så att en deployad sida alltid kan spåras till en commit.

Utan den här filen kan man inte svara på frågan "är det som ligger live
verkligen det jag tror?". Med den räcker det med:

    curl -s https://guiltypleasure-se.pages.dev/build-info.json

Fälten:
  commit      — exakt SHA som byggdes
  built_at    — byggtid (UTC)
  prelaunch   — True = sidorna är noindex. Måste vara True fram till cutover.
  pages       — antal genererade sidor
"""
import json, pathlib, subprocess, datetime, re, sys

ROOT = pathlib.Path(__file__).parent
PUBLIC = ROOT / "public"


def git(*args, fallback="okänd"):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return fallback


def main():
    if not PUBLIC.exists():
        print("build_info: public/ saknas — kör bygget först.")
        return 1

    # PRELAUNCH läses ur build.py:s källa, inte ur en import — filen ska kunna
    # köras även om build.py har sidoeffekter.
    src = (ROOT / "build.py").read_text(encoding="utf-8")
    m = re.search(r"^PRELAUNCH\s*=\s*(True|False)", src, re.M)
    prelaunch = m.group(1) == "True" if m else None

    sidor = sorted(p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob("*.html"))

    info = {
        "commit": git("rev-parse", "HEAD"),
        "commit_short": git("rev-parse", "--short", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "built_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "prelaunch": prelaunch,
        "noindex": prelaunch,
        "pages": len(sidor),
        "page_list": sidor,
        "facts_registry": "data/facts/",
        "note": "prelaunch=true betyder att varje sida bär noindex. Sätts till false EN gång, vid DNS-cutover.",
    }

    (PUBLIC / "build-info.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"build-info.json: {info['commit_short']} · {len(sidor)} sidor · "
          f"prelaunch={prelaunch}")
    if prelaunch is None:
        print("  VARNING: kunde inte läsa PRELAUNCH ur build.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
