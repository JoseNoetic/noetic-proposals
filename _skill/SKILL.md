---
name: noetic-proposal-generator
description: Generates branded HTML deliverables for Noetic Creative — long-scroll capabilities/proposals AND slide decks (Reveal.js or scroll-snap). Use whenever the user asks for a Noetic proposal, capabilities deck, pitch, slides, or client-facing presentation, or mentions "noetic" in the context of generating a document. Outputs land inside the noetic-proposals/ repo as a folder per deliverable, served via GitHub Pages so links open online instead of being downloaded. Pulls logos, team photos, and client portfolio from _assets/.
---

# Noetic Proposal Generator

Generates implementation-ready HTML deliverables that share a single visual language: the Noetic capabilities deck. Two output families are supported — **long-scroll proposals** and **slide decks** — both anchored to the same design tokens, typography, and component library.

The repo is structured to be served via GitHub Pages, so every deliverable produced here is shareable as a URL the moment it's pushed.

## When to use this skill

Trigger on any of:

- "Make a proposal for &lt;client&gt;"
- "Build a Noetic capabilities deck for &lt;industry&gt;"
- "Create slides for the &lt;client&gt; pitch"
- "I need a one-pager for &lt;prospect&gt;"
- "Generate a sales deck"
- Any mention of **noetic-proposals**, the working repo, or files under `_templates/`

Don't trigger when the user wants a non-Noetic-branded artifact, or a Word/PPTX file (use `docx`/`pptx` skills instead).

## Repo layout (source of truth)

```
noetic-proposals/
├── _assets/                       Shared, version-controlled
│   ├── noetic/                    Brand logos (logo-purple, logo-white, mark-only, favicon)
│   ├── team/                      One photo per team member + manifest.json
│   ├── clients-portfolio/         Logos of clients Noetic has worked with
│   ├── partner-badges/            Platform partner badges (Meta, Google, HubSpot, Klaviyo…)
│   └── download-assets.py         Mirrors all assets from noetic.io. Run once after clone.
├── _templates/
│   ├── proposal-base.html         Long-scroll capabilities/proposal template
│   ├── slides-reveal.html         Slide deck — Reveal.js (presenter mode, transitions)
│   ├── slides-snap.html           Slide deck — custom 16:9 scroll-snap, zero deps
│   └── partials/                  Reusable section snippets to copy-paste
├── _skill/SKILL.md                This file (versioned with the repo)
├── <client-slug>/                 One folder per deliverable
│   ├── index.html                 The deliverable itself
│   └── assets/                    Per-deliverable, isolated (variable, e.g. client logo)
└── index.html                     Landing page listing all deliverables
```

