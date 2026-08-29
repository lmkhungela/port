#!/usr/bin/env python3
"""Replace Cosmos case studies with LulaSync work, keep Cosmos chrome."""
from __future__ import annotations

import html
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTFOLIO = Path("/Users/lulamile.mkhungela/Documents/AI-team repositories/portfolio")
ASSETS = ROOT / "assets"

CORNER = '''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 31 31" fill="none" class="corner third"><g filter="url(#filter0_d_8375_688)"><path d="M7 6V20H21" stroke="currentColor" stroke-width="1.5"></path></g><defs><filter id="filter0_d_8375_688" x="0.25" y="0" width="30.75" height="30.75" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB"><feFlood flood-opacity="0" result="BackgroundImageFix"></feFlood><feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"></feColorMatrix><feOffset dx="4" dy="5"></feOffset><feGaussianBlur stdDeviation="5"></feGaussianBlur><feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"></feColorMatrix><feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_8375_687"></feBlend><feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_8375_687" result="shape"></feBlend></filter></defs></svg>'''

BRACKET_L = '''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 6 16" fill="none" class="filter-count_bracket"><path d="M0 8.336V7.344H0.464C0.912 7.344 1.232 7.232 1.424 7.008C1.616 6.77333 1.712 6.40533 1.712 5.904V2.928C1.712 2.02133 1.97333 1.30667 2.496 0.784C3.01867 0.261333 3.86133 0 5.024 0V0.544001C4.33067 0.565334 3.81867 0.778667 3.488 1.184C3.15733 1.57867 2.992 2.208 2.992 3.072V6.08C2.992 6.976 2.58133 7.53067 1.76 7.744V7.936C2.58133 8.14933 2.992 8.704 2.992 9.6V12.608C2.992 13.472 3.15733 14.1013 3.488 14.496C3.81867 14.9013 4.33067 15.1147 5.024 15.136V15.68C3.86133 15.68 3.01867 15.4187 2.496 14.896C1.97333 14.3733 1.712 13.6587 1.712 12.752V9.776C1.712 9.27467 1.616 8.912 1.424 8.688C1.232 8.45333 0.912 8.336 0.464 8.336H0Z" fill="currentColor"></path></svg>'''
BRACKET_R = '''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 6 16" fill="none" class="filter-count_bracket"><path d="M4.56 8.336C4.112 8.336 3.792 8.45333 3.6 8.688C3.408 8.912 3.312 9.27467 3.312 9.776V12.752C3.312 13.6587 3.05067 14.3733 2.528 14.896C2.00533 15.4187 1.16267 15.68 0 15.68V15.136C0.693333 15.1147 1.20533 14.9013 1.536 14.496C1.86667 14.1013 2.032 13.472 2.032 12.608V9.6C2.032 8.704 2.44267 8.14933 3.264 7.936V7.744C2.44267 7.53067 2.032 6.976 2.032 6.08V3.072C2.032 2.208 1.86667 1.57867 1.536 1.184C1.20533 0.778667 0.693333 0.565334 0 0.544001V0C1.16267 0 2.00533 0.261333 2.528 0.784C3.05067 1.30667 3.312 2.02133 3.312 2.928V5.904C3.312 6.40533 3.408 6.77333 3.6 7.008C3.792 7.232 4.112 7.344 4.56 7.344H5.024V8.336H4.56Z" fill="currentColor"></path></svg>'''

ARROW = '''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 34 24" fill="none" class="button_arrow cc--small"><path d="M0 12H34M34 12C29.7911 12 21.8994 11.687 21.8994 0M34 12C29.7911 12 21.8994 12.313 21.8994 24" stroke="currentColor" stroke-width="2"></path></svg>'''


def stylize(title: str) -> str:
    letters = list(title)
    if len(letters) >= 2:
        letters[1] = f"<strong>{html.escape(letters[1])}</strong>"
        letters[0] = html.escape(letters[0])
        rest = "".join(html.escape(ch) if i > 1 else ch for i, ch in enumerate(letters))
        # rebuild properly
        out = []
        for i, ch in enumerate(title):
            if i == 1:
                out.append(f"<strong>{html.escape(ch)}</strong>")
            else:
                out.append(html.escape(ch))
        return "".join(out)
    return html.escape(title)


PROCESS = [
    ("01", "Discover", "Interviews, empathy maps, personas and competitive research. Find the real problem before designing the visible one."),
    ("02", "Define", "User research, requirement analysis, information architecture and stakeholder meetings."),
    ("03", "Ideate", "How-might-we, paper wireframes, user flows, sitemaps and crazy eights."),
    ("04", "Design", "Hi-fi mockups, interactive prototypes, user testing and iterations."),
    ("05", "Test", "User testing, result summary, and a defined next step."),
]


