# noetic-proposals

Single repo for every Noetic client proposal, capabilities deck, and pitch slide deck.
Served via GitHub Pages — every deliverable is a shareable URL the moment it's pushed.

## How it works

```
noetic-proposals/
├── _assets/                    Shared brand kit (versioned, used by all decks)
│   ├── noetic/                 Logos, favicon, brand marks
│   ├── team/                   Team photos + manifest.json (run download-assets.py)
│   ├── clients-portfolio/      Logos of clients we've worked with
│   ├── partner-badges/         Meta, Google, HubSpot, Klaviyo, etc.
│   └── download-assets.py      Mirrors all assets from noetic.io. Run once after clone.
├── _templates/
│   ├── proposal-base.html      Long-scroll capabilities deck (the canonical one)
│   ├── slides-reveal.html      Slide deck — Reveal.js (presenter mode)
│   └── slides-snap.html        Slide deck — custom 16:9 scroll-snap
├── _skill/
│   └── SKILL.md                The skill that drives generation (versioned with the repo)
├── _data/
│   └── deliverables.json       Index manifest — append here when you ship a new deck
├── <client-slug>/              One folder per deliverable
│   ├── index.html              The deck itself
│   └── assets/                 Per-deliverable assets (client logo, custom hero image)
└── index.html                  Landing page that lists every deliverable
```

## First-time setup

The repo ships with `init.ps1` — a one-shot PowerShell script that handles the full bootstrap. From the repo root in PowerShell:

```powershell
.\init.ps1
```

This script will:

1. Clean up any sandbox/agent leftovers (broken `.git`, stub `.claude` folders).
2. Run `python _assets/download-assets.py` to mirror brand assets from noetic.io.
3. Install the `noetic-proposal-generator` skill into your Cowork plugins folder.
4. `git init -b main`, stage, and make the first commit.
5. Print next steps for `gh repo create` / pushing / enabling GitHub Pages.

### Manual equivalent (if you don't want to run the script)

```bash
# 1. Pull the brand assets (idempotent — safe to re-run)
python _assets/download-assets.py

# 2. Copy the skill to your Cowork plugins folder
#    (Windows path; adjust if you've moved your Claude data dir)
copy _skill\SKILL.md "%APPDATA%\Claude\local-agent-mode-sessions\skills-plugin\<...>\skills\noetic-proposal-generator\SKILL.md"

# 3. Init git
git init -b main
git add . && git commit -m "Initial commit"

# 4. Push and enable GitHub Pages (Settings → Pages → main / root)
git remote add origin git@github.com:<your-org>/noetic-proposals.git
git push -u origin main

# 5. Verify locally
python -m http.server 8000   # then open http://localhost:8000/
```

Once Pages is on, every deliverable is live at:

```
https://<your-org>.github.io/noetic-proposals/<client-slug>/
```

## Generating a new deliverable

Open Cowork and ask:

> Make a Noetic proposal for Caesarstone — slides format, scroll-snap.

The `noetic-proposal-generator` skill (lives in `_skill/SKILL.md`, also installed in your Cowork) will:

1. Pick a slug like `caesarstone-7k2x`
2. Copy the right template (`proposal-base.html`, `slides-reveal.html`, or `slides-snap.html`) into `<slug>/index.html`
3. Replace `{{CLIENT_NAME}}`, `{{HERO_LEDE}}`, `{{DATE}}`, etc.
4. Append the entry to `_data/deliverables.json` so it shows up on the landing page
5. Tell you the local preview path and the GitHub Pages URL

You commit, push, share the link.

## Editing the brand kit

When Noetic updates the website (new team member, refreshed client logo, new partner):

```bash
python _assets/download-assets.py          # incremental: only fetches missing
python _assets/download-assets.py --force  # re-download everything
```

The script regenerates `_assets/team/manifest.json` automatically. Templates pull from that manifest.

## The skill, two places

The skill lives in **two** places intentionally:

- **`_skill/SKILL.md`** — versioned with the repo. Anyone who clones gets it. Source of truth.
- **`~/AppData/Roaming/Claude/.../skills/noetic-proposal-generator/SKILL.md`** — installed in your Cowork so you can invoke it without opening this repo.

They should stay in sync. After meaningful changes to the skill, copy the file from `_skill/` into the plugin folder (or vice versa).

## Naming conventions

- Slug: `<client-kebab-case>-<random-4>`. The 4-char suffix lets you iterate without overwriting (`caesarstone-7k2x`, `caesarstone-9p1w`).
- Per-deliverable assets: lowercase, hyphenated, in the slug's `assets/` folder.
- Brand assets: never modify `_assets/` files manually; rerun the download script.

## Style guardrails

The full design system is in `_skill/SKILL.md`. The non-negotiables:

- Tokens only — never inline hex/rgb in components.
- One `display-xl` per page.
- Italic emphasis on exactly one word per headline (Noetic signature).
- Eyebrow + display heading on every section.
- WCAG 2.2 AA. Visible focus rings. Reduced-motion respected.

## License

Internal — Noetic Creative. Do not share assets, team photos, or client logos outside engagement contexts.
