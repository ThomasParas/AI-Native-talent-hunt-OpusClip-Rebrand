# PROCESS — OpusClip Rebrand Thesis & Proof-of-Concept Page

Solo, in person (SF), AI-Native Talent Hunt, 2026-10-11. Brief due 16:00 PDT.
Human: Thomas Paras (direction, decisions). AI: Claude Code (Opus 5.5) for research, option generation, build, packaging.
All times PDT.

## Log

- **15:12** — Session start. Clock checked: 48 min to the brief's 16:00 deadline (Thomas's own 15:30 target was moved to 16:00 at 15:18).
- **15:12** — Research (Firecrawl scrape) of opus.pro homepage + media.opus.pro media kit. Findings: black bg + single purple `#6723FF`, Geist type, dark SaaS template; "viral clips / 1 long → 10 clips" messaging; mega-menu of 13+ features and 10 segments; three separate product logo systems (OpusClip, AI Producer, Agent Opus); media kit still says "16M creators"; site under-tells the new agent story (API + MCP).
- **15:14** — Claude proposed 4 directions (A Raw Cut editorial film-edit, B 9:16 frame-as-system, C premium dark, D agent console) scored on differentiation / fit / Webflow+Rive buildability / time. Recommended A+B.
- **15:18** — Thomas leaned A+B with a "classic Hollywood editing room" feel, *with the constraint that theming must stay peripheral and never hurt usability*. Asked Claude to poke holes.
- **15:19** — Holes raised by Claude: (1) Hollywood glamour contradicts "authenticity" → reframe **"cutting room, not red carpet"**; (2) nostalgia vs "next chapter" → heritage in materials, modern structure; (3) Gen Z won't know Moviola/Steenbeck → only universally legible cues (sprockets, slate, leader countdown, grease pencil, trim bin); (4) kitsch/perf (sepia, grain) → flat vector; (5) usability → hard **"edges only, ≤10% themed surface"** rule; (6) losing purple equity → **two-ink system** (red = human marks, violet = agent marks); (7) light vs dark → light bench + dark screening band; (8) Runway owns "cinematic"; (9) a11y (contrast, reduced motion).
- **15:21** — Tooling decision: no Figma/Lovable signup (Figma MCP unauthenticated; ~10 min cost). Build directly in HTML/CSS (maps 1:1 to Webflow classes) and render frames to PDF with Playwright. Disclosed as a deliberate trade-off.
- **15:22** — Thomas: yes to all three (cutting room reframe, two-ink, light bench + dark band). Asked for a competitor check first.
- **15:22** — Competitor scan (Firecrawl branding extraction; approximate): Runway (white, blue-violet), **Descript (warm cream `#FFF7FA` + red `#F73B3B` + serif)**, Captions (white, cyan, serif, "edits like a professional editor", "20M creators"), Kapwing (grey, Google blue, "30M"), Vizard (purple+pink, "viral"), Submagic (orange, "viral"). Adjustments: neutral bone bg not cream; red only as marks, never buttons; ink-black CTAs; **condensed grotesk headlines, not serif** (serif headline space is crowded); violet only as the *agent's ink*; drop "viral" and "20M" as lead claims. Nobody owns film-editing iconography → open territory.
- **15:25** — Thesis-line brainstorm (14 candidates, 3 finalists). Claude flagged its own first line ("Everyone else is generating video. We cut yours.") as risky because OpusClip ships generative AI B-roll/dubbing. Decision: principle **"Made in the edit."**; hero H1 **"You shot it. We'll make the cut."**
- **15:27** — Thomas: go. Build start.
- **15:29** — Repo scaffolded + pushed. Verified Python Playwright via `uv run --with playwright` (Chromium already cached).
- **15:29** — Parallelised: a Claude sub-agent wrote `thesis/rebrand-thesis.html` + `scripts/render_thesis.py` from a tight outline of the decisions above, while the main session built `page/index.html`. Sub-agent self-checked page count (exactly 2) and font loading.
- **15:31** — Security hook flagged `innerHTML` in the film-strip builder (static data, but rewritten with `createElement`/`textContent`).
- **15:33** — Page committed. Wrote `scripts/render_frames.py`: Playwright captures desktop full page, mobile 390 @2x, and the key moment frozen at each of its 5 states (`?stage=0..4`), then lays them out with annotation + Rive/Webflow spec sheets and merges to a 5-page PDF.
- **15:35** — Visual QA of rendered frames found 2 bugs: (1) trim-bin clips overflowing (fixed width × 5); (2) stage too narrow — `margin:auto` on a flex-column child disables stretch. Fixed both (fluid clips, `width:100%` on the sticky container, smaller strip frames so two agent picks are visible), re-rendered.
- **15:37** — README + `scripts/package.sh`. Fresh-unzip test: both PDFs open (thesis 2 pp, frames 5 pp); live `page/index.html` from the unzipped copy runs with zero JS errors and the scroll sequence advances stages. Secrets scan of zip + git history: clean; no `.env` used (no API keys needed for this assignment).
- **15:40** — Final package + push.

## Deliberate trade-offs (disclosed)
- No Figma file; frames are rendered from production HTML/CSS (Webflow-mappable classes). The Rive file is specified, not built.
- Footage frames + logo mark are vector placeholders. Proof stats from brief/media kit, flagged for verification.
- Competitor scan was homepage-level with automated brand extraction — directional, not a full audit.

## AI usage
- Claude Code: research scraping/summarising (Firecrawl), option space + risk analysis, copy brainstorm, HTML/CSS/JS build, Playwright PDF rendering, packaging script.
- Not used: image generation (all visuals are vector/CSS placeholders by choice), Figma.
