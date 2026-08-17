"""Generates the daily "case study" carousel (14h ET slot, since 2026-08-10 — replaced the old
ebook-sales post at this time, see creatorup-estrategia-engajamento-hustlestack SKILL.md for why).

Mirrors Creator Up's generate_case_study.py (.claude/skills/creatorup-gerar-carrossel/) exactly in
structure — same reasoning for existing (real, researched, no-CTA-to-comment marketing case studies
grow follower/share numbers better than another sales post), just in English and restyled in
HustleStack's ivory/black/gold luxury identity instead of Creator Up's tweet-style green.

Structure (identical to the Creator Up version):
1. COVER (`render_case_cover`) — real photo of the brand/founder/scene, editorial headline with
   gold-boxed key phrase. NO "comment X" CTA — this format never sells, ever.
2. STORY (`render_story_slide`, 5-7 slides) — the case in real depth, each slide with its OWN
   support photo that matches what THAT slide specifically says (never a generic/unrelated photo).
3. LESSON (`render_story_slide` again, second-to-last) — an explicit marketing lesson pulled from
   the case ("The marketing lesson here is: ..."), not company/ownership/legal lessons.
4. OUTRO (`render_case_outro`) — plain ivory background, gold tagline + "Follow for the next one."

IMPORTANT — every number/fact in CASE must come from real research (WebSearch), never invented.
Photos (cover_photo_path and each story slide's "photo") only from Openverse/Wikimedia Commons,
open license (CC BY / CC BY-SA / CC0, commercial + modification allowed) — see the "Como baixar as
fotos" subsection in creatorup-gerar-carrossel/SKILL.md (Creator Up's sibling skill) for the full
method (control-domain test first, Openverse proxy `?full_size=true` trick, Wikimedia fallback,
rate-limit handling) — it's brand-agnostic, reuse it as-is for this format too. Never a photo with
a third-party brand/logo in prominent view, never a date/year visible that contradicts the case's
year, always open and LOOK at each photo before using it (a result's title is not proof of its
content).

Instagram only — HustleStack's Metricool brand has no TikTok connected (unlike Creator Up), so
there's no PNG/JPG-per-network split to worry about; the .jpg siblings these render functions still
emit are harmless unused spares, kept only for consistency with the Creator Up renderer.
"""
import os
from generate_template import render_case_cover, render_story_slide, render_case_outro

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "case-study")
os.makedirs(OUT_DIR, exist_ok=True)

_PHOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "case-study-photos")

# Case: Dollar Shave Club's $4,500 launch video (2012) to $1B Unilever exit (2016).
# Researched 2026-08-17. Not previously covered (only Nike/Kaepernick on 2026-08-12).
CASE = {
    "date": "2026-08-17",
    "cover_photo_path": os.path.join(_PHOTO_DIR, "candidates", "cartridge.jpg"),
    "cover_headline": [
        ("A $4,500 VIDEO", False),
        ("BECAME A $1B EXIT", True),
    ],
    "story_slides": [
        {
            "text": "In 2012, Dollar Shave Club had no ad budget worth mentioning.\n\nFounder Michael Dubin wrote the launch video script himself and shot it in a single day with a friend from his improv days. Total cost: $4,500.",
            "highlight": ["$4,500"],
            "photo": os.path.join(_PHOTO_DIR, "candidates", "camera.jpg"),
        },
        {
            "text": "No big crew, no polish. Just Dubin talking straight into the camera, deadpan, selling a subscription razor like it was the funniest pitch he'd ever made.\n\nThe day it went live, the site crashed from the traffic.",
            "highlight": ["crashed"],
            "photo": os.path.join(_PHOTO_DIR, "candidates", "desk.jpg"),
        },
        {
            "text": "People weren't just watching, they were sending it to everyone they knew.\n\nIn its first 3 months on YouTube, the video passed 4.75 million views, for a company almost nobody had heard of a week earlier.",
            "highlight": ["4.75 million views"],
            "photo": os.path.join(_PHOTO_DIR, "candidates", "laptop_entrepreneur.jpg"),
        },
        {
            "text": "The views turned into signups fast.\n\nWithin 48 hours of the video going live: about 12,000 orders. Gillette suddenly had a company to worry about that hadn't existed in most people's minds a week earlier.",
            "highlight": ["12,000 orders"],
            "photo": os.path.join(_PHOTO_DIR, "candidates", "riches.jpg"),
        },
        {
            "text": "Four years later, in 2016, Unilever bought Dollar Shave Club for a reported $1 billion in cash.\n\nDubin stayed on as CEO. One of the largest e-commerce acquisitions of its time.",
            "highlight": ["$1 billion"],
            "photo": os.path.join(_PHOTO_DIR, "candidates", "handshake.jpg"),
        },
    ],
    "lesson_slide": {
        "text": "The marketing lesson here is:\n\nThe product was ordinary, a razor blade delivered monthly. What wasn't ordinary was the pitch. One person, one camera, one honest voice beat every big-budget razor ad on the market.",
        "highlight": ["one honest voice"],
        "photo": os.path.join(_PHOTO_DIR, "candidates", "mic_vintage.jpg"),
    },
    "outro_lines": ["A DIFFERENT MARKETING", "STRATEGY EVERY DAY."],
}


def generate(case=CASE):
    case_out_dir = os.path.join(OUT_DIR, case["date"])
    os.makedirs(case_out_dir, exist_ok=True)

    n = 1
    cover_path = os.path.join(case_out_dir, f"slide_{n:02d}.png")
    render_case_cover(case["cover_headline"], case["cover_photo_path"], cover_path)
    print("generated", cover_path)

    for slide in case["story_slides"]:
        n += 1
        out_path = os.path.join(case_out_dir, f"slide_{n:02d}.png")
        render_story_slide(slide["text"], slide["highlight"], slide["photo"], out_path)
        print("generated", out_path)

    n += 1
    lesson = case["lesson_slide"]
    lesson_path = os.path.join(case_out_dir, f"slide_{n:02d}.png")
    render_story_slide(lesson["text"], lesson["highlight"], lesson["photo"], lesson_path)
    print("generated", lesson_path)

    n += 1
    outro_path = os.path.join(case_out_dir, f"slide_{n:02d}.png")
    render_case_outro(case["outro_lines"], outro_path)
    print("generated", outro_path)


if __name__ == "__main__":
    generate()
