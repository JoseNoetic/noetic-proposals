#!/usr/bin/env python3
"""
download-assets.py — Mirrors all visual assets from noetic.io into _assets/.

Run once after cloning the repo (or whenever Noetic adds new team members /
clients / refreshes a logo). Idempotent: skips files that already exist with
non-zero size unless --force is passed.

Usage:
    python download-assets.py            # download missing only
    python download-assets.py --force    # re-download everything
    python download-assets.py --dry-run  # print what would be downloaded

Requires Python 3.8+ and `requests` (pip install requests). Falls back to
urllib.request if requests isn't installed.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import requests  # type: ignore

    def fetch(url: str) -> bytes:
        r = requests.get(url, timeout=30, headers={"User-Agent": "noetic-proposals/1.0"})
        r.raise_for_status()
        return r.content
except ImportError:
    from urllib.request import Request, urlopen

    def fetch(url: str) -> bytes:
        req = Request(url, headers={"User-Agent": "noetic-proposals/1.0"})
        with urlopen(req, timeout=30) as resp:
            return resp.read()


ROOT = Path(__file__).resolve().parent  # _assets/

# ---------------------------------------------------------------------------
# Asset inventory — SOURCE OF TRUTH
# ---------------------------------------------------------------------------

NOETIC_LOGOS = {
    "noetic/logo-purple.svg":   "https://noetic.io/wp-content/uploads/2022/11/logo-rounded.svg",
    "noetic/logo-white.svg":    "https://noetic.io/wp-content/uploads/2023/01/noetic-logo-white.svg",
    "noetic/mark-only.svg":     "https://noetic.io/wp-content/uploads/2022/11/Frame.svg",
    "noetic/arrow.svg":         "https://noetic.io/wp-content/uploads/2022/11/arrow-1.svg",
    "noetic/linkedin.svg":      "https://noetic.io/wp-content/uploads/2022/12/linkedin.svg",
    "noetic/favicon.ico":       "https://noetic.io/favicon.ico",
}

# Team — name -> photo URL. Filename derived from a normalized slug.
TEAM = [
    ("Tamir Alush",       "Strategy + Creative Direction",  "https://noetic.io/wp-content/uploads/2025/06/Tamir.webp"),
    ("Nicole Luna",       "Account Director",               "https://noetic.io/wp-content/uploads/2025/06/Nicole.webp"),
    ("Jackie Frysz",      "Head of Operations",             "https://noetic.io/wp-content/uploads/2025/06/Jackie.webp"),
    ("Jonathan Levanon",  "Growth Mentor",                  "https://noetic.io/wp-content/uploads/2026/01/Jonathan.webp"),
    ("Paula Carriel",     "Senior Account Strategist",      "https://noetic.io/wp-content/uploads/2025/06/Paula.webp"),
    ("Vanessa Soria",     "Account Manager",                "https://noetic.io/wp-content/uploads/2025/11/Vane.webp"),
    ("Andrea Martinez",   "Account Manager",                "https://noetic.io/wp-content/uploads/2025/11/Andre.webp"),
    ("Gonzalo Mazzoni",   "Media Buyer",                    "https://noetic.io/wp-content/uploads/2025/10/Gonzalo.webp"),
    ("Luna Murgia",       "Media Buyer",                    "https://noetic.io/wp-content/uploads/2025/11/Luna.webp"),
    ("Tim Newlin",        "Paid Search",                    "https://noetic.io/wp-content/uploads/2025/06/Tim.webp"),
    ("Cory Wray",         "Media Buyer",                    "https://noetic.io/wp-content/uploads/2025/06/Cory.webp"),
    ("Will Kennon",       "Paid Social",                    "https://noetic.io/wp-content/uploads/2025/11/Will.webp"),
    ("Samuel Henke",      "Media Buyer",                    "https://noetic.io/wp-content/uploads/2025/06/Samuel.webp"),
    ("Gabriel Sheridan",  "Media Buyer",                    "https://noetic.io/wp-content/uploads/2025/10/Gabriel.webp"),
    ("Carolina Fallu",    "Strategic Planner",              "https://noetic.io/wp-content/uploads/2025/11/Carolina.webp"),
    ("Maria Arevalo",     "Executive Assistant",            "https://noetic.io/wp-content/uploads/2025/11/Maria-Arevalo.webp"),
    ("Alex Heilbronn",    "Copywriter",                     "https://noetic.io/wp-content/uploads/2025/11/Alex.webp"),
    ("Virginia Mayer",    "Copywriter",                     "https://noetic.io/wp-content/uploads/2025/11/Virginia.webp"),
    ("Andres Gallo",      "Creative Team Lead",             "https://noetic.io/wp-content/uploads/2025/11/Andres.webp"),
    ("Daniel Rojas",      "Video Editor",                   "https://noetic.io/wp-content/uploads/2025/06/Daniel.webp"),
    ("Maggie Bernal",     "Graphic Designer",               "https://noetic.io/wp-content/uploads/2025/11/Maggie.webp"),
    ("Angelica Negron",   "Graphic Designer",               "https://noetic.io/wp-content/uploads/2025/06/Angie.webp"),
    ("Serge Alarcon",     "Email Marketing Specialist",     "https://noetic.io/wp-content/uploads/2025/10/Sergio.webp"),
    ("Daniela Benfele",   "Automations + Email Marketing",  "https://noetic.io/wp-content/uploads/2025/06/Daniela.webp"),
    ("Val Parra",         "Social Media Management",        "https://noetic.io/wp-content/uploads/2025/06/Val.webp"),
    ("Ava Boario",        "Community Manager",              "https://noetic.io/wp-content/uploads/2025/11/Ava.webp"),
    ("Danielle Greenberg","AI Ops Consultant",              "https://noetic.io/wp-content/uploads/2025/11/Danielle.webp"),
    ("Joe Conroy",        "Organic Search",                 "https://noetic.io/wp-content/uploads/2025/06/Joe.webp"),
    ("Monique Johnson",   "Webinar Expert",                 "https://noetic.io/wp-content/uploads/2025/06/Monique.webp"),
    ("Esteban Grijalva",  "Front-End Development",          "https://noetic.io/wp-content/uploads/2025/06/Esteban.webp"),
    ("Natali Alush",      "Human Resources",                "https://noetic.io/wp-content/uploads/2025/11/Natali.webp"),
]

CLIENT_LOGOS = {
    "clients-portfolio/nice.svg":         "https://noetic.io/wp-content/uploads/2024/11/nice.svg",
    "clients-portfolio/lumenis.svg":      "https://noetic.io/wp-content/uploads/2024/11/lumenis.svg",
    "clients-portfolio/wsc-sports.svg":   "https://noetic.io/wp-content/uploads/2024/11/wscsports.svg",
    "clients-portfolio/sapiens.svg":      "https://noetic.io/wp-content/uploads/2024/11/sapiens.svg",
    "clients-portfolio/audiocodes.svg":   "https://noetic.io/wp-content/uploads/2024/11/audiocodes-grey.svg",
    "clients-portfolio/iac.svg":          "https://noetic.io/wp-content/uploads/2024/11/iac.svg",
    "clients-portfolio/roundforest.svg":  "https://noetic.io/wp-content/uploads/2023/01/roundforest.svg",
    "clients-portfolio/babyark.svg":      "https://noetic.io/wp-content/uploads/2024/11/babyark.svg",
    "clients-portfolio/priority.svg":     "https://noetic.io/wp-content/uploads/2024/11/priority.svg",
    "clients-portfolio/dollar-days.png":  "https://noetic.io/wp-content/uploads/2024/11/dollar-days.png",
    "clients-portfolio/tabit.svg":        "https://noetic.io/wp-content/uploads/2024/11/tabit.svg",
    "clients-portfolio/interlight.svg":   "https://noetic.io/wp-content/uploads/2024/11/interlight.svg",
    "clients-portfolio/datumate.svg":     "https://noetic.io/wp-content/uploads/2023/01/datumate.svg",
    "clients-portfolio/animalia.svg":     "https://noetic.io/wp-content/uploads/2024/11/animalia.svg",
    "clients-portfolio/sorbet.svg":       "https://noetic.io/wp-content/uploads/2024/11/sorbetgrey.svg",
    "clients-portfolio/hazera.svg":       "https://noetic.io/wp-content/uploads/2024/11/hazera.svg",
    "clients-portfolio/tipa.svg":         "https://noetic.io/wp-content/uploads/2024/11/tipa.svg",
    "clients-portfolio/the-one-club.svg": "https://noetic.io/wp-content/uploads/2024/11/ONE-CLUB.svg",
    "clients-portfolio/selina.svg":       "https://noetic.io/wp-content/uploads/2024/11/selina.svg",
    "clients-portfolio/impacx.svg":       "https://noetic.io/wp-content/uploads/2024/11/impacx.svg",
    "clients-portfolio/wsc-sports-color.svg": "https://noetic.io/wp-content/uploads/2024/08/Group-1118.svg",
    "clients-portfolio/sapiens-white.svg":    "https://noetic.io/wp-content/uploads/2024/09/Sapiens-logo-white.svg",
    "clients-portfolio/lumenis-color.svg":    "https://noetic.io/wp-content/uploads/2024/09/Lumenis_RGB_Logo_Black.svg",
    "clients-portfolio/nice-color.svg":       "https://noetic.io/wp-content/uploads/2024/08/nice-logo.svg",
}

PARTNER_BADGES = {
    "partner-badges/bigcommerce.svg":     "https://noetic.io/wp-content/uploads/2022/12/Badges_big-commerce.svg",
    "partner-badges/facebook.svg":        "https://noetic.io/wp-content/uploads/2022/12/Badges_facebook.svg",
    "partner-badges/shopify.svg":         "https://noetic.io/wp-content/uploads/2022/12/Badges_shopify.svg",
    "partner-badges/google.svg":          "https://noetic.io/wp-content/uploads/2022/12/Badges_google_google.svg",
    "partner-badges/linkedin-badge.svg":  "https://noetic.io/wp-content/uploads/2022/12/Badges_linked-in.svg",
    "partner-badges/klaviyo.svg":         "https://noetic.io/wp-content/uploads/2022/12/Badges_klaviyo.svg",
    "partner-badges/hubspot.svg":         "https://noetic.io/wp-content/uploads/2022/12/Badges_hubspot_hubspot.svg",
    "partner-badges/demandbase.svg":      "https://noetic.io/wp-content/uploads/2023/05/Badges_demandbase.svg",
    "partner-badges/impact.svg":          "https://noetic.io/wp-content/uploads/2023/10/badges_impact.svg",
}


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace(".", "")


def build_team_map() -> dict[str, str]:
    out = {}
    for name, _role, url in TEAM:
        ext = "webp" if url.endswith(".webp") else url.rsplit(".", 1)[-1]
        out[f"team/{slugify(name)}.{ext}"] = url
    return out


def build_team_manifest() -> str:
    """Generate _assets/team/manifest.json content listing each member."""
    import json
    members = []
    for name, role, url in TEAM:
        ext = "webp" if url.endswith(".webp") else url.rsplit(".", 1)[-1]
        members.append({
            "name": name,
            "role": role,
            "photo": f"team/{slugify(name)}.{ext}",
        })
    return json.dumps({"team": members}, indent=2)


def download(rel_path: str, url: str, force: bool, dry: bool) -> str:
    dest = ROOT / rel_path
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return f"skip   {rel_path}"
    if dry:
        return f"would  {rel_path}  <- {url}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = fetch(url)
    except Exception as e:  # noqa: BLE001
        return f"FAIL   {rel_path} :: {e}"
    dest.write_bytes(data)
    return f"ok     {rel_path}  ({len(data):,} bytes)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--force", action="store_true", help="re-download even if file exists")
    ap.add_argument("--dry-run", action="store_true", help="print plan, don't download")
    args = ap.parse_args()

    plan: dict[str, str] = {}
    plan.update(NOETIC_LOGOS)
    plan.update(build_team_map())
    plan.update(CLIENT_LOGOS)
    plan.update(PARTNER_BADGES)

    print(f"noetic-proposals asset sync — {len(plan)} files\n")

    fail = 0
    for rel, url in plan.items():
        line = download(rel, url, args.force, args.dry_run)
        print(line)
        if line.startswith("FAIL"):
            fail += 1

    # write team manifest (always, deterministic)
    if not args.dry_run:
        manifest_path = ROOT / "team" / "manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(build_team_manifest(), encoding="utf-8")
        print(f"\nwrote  team/manifest.json  ({len(TEAM)} members)")

    if fail:
        print(f"\n{fail} download(s) failed", file=sys.stderr)
        return 1
    print("\ndone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
