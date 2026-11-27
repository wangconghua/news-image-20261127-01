#!/usr/bin/env python3
"""Draw the front page for Friday 27 November 2026 as a 1024x1024 PNG.

Layout: masthead, one lead story, then three columns of 12 briefs each
(36 briefs in total). Every brief names its source wire at the end of
its text. Run: python3 draw.py  ->  writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 250, 244)
INK = (17, 17, 17)
MUTED = (96, 94, 86)
RED = (155, 28, 28)
RULE = (150, 148, 138)
FAINT = (208, 206, 195)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

MARGIN = 28
COL_GAP = 24
COL_W = (W - 2 * MARGIN - 2 * COL_GAP) // 3  # 306


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


LEAD_KICKER = "TOP STORY  ·  BRUSSELS"
LEAD_HEAD = "EU leaders deadlocked over \u20ac1.6 trillion budget and $49bn Ukraine loan"
LEAD_BODY = (
    "European Union leaders failed to bridge deep divides over the bloc's next "
    "seven-year budget and a new $49 billion loan for Ukraine after more than "
    "12 hours of talks in Brussels on Thursday. France's Emmanuel Macron ruled "
    "out a deal at the summit and set a year-end deadline, with leaders due to "
    "meet again on 18\u201319 December. The package earmarks \u20ac100 billion for "
    "Kyiv over seven years, \u20ac25 billion of it for weapons."
)
LEAD_WHY = (
    "Without a deal, Kyiv faces a funding gap next year as the war nears its "
    "fifth year \u2014 and the fight over the budget will shape the EU until 2034."
)

# (headline, body) — headline carries a region tag; body ends with the source.
BRIEFS = [
    # Column 1: Europe and the Middle East
    ("EUROPE \u2014 Budget talks run into Friday",
     "Council chief Ant\u00f3nio Costa urged compromise as talks stretched on, with no deal in sight. (AP)"),
    ("EUROPE \u2014 Trump, Rutte warn Russia",
     "The US president and NATO chief told Moscow not to widen the Ukraine war as allies weigh aid. (AFP)"),
    ("EUROPE \u2014 Macron rules out summit deal",
     "France's leader said no budget deal would come in Brussels, but one could be signed in December. (AP)"),
    ("MIDEAST \u2014 Saudis down Riyadh missiles",
     "Saudi defences intercepted missiles aimed at the capital in the latest Gulf strikes. (AFP)"),
    ("MIDEAST \u2014 Gaza strike kills Hamas official",
     "An Israeli strike killed a Hamas security official and his family, Gaza officials said. (AP)"),
    ("MIDEAST \u2014 Fresh strikes test Gaza truce",
     "New Israeli attacks raised fears for the ceasefire as mediators pressed both sides to hold it. (Reuters)"),
    ("MIDEAST \u2014 Myanmar defies genocide ruling",
     "Myanmar said it will not comply with parts of the world court's genocide ruling against it. (AFP)"),
    ("EUROPE \u2014 Depardieu to face rape trial",
     "French actor G\u00e9rard Depardieu will stand trial on a rape charge, his lawyer confirmed. (AFP)"),
    ("EUROPE \u2014 Pope backs prison ministry",
     "The Pope formed a new initiative to coordinate the Catholic Church's prison ministry worldwide. (AP)"),
    ("EUROPE \u2014 UK youth: less sex, more sexting",
     "A study found young Britons have less sex but sext more, in a snapshot of changing habits. (Reuters)"),
    ("EUROPE \u2014 Bulgaria backs Ukraine loan",
     "Bulgaria will support the \u20ac45bn EU loan for Ukraine, but only the \u20ac20bn share for civilian aid. (Reuters)"),
    ("MIDEAST \u2014 Slain Gaza reporter wins prize",
     "A Gaza journalist killed in an Israeli strike won the Rory Peck Prize for frontline reporting. (AP)"),
    # Column 2: the Americas and East Asia-Pacific
    ("TRADE \u2014 US tariff plan hits 14 partners",
     "Washington proposed duties of up to 25% on Indian goods and levies on China and the EU. (Reuters)"),
    ("AMERICAS \u2014 Storm floods US East Coast",
     "Heavy rain, wind and flooding hit much of the US on Thanksgiving, with high winds in New York. (AP)"),
    ("AMERICAS \u2014 King tides batter California",
     "Huge seasonal king tides battered California's coast, flooding low-lying streets and car parks. (AP)"),
    ("AMERICAS \u2014 Black Friday sales begin",
     "Shoppers hunted deals as Black Friday opened after a storm-hit Thanksgiving across the US. (AP)"),
    ("AMERICAS \u2014 Vance serves troops turkey",
     "Vice-President J.D. Vance spent Thanksgiving with US troops, serving turkey and chatting. (AP)"),
    ("TECH \u2014 SpaceX cleared for 1m satellites",
     "US regulators cleared SpaceX to launch up to a million satellites for orbital data centres. (AP)"),
    ("TECH \u2014 Musk: SpaceX shares for children",
     "Musk said every US child will get two SpaceX shares, worth about $18bn in all. (NDTV)"),
    ("TECH \u2014 Nvidia halts server shipments",
     "Nvidia halted server shipments to four Southeast Asian countries, a report said. (Reuters)"),
    ("ASIA \u2014 Japan warns Chinese ships off",
     "Japan warned Chinese ships to leave waters near disputed islands, in the latest maritime spat. (AFP)"),
    ("ASIA \u2014 China: border with India stable",
     "Beijing said the situation along the India-China border remains generally stable. (Reuters)"),
    ("ASIA \u2014 Bangkok refinery blast hurts nine",
     "An explosion at Bangchak's Bangkok refinery injured nine and shut all its production units. (Reuters)"),
    ("ASIA \u2014 Indonesia mine search goes on",
     "Rescuers kept digging for miners trapped in an illegal gold mine after 13 deaths. (AP)"),
    # Column 3: South Asia, Africa, sport and business
    ("INDIA \u2014 Cabinet meets on quota bill",
     "PM Modi chairs a cabinet meeting on the women's reservation bill before Parliament returns. (PTI)"),
    ("INDIA \u2014 Congress maps Parliament plan",
     "Sonia Gandhi chairs the party's strategy meeting ahead of special Parliament sittings. (PTI)"),
    ("INDIA \u2014 Graft charges stand vs Lalu",
     "Delhi High Court upheld corruption charges against RJD leader Lalu Prasad in the IRCTC case. (PTI)"),
    ("INDIA \u2014 500,000 jobs at risk: trade body",
     "A trade body urged retaliatory US tariffs, warning 500,000 jobs and $48bn of exports are at risk. (CNA)"),
    ("INDIA \u2014 NSE value hits record high",
     "National Stock Exchange shares hit a record, taking its valuation to Rs 5.88 lakh crore. (PTI)"),
    ("ASIA \u2014 Nepal: 213 missing presumed dead",
     "Nepal began declaring 213 Indians missing in August floods presumed dead, officials said. (PTI)"),
    ("AFRICA \u2014 Ebola cases pass 12,000 in DRC",
     "Confirmed Ebola cases in DR Congo crossed 12,000, health authorities reported. (Reuters)"),
    ("AFRICA \u2014 Ramaphosa wins court challenge",
     "South Africa's president won a court bid to overturn an impeachment report against him. (Reuters)"),
    ("ASIA \u2014 Kim vows bigger nuclear arsenal",
     "Kim Jong Un vowed to grow the nuclear arsenal, ignoring a US diplomatic overture. (AP)"),
    ("ASIA \u2014 Bangladesh lifts garment wage 36%",
     "Bangladesh raised the minimum wage for garment workers by 36% after weeks of protests. (Reuters)"),
    ("SPORT \u2014 Gukesh draws game two",
     "Champion D. Gukesh drew game two of his title defence vs Javokhir Sindarov. (Reuters)"),
    ("SPORT \u2014 Sooryavanshi smashes 204 not out",
     "Teenager Vaibhav Sooryavanshi hit an unbeaten 204 off 53 balls against the UAE in Doha. (PTI)"),
]


def draw_masthead(d):
    y = 18
    name_f = font(SERIF_B, 47)
    name = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(name, font=name_f)) / 2, y), name, font=name_f, fill=INK)
    y += 58
    date_f = font(SANS_B, 17)
    date = "FRIDAY  27  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, y), date, font=date_f, fill=RED)
    y += 26
    tag_f = font(SANS, 13)
    tag = "36 STORIES  \u00b7  FIVE CONTINENTS  \u00b7  EVERY STORY SOURCED"
    d.text(((W - d.textlength(tag, font=tag_f)) / 2, y), tag, font=tag_f, fill=MUTED)
    y += 24
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    d.line([(MARGIN, y + 5), (W - MARGIN, y + 5)], fill=INK, width=1)
    return y + 12


def draw_lead(d, y):
    kick_f = font(SANS_B, 13)
    d.text((MARGIN, y), LEAD_KICKER, font=kick_f, fill=RED)
    y += 20
    head_f = font(SANS_B, 30)
    lines = wrap(d, LEAD_HEAD, head_f, W - 2 * MARGIN)
    assert len(lines) <= 2, "lead headline wrapped to %d lines" % len(lines)
    for line in lines:
        d.text((MARGIN, y), line, font=head_f, fill=INK)
        y += 36
    y += 2
    body_f = font(SANS, 15)
    lines = wrap(d, LEAD_BODY, body_f, W - 2 * MARGIN)
    assert len(lines) <= 3, "lead body wrapped to %d lines" % len(lines)
    for line in lines:
        d.text((MARGIN, y), line, font=body_f, fill=INK)
        y += 19
    y += 4
    why_f = font(SANS, 13)
    why_b = font(SANS_B, 13)
    label = "WHY IT MATTERS \u2014 "
    lw = d.textlength(label, font=why_b)
    full_w = W - 2 * MARGIN
    # First line shares its row with the label; later lines use the full width.
    lines, cur, limit = [], "", full_w - lw
    for word in LEAD_WHY.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=why_f) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur, limit = word, full_w
    if cur:
        lines.append(cur)
    assert len(lines) <= 2, "why-it-matters wrapped to %d lines" % len(lines)
    d.text((MARGIN, y), label, font=why_b, fill=RED)
    d.text((MARGIN + lw, y), lines[0], font=why_f, fill=INK)
    y += 17
    for line in lines[1:]:
        d.text((MARGIN, y), line, font=why_f, fill=INK)
        y += 17
    y += 6
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    return y + 12


def draw_columns(d, y0):
    head_f = font(SANS_B, 14)
    body_f = font(SANS, 13)
    bottom = y0
    for col in range(3):
        x = MARGIN + col * (COL_W + COL_GAP)
        y = y0
        for head, body in BRIEFS[col * 12:(col + 1) * 12]:
            hlines = wrap(d, head, head_f, COL_W)
            assert len(hlines) <= 2, "headline too long: %r" % head
            for line in hlines:
                d.text((x, y), line, font=head_f, fill=INK)
                y += 16
            blines = wrap(d, body, body_f, COL_W)
            assert len(blines) <= 2, "body too long (%d lines): %r" % (len(blines), body)
            for line in blines:
                d.text((x, y), line, font=body_f, fill=(40, 40, 40))
                y += 15
            y += 5
            d.line([(x, y - 3), (x + COL_W, y - 3)], fill=FAINT, width=1)
            y += 1
        bottom = max(bottom, y)
        if col < 2:
            d.line([(x + COL_W + COL_GAP // 2, y0),
                    (x + COL_W + COL_GAP // 2, y - 4)], fill=FAINT, width=1)
    return bottom


def draw_footer(d, y):
    foot_f = font(SANS_I, 13)
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 8
    foot = "The World in One Day  \u00b7  Friday 27 November 2026  \u00b7  Sources: AP, AFP, Reuters, PTI, CNA, NDTV"
    d.text(((W - d.textlength(foot, font=foot_f)) / 2, y), foot, font=foot_f, fill=MUTED)
    return y + 18


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d)
    y = draw_lead(d, y)
    y = draw_columns(d, y)
    print("columns end at y=%d (limit 1000)" % y)
    if y > 1000:
        raise SystemExit("layout overflow: columns end at y=%d" % y)
    y = draw_footer(d, y)
    print("footer ends at y=%d" % y)
    if y > H - 6:
        raise SystemExit("layout overflow: footer ends at y=%d" % y)
    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote %s  %d bytes  %s" % (OUT, size, img.size))
    if size > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB: %d bytes" % size)


if __name__ == "__main__":
    main()
