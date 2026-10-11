"""Render proof-of-concept-page.pdf: high-fidelity frames of page/index.html + annotated spec pages.

Run: uv run -q --with playwright --with pypdf python scripts/render_frames.py
"""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "page" / "index.html").as_uri()
SHOTS = ROOT / "build" / "shots"
PARTS = ROOT / "build" / "parts"
OUT = ROOT / "dist" / "proof-of-concept-page.pdf"

# Freeze the scroll section into a static, full-height frame for full-page captures.
STATIC_CSS = """
.section_cutting-room{height:auto!important;padding:40px 0 90px}
.cutting-room_sticky{position:relative!important;height:auto!important;padding-top:60px}
.navbar{position:relative!important}
.mark-human path{animation:none!important;stroke-dashoffset:0!important}
*{transition:none!important}
"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">'

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#EDEBE6;color:#141210;font-family:Geist,system-ui,sans-serif;font-size:15px;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{padding:56px 64px}
.tc{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:#55504A}
h1,h2{font-family:Archivo;font-stretch:62%;font-weight:800;text-transform:uppercase;line-height:.92}
h1{font-size:96px} h2{font-size:52px;margin:6px 0 18px}
h3{font-size:17px;font-weight:600;margin:0 0 6px}
p,li{color:#2b2723} ul{padding-left:18px} li{margin-bottom:5px}
.rail{height:14px;background:repeating-linear-gradient(90deg,transparent 0 10px,rgba(20,18,16,.18) 10px 22px,transparent 22px 32px);-webkit-mask:linear-gradient(#000 0 0) center/100% 6px no-repeat;margin-bottom:28px}
.v{color:#6723FF;font-weight:600} .r{color:#A3160E;font-weight:600}
.n{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:#6723FF;color:#fff;font:600 12px 'Geist Mono';margin-right:8px;flex:0 0 24px}
.n.h{background:#D9271C}
.note{display:flex;gap:4px;margin-bottom:14px} .note div{flex:1}
img{display:block;max-width:100%;border:1px solid rgba(20,18,16,.18);border-radius:6px}
code{font-family:'Geist Mono',monospace;font-size:12.5px;background:#E3E0D9;padding:1px 5px;border-radius:3px}
table{border-collapse:collapse;width:100%;font-size:13.5px} td,th{border-top:1px solid rgba(20,18,16,.18);padding:7px 8px;text-align:left;vertical-align:top} th{font-family:'Geist Mono';font-size:11px;text-transform:uppercase;color:#55504A;font-weight:500}
.sw{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:-2px;margin-right:6px;border:1px solid rgba(0,0,0,.15)}
"""


