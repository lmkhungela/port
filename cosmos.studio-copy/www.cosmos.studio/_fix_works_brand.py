#!/usr/bin/env python3
from __future__ import annotations

import html as htmlmod
import importlib.util
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKUP = Path("/Users/lulamile.mkhungela/Documents/mee copy/cosmos.studio-copy/www.cosmos.studio")

spec = importlib.util.spec_from_file_location("rb", str(ROOT / "_rebuild_work.py"))
rb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rb)


def project_list():
    items = []
    for cs in rb.CASE_STUDIES:
        items.append(
            {
                "href": f'projects/{cs["slug"]}.html',
                "title": cs["title"],
                "tags": cs["tags"],
                "year": cs["year"],
                "category": "Case studies",
                "external": False,
                "img": Path(cs["cover"]).name,
            }
        )
    for href, img, title, tags in rb.WEBSITES:
        items.append({"href": href, "title": title, "tags": tags, "year": "2024", "category": "Websites", "external": href.startswith("http"), "img": img})
    for href, img, title, tags in rb.LIVE_APPS:
        items.append({"href": href, "title": title, "tags": tags, "year": "2024", "category": "Live apps", "external": True, "img": img})
    for href, img, title, tags in rb.HACKS:
        items.append({"href": href, "title": title, "tags": tags, "year": "2023", "category": "Hackathons", "external": True, "img": img})
    for href, img, title, tags in rb.FIGMA + rb.FE_BUILDS:
        items.append({"href": href, "title": title, "tags": tags, "year": "2024", "category": "Figma + FE builds", "external": href.startswith("http"), "img": img})
    return items


def trim_card(card: str) -> str:
    m = list(re.finditer(r'class="category-counter_text">[^<]*</div></div></div></div></div>', card))
    if not m:
        return card
    return card[: m[-1].end()]


def retarget(card: str, proj: dict) -> str:
    cat = proj["category"]
    card = re.sub(
        r'<div role="listitem" class="work column w-dyn-item">',
        '<div role="listitem" class="work column w-dyn-item">',
        card,
        count=1,
    )
    ext = ' target="_blank" rel="noopener noreferrer"' if proj["external"] else ""
    card = re.sub(
        r'<a href="[^"]+" class="case-wrapper w-inline-block">',
        f'<a href="{htmlmod.escape(proj["href"])}" class="case-wrapper w-inline-block"{ext}>',
        card,
        count=1,
    )
    card = re.sub(
        r'<div class="additional-text">[^<]*</div>',
        f'<div class="additional-text">{htmlmod.escape(proj["tags"])}</div>',
        card,
        count=1,
    )
    card = re.sub(
        r'<div class="additional-text case-year">[^<]*</div>',
        f'<div class="additional-text case-year">{htmlmod.escape(proj["year"])}</div>',
        card,
        count=1,
    )
    card = re.sub(
        r'<h3 class="p-large">[^<]*</h3>',
        f'<h3 class="p-large">{htmlmod.escape(proj["title"])}</h3>',
        card,
        count=1,
    )
    card = re.sub(r'(class="category-counter_text">)[^<]*', r"\1" + cat, card)
    card = re.sub(
        r'(<img src="[^"]+" loading="eager" alt=")[^"]*"',
        r"\1" + htmlmod.escape(proj["title"]) + '"',
        card,
        count=1,
    )
    img = proj.get("img")
    if img:
        card = re.sub(
            r'<img src="[^"]+"',
            f'<img src="assets/{htmlmod.escape(img)}"',
            card,
            count=1,
        )
        card = re.sub(r'\s+srcset="[^"]*"', "", card, count=1)
        card = re.sub(r'\s+sizes="[^"]*"', "", card, count=1)
    return card


FILTERS = [
    ("case-studies", "Case st<strong>u</strong>dies", "Case studies"),
    ("websites", "Web<strong>s</strong>ites", "Websites"),
    ("live-apps", "Live a<strong>p</strong>ps", "Live apps"),
    ("hackathons", "Hacky hac<strong>k</strong>y", "Hackathons"),
    ("figma-fe", "Figma + FE b<strong>u</strong>ilds", "Figma + FE builds"),
]


