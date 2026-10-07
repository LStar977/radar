#!/usr/bin/env python3
"""Build the Radar app prototype.

Inlines Echo's Rive file and the SVG fallback rig (shared with the website) into src/app.html.

  python3 app/build.py                  -> writes app/index.html (uses ../site/rive.wasm)
  python3 app/build.py --fragment OUT   -> also writes a body-only copy that expects rive.wasm
                                           next to it, for hosts that add their own wrapper
"""
import base64
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SITE_BUILD = ROOT.parent / "site" / "build.py"
SRC = ROOT / "src" / "app.html"

_spec = importlib.util.spec_from_file_location("site_build", SITE_BUILD)
site_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site_build)


def build(wasm_url: str) -> str:
    page = SRC.read_text(encoding="utf-8")
    for marker in ("__RIV_B64__", "<!--__ECHO_SVG__-->", "<!--__BODY__-->", "__WASM_URL__"):
        if marker not in page:
            raise SystemExit(f"app.html is missing {marker}")
    riv_b64 = base64.b64encode(site_build.RIV.read_bytes()).decode("ascii")
    return (page.replace("__RIV_B64__", riv_b64)
                .replace("<!--__ECHO_SVG__-->", site_build.echo_svg())
                .replace("__WASM_URL__", wasm_url))


def main() -> None:
    head, body = build("../site/rive.wasm").split("<!--__BODY__-->", 1)
    full = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        f"{head.strip()}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
    )
    (ROOT / "index.html").write_text(full, encoding="utf-8")
    print(f"wrote {ROOT / 'index.html'} ({len(full) // 1024} KB)")
    if "--fragment" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--fragment") + 1])
        fhead, fbody = build("rive.wasm").split("<!--__BODY__-->", 1)
        out.write_text(fhead.strip() + "\n" + fbody.strip() + "\n", encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
