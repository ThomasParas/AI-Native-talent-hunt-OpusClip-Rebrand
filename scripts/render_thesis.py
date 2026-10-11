"""Render thesis/rebrand-thesis.html to dist/rebrand-thesis.pdf.

Run: uv run -q --with playwright python scripts/render_thesis.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "thesis" / "rebrand-thesis.html"
OUT = ROOT / "dist" / "rebrand-thesis.pdf"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SRC.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready.then(() => true)")
        page.emulate_media(media="print")
        # Each .sheet is a fixed Letter page with overflow hidden; flag clipped content.
        overflow = page.evaluate(
            """() => [...document.querySelectorAll('.sheet')].map((s, i) => {
                const foot = s.querySelector('.foot');
                const kids = [...s.children].filter(c => c !== foot && !c.classList.contains('rail'));
                const bottom = Math.max(...kids.map(c => c.getBoundingClientRect().bottom));
                const limit = s.getBoundingClientRect().bottom - 0.6 * 96;
                return {page: i + 1, spare_px: Math.round(limit - bottom)};
            })"""
        )
        for o in overflow:
            status = "OK" if o["spare_px"] >= 0 else "OVERFLOW"
            print(f"page {o['page']}: {status} (spare {o['spare_px']}px)")
        page.pdf(
            path=str(OUT),
            format="Letter",
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
