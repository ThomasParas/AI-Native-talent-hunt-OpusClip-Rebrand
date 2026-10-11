# OpusClip Rebrand — "Made in the edit." (The Cutting Room)

Submission for the AI-Native Talent Hunt (OpusClip · Senior Visual Designer), Oct 11, 2026 — Thomas Paras.

## Deliverables (root of the zip)
| File | What it is |
|---|---|
| `rebrand-thesis.pdf` | 2-page rebrand thesis: the new direction (look, feel, principle), why it fits OpusClip now, contrast with today's brand. |
| `proof-of-concept-page.pdf` | High-fidelity frames of the redesigned homepage (desktop + mobile), the annotated key interactive moment ("The Cutting Room" scroll sequence, 5 states) and a Rive + Webflow build spec. |
| `page/index.html` | The production HTML/CSS the frames were rendered from. Open it in a browser and scroll to see the key moment live. |

## View the live page
Open `page/index.html` in Chrome/Safari (needs internet for Google Fonts). Scroll through the dark "Cutting Room" band to scrub the animation. Add `?stage=0`…`?stage=4` to the URL to freeze a state.

## Direction in one paragraph
OpusClip is the editor's bench, automated. A light bone "bench" surface for reading and deciding, a dark "screening band" only where footage plays, condensed slate-style display type, and a **two-ink system**: violet (OpusClip's existing purple) marks what the agent found, red grease pencil marks what the human decided. Film-editing cues (sprocket rails, slates, timecode, trim bin) stay at the edges — ≤10% of any screen — so the theme never gets in the way of using the site.

## Honest notes
- No Figma file: frames were rendered from code with Playwright (deliberate — Webflow is HTML/CSS, so the design is buildable exactly as specified). Classes follow Webflow Client-First naming.
- Footage frames and the logo mark are vector placeholders. Proof figures come from the brief and the public OpusClip media kit and are flagged for verification.
- AI usage and decision log: see `PROCESS.md` (uploaded separately) and the repo.

Rebuild PDFs: `uv run -q --with playwright python scripts/render_thesis.py` and `uv run -q --with playwright --with pypdf python scripts/render_frames.py`; package with `scripts/package.sh`.