def rebuild_works():
    src = (BACKUP / "works.html").read_text(errors="replace")
    start_token = '<div fs-cmsfilter-element="list" role="list" class="works-list grid-layout w-dyn-items">'
    start = src.find(start_token)
    inner = start + len(start_token)
    marker = '</section><article class="u--relative">'
    end = src.find(marker, start)
    k = end
    while src[k - 6 : k] == "</div>":
        k -= 6
    chunk = src[inner:k]
    parts = re.split(r'(?=<div role="listitem" class="work column w-dyn-item">)', chunk)
    orig = [trim_card(p) for p in parts if '<div role="listitem" class="work column w-dyn-item">' in p]
    if len(orig) < 5:
        raise SystemExit(f"expected original cards, got {len(orig)}")

    # original extra filter button template (Products)
    form = re.search(r'<form[^>]*class="works-filter_list".*?</form>', src, re.S).group(0)
    item_m = re.search(
        r'(<div role="listitem" class="w-dyn-item"><label class="filter-button w-radio">.*?</label></div>)',
        form,
        re.S,
    )
    item_tpl = item_m.group(1)

    def make_filter(fid, heading, field):
        block = item_tpl
        block = block.replace('id="radio"', f'id="{fid}"', 1)
        block = re.sub(r"<h4>.*?</h4>", f"<h4>{heading}</h4>", block, count=1)
        block = re.sub(
            r'(<span fs-cmsfilter-field="category" class="h4 hidden w-form-label" for=")[^"]+("[^>]*>)[^<]*',
            rf"\1{fid}\2{field}",
            block,
            count=1,
        )
        return block

    extras = "".join(make_filter(fid, heading, field) for fid, heading, field in FILTERS)
    src = re.sub(
        r'(<div role="list" class="works-filter_list w-dyn-items">).*?(</div></div></div></form>)',
        lambda m: m.group(1).split("w-dyn-items")[0] and None,
        src,
        count=1,
        flags=re.S,
    )
    # more reliable: replace inner of works-filter_list w-dyn-items
    src = re.sub(
        r'(<div role="list" class="works-filter_list w-dyn-items">).*?(</div></div></div></form>)',
        r"\1" + extras + r"</div></div></div></form>",
        src,
        count=1,
        flags=re.S,
    )
    # the regex above is wrong because group 1 is only the opening tag if I used \1 extras
    # Let me do it with a simpler find
    return src, orig, extras, start_token, inner, end, orig


def rebuild_works_clean():
    src = (BACKUP / "works.html").read_text(errors="replace")
    start_token = '<div fs-cmsfilter-element="list" role="list" class="works-list grid-layout w-dyn-items">'
    start = src.find(start_token)
    inner = start + len(start_token)
    marker = '</section><article class="u--relative">'
    end = src.find(marker, start)
    # Do not walk back through </div> — that ate the last card and collapsed the grid.
    chunk = src[inner:end]
    parts = re.split(r'(?=<div role="listitem" class="work column w-dyn-item">)', chunk)
    orig = [trim_card(p) for p in parts if '<div role="listitem" class="work column w-dyn-item">' in p]

    form_inner_start = src.find('<div role="list" class="works-filter_list w-dyn-items">')
    form_inner_open = src.find(">", form_inner_start) + 1
    form_inner_end = src.find("</div></div></div></form>", form_inner_start)
    item_tpl = re.search(
        r'<div role="listitem" class="w-dyn-item"><label class="filter-button w-radio">.*?</label></div>',
        src[form_inner_open:form_inner_end],
        re.S,
    ).group(0)

    def make_filter(fid, heading, field):
        block = item_tpl
        block = block.replace('id="radio"', f'id="{fid}"', 1)
        block = re.sub(r"<h4>.*?</h4>", f"<h4>{heading}</h4>", block, count=1)
        block = re.sub(
            r'(for=")radio("[^>]*>)[^<]*',
            rf"\1{fid}\2{field}",
            block,
            count=1,
        )
        return block

    extras = "".join(make_filter(fid, heading, field) for fid, heading, field in FILTERS)
    src = src[:form_inner_open] + extras + src[form_inner_end:]

    # re-find list after filter splice (offsets may shift)
    start = src.find(start_token)
    inner = start + len(start_token)
    end = src.find(marker, start)

    cards = []
    projects = project_list()
    for i, proj in enumerate(projects):
        cards.append(retarget(orig[i % len(orig)], proj))

    # Original Cosmos: each card ends with 5 </div>, then 4 wrappers
    # (list, column, track, section inner) before </section>.
    src = src[:inner] + "".join(cards) + "</div></div></div></div>" + src[end:]

    arrow = """
<style>
.filter-button.is--active .h4::before,
.filter-button.is--active h4::before {
  content: ">";
  display: inline-block;
  margin-right: 0.4em;
}
.line-divider.cc--filter { margin-bottom: 2px !important; }
.works.column.w-dyn-list,
.works-list.grid-layout {
  padding-top: 2px;
  margin-top: 0;
}
</style>
<script>
window.addEventListener("load", function () {
  setTimeout(function () {
    document.querySelectorAll(".work, .filter-button, .line-divider").forEach(function (el) {
      if (parseFloat(getComputedStyle(el).opacity) < 0.05) el.style.opacity = "1";
    });
  }, 2800);
});
</script>
"""
    if "content: \">\"" not in src:
        src = src.replace("</head>", arrow + "</head>", 1)
    if "js/local-nav.js" not in src:
        src = src.replace("</head>", '<script src="js/local-nav.js"></script>\n</head>', 1)
    if "js/globe-sa.js" not in src:
        src = src.replace("</head>", '<script src="js/globe-sa.js"></script>\n</head>', 1)

    (ROOT / "works.html").write_text(src)
    print("works cards", len(cards), "orig templates", len(orig))
    print("academia", "projects/academia.html" in src)
    print("sportfaction name", "Sportfaction" in src)