def b64(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def shoot(pw):
    SHOTS.mkdir(parents=True, exist_ok=True)
    b = pw.chromium.launch()
    # Desktop full page (stage 4 frozen)
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    pg.goto(PAGE + "?stage=4&theme=light", wait_until="networkidle"); pg.evaluate("document.fonts.ready")
    pg.add_style_tag(content=STATIC_CSS); pg.wait_for_timeout(400)
    pg.screenshot(path=SHOTS / "desktop-full.png", full_page=True)
    pg.screenshot(path=SHOTS / "desktop-hero.png")
    # Each stage of the key moment, captured as it appears in the sticky viewport
    for s in range(5):
        p2 = b.new_page(viewport={"width": 1440, "height": 900})
        p2.goto(PAGE + f"?stage={s}&theme=light", wait_until="networkidle"); p2.evaluate("document.fonts.ready")
        p2.add_style_tag(content="*{transition:none!important}")
        p2.wait_for_timeout(250)
        p2.locator(".cutting-room_sticky .container-large").screenshot(path=SHOTS / f"stage-{s}.png")
        p2.close()
    # Mobile full page
    m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    m.goto(PAGE + "?stage=4&theme=light", wait_until="networkidle"); m.evaluate("document.fonts.ready")
    m.add_style_tag(content=STATIC_CSS); m.wait_for_timeout(400)
    m.screenshot(path=SHOTS / "mobile-full.png", full_page=True)
    # Dark theme (toggle in nav) — desktop full page + hero
    d = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    d.goto(PAGE + "?stage=4&theme=dark", wait_until="networkidle"); d.evaluate("document.fonts.ready")
    d.add_style_tag(content=STATIC_CSS); d.wait_for_timeout(400)
    d.screenshot(path=SHOTS / "dark-hero.png")
    d.screenshot(path=SHOTS / "dark-full.png", full_page=True)
    b.close()


def sheets():
    s = {k: b64(SHOTS / f"{k}.png") for k in ["desktop-full", "desktop-hero", "mobile-full", "dark-hero", "dark-full"] + [f"stage-{i}" for i in range(5)]}
    out = []

    out.append(("cover", 1600, 1000, f"""
<div class="sheet"><div class="rail"></div>
<span class="tc">OpusClip · Proof-of-concept page · Oct 11, 2026 · Thomas Paras</span>
<h1 style="margin:18px 0 22px">The Cutting Room<br>— Homepage</h1>
<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:48px">
<div>
<p style="font-size:19px;max-width:620px">A redesigned opus.pro homepage that proves the rebrand thesis <b>"Made in the edit."</b> Light editing-bench surfaces, a dark screening band only where footage plays, and a two-ink system: <span class="v">violet = what the agent found</span>, <span class="r">red = what the human decided</span>.</p>
<h3 style="margin-top:28px">In this PDF</h3>
<ol style="padding-left:18px"><li>Desktop homepage — full frame, annotated</li><li>Key interactive moment — "The Cutting Room" scroll sequence, 5 states + Rive/Webflow build spec</li><li>Mobile frame (390 px) + secondary motion</li><li>Design tokens + Webflow class map</li><li>Dark mode (visitor toggle)</li></ol>
<p class="tc" style="margin-top:24px">Frames rendered from the production HTML/CSS (page/index.html) with Playwright — no Figma file. Every block uses Webflow-style classes so it rebuilds 1:1.</p>
</div>
<img src="{s['desktop-hero']}">
</div></div>"""))

    out.append(("desktop", 1600, 0, f"""
<div class="sheet" style="display:grid;grid-template-columns:1000px 1fr;gap:44px;align-items:start">
<img src="{s['desktop-full']}" style="width:1000px">
<div style="position:sticky;top:0">
<span class="tc">Frame 01 · Desktop 1440 · full page</span><h2>Homepage, top to bottom</h2>
<div class="note"><span class="n">1</span><div><h3>Nav — plain, modern</h3><p>Theme never touches navigation. Four links instead of today's 13-feature mega-menu. Ink-black primary CTA. Light/dark toggle (see Frame 04).</p></div></div>
<div class="note"><span class="n h">2</span><div><h3>Hero — "You shot it. We'll make the cut."</h3><p>Condensed slate display (Archivo 62% width). A <span class="r">red grease-pencil</span> stroke draws under "make the cut" on load (0.9s, delay 0.5s, ease <code>cubic-bezier(.6,0,.2,1)</code>). Right column: paste-a-link drop zone + proof stats.</p></div></div>
<div class="note"><span class="n">3</span><div><h3>The Cutting Room — key moment</h3><p>Dark screening band. Scroll-driven Rive sequence: roll → agent marks → splice → trim bin → human approves. Full spec on the next page.</p></div></div>
<div class="note"><span class="n">4</span><div><h3>Three takes (slates)</h3><p>Slate clapper stripe + scene/take/time header are the only themed parts; body copy is plain. Each card tagged with whose ink it is.</p></div></div>
<div class="note"><span class="n">5</span><div><h3>Two inks</h3><p>States the system's principle in product terms: the agent proposes in <span class="v">violet</span>, you decide in <span class="r">red</span>. Builds trust for teams and businesses.</p></div></div>
<div class="note"><span class="n">6</span><div><h3>Three reels</h3><p>Unifies OpusClip, AI Producer and Agent Opus (API + MCP) into one architecture instead of three logo systems.</p></div></div>
<div class="note"><span class="n">7</span><div><h3>Proof</h3><p>Big condensed numerals on a ruled line. Figures from brief + public media kit; flagged for verification.</p></div></div>
<div class="note"><span class="n">8</span><div><h3>Closing CTA — leader countdown</h3><p>Film-leader circle counts 3-2-1 on loop (1s/step, conic sweep). Pure CSS; static "3" under reduced motion.</p></div></div>
<p class="tc" style="margin-top:18px">Themed surface per viewport stays ≤10%: sprocket rails, slates, timecode, marks. Copy, forms and buttons are untouched.</p>
</div></div>"""))

    stages = [
        ("0 · ROLL", "progress 0–20", "Film strip of the raw 58-min video scrolls left under a fixed playhead (strip translateX 0 → −380px, linear, scrubbed). Timecode counter ticks with scroll."),
        ("1 · MARK", "progress 20–40", "Agent marks 4 frames: violet rings scale 1.08 → 1 + fade in, score chips (94/91/88/86) drop 4px. Stagger 80ms. Step 02 highlights in violet."),
        ("2 · SPLICE", "progress 40–60", "Unpicked frames dim to 25% opacity; picks lift −14px (600ms). This is the 'cut' — the agent's selection made physical."),
        ("3 · HANG", "progress 60–80", "Strip retracts up to 35% opacity; trim bin slides up 30px + fades in. Picks land as 9:16 clips hanging on pins with ±1° sway, captions + scores."),
        ("4 · APPROVE", "progress 80–100", "Human beat: red grease-pencil loop draws around clip 1 (path trim 0 → 100%, 800ms). Others dim to 55%. Pill 'Approved · posting to…' rises in (delay 500ms)."),
    ]
    rows = "".join(
        f'<div><img src="{s[f"stage-{i}"]}"><p style="margin-top:8px"><span class="n{" h" if i==4 else ""}">{i}</span><b>{t}</b> <span class="tc">{p}</span></p><p style="font-size:13.5px">{d}</p></div>'
        for i, (t, p, d) in enumerate(stages))
    out.append(("moment", 1600, 0, f"""
<div class="sheet"><div class="rail"></div>
<span class="tc">Frame 02 · Key interactive moment · annotated</span><h2>The Cutting Room — scroll sequence</h2>
<p style="max-width:1100px;margin-bottom:24px">One long video becomes approved, posted clips — in the language of a real cutting room. The agent's actions are drawn in <span class="v">violet</span>; the human's single, final decision is drawn in <span class="r">red</span>. That split <i>is</i> the brand principle, so the key moment demonstrates it rather than decorating it.</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px 32px">{rows}
<div style="background:#E3E0D9;border-radius:8px;padding:20px 22px">
<h3>Reduced motion &amp; mobile</h3>
<ul><li><code>prefers-reduced-motion</code>: section collapses to normal height, shows state 4 statically; no scrub, no countdown.</li><li>≤900px: step list becomes a 5-segment progress bar; 3 clips instead of 5; same state machine.</li><li>Steps list is real HTML text (accessible); Rive canvas gets <code>aria-label</code> describing the sequence.</li></ul>
</div></div></div>"""))

    out.append(("spec", 1600, 0, """
<div class="sheet"><div class="rail"></div>
<span class="tc">Frame 02b · Build spec for a Webflow + Rive designer</span><h2>How to build it</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:44px">
<div>
<h3>Rive file: <code>cutting-room.riv</code></h3>
<table>
<tr><th>Item</th><th>Spec</th></tr>
<tr><td>Artboard</td><td><code>CuttingRoom</code> 1200×520 (desktop), <code>CuttingRoomMobile</code> 360×440. Background #1A1816, radius 10.</td></tr>
<tr><td>State machine</td><td><code>SM_Scroll</code></td></tr>
<tr><td>Inputs</td><td><code>progress</code> (Number 0–100, scrubbed by scroll) · <code>reducedMotion</code> (Boolean) · <code>approve</code> (Trigger, optional click-to-approve on clip 1)</td></tr>
<tr><td>Layers</td><td>Strip (18 frames + 2 sprocket rails), Playhead, Rings×4, Scores×4, Bin bar + pins, Clips×5 (9:16), ApproveLoop (red path), PostPill</td></tr>
<tr><td>Roll (0–20)</td><td>Blend state: Strip.x = −progress×19px (1D blend on <code>progress</code>), linear.</td></tr>
<tr><td>Mark (20–40)</td><td>Transition when progress ≥ 20: Rings opacity 0→1, scale 108→100%, 350ms, ease-out; Scores y −4→0. Stagger 80ms.</td></tr>
<tr><td>Splice (40–60)</td><td>≥ 40: non-picks opacity → 25%, picks y −14, 600ms <code>cubic-bezier(.6,0,.2,1)</code>.</td></tr>
<tr><td>Hang (60–80)</td><td>≥ 60: Strip y −74, opacity 35%; Bin y +30→0, opacity 0→1, 700ms. Clips: idle sway ±1° loop 2.4s.</td></tr>
<tr><td>Approve (80–100)</td><td>≥ 80 (or <code>approve</code> fires): ApproveLoop trim-path end 0→100%, 800ms; other clips 55%; PostPill fade+y 8→0, delay 500ms.</td></tr>
<tr><td>Reverse</td><td>Every transition has a mirrored transition on progress &lt; threshold so scrolling up rewinds.</td></tr>
<tr><td>Reduced motion</td><td><code>reducedMotion = true</code> → jump to Approve end state, no animation.</td></tr>
</table>
</div>
<div>
<h3>Webflow page build</h3>
<table>
<tr><th>Element</th><th>Spec</th></tr>
<tr><td><code>section_cutting-room</code></td><td>Height 420vh, bg #0E0D0C, position relative. Child <code>cutting-room_sticky</code>: position sticky, top 0, height 100vh, flex column centered.</td></tr>
<tr><td>Rive element</td><td>Webflow native Rive element inside <code>cr-stage</code>, file <code>cutting-room.riv</code>, state machine <code>SM_Scroll</code>, fit: contain.</td></tr>
<tr><td>Interaction</td><td>Trigger: <i>Scroll → While page is scrolling</i> scoped to <code>section_cutting-room</code>. Action: <i>Rive → set input</i> <code>progress</code> 0 at 0% → 100 at 100%. Smoothing 50%.</td></tr>
<tr><td>Step list</td><td>Same interaction: <code>cr-steps li</code> get combo class <code>is-active</code> at 0/20/40/60/80% (Webflow class toggle keyframes).</td></tr>
<tr><td>Timecode</td><td>Small custom-code embed (≈10 lines, as in page/index.html) maps scroll % → <code>00:MM:SS:FF</code>.</td></tr>
<tr><td>Reduced motion</td><td>Embed sets <code>reducedMotion</code> from <code>matchMedia</code>; CSS in page settings un-sticks section.</td></tr>
<tr><td>Hero underline</td><td>Inline SVG embed, path stroke-dashoffset 420→0 via Webflow <i>Page load</i> interaction, 900ms, delay 500ms. (Or a 2-state Rive file reused site-wide as the "human mark" component.)</td></tr>
<tr><td>Leader countdown</td><td>CSS-only embed (conic sweep + 3-2-1). Can be swapped for a tiny Rive loop.</td></tr>
<tr><td>Performance</td><td>Rive file target &lt; 150 KB; lazy-load when section is within 1 viewport. No video, no raster textures on this section.</td></tr>
</table>
<p class="tc" style="margin-top:16px">Reference implementation (CSS + 40 lines JS) ships in page/index.html — open it and scroll to see the exact timing.</p>
</div></div></div>"""))

    out.append(("mobile", 1600, 0, f"""
<div class="sheet" style="display:grid;grid-template-columns:420px 1fr;gap:56px;align-items:start">
<img src="{s['mobile-full']}" style="width:420px">
<div>
<span class="tc">Frame 03 · Mobile 390</span><h2>Mobile + system</h2>
<div class="note"><span class="n">1</span><div><h3>Same hierarchy, single column</h3><p>Nav collapses to logo + one CTA. Hero headline stays condensed so "You shot it. We'll make the cut." holds in 4 lines at 56px.</p></div></div>
<div class="note"><span class="n">2</span><div><h3>Cutting Room on mobile</h3><p>Steps become a 5-segment progress bar; Rive artboard <code>CuttingRoomMobile</code> shows 3 clips. Same <code>progress</code> input.</p></div></div>
<h3 style="margin-top:26px">Design tokens</h3>
<table>
<tr><th>Token</th><th>Value</th><th>Rule</th></tr>
<tr><td><span class="sw" style="background:#EDEBE6"></span>bench</td><td>#EDEBE6</td><td>Default surface — neutral bone, deliberately not cream (Descript owns warm cream).</td></tr>
<tr><td><span class="sw" style="background:#0E0D0C"></span>screen</td><td>#0E0D0C</td><td>Only where footage plays.</td></tr>
<tr><td><span class="sw" style="background:#141210"></span>ink</td><td>#141210</td><td>Text + all primary buttons.</td></tr>
<tr><td><span class="sw" style="background:#6723FF"></span>agent</td><td>#6723FF</td><td>Agent's marks only (existing OpusClip purple — equity kept).</td></tr>
<tr><td><span class="sw" style="background:#D9271C"></span>human</td><td>#D9271C / text #A3160E</td><td>Human's marks only. Strokes, never fills or buttons.</td></tr>
<tr><td>Display</td><td>Archivo, wdth 62, 800</td><td>Uppercase headlines (slate / edge-code feel).</td></tr>
<tr><td>Body</td><td>Geist 400–600</td><td>Continuity with today's site.</td></tr>
<tr><td>Mono</td><td>Geist Mono</td><td>Timecodes, labels.</td></tr>
</table>
<h3 style="margin-top:22px">Webflow class map</h3>
<p><code>navbar</code> · <code>section_hero</code> · <code>section_cutting-room</code> + <code>cutting-room_sticky</code> · <code>section_how</code> + <code>slate</code> (component) · <code>section_inks</code> · <code>section_reels</code> + <code>reel</code> (component, CMS-ready) · <code>section_proof</code> · <code>section_cta</code> + <code>leader</code> · <code>footer</code>. Global: <code>container-large</code>, <code>heading-display</code>, <code>button is-primary/is-secondary/is-light</code>, <code>timecode</code>, <code>sprocket-rail</code>, <code>mark-human</code>, <code>ink-tag is-agent/is-human</code>.</p>
<p class="tc" style="margin-top:14px">Placeholders: footage frames are vector stand-ins; swap for real customer clips via CMS. Logo mark is a placeholder — logo work is out of scope for this PoC.</p>
</div></div>"""))
    out.append(("dark", 1600, 0, f"""
<div class="sheet" style="display:grid;grid-template-columns:1000px 1fr;gap:44px;align-items:start">
<img src="{s['dark-full']}" style="width:1000px">
<div>
<span class="tc">Frame 04 · Dark mode · visitor toggle</span><h2>Same room,<br>lights down</h2>
<img src="{s['dark-hero']}" style="margin-bottom:22px">
<div class="note"><span class="n">1</span><div><h3>Toggle</h3><p>Nav button (moon / sun + label), <code>aria-pressed</code>, keyboard-focusable. Default follows the OS (<code>prefers-color-scheme</code>); a visitor's choice is remembered (<code>localStorage</code>). Set before first paint, so no flash.</p></div></div>
<div class="note"><span class="n">2</span><div><h3>Only tokens change</h3><p>Bench → #191715, ink → #EDEBE6, cards → #211F1C. The screening band drops a step to #0A0908 so footage still reads as "the screen". No component has its own dark styles.</p></div></div>
<div class="note"><span class="n h">3</span><div><h3>Inks keep their meaning</h3><p>Agent violet lifts to #B79BFF and human red text to #FF7A6E for contrast on dark; strokes keep #6723FF / #D9271C fills where they sit on footage.</p></div></div>
<div class="note"><span class="n">4</span><div><h3>Webflow build</h3><p>Two Variable modes (Light / Dark) in Webflow Variables; a 10-line embed sets <code>data-theme</code> on <code>&lt;html&gt;</code> and the toggle flips it. Rive file unchanged (it sits in the screening band, which is dark in both modes).</p></div></div>
</div></div>"""))
    return out


def main():
    PARTS.mkdir(parents=True, exist_ok=True); OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        shoot(pw)
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 1000})
        files = []
        for name, w, h, body in sheets():
            pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{BASE_CSS}</style></head><body>{body}</body></html>", wait_until="networkidle")
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            height = h or pg.evaluate("document.documentElement.scrollHeight")
            f = PARTS / f"{name}.pdf"
            pg.pdf(path=str(f), width=f"{w}px", height=f"{height + 2}px", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            files.append(f)
        b.close()
    w = PdfWriter()
    for f in files:
        w.append(str(f))
    w.write(str(OUT))
    print("wrote", OUT, "pages:", len(w.pages))


if __name__ == "__main__":
    main()