CASE_STUDIES = [
    {
        "slug": "academia",
        "title": "Academia",
        "year": "2024",
        "services": ["UI/UX", "Product Design"],
        "tags": "UI/UX, Product Design, EdTech",
        "category": "case-studies",
        "cover": "assets/academia-cover.webp",
        "site_label": "Behance — GoLearn",
        "site_url": "https://www.behance.net/gallery/184372861/GoLearn-An-Online-Educational-UX-Design-Case-Study",
        "about": "Academia (GoLearn) is an online learning platform that combines courses with Student Relationship Management so learners and educators share one product instead of a fragmented admin and classroom.",
        "role": "Lead UX/UI Designer. UX/UI design, user research, design system, wireframes, interactive prototype, information architecture and user flow.",
        "challenge": "Learners and educators needed a user-friendly interface, course integration, SRM tools, interactive learning and secure data — without splitting student and admin into two disconnected products.",
        "solution": "The GoLearn case study process: research and interviews, competitive analysis, personas, journey mapping, information architecture, ideation, wireframes, hi-fi UI, interactive prototype and usability testing, then iteration on navigation, search and course progress.",
        "images": [
            "assets/academia-cover.webp",
            "assets/academia-01.webp",
            "assets/academia-02.webp",
            "assets/academia-03.webp",
            "assets/academia-04.webp",
            "assets/academia-process.webp",
        ],
        "story": [
            (
                "Research",
                [
                    "The GoLearn case study starts with the people who study and teach online: interviews, competitor analysis, personas and journey maps before any high-fidelity UI.",
                    "Goals included daily active use, time on courses, forum activity, certifications, NPS and satisfaction — not only a prettier course list.",
                ],
                "assets/academia-process.webp",
            ),
            (
                "Define & Ideate",
                [
                    "Requirements and information architecture split learner, educator and SRM paths so registration, analytics, tasks and courses sit in one mental model.",
                    "How-might-we, paper wireframes, user flows and sitemaps reduced the number of places a user had to go to start a lesson or check a student.",
                ],
                "assets/academia-01.webp",
            ),
            (
                "Design & Test",
                [
                    "Hi-fi mockups and an interactive prototype were tested for navigation quality, visual hierarchy and whether progress and certifications were obvious.",
                    "Findings fed the next iteration: clearer course structure, stronger SRM cues, and less friction between learning and administration.",
                ],
                "assets/academia-02.webp",
            ),
        ],
        "next": "onli-pay",
    },
    {
        "slug": "onli-pay",
        "title": "Onli-Pay",
        "year": "2024",
        "services": ["UI/UX", "Product Design"],
        "tags": "UI/UX, Product Design, Fintech",
        "category": "case-studies",
        "text_only": True,
        "cover": "assets/onli-pay-cover.webp",
        "site_label": "Behance — SwiftPay / Onli-Pay",
        "site_url": "https://www.behance.net/gallery/187334383/SwiftPay-Banking-App-A-Comprehensive-Case-Study",
        "about": "Onli-Pay is an online banking application designed to give individuals and businesses a seamless, secure way to manage money in South African Rand — balances, cards, savings, loans, payments and insights in one product.",
        "role": "UX/UI Designer. UX/UI design, user research, design system, wireframes, interactive prototype and user flow. First iteration, in progress toward a fifth.",
        "challenge": "Users struggled to tell accounts apart, follow payments, track savings and loans, and stay confident about security. The product also had to work in light and dark mode, meet contrast needs, and stay usable for colour-blind users.",
        "solution": "A research-led process: interviews with 35 participants, personas, joint-account scenarios, user flows and journey maps, hi-fi wireframes, a Figma prototype for light and dark mode (320+ screens), usability testing, then targeted UX fixes and an accessibility pass.",
        "images": [],
        "story": [
            (
                "Project Overview",
                [
                    "Onli-Pay (published as SwiftPay on Behance) is a comprehensive UX/UI case study for an online banking application: a user-friendly interface, advanced features and robust security for individuals and businesses managing money in South African Rand.",
                    "Role: UX/UI Designer. Responsibility: UX/UI design, user research, design system, wireframes, interactive prototype and user flow. First iteration, in progress toward a fifth.",
                    "Goals. A. User interface: enhance experience, surveys and feedback, intuitive design, seamless navigation. B. Accessibility: compatibility across devices, users with disabilities, usability testing. C. Account integration: financial institutions, synchronised account data, partnerships. D. Advanced budgeting: personalised insights and goal tracking. E. Payment flexibility: digital wallets and streamlined bill pay.",
                    "Scope: Research (interviews, empathy map, personas, customer journey map, competitive research) → Ideation (how-might-we, paper wireframes, userflows, sitemap, crazy eights) → Prototype (hi-fi, interactive prototype, user testing, adjustment) → Visual design (conception, all layouts, design systems, mobile) → User testing, with a loop back into prototype.",
                ],
                None,
            ),
            (
                "Understanding the Users",
                [
                    "Research methods: interviews, competitor analysis, user personas and a user journey map. The goal of interviews was to connect with end users, understand their needs, and inform an interface that meets and exceeds expectations.",
                    "35 participants were invited. 27 responded and 8 did not. Interviews were one-on-one and virtual. Each person received a R100 Takealot voucher at the end of the session.",
                    "Process. Participant selection: a diverse group across familiarity with online banking and financial needs. Questionnaire: open-ended questions tied to project goals. Conducting interviews: scheduled virtual sessions, interpersonal probing for honest stories. Observations: body language, facial expression, and follow-up on specific topics.",
                ],
                None,
            ),
            (
                "Pain Points & Personas",
                [
                    "Surveys and interviews with people who already use mobile banking surfaced navigation complexity, security-feature clarity, and the need for clearer shared-money tools.",
                    "Pain point A — navigation: Juliet Kuezi (student) wanted a simpler layout; Cori Ndlela spent too long searching for a feature. Pain point B — security: Richard Williams wanted fingerprint or Face ID; Sarah Sana wanted two-factor authentication for certain transactions.",
                    "Samantha (24, freelance): needs a fast, clear UI; pain is complex navigation. Alex (32): values privacy; needs multi-factor authentication and activity notifications.",
                    "Joint account: Sarah and Cori, siblings in their 30s and 40s, share household expenses and savings. They need a shared dashboard, joint goals, and real-time notifications on joint-account activity.",
                ],
                None,
            ),
            (
                "Ideation & Prototyping",
                [
                    "Features were defined from research, then sketched: navigation, transaction history and account details, with arrows for user flow and standardised buttons and icons.",
                    "User flow: Onli-Pay splits into User Onboarding (sign up with email, phone, password; personal information; upload ID, licence or utility bill; account overview) and Dashboard (payment, manage accounts, profile, customer support). Payments include send money and pay bills (utilities, internet, electricity, water).",
                    "Journey map stages: Login, Dashboard, Make a Payment, Expense Tracking, Savings, Loan Tracking, Logout — with user action, app interaction, touchpoints and emotional experience on each.",
                ],
                None,
            ),
            (
                "Wireframes, Prototype & Visual Design",
                [
                    "Notebook sketches became clickable high-fidelity wireframes so every intended element could be tested with end-user feedback: home (total balance in Rand), passcode login, spending insights, credit score, savings, payments and onboarding with +27.",
                    "The Figma prototype turned wireframes into an interactive UI for light mode and dark mode. Light mode is for well-lit, easy-to-read use; users can switch to dark mode. 320+ screens were designed. After learning that many iPhone users prefer dark mode, Figma colour variables made the switch automatic.",
                    "Launching the app: security-first onboarding (proof of residence, passport or licence), passcode and Face ID. Home shows every account without extra swipes, monthly spending versus last month, savings and credit, plus Apple Pay / Google Pay. Loans: repayment progress and history. Credit score: gauge, factors, improvement tips. Help: search, FAQs and live chat.",
                ],
                None,
            ),
            (
                "Solving UX Problems",
                [
                    "Different account display: the old summary hid per-account balances. The main page now lists all accounts with a uniform data flow.",
                    "Savings: simplified layout, visible information and clearer icons.",
                    "Payments: users can see and select the source account at every stage, with a visual indicator on Pay Now.",
                    "Recent payments: vertical scroll of favourite transfers instead of a confusing horizontal row, with source account visible.",
                    "Loans: emphasised day-of-month progress, amount paid and remaining months.",
                ],
                None,
            ),
            (
                "Usability Testing & Accessibility",
                [
                    "Remote usability study (Miro, UserTesting): objective to evaluate UI/UX; participants across ages 20–55; remote via Teams/Zoom. KPIs included task success (aim 90%+), time on task, and satisfaction (aim 4.5+).",
                    "Testing areas: navigation and information quality, visual design, efficiency, ease of use, overall satisfaction. Insights included clearer navigation prompts, guided search/filters, authentication updates, login screen, pending transactions, and premium fee transparency.",
                    "Accessibility: contrast check so balances are readable; colour-blindness check so meaning is not colour-only; palettes (blue, red, green, yellow, dark blue/grey) aligned with the brand.",
                ],
                None,
            ),
        ],
        "next": "ridemelo",
    },
    {
        "slug": "ridemelo",
        "title": "RideMelo",
        "year": "2024",
        "services": ["UI/UX", "Product Design"],
        "tags": "UI/UX, Product Design, Mobility",
        "category": "case-studies",
        "cover": "assets/ridemelo-cover.webp",
        "site_label": "Behance — Ride-hailing",
        "site_url": "https://www.behance.net/gallery/199542731/Ride-Hailing-Services-Case-Study",
        "about": "RideMelo is a ride-hailing product designed around two sides of the same trip: riders who need price transparency and safety, and drivers who need clear earnings and safer pickups. The Behance case study (PickMe) used research, personas, journey maps, wireframes, hi-fi mockups and tested prototypes.",
        "role": "UX/UI Designer. Design process from Discover through Test, with interviews on both sides of the marketplace.",
        "challenge": "Riders reported unexpected surcharges, fare discrepancies, and feeling unsafe with reckless driving or missing in-app safety features. Drivers reported opaque earnings (fares, incentives, deductions) and safety risks with unruly passengers or unsafe locations, especially at night.",
        "solution": "Discover (interviews, empathy map, personas, competitive research) → Define → Ideate → Design → Test. Accessibility work included high-contrast colour and non-colour cues for colour-blind users. Recommendations included push notifications for driver arrival and destination alerts. Interview work included riders Aisha Mohamed and Munachi Uche, and drivers Emeka Nwasu and Tunde Ndlela.",
        "images": [
            "assets/ridemelo-cover.webp",
            "assets/ridemelo-01.webp",
            "assets/ridemelo-02.webp",
            "assets/ridemelo-03.webp",
            "assets/ridemelo-04.webp",
            "assets/ridemelo-process.webp",
        ],
        "story": [
            (
                "Two-sided research",
                [
                    "Riders wanted upfront fares, fewer surprise charges, and in-app safety they could actually find. Drivers wanted earnings they could explain and pickups they trusted after dark.",
                    "Personas and empathy maps kept both jobs visible in every flow: request a ride, match, trip, pay, rate — and the driver equivalent for accept, navigate, complete, cash out.",
                ],
                "assets/ridemelo-process.webp",
            ),
            (
                "Ideate & Design",
                [
                    "How-might-we, paper wireframes, user flows and a sitemap defined rider and driver IA before hi-fi.",
                    "Hi-fi and an interactive prototype made fare breakdown, SOS, trip sharing and driver earnings visible instead of buried in settings.",
                ],
                "assets/ridemelo-01.webp",
            ),
            (
                "Test & next step",
                [
                    "Usability testing checked whether riders could predict the price before confirming, and whether drivers could see why a payout was what it was.",
                    "Next step: iterate safety entry points and overnight pickup guidance without adding steps to a normal daytime trip.",
                ],
                "assets/ridemelo-02.webp",
            ),
        ],
        "next": "academia",
    },
]


