from PIL import Image, ImageDraw, ImageFont
import os

CANVAS_W, CANVAS_H = 1080, 1350
MARGIN_X = 80
TEXT_MAX_WIDTH = CANVAS_W - 2 * MARGIN_X  # 920
AVATAR_SIZE = 90
NAME_SIZE = 30
HANDLE_SIZE = 24
TEXT_SIZE = 42
LINE_HEIGHT = 60
HEADER_TEXT_GAP = 34
AVATAR_TEXT_GAP = 24
WORDMARK_TRACKING = 4  # extra px between letters, luxury wordmarks read wide/tracked

BG_COLOR = (0xF3, 0xEF, 0xE7)   # warm ivory, not stark white — "boutique paper" instead of app UI
TEXT_COLOR = (0x1A, 0x1A, 0x1A) # near-black
HANDLE_COLOR = (0x6B, 0x63, 0x55)  # muted warm grey, quiet not loud
ACCENT_COLOR = (0x9C, 0x7A, 0x4F)  # brushed gold, used sparingly for emphasis only

def _first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


FONT_SERIF_REGULAR = _first_existing([
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    r"C:\Windows\Fonts\georgia.ttf",
])
FONT_SERIF_ITALIC = _first_existing([
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    r"C:\Windows\Fonts\georgiai.ttf",
])
FONT_SERIF_BOLD = _first_existing([
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    r"C:\Windows\Fonts\georgiab.ttf",
])

NAME = "HUSTLESTACK"
HANDLE = "@hustlestackhq"
AVATAR_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "avatar_luxury_a_bare.png")

# Cores só do formato "case study" (14h ET, desde 2026-08-10) — mesmo roxo/painel escuro
# do case de estratégia da Creator Up seria destoante da paleta ivory/gold da HustleStack;
# aqui o destaque usa o ACCENT_COLOR (gold) de sempre da marca, e o painel escuro é
# TEXT_COLOR (quase preto), não um preto puro nem o roxo #6C4CE8 da outra marca.
CASE_PANEL_BG = TEXT_COLOR
CASE_ACCENT = ACCENT_COLOR
CASE_IVORY = BG_COLOR

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT_DIR, exist_ok=True)


def make_square_avatar(src_path, size):
    """Sharp corners, not rounded — reads gallery/editorial rather than app-icon."""
    ss = size * 4
    img = Image.open(src_path).convert("RGB")
    img = img.resize((ss, ss), Image.LANCZOS)
    img = img.resize((size, size), Image.LANCZOS)
    return img


def tracked_text_width(draw, text, font, tracking):
    total = 0
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        total += (bbox[2] - bbox[0]) + tracking
    return total - tracking if text else 0


def draw_tracked_text(draw, text, xy, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), ch, font=font)
        x += (bbox[2] - bbox[0]) + tracking
    return x


