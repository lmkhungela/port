#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
SRC = Path("/Users/lulamile.mkhungela/.cursor/projects/Users-lulamile-mkhungela-Documents-mee/assets")
DEST = ROOT / "assets" / "onli-pay"

MAP = {
    "Cover-c08c5c74-b19b-424f-9c07-457d845fa770.jpg": "cover.jpg",
    "2-f1ef98c3-b404-43e6-b019-4d5d4f9f7188.png": "02-joint.png",
    "3-6d305474-0fb7-4a4a-a665-c46aa1de1e55.png": "03-users.png",
    "4-7c3686b4-5219-46f4-b204-f223d625b527.jpg": "04-personas.jpg",
    "5-c7de8e37-4925-4081-ab25-e7681461c94f.png": "05-usability.png",
    "6-c722d223-f8eb-4420-b9fd-9a455ff5ae54.png": "06-accessibility.png",
    "7-bef96173-5316-4aad-83d0-6b8ace9b0f41.jpg": "07-wireframes.jpg",
    "8-8fff787b-f0e8-420e-ae1b-62c1f27cf217.png": "08-solving.png",
    "9-4a13c13a-93f9-40e1-980d-dc8a9158ca6c.jpg": "09-screens.jpg",
    "10-49194284-7de1-48d2-b831-a95aa4d7e75e.jpg": "10-launch.jpg",
    "11-d8c74cca-cb26-4b84-952e-4d586ae29231.png": "11-prototype.png",
    "12-90d54a64-bd3f-4bcb-8682-3d41a5e25ee5.jpg": "12-loans.jpg",
    "13-45bead93-b0ba-4263-b24a-c931f7976243.jpg": "13-light.jpg",
    "14-fb2fa700-04eb-47e5-9a67-f378f202782c.png": "14-ideation.png",
    "15-342deb5e-650c-4625-8d6a-1e78a83c1c35.jpg": "15-ui.jpg",
    "16-2cc8846a-594b-4012-8f0e-5276045f8b94.jpg": "16-dark.jpg",
    "17-5fbc9a2b-3188-4349-8356-7997f8fd1abb.png": "17-overview.png",
    "image-ea52e424-5cab-4426-ad59-d87aea958ca7.png": "extra-1.png",
    "image-9b69aeec-fc75-4475-b09c-c76efcd2b6cd.png": "extra-2.png",
}


def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def inject_site_scripts():
    for p in ROOT.rglob("*.html"):
        if p.name.startswith("_"):
            continue
        t = p.read_text(errors="replace")
        if "canvas class=\"webgl" not in t:
            continue
        rel = Path(*([".."] * (len(p.relative_to(ROOT).parts) - 1)))
        prefix = "" if str(rel) == "." else str(rel) + "/"
        changed = False
        for src in ("js/local-nav.js", "js/globe-sa.js"):
            if src.split("/")[-1] in t:
                continue
            t = t.replace("</head>", f'<script src="{prefix}{src}"></script>\n</head>', 1)
            changed = True
        if changed:
            p.write_text(t)
            print("scripts", p.relative_to(ROOT))


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for src_name, dest_name in MAP.items():
        src = SRC / src_name
        if not src.exists():
            print("missing", src_name)
            continue
        shutil.copy2(src, DEST / dest_name)
        print("copied", dest_name, src.stat().st_size)

    rb = load("_rebuild_work.py")
    fx = load("_fix_works_brand.py")
    rb.write_case_pages()
    fx.rebuild_works_clean()

    for slug in ("academia", "onli-pay", "ridemelo"):
        for p in (ROOT / "projects" / f"{slug}.html", ROOT / "projects" / slug / "index.html"):
            if p.exists():
                t = fx.point_globe_south_africa(fx.social_hashes(fx.brand_html(p.read_text(errors="replace"))))
                p.write_text(t)
                print("branded", p.relative_to(ROOT))

    works = ROOT / "works.html"
    works.write_text(fx.point_globe_south_africa(fx.social_hashes(fx.brand_html(works.read_text(errors="replace")))))
    fx.apply_sitewide()
    inject_site_scripts()

    w = works.read_text(errors="replace")
    print("works cards", w.count("work column w-dyn-item"))
    print("UI filter present", "UI des" in w)
    print("onli images", (ROOT / "projects" / "onli-pay.html").read_text().count("assets/onli-pay/"))


if __name__ == "__main__":
    main()