def work_card(href, img, tags, year, title, category, extra=""):
    target = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
    return (
        f'<div role="listitem" class="work column w-dyn-item" data-category="{category}">'
        f'<a href="{href}" class="case-wrapper w-inline-block"{target}>'
        f'<div class="case-img cc--works"><div class="case-element"><div class="case-blur"></div>'
        f'<img src="{img}" loading="eager" alt="{html.escape(title)}" class="case-embed"/>'
        f"</div></div>"
        f'<div class="case-text cc--works"><div class="flex-sides">'
        f'<div class="additional-text">{html.escape(tags)}</div>'
        f'<div class="additional-text case-year">{html.escape(year)}</div></div>'
        f'<h3 class="p-large">{html.escape(title)}</h3>{CORNER}</div></a>'
        f'<div class="category-counter w-dyn-list"><div role="list" class="w-dyn-items">'
        f'<div role="listitem" class="w-dyn-item"><div fs-cmsfilter-field="category" class="category-counter_text">{html.escape(category)}</div></div>'
        f"</div></div></div>"
    )


def filter_btn(fid, label_html, value, active=False):
    cls = "filter-button all is--active w-radio" if active else "filter-button w-radio"
    count_cls = "filter-count_all-works" if value == "all" else "filter-count"
    checked = ' checked=""' if active else ""
    return (
        f'<div role="listitem" class="w-dyn-item"><label class="{cls}" data-filter="{value}">'
        f'<input type="radio" name="category" id="{fid}" data-name="category" class="w-form-formradioinput hidden w-radio-input" value="{value}"{checked}/>'
        f'<div class="rt white-space w-richtext"><h4>{label_html}</h4></div>'
        f'<span fs-cmsfilter-field="category" class="h4 hidden w-form-label" for="{fid}">{value}</span>'
        f'<div class="filter-count_wr">{BRACKET_L}<div class="additional-text {count_cls}">0<br/></div>{BRACKET_R}</div>'
        f"</label></div>"
    )