def brand_html(text: str) -> str:
    protected = []

    def stash(m):
        protected.append(m.group(0))
        return f"@@P{len(protected)-1}@@"

    # Stash srcset first, then remaining URLs. Nested @@P tokens in srcset
    # were never restored and broke cover images / card alignment.
    text = re.sub(r"srcset=\"[^\"]+\"", stash, text)
    text = re.sub(r"https?://[^\"'\s<]+", stash, text)

    text = text.replace("Cosmos Studio", "LulaSync")
    text = text.replace("Cosmos UX/UI Studio", "LulaSync")
    text = re.sub(r"\bCosmos\b", "LulaSync", text)

    text = text.replace("KYIV", "Jo'burg")
    text = text.replace("Kyiv,<br/>Ukraine", "Jo'burg,<br/>ZA")
    text = text.replace("Kyiv, Ukraine", "Jo'burg, ZA")
    text = text.replace("Kyiv", "Jo'burg")
    text = re.sub(r"\bUkraine\b", "ZA", text)

    text = re.sub(r"(?i)since 2018", "since 2017", text)
    text = text.replace("2018–", "2017–")
    text = text.replace("© 2018", "© 2017")

    text = re.sub(r"\$(\d)", r"R\1", text)

    text = text.replace("We help", "I help")
    text = text.replace("we help", "I help")
    text = text.replace("We specialize", "I specialize")
    text = text.replace("we specialize", "I specialize")
    text = text.replace("We believe", "I believe")
    text = text.replace("We love", "I love")
    text = text.replace("We do", "I do")
    text = text.replace(">We do<", ">I do<")
    text = text.replace("Our big dream", "My big dream")
    text = text.replace("How can we contact", "How can I contact")
    text = text.replace("so we can address", "so I can address")
    text = text.replace("We’ll contact", "I'll contact")
    text = text.replace("We'll contact", "I'll contact")
    text = text.replace("We are a", "I am a")
    text = text.replace("we're a", "I am a")

    for i in range(len(protected) - 1, -1, -1):
        text = text.replace(f"@@P{i}@@", protected[i])
    while "@@P" in text:
        changed = False
        for i, val in enumerate(protected):
            token = f"@@P{i}@@"
            if token in text:
                text = text.replace(token, val)
                changed = True
        if not changed:
            break
    return text


def social_hashes(text: str) -> str:
    # Keep split-type / rounded / class markup. href="#" with target=_blank
    # opened a blank tab and looked broken. Drop only the target on those links.
    def repl(m):
        before, after = m.group(1), m.group(2)
        after = re.sub(r'\s*target="_blank"', "", after, flags=re.I)
        after = re.sub(r'\s*rel="noopener[^"]*"', "", after, flags=re.I)
        return f"{before}href=\"#\"{after}"

    text = re.sub(
        r'(<a\b[^>]*?)href="https?://(?:www\.)?(?:linkedin\.com|behance\.net|instagram\.com|facebook\.com)[^"]*"([^>]*)',
        repl,
        text,
        flags=re.I,
    )
    return text


def point_globe_south_africa(text: str) -> str:
    text = text.replace("50° 27&#x27; 0.0036&#x27;&#x27; N", "26° 12&#x27; 16&#x27;&#x27; S")
    text = text.replace("30° 31&#x27; 23.9988&#x27;&#x27; E", "28° 2&#x27; 44&#x27;&#x27; E")
    text = text.replace("50° 27' 0.0036'' N", "26° 12' 16'' S")
    text = text.replace("30° 31' 23.9988'' E", "28° 2' 44'' E")
    return text


def apply_sitewide():
    n = 0
    for p in ROOT.rglob("*.html"):
        if p.name.startswith("_"):
            continue
        t = p.read_text(errors="replace")
        t2 = brand_html(t)
        if t2 != t:
            p.write_text(t2)
            n += 1
    print("branded files", n)


if __name__ == "__main__":
    rebuild_works_clean()
    apply_sitewide()
    # keep works/index redirect
    (ROOT / "works").mkdir(exist_ok=True)
    (ROOT / "works" / "index.html").write_text(
        '<!DOCTYPE html><html><head><meta charset="utf-8"/><script>location.replace("../works.html");</script>'
        '<meta http-equiv="refresh" content="0;url=../works.html"/></head><body><a href="../works.html">Works</a></body></html>\n'
    )