**Asset path rules:** templates reference `../_assets/...` (relative). Per-deliverable assets (the client's own logo, a custom hero image) live in `<client-slug>/assets/` and are referenced as `assets/...`.

## Design tokens — non-negotiable

Apply these exactly. They are the visual signature of the deck.

### Colors

| Token | Value | Usage |
|---|---|---|
| `--paper` | `#FAFAF7` | Main background |
| `--paper-warm` | `#F2F0EA` | Warm section variant |
| `--paper-cool` | `#F0F0F4` | Cool section variant |
| `--ink` | `#0A0A0E` | Primary text & display headings |
| `--ink-soft` | `#1A1A1F` | Body text |
| `--ink-mute` | `#6B6B7B` | Captions, labels, eyebrows |
| `--ink-faint` | `#A8A8B5` | Lightest text |
| `--card` | `#FFFFFF` | Card backgrounds |
| `--purple` | `#6C5CE7` | Primary accent (CTAs, dots, focus) |
| `--purple-deep` | `#4D3FC9` | Hover state for primary |
| `--purple-soft` | `#EFEDFE` | Tinted backgrounds |
| `--purple-glow` | `rgba(108, 92, 231, 0.18)` | Glow shadows |
| `--mint` | `#00D4B4` | Secondary accent |
| `--coral` | `#FF6B6B` | Tertiary accent (rare) |
| `--amber` | `#F5B400` | Quaternary accent (rare) |
| `--rule` | `rgba(10, 10, 14, 0.08)` | Hairline dividers |
| `--rule-strong` | `rgba(10, 10, 14, 0.16)` | Stronger dividers |

### Typography

```
--font-display: 'Fraunces', 'Times New Roman', serif;   /* all displays + h1-h4 */
--font-sans:    'Manrope', -apple-system, sans-serif;   /* body + UI */
--font-mono:    'JetBrains Mono', monospace;            /* eyebrows + small labels */
```

Always preconnect Google Fonts and load:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400;1,9..144,600&family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Type scale (use the helper classes — never raw `font-size`):

| Class | Size | Use |
|---|---|---|
| `.display-xl` | clamp(56–132px) | Hero headlines (one per page) |
| `.display-lg` | clamp(44–88px) | Section headlines |
| `.display-md` | clamp(34–60px) | Sub-section / feature headlines |
| `.display-sm` | clamp(26–40px) | Component titles, deep-dive H3s |
| `.lede-lg` | clamp(22–30px) | Strong intro paragraph (max 32ch) |
| `.lede` | clamp(18–22px) | Standard lede (max 60ch) |
| `.eyebrow` | 11px mono | Uppercase section label with purple dot prefix |
| body | 17px | Standard text |

Italic via `<em>` or `.italic` is reserved for emphasis inside displays — Noetic signature: italicize one word per headline (e.g. *"solving?"*).

### Spacing & layout

- Container: `max-width: 1240px`, padding `0 32px`. Narrow variant: `920px`.
- Section vertical padding: `clamp(80px, 12vh, 160px)`. Tight variant: `clamp(60px, 9vh, 110px)`.
- Section heads: 48–80px bottom margin.
- Cards: `border-radius: 16px` default, `8px` for tight UI.

### Motion

- `--motion-fast: 200ms`, `--motion-normal: 400ms`, `--motion-slow: 800ms` (fade-ins).
- Always wrap motion in `@media (prefers-reduced-motion: reduce)` fallback.
- Scroll-triggered fade: opacity 0 → 1, translateY(20px) → 0, 0.8s ease.

## Component library

Each section type below is a copy-paste pattern from `_templates/proposal-base.html`. Don't reinvent.

| Component | Class | Anatomy |
|---|---|---|
| **Nav** | `.nav` | Fixed, backdrop-blur, brand mark + links + CTA. Adds `.scrolled` on scroll. |
| **Hero** | `.hero` | `display-xl` headline, lede, meta strip (location · founded · headcount), 4-stat grid. Optional grid background + blob gradients. |
| **Marquee** | `.marquee` | Dark band, looping horizontal scroll of service labels separated by `✦`. |
| **Philosophy** | `.philosophy` | 2-col: eyebrow + display-md left, 3 numbered belief items right. |
| **Verticals** | `.verticals-grid` | 3-col card grid. Each `.vertical-card` = icon + h4 + description + example clients. |
| **Lanes** | `.lanes` | 2-col dark section. Each `.lane` = tag + h3 + description + 3 specs. |
| **Services overview** | `.services-grid` | 4-col grid of `.service-tile`s = `/NN` number + h4 + 1-line desc + hover arrow. |
| **Service deep-dive** | `.service-deep` | 2-col, sticky left number + title, right case-card(s). Repeats per service. |
| **Case study (featured)** | `.case-card.featured` | Dark, large. Meta tag + h3 + description + channel chips + narrative + result grid. |
| **Process** | `.process` | Vertical 5-step list. Each `.process-step` = `process-num` + h4 + paragraph. |
| **AI band** | `.ai-band` | Dark section, eyebrow + display-lg + lede + 4-stat grid. |
| **Differentiators** | `.diff-grid` | 3-col grid of 9 `.diff-card`s = `/NN` + h4 + short description. |
| **Team** | `.team-grid` | 5-col grid. Each `.team-card` = avatar + name (h5) + role tag (mono). Pull from `_assets/team/manifest.json`. |
| **Client roster** | `.clients-grid` | 6-col text grid (no logos — names only). |
| **Tech stack** | `.tech-grid` | 8-col grid. Each `.tech-cell` = mono category + tool name. |
| **CTA / Footer** | `.cta` | Dark. Big italic-emphasized headline + primary + ghost buttons + 3-col footer meta. |

### State requirements (every interactive element)

Every `.btn`, `.card`, link, and tile must define: **default, hover, focus-visible, active, disabled**. Loading and error states for forms.

Focus ring: `outline: 2px solid var(--purple); outline-offset: 3px;` — never `outline: none` without a visible replacement.

## Accessibility — testable rules

- WCAG 2.2 AA. Body text ≥ 4.5:1 contrast on its background.
- Headings in correct order (h1 → h2 → h3, no skipping).
- All `<img>` have `alt`. Decorative images use `alt=""`.
- Interactive controls reachable via Tab in DOM order.
- Reduced motion: any auto-animation respects `prefers-reduced-motion`.
- Marquee includes `aria-hidden="true"` and a static fallback for screen readers.
- Slides: keyboard navigation (arrow keys + Esc) is mandatory in both Reveal and snap variants.

## GitHub auto-push

Every deliverable is pushed to the repo automatically using the GitHub Contents API. No manual `git` commands needed.

**Credentials:**
- Repo: `JoseNoetic/noetic-proposals`
- Token: read from environment variable `NOETIC_GITHUB_TOKEN`

Set it once in your shell before running Claude:
```bash
export NOETIC_GITHUB_TOKEN="your_token_here"
```
Or pass it at generation time — Claude will read it with `os.environ["NOETIC_GITHUB_TOKEN"]`.

**Push function (Python — run after generating each file):**

```python
import base64, json
import urllib.request, urllib.error

def github_push(repo, token, path, content_str, commit_msg):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
    }
    content_b64 = base64.b64encode(content_str.encode()).decode()
    sha = None
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            sha = json.loads(r.read())["sha"]
    except urllib.error.HTTPError:
        pass
    body = {"message": commit_msg, "content": content_b64}
    if sha:
        body["sha"] = sha
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers=headers, method="PUT",
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
    return result["content"]["html_url"]
```

**Usage after generating `<slug>/index.html`:**

```python
REPO  = "JoseNoetic/noetic-proposals"
TOKEN = os.environ["NOETIC_GITHUB_TOKEN"]  # set: export NOETIC_GITHUB_TOKEN=ghp_...

with open(f"{slug}/index.html") as f:
    html = f.read()
github_push(REPO, TOKEN, f"{slug}/index.html", html, f"add: {slug} ({client_name})")

with open("_data/deliverables.json") as f:
    manifest = f.read()
github_push(REPO, TOKEN, "_data/deliverables.json", manifest, f"manifest: add {slug}")

pages_url = f"https://josenoetic.github.io/noetic-proposals/{slug}/"
print(f"✓ Live at: {pages_url}")
```

GitHub Pages deploys within ~60 seconds. Always share the `pages_url` with the user at the end.

## Output workflow

When the user asks to generate a deliverable:

1. **Confirm intent.** Use AskUserQuestion if any of: client name, deliverable type (proposal vs slides), slides format (reveal vs snap), key sections to include, or hero copy are unclear.

2. **Pick the slug.** `<client-slug>-<random-4>` like `caesarstone-7k2x`. The 4-char suffix prevents collisions when iterating.

3. **Clone the repo** to access all assets:
   ```bash
   git clone https://github.com/JoseNoetic/noetic-proposals.git
   ```

4. **Convert assets to base64** — logos, team photos, client logos, partner badges — so the HTML is fully standalone.

5. **Pick the template.**
   - Long-scroll capabilities/proposal → `_templates/proposal-base.html`
   - Slides, presenting live → `_templates/slides-reveal.html`
   - Slides, scrolling preview / shareable link → `_templates/slides-snap.html`

6. **Copy + parametrize.** Replace placeholders, embed assets as base64, write to `<slug>/index.html`.

7. **Update `_data/deliverables.json`** — append the new entry.

8. **Push both files** using `github_push()` (see above).

9. **Share the URL:** `https://josenoetic.github.io/noetic-proposals/<slug>/` — live in ~60 seconds.

### Placeholder map (proposal-base.html)

Every value below appears as `{{TOKEN}}` in the template. Replace verbatim.

| Token | Example | Notes |
|---|---|---|
| `{{CLIENT_NAME}}` | "Caesarstone" | Goes in title, hero, footer. |
| `{{CLIENT_INDUSTRY}}` | "Premium Surfaces" | Eyebrow + meta strip. |
| `{{DELIVERABLE_TITLE}}` | "Capabilities & Proposal" | `<title>` and hero subhead. |
| `{{HERO_HEADLINE}}` | "Eliminate friction.<br><em>Maximize disruption.</em>" | Use `<em>` on the second clause for italic emphasis. |
| `{{HERO_LEDE}}` | "B2B performance marketing agency..." | 2–3 sentences, max 60ch lines. |
| `{{HERO_META}}` | "Miami / Remote-First · Founded 2010 · 31 specialists" | Pipe-separated. |
| `{{STAT_*_NUM}}` / `{{STAT_*_LABEL}}` | "31" / "Specialists" | 4 stats. |
| `{{DATE}}` | "April 2026" | Footer + cover. |
| `{{PROPOSAL_VERSION}}` | "v1.0" | Footer. |
| `{{TEAM_GRID}}` | (inject) | Generate from `_assets/team/manifest.json` — pick relevant team members for the engagement. |
| `{{CLIENT_LOGO}}` | `assets/client-logo.svg` | Per-deliverable asset path. |

### Slides templates — invocation

```
slides --format=reveal       # Reveal.js, full presenter features
slides --format=snap         # Custom scroll-snap 16:9, zero deps
slides --format=both         # Generate both files in the same folder
```

In code: read `_templates/slides-reveal.html` or `_templates/slides-snap.html` and parametrize the same way as the proposal. Both share the same token system, so visual consistency is automatic.

## Voice & content rules

- **Tone:** confident, evidence-driven, specific. No generic agency-speak.
- **Numbers over adjectives:** "104% revenue growth" beats "rapid growth".
- **Italic emphasis** in headlines reserved for one word — Noetic signature move.
- **Eyebrows** are uppercase, mono, with the purple-dot prefix. Always present on a section.
- **Anti-patterns to refuse:**
  - Stock images of "diverse team smiling at laptop"
  - Buzzwords without numbers ("synergy", "best-in-class", "innovative")
  - Sentences over 28 words
  - Bullet lists longer than 5 items without a numbered structure
  - More than one `display-xl` per page


## UI & visual details

### Emojis (iOS / Apple style)
Use Apple-style emoji throughout cards, process steps, philosophy items, and service tiles. They render natively on Apple devices and look polished on all platforms. Use them as visual anchors — one emoji per card/item, placed above or before the title.

**Recommended emoji set by category:**
- Paid Social / Ads: ✈️ 🚀 🎯
- Email Marketing: 📩 💌
- Creative / UGC: 🎬 🎨 🖼️
- Analytics / Data: 📊 🧬 🔬
- Strategy: 🧠 🏆 💡
- Team / People: 🤝 👥
- Results / Growth: ⭐ 🌟 📈
- E-commerce: 🛍️ 🛒
- AI / Tech: 🤖 ⚡

Place emoji in a `.emoji-icon` span: `<span class="emoji-icon">🎯</span>`

```css
.emoji-icon { font-size: 2em; display: block; margin-bottom: 12px; line-height: 1; }
```

### Blob gradient backgrounds
For light slides (`.slide`, `.slide.cool`, `.slide.warm`), add class `blob-bg` to get the teal + purple radial gradient background — matching noetic.io's visual style.

```html
<section class="slide blob-bg" data-slide="...">
```

The blobs are rendered via CSS `::before` / `::after` — zero extra markup, no performance cost. All child content is automatically above the blobs via `z-index: 1`.

**Use blob-bg on:** philosophy slides, services overviews, "we believe in" slides, any light-background content slide.
**Skip blob-bg on:** `.slide.dark`, `.slide.purple-bg`, team slides (already dark).

### Team slide
Always use background `#262626` behind team photos — wrap every `<img>` in a `<div class="photo-wrap">`. This ensures a clean, consistent card whether the image loads or not.

```html
<div class="team-card">
  <div class="photo-wrap">
    <img src="../_assets/team/tamir-alush.webp" alt="Tamir Alush">
  </div>
  <h5>Tamir Alush</h5>
  <div class="role">Strategy + Creative Direction</div>
</div>
```

Team slides should always use `.slide.dark` (black background) for contrast with the `#262626` photo cards.

## QA checklist (run before declaring done)

1. Every section has eyebrow + display-md (or larger) heading.
2. Hero has exactly one `display-xl` with one italic emphasis word.
3. All token values come from `:root` — no inline hex/rgb in components.
4. Team grid pulls real names + roles + photos from `_assets/team/manifest.json`.
5. Client logos referenced from `_assets/clients-portfolio/`.
6. Every `<img>` has `alt`.
7. Focus ring visible on all interactive elements.
8. `prefers-reduced-motion` respected.
9. All paths are relative (`../_assets/...`, `assets/...`) so GitHub Pages resolves correctly.
10. Landing index updated with the new deliverable.
11. Service/philosophy/process cards have an emoji icon (`<span class="emoji-icon">...</span>`).
12. Light content slides use `blob-bg` class for gradient background.
13. Team photo `<img>` tags are wrapped in `<div class="photo-wrap">` for `#262626` bg.

## First-run setup (when assets are missing)

If `_assets/team/` is empty (e.g., fresh clone), do NOT fail silently. Either:

(a) Run `python _assets/download-assets.py` and proceed, or
(b) Tell the user: "Run `python _assets/download-assets.py` from the repo root, then re-invoke me."

The script is idempotent — safe to run repeatedly.