def img_tag(src, extra_class="image full-screen"):
    return f'<img src="{src}" loading="eager" alt="" class="{extra_class}"/>'


def story_sections(cs, prefix="../"):
    blocks = []
    order = 4
    for heading, paragraphs, image in cs.get("story") or []:
        paras = "".join(f"<p>{html.escape(p)}</p>" if not p.startswith("<") else p for p in paragraphs)
        blocks.append(
            f'<section order="{order}" class="section"><div class="project-container container">'
            f'<div class="about-section grid-layout"><div class="about-title column"><div class="rt w-richtext">'
            f"<h2>{stylize(heading)}</h2></div></div>"
            f'<div class="about-text column"><div class="rt w-richtext">{paras}</div></div></div></div></section>'
        )
        order += 1
        if image:
            blocks.append(
                f'<section order="{order}" class="section"><div>{img_tag(prefix + image, "image full-screen")}</div></section>'
            )
            order += 1
    return "".join(blocks)


def build_project_body(cs, prefix="../"):
    services = "".join(
        f'<div role="listitem" class="w-dyn-item"><div class="p-small">{html.escape(s)}</div></div>'
        for s in cs["services"]
    )
    cover = prefix + cs["cover"]
    process_steps = "".join(
        f"<h4><strong>{num}</strong> {html.escape(name)}</h4><p>{html.escape(blurb)}</p>"
        for num, name, blurb in PROCESS
    )
    grid_imgs = "".join(
        f'<div role="listitem" class="grid-image w-dyn-item w-dyn-repeater-item">{img_tag(prefix + src, "image cc--grid")}</div>'
        for src in cs["images"][1:]
    )
    nxt = cs["next"]
    nxt_title = next(x["title"] for x in CASE_STUDIES if x["slug"] == nxt)
    story = story_sections(cs, prefix)
    return f'''<div class="page-wrapper"><section class="section"><div class="container cc--secondary"><div class="project-header grid-layout"><div class="project-title column"><div carousel-general="on" split-type="on" carousel="on" class="rt-heading w-richtext"><h1>{stylize(cs["title"])}</h1></div></div><div class="project-year column"><div class="p-small">{cs["year"]}</div></div><div class="project-info column grid-layout"><div class="project-services column w-dyn-list"><div role="list" class="w-dyn-items">{services}</div></div><div class="project-site column"><div class="u--hide_mobile"><div class="p-small title-wrapper">{html.escape(cs["site_label"])}</div></div><div><div class="u--hide_mobile"><a href="{html.escape(cs["site_url"])}" target="_blank" rel="noopener noreferrer" class="button cc--small w-inline-block"><div class="button_flex cc--small"><div class="button-text_wr"><div class="button-text">open figma</div></div>{ARROW}</div></a></div><div class="u--hide-desktop"><a href="{html.escape(cs["site_url"])}" target="_blank" rel="noopener noreferrer" class="p-small">{html.escape(cs["site_label"])}</a></div></div></div></div></div><div>{img_tag(cover, "image full-screen cc--cover")}</div></div></section><div class="w-dyn-list"><div role="list" class="w-dyn-items"><div role="listitem" class="section-order w-dyn-item"><section order="1" class="section"><div class="project-container container"><div class="about-section grid-layout"><div class="about-title column"><div class="rt w-richtext"><h2>Abo<strong>ut</strong></h2></div></div><div class="about-text column"><div class="rt w-richtext"><h3>{html.escape(cs["about"])}</h3><p>{html.escape(cs["role"])}</p><h4><strong>C</strong>HALL<strong>E</strong>NGE</h4><p>{html.escape(cs["challenge"])}</p><h4><strong>S</strong>OL<strong>U</strong>TION</h4><p>{html.escape(cs["solution"])}</p></div></div></div></div></section><section order="2" class="section"><div class="project-container container"><div class="about-section grid-layout"><div class="about-title column"><div class="rt w-richtext"><h2>Pro<strong>c</strong>ess</h2></div></div><div class="about-text column"><div class="rt w-richtext"><h3>Design Process</h3><p>From the Figma case study: Discover, Define, Ideate, Design, Test.</p>{process_steps}</div></div></div></div></section><section order="3" class="section"><div class="project-container container"><div role="list" class="project_image-grid cc--no-wrap w-dyn-items">{grid_imgs}</div></div></section>{story}</div></div></div><section class="section cc--clipx"><div class="project-container container"><div class="next-case"><div class="nex-case_wr"><a href="{nxt}.html" class="case-wrapper w-inline-block"><div class="additional-text">Next case</div><h2 class="p-large">{html.escape(nxt_title)}</h2></a></div></div></div></section></div>'''


