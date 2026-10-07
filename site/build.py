#!/usr/bin/env python3
"""Build the Radar site.

Inlines Echo's Rive file (base64) and the SVG fallback rig into src/page.html.

  python3 site/build.py                    -> writes site/index.html (deployable page)
  python3 site/build.py --fragment OUT     -> also writes a body-only copy for hosts
                                              that add their own <html>/<head> wrapper
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src" / "page.html"
RIV = ROOT / "assets" / "echo.riv"
SVG = ROOT / "assets" / "echo.svg"

# Extra parts the SVG fallback rig needs for modes the base artwork doesn't draw.
EXTRAS = """
<g id="echo-x-signal" class="x" data-pivot-x="400" data-pivot-y="236"><path d="M378 240 Q400 220 422 240"/><path d="M360 224 Q400 190 440 224"/><path d="M342 208 Q400 160 458 208"/></g>
<g id="echo-x-check" class="x" data-pivot-x="612" data-pivot-y="429"><circle cx="612" cy="429" r="26" fill="#F6C9DC" stroke="#422A51" stroke-width="5"/><path d="M600 430l9 9 16-18" fill="none" stroke="#422A51" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>
<g id="echo-x-heart" class="x" data-pivot-x="590" data-pivot-y="400"><path d="M590 424C560 404 562 378 578 374c8-2 12 4 12 10 0-6 4-12 12-10 16 4 18 30-12 50z" fill="#FF9CC8" stroke="#422A51" stroke-width="4" stroke-linejoin="round"/></g>
<g id="echo-x-sparkles" class="x" data-pivot-x="400" data-pivot-y="400" fill="#F6C9DC"><path d="M230 260l6 16 16 6-16 6-6 16-6-16-16-6 16-6z"/><path d="M580 220l5 13 13 5-13 5-5 13-5-13-13-5 13-5z"/><path d="M640 360l4 10 10 4-10 4-4 10-4-10-10-4 10-4z"/><path d="M170 410l4 10 10 4-10 4-4 10-4-10-10-4 10-4z"/></g>
<g id="echo-x-card" class="x" data-pivot-x="400" data-pivot-y="590"><rect x="318" y="548" width="164" height="92" rx="14" fill="#FFF8EE" stroke="#422A51" stroke-width="5"/><circle cx="352" cy="594" r="16" fill="#F6C9DC"/><rect x="380" y="580" width="78" height="9" rx="4.5" fill="#CFB8E7"/><rect x="380" y="598" width="56" height="9" rx="4.5" fill="#E6DAF2"/></g>
<path id="echo-x-mouth" class="x" d="M384 456Q400 480 416 456Z" fill="#422A51" stroke="#422A51" stroke-width="3" stroke-linejoin="round"/>
"""


def echo_svg() -> str:
    svg = SVG.read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r"<title[^>]*>.*?</title>", "", svg, flags=re.S)
    svg = re.sub(r"<desc[^>]*>.*?</desc>", "", svg, flags=re.S)
    svg = re.sub(r'\s(role|aria-labelledby)="[^"]*"', "", svg)
    svg = svg.replace('id="', 'id="echo-')
    close = svg.rfind("</g>")
    if close == -1:
        raise SystemExit("echo.svg: root group not found")
    svg = svg[:close] + EXTRAS + svg[close:]
    return " ".join(svg.split())


def build() -> str:
    page = SRC.read_text(encoding="utf-8")
    riv_b64 = base64.b64encode(RIV.read_bytes()).decode("ascii")
    for marker in ("__RIV_B64__", "<!--__ECHO_SVG__-->", "<!--__BODY__-->"):
        if marker not in page:
            raise SystemExit(f"page.html is missing {marker}")
    return page.replace("__RIV_B64__", riv_b64).replace("<!--__ECHO_SVG__-->", echo_svg())


def main() -> None:
    page = build()
    head, body = page.split("<!--__BODY__-->", 1)
    full = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        f"{head.strip()}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
    )
    (ROOT / "index.html").write_text(full, encoding="utf-8")
    print(f"wrote {ROOT / 'index.html'} ({len(full) // 1024} KB)")
    if "--fragment" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--fragment") + 1])
        out.write_text(head.strip() + "\n" + body.strip() + "\n", encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