def wrap_paragraph(paragraph, font, max_width, draw):
    words = paragraph.split(" ")
    lines = []
    current = []
    for w in words:
        test_line = " ".join([x[0] for x in current] + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w_width = bbox[2] - bbox[0]
        if w_width <= max_width or not current:
            current.append((w, False))
        else:
            lines.append(current)
            current = [(w, False)]
    if current:
        lines.append(current)
    return lines


def build_slide_lines(text, highlight_words, font, draw):
    paragraphs = text.split("\n\n")
    all_lines = []
    for i, para in enumerate(paragraphs):
        lines = wrap_paragraph(para, font, TEXT_MAX_WIDTH, draw)
        marked_lines = []
        for line in lines:
            marked = []
            for word, _ in line:
                clean = word.strip(".,!?").upper()
                is_hl = any(clean == hw.upper() for hw in highlight_words)
                marked.append((word, is_hl))
            marked_lines.append(marked)
        all_lines.extend(marked_lines)
        if i < len(paragraphs) - 1:
            all_lines.append(None)
    return all_lines


def draw_line(draw, line, x, y, font, italic_font):
    cursor_x = x
    for word, is_hl in line:
        f = italic_font if is_hl else font
        color = ACCENT_COLOR if is_hl else TEXT_COLOR
        draw.text((cursor_x, y), word, font=f, fill=color)
        bbox = draw.textbbox((0, 0), word + " ", font=f)
        cursor_x += bbox[2] - bbox[0]


def render_slide(text, highlight_words, out_path):
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    name_font = ImageFont.truetype(FONT_SERIF_REGULAR, NAME_SIZE)
    handle_font = ImageFont.truetype(FONT_SERIF_ITALIC, HANDLE_SIZE)
    body_font = ImageFont.truetype(FONT_SERIF_REGULAR, TEXT_SIZE)
    body_italic_font = ImageFont.truetype(FONT_SERIF_ITALIC, TEXT_SIZE)

    avatar = make_square_avatar(AVATAR_SRC, AVATAR_SIZE)

    header_height = AVATAR_SIZE

    lines = build_slide_lines(text, highlight_words, body_font, draw)
    text_height = 0
    for line in lines:
        text_height += LINE_HEIGHT

    total_height = header_height + HEADER_TEXT_GAP + text_height
    start_y = (CANVAS_H - total_height) // 2

    header_y = start_y
    avatar_x = MARGIN_X
    img.paste(avatar, (avatar_x, header_y))

    text_x = avatar_x + AVATAR_SIZE + AVATAR_TEXT_GAP
    name_bbox = draw.textbbox((0, 0), "H", font=name_font)
    name_h = name_bbox[3] - name_bbox[1]
    handle_bbox = draw.textbbox((0, 0), HANDLE, font=handle_font)
    handle_h = handle_bbox[3] - handle_bbox[1]

    name_y = header_y + (AVATAR_SIZE // 2) - name_h - 6
    draw_tracked_text(draw, NAME, (text_x, name_y), name_font, TEXT_COLOR, WORDMARK_TRACKING)

    handle_y = header_y + (AVATAR_SIZE // 2) + 6
    draw.text((text_x, handle_y), HANDLE, font=handle_font, fill=HANDLE_COLOR)

    body_y = start_y + header_height + HEADER_TEXT_GAP
    for line in lines:
        if line is None:
            body_y += LINE_HEIGHT
            continue
        draw_line(draw, line, MARGIN_X, body_y, body_font, body_italic_font)
        body_y += LINE_HEIGHT

    img.save(out_path)


def _cover_crop(img, target_w, target_h, vertical_bias=0.25):
    """Resize+crop to fill target_w x target_h without distorting (cover-fit).

    vertical_bias mirrors the fix applied 2026-08-10 to the Creator Up renderer
    (creatorup-gerar-carrossel/generate_template.py) after user feedback that photos
    were coming out cropped: a pure top-anchored crop discards the entire bottom half
    of a photo when the target box is much shorter than the photo's natural width-fit
    height (common in these bottom-of-slide photo strips), cutting off faces/subjects
    that aren't pinned to y=0. vertical_bias=0.25 keeps a bias toward the top (subjects
    are usually upper-half, not lower) while giving slack so it doesn't cut a subject
    that's a bit more centered."""
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        new_h = target_h
        new_w = int(new_h * src_ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - target_w) // 2
        img = img.crop((left, 0, left + target_w, target_h))
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        excess = new_h - target_h
        top = int(excess * vertical_bias)
        img = img.crop((0, top, target_w, top + target_h))
    return img


def render_case_cover(headline_lines, photo_path, out_path):
    """Cover slide of the "case study" format (14h ET slot, since 2026-08-10 — replaces
    the old ebook-sales post at this time, see creatorup-estrategia-engajamento-hustlestack).
    Real photo of the brand/founder in the case up top, dark panel below with an editorial
    serif headline and gold-boxed key phrases — same structural idea as Creator Up's
    render_case_cover, restyled in the ivory/black/gold luxury identity instead of
    tweet-style white/purple. No "comment X" CTA — this format never sells."""
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), CASE_PANEL_BG)
    draw = ImageDraw.Draw(img)

    photo_h = 760
    photo = Image.open(photo_path).convert("RGB")
    photo = _cover_crop(photo, CANVAS_W, photo_h)
    img.paste(photo, (0, 0))

    headline_font = ImageFont.truetype(FONT_SERIF_BOLD, 50)
    line_gap = 14
    box_pad_x, box_pad_y = 14, 8
    headline_max_w = CANVAS_W - 2 * MARGIN_X - 2 * box_pad_x  # room for the box padding too

    y = photo_h + 40
    for text, is_boxed in headline_lines:
        # Wrap long headline phrases instead of letting them run off-canvas (bug found
        # 2026-08-10 in visual QA: a longer EN phrase like "FOR A PRODUCT THAT DID NOT
        # EXIST" overflowed past x=1080 at this font size with no wrap).
        wrapped = wrap_paragraph(text, headline_font, headline_max_w, draw)
        sub_lines = [" ".join(w for w, _ in line) for line in wrapped]
        for sub in sub_lines:
            bbox = draw.textbbox((0, 0), sub, font=headline_font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if is_boxed:
                draw.rectangle(
                    (MARGIN_X - box_pad_x, y - box_pad_y, MARGIN_X + w + box_pad_x, y + h + box_pad_y),
                    fill=CASE_ACCENT,
                )
                draw.text((MARGIN_X, y - bbox[1]), sub, font=headline_font, fill=CASE_PANEL_BG)
            else:
                draw.text((MARGIN_X, y - bbox[1]), sub, font=headline_font, fill=CASE_IVORY)
            y += h + line_gap + box_pad_y

    bar_y = CANVAS_H - 90
    avatar = make_square_avatar(AVATAR_SRC, 48)
    img.paste(avatar, (MARGIN_X, bar_y))

    cta_font = ImageFont.truetype(FONT_SERIF_ITALIC, 26)
    cta_text = "swipe for the story"
    cta_x = MARGIN_X + 48 + 16
    cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_h = cta_bbox[3] - cta_bbox[1]
    draw.text((cta_x, bar_y + (48 - cta_h) // 2 - cta_bbox[1]), cta_text, font=cta_font, fill=CASE_IVORY)

    arrow_font = ImageFont.truetype(FONT_SERIF_BOLD, 30)
    arrow_bbox = draw.textbbox((0, 0), "→", font=arrow_font)
    arrow_w = arrow_bbox[2] - arrow_bbox[0]
    arrow_h = arrow_bbox[3] - arrow_bbox[1]
    arrow_x = CANVAS_W - MARGIN_X - arrow_w
    draw.text((arrow_x, bar_y + (48 - arrow_h) // 2 - arrow_bbox[1]), "→", font=arrow_font, fill=CASE_ACCENT)

    img.save(out_path)
    jpg_path = os.path.splitext(out_path)[0] + ".jpg"
    img.convert("RGB").save(jpg_path, quality=95)


def render_story_slide(text, highlight_words, photo_path, out_path):
    """Body slide of the "case study" format: header (avatar + wordmark) and text on top,
    a support photo for THIS specific slide's point on the bottom half — same idea as
    Creator Up's render_story_slide, restyled ivory/serif. Highlighted words render in
    italic gold (ACCENT_COLOR), matching render_slide's existing highlight treatment."""
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    name_font = ImageFont.truetype(FONT_SERIF_REGULAR, NAME_SIZE)
    handle_font = ImageFont.truetype(FONT_SERIF_ITALIC, HANDLE_SIZE)
    body_font = ImageFont.truetype(FONT_SERIF_REGULAR, TEXT_SIZE)
    body_italic_font = ImageFont.truetype(FONT_SERIF_ITALIC, TEXT_SIZE)

    avatar = make_square_avatar(AVATAR_SRC, AVATAR_SIZE)

    top_margin = 70
    header_y = top_margin
    avatar_x = MARGIN_X
    img.paste(avatar, (avatar_x, header_y))

    text_x = avatar_x + AVATAR_SIZE + AVATAR_TEXT_GAP
    name_bbox = draw.textbbox((0, 0), "H", font=name_font)
    name_h = name_bbox[3] - name_bbox[1]
    name_y = header_y + (AVATAR_SIZE // 2) - name_h - 6
    draw_tracked_text(draw, NAME, (text_x, name_y), name_font, TEXT_COLOR, WORDMARK_TRACKING)
    handle_y = header_y + (AVATAR_SIZE // 2) + 6
    draw.text((text_x, handle_y), HANDLE, font=handle_font, fill=HANDLE_COLOR)

    lines = build_slide_lines(text, highlight_words, body_font, draw)
    body_y = header_y + AVATAR_SIZE + HEADER_TEXT_GAP
    for line in lines:
        if line is None:
            body_y += LINE_HEIGHT
            continue
        draw_line(draw, line, MARGIN_X, body_y, body_font, body_italic_font)
        body_y += LINE_HEIGHT

    photo_top = body_y + 30
    photo_h = CANVAS_H - photo_top
    photo = Image.open(photo_path).convert("RGB")
    photo = _cover_crop(photo, CANVAS_W, photo_h)
    img.paste(photo, (0, photo_top))

    img.save(out_path)
    jpg_path = os.path.splitext(out_path)[0] + ".jpg"
    img.convert("RGB").save(jpg_path, quality=95)


def render_case_outro(tagline_lines, out_path):
    """Closing slide of the "case study" format: plain ivory background (no fixed brand
    photo exists yet for HustleStack, unlike Creator Up's case_study_bg.jpg — the minimal
    luxury identity doesn't need one), gold tagline + "Follow for the next one" + handle."""
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), CASE_IVORY)
    draw = ImageDraw.Draw(img)

    y = int(CANVAS_H * 0.38)
    tagline_font = ImageFont.truetype(FONT_SERIF_BOLD, 44)
    for text in tagline_lines:
        bbox = draw.textbbox((0, 0), text, font=tagline_font)
        h = bbox[3] - bbox[1]
        draw.text((MARGIN_X, y - bbox[1]), text, font=tagline_font, fill=CASE_ACCENT)
        y += h + 14

    y += 30
    cta_font = ImageFont.truetype(FONT_SERIF_ITALIC, 30)
    cta_bbox = draw.textbbox((0, 0), "Follow for the next one.", font=cta_font)
    draw.text((MARGIN_X, y - cta_bbox[1]), "Follow for the next one.", font=cta_font, fill=TEXT_COLOR)
    y += (cta_bbox[3] - cta_bbox[1]) + 20

    handle_font = ImageFont.truetype(FONT_SERIF_REGULAR, 26)
    draw.text((MARGIN_X, y), HANDLE, font=handle_font, fill=HANDLE_COLOR)

    img.save(out_path)
    jpg_path = os.path.splitext(out_path)[0] + ".jpg"
    img.convert("RGB").save(jpg_path, quality=95)


# HustleStack Collection: 3 ebooks. Each becomes a 6-slide carousel, generated
# in its own subfolder under out/<slug>/. CTA points to "link in bio" (the
# HustleStack GitHub Pages site), not a free DM giveaway — every carousel
# drives straight to the paid guide. Visual identity switched 2026-07-16 to a
# minimalist luxury-house look (ivory/black/muted gold, serif wordmark, no
# verified badge) — copy below is unchanged from the previous identity.
EBOOKS = [
    {
        "slug": "grow-instagram-tiktok",
        "titulo": "Zero to 10K Followers",
        "slides": [
            {
                "text": "Most people think posting every day is what grows an account.\n\nIt's not.\n\nIt's posting with the algorithm, not against it.",
                "highlight": ["algorithm"],
            },
            {
                "text": "You film a good video and it barely gets views.\n\nIt's not bad luck.\n\nIt's missing a retention trigger in the first three seconds.",
                "highlight": ["retention"],
            },
            {
                "text": "A viral video isn't the prettiest one.\n\nIt's the one that stops the scroll.",
                "highlight": ["stops"],
            },
            {
                "text": "Growth isn't posting more.\n\nIt's posting with a plan.\n\nWhoever improvises every week burns out and quits.",
                "highlight": ["plan"],
            },
            {
                "text": "Your first 10K followers don't come from luck.\n\nThey come from repeating what works and cutting what doesn't.",
                "highlight": ["repeating"],
            },
            {
                "text": "Inside: the algorithm explained, viral video structure, weekly planning, and the mistakes stalling your growth.\n\nGet the full guide, link in bio.",
                "highlight": ["bio"],
            },
        ],
    },
    {
        "slug": "ai-side-hustles",
        "titulo": "AI Side Hustles",
        "slides": [
            {
                "text": "Most people think you need to be a coder to make money with AI.\n\nYou don't.\n\nYou need one skill AI makes faster.",
                "highlight": ["skill"],
            },
            {
                "text": "You bookmark a dozen AI tools and still make zero dollars.\n\nIt's not the tools.\n\nIt's not knowing what to actually sell.",
                "highlight": ["sell"],
            },
            {
                "text": "AI doesn't replace your judgment.\n\nIt does the first draft faster, so you can sell the finished result.",
                "highlight": ["faster"],
            },
            {
                "text": "Charging less because you used AI is the wrong move.\n\nClients pay for the result, not for how long it took.",
                "highlight": ["result"],
            },
            {
                "text": "The people making real money with AI aren't the ones with the most tools.\n\nThey're the ones who picked one and shipped it.",
                "highlight": ["shipped"],
            },
            {
                "text": "Inside: ten realistic AI side hustles, real pricing, and exactly where to find your first client.\n\nGet the full guide, link in bio.",
                "highlight": ["bio"],
            },
        ],
    },
    {
        "slug": "passive-income-online",
        "titulo": "Passive Income Online",
        "slides": [
            {
                "text": "Most people think passive income means doing nothing.\n\nIt's not that.\n\nIt's work once, paid for years.",
                "highlight": ["once"],
            },
            {
                "text": "You start a side project and give up in a month.\n\nIt's not laziness.\n\nIt's picking a stream with no real timeline.",
                "highlight": ["timeline"],
            },
            {
                "text": "Passive income isn't a single silver bullet.\n\nIt's two or three small streams stacked together.",
                "highlight": ["stacked"],
            },
            {
                "text": "A digital product isn't complicated.\n\nBuild it once, and it can sell for years with zero extra cost.",
                "highlight": ["zero"],
            },
            {
                "text": "Nobody replaces a full income with one lucky stream.\n\nThey stack a few boring, specific ones over time.",
                "highlight": ["stack"],
            },
            {
                "text": "Inside: nine real income streams, honest timelines, and how to stack them without burning out.\n\nGet the full guide, link in bio.",
                "highlight": ["bio"],
            },
        ],
    },
    {
        "slug": "ai-avatar-tiktok-shop",
        "titulo": "The AI Avatar Playbook",
        "slides": [
            {
                "text": "Most people think you need to show your face to grow on TikTok.\n\nYou don't.\n\nYou need one avatar that never gets tired.",
                "highlight": ["never gets tired"],
            },
            {
                "text": "You watch faceless accounts blow up and assume it's luck.\n\nIt's not.\n\nIt's one consistent AI identity, reused every single day.",
                "highlight": ["consistent"],
            },
            {
                "text": "An AI avatar isn't a gimmick.\n\nIt's a creator that shows up even on the days you can't.",
                "highlight": ["shows up"],
            },
            {
                "text": "You don't get paid for posting.\n\nYou get paid when that avatar sells something, through TikTok Shop Affiliate.",
                "highlight": ["TikTok Shop Affiliate"],
            },
            {
                "text": "The creators earning real commission aren't the ones with the most videos.\n\nThey're the ones who never miss a day, because their avatar can't get tired.",
                "highlight": ["can't get tired"],
            },
            {
                "text": "Inside: how to build a realistic avatar, a script that sells, and TikTok Shop Affiliate set up step by step.\n\nGet the full guide, link in bio.",
                "highlight": ["bio"],
            },
        ],
    },
]

if __name__ == "__main__":
    for ebook in EBOOKS:
        ebook_out_dir = os.path.join(OUT_DIR, ebook["slug"])
        os.makedirs(ebook_out_dir, exist_ok=True)
        for i, slide in enumerate(ebook["slides"], start=1):
            out_path = os.path.join(ebook_out_dir, f"slide_{i:02d}.png")
            render_slide(slide["text"], slide["highlight"], out_path)
            print("gerado", out_path)


# Engagement rotation added 2026-07-22: pure-value mini-carousels (3 slides,
# hook / reframe / payoff) with NO ebook mention and NO link-in-bio CTA — these
# exist to diversify the feed away from 100% sales content and earn saves/
# shares, per the content-mix decision in
# creatorup-estrategia-engajamento-hustlestack. 14 rotations so 2 posts/day
# (the "aggressive mix" cadence) never repeats within a single week. Same
# render_slide() engine and visual identity as the ebook carousels above —
# only the copy and absence of a CTA differ.
QUOTE_POSTS = [
    {
        "slug": "consistency-not-motivation",
        "slides": [
            {"text": "Motivation shows up for the first three days.\n\nThen it disappears.", "highlight": ["disappears"]},
            {"text": "What's left after motivation is gone is the only thing that ever built anything.\n\nDiscipline.", "highlight": ["Discipline"]},
            {"text": "Save this for the day you don't feel like showing up.\n\nShow up anyway.", "highlight": ["anyway"]},
        ],
    },
    {
        "slug": "small-wins-compound",
        "slides": [
            {"text": "Nobody builds an audience, a business, or a body in one big move.\n\nIt's built in small, boring reps.", "highlight": ["reps"]},
            {"text": "The compound effect looks like nothing for months.\n\nThen it looks like everything at once.", "highlight": ["everything"]},
            {"text": "Do the small thing today.\n\nIt's the only version of tomorrow that counts.", "highlight": ["today"]},
        ],
    },
    {
        "slug": "comparison-trap",
        "slides": [
            {"text": "You're comparing your year one to someone else's year ten.\n\nThat's not a fair fight.", "highlight": ["fight"]},
            {"text": "The account you keep scrolling took years of quiet, unglamorous work to look effortless.", "highlight": ["quiet"]},
            {"text": "Stop measuring your day twelve against someone else's day twelve hundred.", "highlight": ["twelve"]},
        ],
    },
    {
        "slug": "fear-of-starting",
        "slides": [
            {"text": "You don't need a better plan.\n\nYou need to post the first one.", "highlight": ["first"]},
            {"text": "The version of you that's embarrassed by old work is proof you've grown.\n\nStart embarrassing.", "highlight": ["grown"]},
            {"text": "Perfect is a place you visit after a hundred imperfect tries.\n\nNot before.", "highlight": ["hundred"]},
        ],
    },
    {
        "slug": "overnight-success-myth",
        "slides": [
            {"text": "There's no such thing as an overnight success.\n\nJust a late night nobody filmed.", "highlight": ["filmed"]},
            {"text": "Every big launch you admire had a version zero nobody saw and nobody liked.", "highlight": ["zero"]},
            {"text": "You're not behind.\n\nYou're just early in your own story.", "highlight": ["early"]},
        ],
    },
    {
        "slug": "boring-work",
        "slides": [
            {"text": "The boring part is the whole business model.\n\nMost people quit right before it pays off.", "highlight": ["pays"]},
            {"text": "Nobody talks about the thousand unremarkable Tuesdays behind one remarkable result.", "highlight": ["Tuesdays"]},
            {"text": "If it were exciting every day, everyone would already be doing it.", "highlight": ["exciting"]},
        ],
    },
    {
        "slug": "following-through",
        "slides": [
            {"text": "Ideas are cheap.\n\nFinishing is the entire skill.", "highlight": ["Finishing"]},
            {"text": "You don't need ten new ideas this month.\n\nYou need to finish the one from three months ago.", "highlight": ["finish"]},
            {"text": "The gap between where you are and where you want to be is called follow through.", "highlight": ["through"]},
        ],
    },
    {
        "slug": "one-skill-mastered",
        "slides": [
            {"text": "You don't need ten skills to change your income.\n\nYou need one, sharpened for a year.", "highlight": ["one"]},
            {"text": "Jumping skills every month resets the clock every month.", "highlight": ["resets"]},
            {"text": "Pick the one thing.\n\nGet boringly good at it.", "highlight": ["boringly"]},
        ],
    },
    {
        "slug": "time-vs-money",
        "slides": [
            {"text": "You can always make more money.\n\nYou can't make more of this year.", "highlight": ["year"]},
            {"text": "Trading your best hours for someone else's dream is fine, until it isn't.", "highlight": ["dream"]},
            {"text": "Build something that pays you back for the hours you already spent.", "highlight": ["back"]},
        ],
    },
    {
        "slug": "progress-over-perfection",
        "slides": [
            {"text": "Perfect doesn't ship.\n\nGood enough, on time, ships every week.", "highlight": ["ships"]},
            {"text": "You're not failing.\n\nYou're just looking at draft one and calling it final.", "highlight": ["draft"]},
            {"text": "Post the version you have.\n\nThe perfect one doesn't exist yet.", "highlight": ["exist"]},
        ],
    },
    {
        "slug": "saying-no-to-distractions",
        "slides": [
            {"text": "Every new app you download is a vote against the one thing you said you'd finish.", "highlight": ["vote"]},
            {"text": "Focus isn't doing more things.\n\nIt's saying no to almost everything else.", "highlight": ["no"]},
            {"text": "Close the elective tabs.\n\nFinish the one that pays.", "highlight": ["pays"]},
        ],
    },
    {
        "slug": "long-game-mindset",
        "slides": [
            {"text": "Everyone wants the result.\n\nAlmost nobody wants the five years before it.", "highlight": ["five"]},
            {"text": "The people who make it aren't smarter.\n\nThey just didn't leave.", "highlight": ["leave"]},
            {"text": "Play the long game.\n\nMost of your competition already quit.", "highlight": ["quit"]},
        ],
    },
    {
        "slug": "showing-up-on-bad-days",
        "slides": [
            {"text": "You don't need to feel ready.\n\nYou need to show up anyway.", "highlight": ["anyway"]},
            {"text": "Bad days build the account just as much as good ones.\n\nNobody posts about that part.", "highlight": ["Bad"]},
            {"text": "Save this for the day you want to quit.\n\nThat's the day that counts most.", "highlight": ["counts"]},
        ],
    },
    {
        "slug": "algorithm-rewards-consistency",
        "slides": [
            {"text": "The algorithm doesn't reward talent.\n\nIt rewards whoever kept showing up.", "highlight": ["showing"]},
            {"text": "One good post won't grow an account.\n\nFifty ordinary ones, on schedule, will.", "highlight": ["Fifty"]},
            {"text": "Consistency is the whole strategy.\n\nEveryone's just looking for a shortcut around it.", "highlight": ["Consistency"]},
        ],
    },
]

if __name__ == "__main__":
    for post in QUOTE_POSTS:
        post_out_dir = os.path.join(OUT_DIR, "quotes", post["slug"])
        os.makedirs(post_out_dir, exist_ok=True)
        for i, slide in enumerate(post["slides"], start=1):
            out_path = os.path.join(post_out_dir, f"slide_{i:02d}.png")
            render_slide(slide["text"], slide["highlight"], out_path)
            print("gerado", out_path)


# Follower-growth rotation added 2026-08-11: full free tactics (6 slides), one
# complete, applicable technique per post, never gated toward the ebooks. This
# is the 10am ET slot's content per the 2026-08-11 mix revision (see
# creatorup-estrategia-engajamento-hustlestack) — replaces that slot's old
# quote-card rotation with something built specifically to earn shares from
# non-followers ("you need to see this") instead of just saves. Primary CTA
# is a follow ask (growing followers is this slot's entire purpose), but each
# closing slide also carries a soft "full guides in bio" mention — the user
# confirmed 2026-08-11 it's fine for this slot to nod at the bio link too, as
# long as the follow ask stays the lead line, not a hard ebook pitch. 7 items,
# cycles weekly (same accepted evergreen-cycling precedent as QUOTE_POSTS).
TACTIC_POSTS = [
    {
        "slug": "hook-in-three-seconds",
        "slides": [
            {"text": "Most hooks die in the first three words.\n\nHere is the fix, step by step.", "highlight": ["step by step"]},
            {"text": "Open with the moment things went wrong, not your name or your niche.\n\n\"I lost my first three clients because of this\" beats \"Hey guys, today I want to talk about...\"", "highlight": ["went wrong"]},
            {"text": "Cut every setup word. No \"so\", no \"okay\", no \"today I want to show you\".\n\nStart on the sentence that hurts or surprises.", "highlight": ["hurts or surprises"]},
            {"text": "Read your hook out loud in five seconds.\n\nIf you have not said anything specific yet, it is still a setup line. Cut it.", "highlight": ["five seconds"]},
            {"text": "This is not a trick. It is math.\n\nThe algorithm decides reach in the first three seconds. A weak hook caps everything after it.", "highlight": ["first three seconds"]},
            {"text": "Save this before your next post.\n\nFollow @hustlestackhq for one free tactic like this every week. Full guides in bio.", "highlight": ["Follow @hustlestackhq"]},
        ],
    },
    {
        "slug": "reverse-engineer-a-viral-post",
        "slides": [
            {"text": "You do not need a new idea.\n\nYou need someone else's proven structure.", "highlight": ["proven structure"]},
            {"text": "Open the 5 best-performing posts in your niche. Ignore the topic. Write down only the shape: how many beats, where the twist lands, how it ends.", "highlight": ["only the shape"]},
            {"text": "That shape is the formula. Swap in your own story, your own numbers, your own voice. The structure carries the weight, not the topic.", "highlight": ["formula"]},
            {"text": "Test the same formula three times before judging it.\n\nOne post is luck. Three is a pattern.", "highlight": ["Three is a pattern"]},
            {"text": "This is why some accounts post less but grow faster. They stopped guessing the shape and started reusing what already works.", "highlight": ["reusing"]},
            {"text": "Save this for your next content day.\n\nFollow @hustlestackhq for more free tactics like this. Full guides in bio.", "highlight": ["Follow @hustlestackhq"]},
        ],
    },
    {
        "slug": "first-ai-client-in-a-week",
        "slides": [
            {"text": "You do not need a portfolio to get your first AI client.\n\nYou need one offer, sent to ten people.", "highlight": ["one offer"]},
            {"text": "Pick one task AI makes fast: product descriptions, short-form scripts, cold emails, simple websites.\n\nPick ONE. Not a menu of five services nobody can picture.", "highlight": ["Pick ONE"]},
            {"text": "Message ten small businesses that clearly need it. Offer one free sample built specifically for them, not a generic template.", "highlight": ["built specifically"]},
            {"text": "Price the result, not the hours. A cold email sequence that books calls is worth more than the twenty minutes AI took to draft it.", "highlight": ["the result"]},
            {"text": "Most people never send the first ten messages.\n\nThat is the entire gap between them and someone with a client.", "highlight": ["first ten messages"]},
            {"text": "Save this and send message one today.\n\nFollow @hustlestackhq for more free tactics like this. Full guides in bio.", "highlight": ["Follow @hustlestackhq"]},
        ],
    },
    {
        "slug": "price-ai-work-right",
        "slides": [
            {"text": "Undercharging is the fastest way to quit an AI side hustle.\n\nHere is how to price it instead.", "highlight": ["price it"]},
            {"text": "Never price by how long AI took. Price by what the result is worth to the client: more leads, more time back, more sales.", "highlight": ["what the result is worth"]},
            {"text": "Charge a flat project fee, not an hourly rate.\n\nHourly punishes you for getting faster with practice.", "highlight": ["flat project fee"]},
            {"text": "If a client asks why it costs more than they expected, show them what doing it badly costs them instead. That is the real comparison.", "highlight": ["real comparison"]},
            {"text": "The people charging three times more are not better at the tools. They just stopped explaining the process and started selling the outcome.", "highlight": ["selling the outcome"]},
            {"text": "Save this before your next quote.\n\nFollow @hustlestackhq for more free tactics like this. Full guides in bio.", "highlight": ["Follow @hustlestackhq"]},
        ],
    },
    {
        "slug": "one-digital-product-stack",
        "slides": [
            {"text": "You do not need five income streams.\n\nYou need one product, built once.", "highlight": ["built once"]},
            {"text": "Take the question people ask you most for free.\n\nThat question is your product topic. It already has proven demand.", "highlight": ["proven demand"]},
            {"text": "Build the smallest version that fully solves it. A ten page guide that actually works beats a bloated course nobody finishes.", "highlight": ["actually works"]},
            {"text": "Put it somewhere it can sell without you: a simple checkout page, linked from one place people already trust you.", "highlight": ["without you"]},
            {"text": "It will not make real money the first week.\n\nIt compounds the month you stop touching it and it still sells.", "highlight": ["compounds"]},
            {"text": "Save this and start today.\n\nFollow @hustlestackhq for more free tactics like this. Full guides in bio.", "highlight": ["Follow @hustlestackhq"]},
        ],
    },
    {
        "slug": "turn-a-skill-into-a-template",
        "slides": [
            {"text": "The fastest digital product is not a new idea.\n\nIt is the thing you already do manually, turned into a template.", "highlight": ["turned into a template"]},
            {"text": "Look at the last file you rebuilt from scratch for the third time this month.\n\nThat is your product.", "highlight": ["That is your product"]},
            {"text": "Strip out anything specific to one client. Keep the structure, the formulas, the parts that took you years to get right.", "highlight": ["parts that took you years"]},
            {"text": "Sell it to the version of you from two years ago, the one who would have paid for this shortcut.", "highlight": ["would have paid"]},
            {"text": "You already did the hard part once.\n\nA template just means you never do it from zero again.", "highlight": ["never do it from zero again"]},
            {"text": "Save this and look at your files today.\n\nFollow @hustlestackhq for more free tactics like this. Full guides in bio.", "highlight": ["Follow @hustlestackhq"]},
        ],
    },
    {
        "slug": "posting-schedule-that-works",
        "slides": [
            {"text": "A content calendar does not fail because of bad ideas.\n\nIt fails because it depends on daily motivation.", "highlight": ["daily motivation"]},
            {"text": "Batch one day a month. Film or write everything in one sitting, while you still have the energy for all of it.", "highlight": ["Batch one day"]},
            {"text": "Schedule every post the same day you make it.\n\nA draft sitting in your camera roll never posts itself.", "highlight": ["never posts itself"]},
            {"text": "Pick three posting days, not seven. Fewer, consistent days beat a daily habit that quietly stops in week two.", "highlight": ["Fewer, consistent days"]},
            {"text": "The accounts that never miss a week are not the most inspired ones.\n\nThey are the ones who removed the daily decision.", "highlight": ["removed the daily decision"]},
            {"text": "Save this before you plan next month.\n\nFollow @hustlestackhq for more free tactics like this. Full guides in bio.", "highlight": ["Follow @hustlestackhq"]},
        ],
    },
]

if __name__ == "__main__":
    for post in TACTIC_POSTS:
        post_out_dir = os.path.join(OUT_DIR, "tactics", post["slug"])
        os.makedirs(post_out_dir, exist_ok=True)
        for i, slide in enumerate(post["slides"], start=1):
            out_path = os.path.join(post_out_dir, f"slide_{i:02d}.png")
            render_slide(slide["text"], slide["highlight"], out_path)
            print("gerado", out_path)