def inject_scripts(html_text: str, extra_srcs: list[str], relative: str) -> str:
    for src in extra_srcs:
        tag = f'<script src="{relative}{src}"></script>'
        if src.split("/")[-1] in html_text:
            continue
        html_text = html_text.replace("</head>", f"{tag}\n</head>", 1)
    return html_text


def placeholder_svg(path: Path, label: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">
  <rect fill="#111" width="1600" height="1000"/>
  <rect fill="#1c1c1c" x="40" y="40" width="1520" height="920"/>
  <text x="80" y="520" fill="#c8c8c8" font-family="Georgia, serif" font-size="48">{html.escape(label)}</text>
  <text x="80" y="580" fill="#666" font-family="sans-serif" font-size="22">{html.escape(path.name)}</text>
</svg>'''
    # store as svg even if requested name is png/webp so the file exists; user will replace
    if path.suffix.lower() in {".svg"}:
        path.write_text(svg)
        return
    path.write_bytes(svg.encode("utf-8"))


ASSET_FILES = {
    "academia-cover.webp": "Academia cover",
    "academia-01.webp": "Academia 01",
    "academia-02.webp": "Academia 02",
    "academia-03.webp": "Academia 03",
    "academia-04.webp": "Academia 04",
    "academia-process.webp": "Academia process",
    "onli-pay-cover.webp": "Onli-Pay cover",
    "onli-pay-01.webp": "Onli-Pay 01",
    "onli-pay-02.webp": "Onli-Pay 02",
    "onli-pay-03.webp": "Onli-Pay 03",
    "onli-pay-04.webp": "Onli-Pay 04",
    "onli-pay-process.webp": "Onli-Pay process",
    "ridemelo-cover.webp": "RideMelo cover",
    "ridemelo-01.webp": "RideMelo 01",
    "ridemelo-02.webp": "RideMelo 02",
    "ridemelo-03.webp": "RideMelo 03",
    "ridemelo-04.webp": "RideMelo 04",
    "ridemelo-process.webp": "RideMelo process",
    "foodiezone.png": "FoodieZone",
    "king-cutter.png": "King Cutter",
    "africa-cuisine.png": "Africa Cuisine",
    "sk-auto.png": "SK Auto Emporium",
    "wandies.png": "Wandies",
    "servicewaze.webp": "ServiceWaze",
    "westudysync-cover.svg": "WeStudySync",
    "coming.png": "LulaUnifidMarket",
    "design-ops.png": "DesignOps dashboard",
    "design-op.png": "Meridian design system",
    "figma.png": "Collection of projects",
    "ux-resources.png": "UX resource library",
    "snb.webp": "SNB Website",
    "nerdma.png": "Nerdma",
    "addmore.png": "Add More Digital",
    "fitness-studio.jpg": "Fitness Studio",
    "hosdo.png": "Hosdo",
    "explora.jpg": "Explora",
    "studyzel.jpg": "Studyzel",
    "hack.png": "Retail Hackathon",
    "farmers-funding.webp": "AgriTech Hackathon",
    "hacky.webp": "GBV Hackathon",
    "ui-neo-banking.webp": "Neo Banking App",
    "ui-investment-dashboard.webp": "Investment Dashboard",
    "ui-trading-operations.webp": "Trading Operations",
    "ui-auto-claims.webp": "Auto Claims",
    "ui-policy-portal.webp": "Policy Management",
    "ui-virtual-doctor.webp": "Virtual Doctor",
    "ui-hospital-command.webp": "Hospital Command Center",
    "ui-patient-records-admin.webp": "Patient Records Admin",
    "ui-fashion-marketplace.webp": "Fashion Marketplace",
    "ui-b2b-marketplace.webp": "B2B Marketplace",
    "ui-retail-intelligence.webp": "Retail Intelligence",
    "ui-connected-vehicle.webp": "Connected Vehicle",
    "ui-fleet-operations.webp": "Fleet Operations",
    "ui-smart-hotel.webp": "Smart Hotel",
    "ui-restaurant-hub.webp": "Restaurant Hub",
    "ui-travel-operations.webp": "Travel Operations",
    "ui-driver-companion.webp": "Driver Companion",
    "ui-warehouse-command.webp": "Warehouse Command",
    "ui-study-companion.webp": "Study Companion",
    "ui-campus-lms.webp": "Campus LMS",
    "ui-school-management.webp": "School Management",
    "ui-property-explorer.webp": "Property Explorer",
    "ui-property-manager.webp": "Property Manager Pro",
    "ui-employee-hub.webp": "Employee Hub",
    "ui-workforce-analytics.svg": "Workforce Analytics",
    "ui-production-control.webp": "Production Control",
    "ui-factory-floor.webp": "Factory Floor",
    "ui-project-orchestrator.webp": "Project Orchestrator",
    "ui-sales-pipeline.webp": "Sales Pipeline Pro",
    "ui-marketing-automation.webp": "Marketing Automation",
    "ui-citizen-services.webp": "Citizen Services",
    "ui-smart-city.webp": "Smart City",
}

UI_ITEMS = [
    ("ui-neo-banking.webp", "Neo Banking App", "Mobile · Card Controls · Instant Transfers"),
    ("ui-investment-dashboard.webp", "Investment Dashboard", "Web Platform · Portfolio Analytics"),
    ("ui-trading-operations.webp", "Trading Operations", "Admin Dashboard · Order Management"),
    ("ui-auto-claims.webp", "Auto Claims", "Mobile App · Photo Claims"),
    ("ui-policy-portal.webp", "Policy Management", "Web Portal · Premium Calculator"),
    ("ui-virtual-doctor.webp", "Virtual Doctor", "Mobile App · Video Consultations"),
    ("ui-hospital-command.webp", "Hospital Command Center", "Web Dashboard · Bed Management"),
    ("ui-patient-records-admin.webp", "Patient Records Admin", "Admin Panel · EMR"),
    ("ui-fashion-marketplace.webp", "Fashion Marketplace", "Mobile App · AR Try-On"),
    ("ui-b2b-marketplace.webp", "B2B Marketplace", "Web Platform · Vendor Management"),
    ("ui-retail-intelligence.webp", "Retail Intelligence", "Admin Dashboard · Sales Analytics"),
    ("ui-connected-vehicle.webp", "Connected Vehicle", "Mobile App · Remote Start"),
    ("ui-fleet-operations.webp", "Fleet Operations", "Web Dashboard · Route Optimization"),
    ("ui-smart-hotel.webp", "Smart Hotel", "Mobile App · Contactless Check-in"),
    ("ui-restaurant-hub.webp", "Restaurant Hub", "Web Platform · Table Management"),
    ("ui-travel-operations.webp", "Travel Operations", "Admin Dashboard · Booking Management"),
    ("ui-driver-companion.webp", "Driver Companion", "Mobile App · Proof of Delivery"),
    ("ui-warehouse-command.webp", "Warehouse Command", "Web Platform · Inventory Tracking"),
    ("ui-study-companion.webp", "Study Companion", "Mobile App · Interactive Lessons"),
    ("ui-campus-lms.webp", "Campus LMS", "Web Platform · Course Builder"),
    ("ui-school-management.webp", "School Management", "Admin Dashboard · Student Records"),
    ("ui-property-explorer.webp", "Property Explorer", "Mobile App · AR Property Tours"),
    ("ui-property-manager.webp", "Property Manager Pro", "Web Platform · Tenant Portal"),
    ("ui-employee-hub.webp", "Employee Hub", "Mobile App · Leave Requests"),
    ("ui-workforce-analytics.svg", "Workforce Analytics", "Web Platform · Recruitment"),
    ("ui-production-control.webp", "Production Control", "Web Dashboard · OEE Monitoring"),
    ("ui-factory-floor.webp", "Factory Floor", "Mobile App · Equipment Status"),
    ("ui-project-orchestrator.webp", "Project Orchestrator", "SaaS Platform · Collaboration"),
    ("ui-sales-pipeline.webp", "Sales Pipeline Pro", "SaaS Tool · Lead Management"),
    ("ui-marketing-automation.webp", "Marketing Automation", "SaaS Platform · Campaigns"),
    ("ui-citizen-services.webp", "Citizen Services", "Web Portal · Document Applications"),
    ("ui-smart-city.webp", "Smart City", "Mobile App · Public Transport"),
]

LIVE_APPS = [
    ("https://loux91.github.io/foodiezone/", "foodiezone.png", "FoodieZone", "Order + Delivery & Tracking"),
    ("https://king-cutter-s-royal-web.vercel.app/", "king-cutter.png", "King Cutter", "Bookings + WhatsApp"),
    ("https://africa-cuisine-pro.vercel.app/", "africa-cuisine.png", "Africa Cuisine", "Menu + delivery"),
    ("https://skautos.vercel.app/", "sk-auto.png", "SK Auto Emporium", "Quotes + bookings"),
    ("https://wandies.vercel.app/", "wandies.png", "Wandies", "Menu + WhatsApp orders"),
]

FE_BUILDS = [
    ("https://github.com/LulamileMkhungela/ServiceWaze", "servicewaze.webp", "ServiceWaze", "Offline-first Angular PWA"),
    ("https://github.com/LulamileMkhungela/WeStudySync", "westudysync-cover.svg", "WeStudySync", "APS, NSFAS, student tools"),
    ("https://github.com/LulamileMkhungela/LulaUnifidMarket", "coming.png", "LulaUnifidMarket", "Unified marketplace platform"),
]

FIGMA = [
    ("#", "design-ops.png", "DesignOps dashboard", "Token pipeline, drift and coverage"),
    ("https://www.figma.com/make/gkTm2bYYnzAmDBwWbWE7kb/Innovative-Design-System-Creation?t=871NF4mO6SlkhYAP-1", "design-op.png", "Meridian design system", "Figma · token graph and components"),
    ("https://www.figma.com/design/SeCP6cuxXX8UyhnOn2wYcJ/Collection-Of-Projects?node-id=8949-77053", "figma.png", "Collection of projects", "Figma · product UI and Angular screens"),
    ("https://chartreuse-scale-c4a.notion.site/Lula-Creatives-UX-Resources-Bookmarks-1e2962b93ef1809dbe07c896db79ad65", "ux-resources.png", "UX resource library", "Notion · bookmarks and templates"),
]

WEBSITES = [
    ("https://www.snbconsultancy.co.za/", "snb.webp", "SNB Website", "Web design"),
    ("https://www.nerdma.co.za/", "nerdma.png", "Nerdma", "Web design"),
    ("https://addmoredigital.co.za/", "addmore.png", "Add More Digital", "Web design"),
    ("#", "fitness-studio.jpg", "Fitness Studio", "Web design"),
    ("#", "hosdo.png", "Hosdo", "Web design"),
    ("#", "explora.jpg", "Explora", "Web admin experience"),
    ("#", "studyzel.jpg", "Studyzel", "Digital product surface"),
]

HACKS = [
    ("https://drive.google.com/file/d/1anSnYJt_4Okl3xQuCkCJDAVROcVOqEFr/view", "hack.png", "Retail Hackathon", "AI inventory with video analytics"),
    ("https://drive.google.com/file/d/19_dk5NRI_gJzYwyyR5kw_POwazmNhgp-/view", "farmers-funding.webp", "AgriTech Hackathon", "Farmers & co-op funding platform"),
    ("https://www.itweb.co.za/article/wethinkcode-female-developers-triumph-at-gbv-hackathon/KzQenMjVgjAMZd2r", "hacky.webp", "GBV Hackathon", "GBV hackathon — multi-platform solution"),
]

TEAM_KEEP = {
    "kulbachny.html",
    "hope-partners.html",
    "kyrylo-prytula.html",
    "edcamp.html",
    "zeuss.html",
    "acrode.html",
    "jessy-grossi.html",
    "umami-ware.html",
}

JUNK = [
    "a.html", "c.html", "Mc.html", "gtm.html", "analytics.html", "sw_iframe.html",
    "b.blockedURI.html", "e.path,w.location.origin.html",
]


def copy_or_placeholder(name: str, label: str):
    dest = ASSETS / name
    if dest.exists() and dest.stat().st_size > 200:
        return
    src = PORTFOLIO / "assets" / "portfolio" / name
    if src.exists() and src.stat().st_size > 200:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return
    placeholder_svg(dest, label)


def home_case(cs):
    return (
        f'<div role="listitem" class="case w-dyn-item">'
        f'<a href="projects/{cs["slug"]}.html" class="case-wrapper w-inline-block">'
        f'<div class="case-img"><div class="case-element"><div class="case-blur"></div>'
        f'<img src="{cs["cover"]}" loading="eager" alt="{html.escape(cs["title"])}" class="case-embed"/>'
        f"</div></div>"
        f'<div class="case-text"><div class="flex-sides">'
        f'<div class="additional-text">{html.escape(cs["tags"])}</div>'
        f'<div class="additional-text case-year">{cs["year"]}</div></div>'
        f'<h3 class="p-large">{html.escape(cs["title"])}</h3>{CORNER}</div></a></div>'
    )


def write_case_pages():
    edway = (ROOT / "projects" / "edway.html").read_text(errors="replace")
    chrome_head, rest = edway.split('<div class="page-wrapper">', 1)
    m = re.search(r'(<script[^>]+src="https://d3e54v103j8qbb\.cloudfront\.net)', rest)
    if not m:
        raise SystemExit("could not find trailing scripts in edway")
    chrome_tail = rest[m.start() :]
    for cs in CASE_STUDIES:
        body = build_project_body(cs, prefix="../")
        page = chrome_head + body + chrome_tail
        page = page.replace("Cosmos Studio | EdWay", f"LulaSync | {cs['title']}")
        page = page.replace('href="edway.html"', f'href="{cs["slug"]}.html"')
        page = inject_scripts(page, ["js/local-nav.js", "js/globe-sa.js"], "../")
        out = ROOT / "projects" / f"{cs['slug']}.html"
        out.write_text(page)
        folder = ROOT / "projects" / cs["slug"]
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(page)
        print("wrote", out)


def main():
    ASSETS.mkdir(exist_ok=True)
    for name, label in ASSET_FILES.items():
        copy_or_placeholder(name, label)
    (ASSETS / "README.md").write_text(
        """# Assets

Upload your images here using these exact filenames. Pages already reference them.

## Case studies
"""
        + "\n".join(f"- `{n}`" for n in ASSET_FILES if n.split("-")[0] in {"academia", "onli", "ridemelo"} or n.startswith("onli-pay") or n.startswith("ridemelo") or n.startswith("academia"))
        + "\n\n## Live apps, UI, websites, hackathons, Figma & frontend\n"
        + "\n".join(f"- `{n}`" for n in ASSET_FILES)
        + "\n"
    )

    write_case_pages()

    # works.html
    works = (ROOT / "works.html").read_text(errors="replace")
    filters = [
        filter_btn("all", 'a<span class="gridular">ll</span>', "all", True),
        filter_btn("case-studies", 'Case st<strong>u</strong>dies', "case-studies"),
        filter_btn("websites", 'Web<strong>s</strong>ites', "websites"),
        filter_btn("live-apps", 'Live a<strong>p</strong>ps', "live-apps"),
        filter_btn("hackathons", 'Hacky hac<strong>k</strong>y', "hackathons"),
        filter_btn("ui-design", 'UI des<strong>i</strong>gn', "ui-design"),
        filter_btn("figma-fe", 'Figma + FE b<strong>u</strong>ilds', "figma-fe"),
    ]
    # replace filter list items inside works-filter_list
    works = re.sub(
        r'(<form[^>]*class="works-filter_list"[^>]*>).*?(</form>)',
        lambda m: m.group(1) + '<div class="w-dyn-list"><div role="list" class="w-dyn-items">' + "".join(filters) + "</div></div>" + m.group(2),
        works,
        count=1,
        flags=re.S,
    )

    cards = []
    for cs in CASE_STUDIES:
        cards.append(work_card(f'projects/{cs["slug"]}.html', cs["cover"], cs["tags"], cs["year"], cs["title"], "case-studies"))
    for href, img, title, tags in WEBSITES:
        cards.append(work_card(href, f"assets/{img}", tags, "2024", title, "websites"))
    for href, img, title, tags in LIVE_APPS:
        cards.append(work_card(href, f"assets/{img}", tags, "2024", title, "live-apps"))
    for href, img, title, tags in HACKS:
        cards.append(work_card(href, f"assets/{img}", tags, "2023", title, "hackathons"))
    for img, title, tags in UI_ITEMS:
        cards.append(work_card(f"assets/{img}", f"assets/{img}", tags, "2024", title, "ui-design"))
    for href, img, title, tags in FIGMA + FE_BUILDS:
        cards.append(work_card(href, f"assets/{img}", tags, "2024", title, "figma-fe"))

    works = re.sub(
        r'(<div fs-cmsfilter-element="list" role="list" class="works-list grid-layout w-dyn-items">).*?(</div></div><div class="w-dyn-hide)',
        lambda m: m.group(1) + "".join(cards) + "</div></div><div class=\"w-dyn-hide",
        works,
        count=1,
        flags=re.S,
    )
    works = inject_scripts(works, ["js/local-nav.js", "js/works-filter.js"], "")
    works = works.replace("Cosmos Studio | Works", "LulaSync | Works")
    (ROOT / "works.html").write_text(works)
    works_dir = ROOT / "works"
    works_dir.mkdir(exist_ok=True)
    # works/index.html needs ../ for assets in cards? cards use assets/ from site root.
    # If served as /works/ then assets/ breaks. Redirect instead.
    (works_dir / "index.html").write_text(
        '<!DOCTYPE html><html><head><meta charset="utf-8"/><script>location.replace("../works.html");</script>'
        '<meta http-equiv="refresh" content="0;url=../works.html"/></head>'
        '<body><a href="../works.html">Works</a></body></html>\n'
    )

    # homepage cases
    index = (ROOT / "index.html").read_text(errors="replace")
    new_cases = "".join(home_case(cs) for cs in CASE_STUDIES)
    index = re.sub(
        r'(<div role="list" class="cases-wr w-dyn-items">).*?(</div></div></div><div class="button_wrapper u--hide-desktop">)',
        lambda m: m.group(1) + new_cases + "</div></div></div><div class=\"button_wrapper u--hide-desktop\">",
        index,
        count=1,
        flags=re.S,
    )
    # if that pattern failed, try alternate end
    if 'projects/academia.html' not in index:
        index = re.sub(
            r'(<div role="list" class="cases-wr w-dyn-items">).*?(</div></div><div class="cases-track cc--absolute">)',
            lambda m: m.group(1) + new_cases + "</div></div><div class=\"cases-track cc--absolute\">",
            index,
            count=1,
            flags=re.S,
        )
    index = inject_scripts(index, ["js/local-nav.js"], "")
    index = index.replace("Cosmos Studio | UI/UX", "LulaSync | UI/UX")
    (ROOT / "index.html").write_text(index)

    # delete old cosmos project pages
    proj_dir = ROOT / "projects"
    for p in list(proj_dir.glob("*.html")):
        if p.name in TEAM_KEEP:
            continue
        if p.stem in {c["slug"] for c in CASE_STUDIES}:
            continue
        p.unlink()
        print("removed", p.name)

    for name in JUNK:
        p = ROOT / name
        if p.exists():
            p.unlink()
            print("removed junk", name)
    for d in ["embed", "Edg", "EdgA", "EdgiOS", "+", "_"]:
        p = ROOT / d
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)

    print("done")


if __name__ == "__main__":
    main()
