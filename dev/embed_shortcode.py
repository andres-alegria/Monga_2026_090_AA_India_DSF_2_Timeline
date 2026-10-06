#!/usr/bin/env python3
"""
Builds the WordPress [iframe] shortcode for the timeline, and checks it.

A Mongabay post takes only the [iframe] shortcode: no script, no HTML block. So the frame's height comes from a CSS
formula in its style attribute:
  - it works out the article column's width from the screen width (Mongabay's theme rule, COL below);
  - it gives a height a few pixels taller than the timeline needs at that column width (dev/heights.json).
The ?fill=1 in the URL makes the timeline stretch to the frame, so those few spare pixels are shared out between the
rows of the list instead of showing as a gap at the bottom.

The formula is fitted here from the measurements, so it follows the content when that changes:
  1. Re-measure: serve the repo root (python3 -m http.server), open /dev/measure.html, and save its JSON as
     dev/heights.json.
  2. Run this script. It fits the formula, checks every screen width from 320 to 1,600 px, then writes
     embed-shortcode.txt (paste its contents into the post) and dev/shortcode-test.html (a stand-in Mongabay article).

    python3 dev/embed_shortcode.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
URL = "https://monga2026090aaindiadsf2timeline.vercel.app/?fill=1"
TITLE = "India’s deep-sea fishing policy: 1950s to present (interactive timeline)"

# Mongabay's article column (news.mongabay.com theme CSS, 30 Sep 2026): the container has
# `.ph--40 { padding: 0 clamp(20px, 1px + 5vw, 40px) }` and the text column inside it has max-width 780px.
COL = "min(780px, 100vw - 2 * clamp(20px, 1px + 5vw, 40px))"


def col(vw):
    return min(780, vw - 2 * min(40, max(20, 1 + 0.05 * vw)))


LAYOUT_SWITCH = 719   # style.css: the phone layout applies up to a 719 px wide frame
MARGIN = 6            # px added everywhere, so rounding and font differences never leave the timeline short
LATE_WRAP = 8         # px: allow for a browser wrapping text up to this much later (wider) than the measurements
SCROLLBAR = 17        # px: Windows desktop browsers count the scrollbar in 100vw, so the formula sees a column this
                      # much wider than the real one; without this, a re-wrap step in that band leaves the frame short
SCROLLBAR_FROM = 560  # px of column (a screen of about 624 px): below it only phones are likely, and phones have no
                      # such scrollbar, so the allowance would only add spare height there
MERGE_TOL = 12        # px of extra spare allowed when merging segments, to keep the formula short
STEEP = 100000        # makes a ramp into a step: the full jump is reached within a fraction of a pixel


def load_rows():
    """The timeline's entries, from content.js (the list has one row each)."""
    src = open(os.path.join(ROOT, "content.js"), encoding="utf-8").read()
    return json.loads(re.search(r"=\s*(\{.*\})\s*;\s*$", src, re.S).group(1))["events"]


def needed_fn(heights):
    """The timeline's natural height at column width c: the taller of the two measurements around it, taken on the
    same side of the layout switch as c."""
    def needed(c):
        ws = sorted(w for w in heights if (w <= LAYOUT_SWITCH) == (c <= LAYOUT_SWITCH))
        if c < ws[0]:
            return max(heights[w] for w in ws)
        if c > ws[-1]:
            return heights[ws[-1]]
        lo = max(w for w in ws if w <= c)
        hi = min(w for w in ws if w >= c)
        return max(heights[lo], heights[hi])
    return needed


def fit(needed, lo, hi, step=0.5):
    """A chain of straight segments from lo to hi that never dips below needed().
    First it runs through the top corner of every step down (the last width before a line of text re-wraps), then it
    merges neighbouring segments wherever that adds no more than MERGE_TOL px of spare height."""
    xs = [lo + i * step for i in range(int(round((hi - lo) / step)) + 1)]
    ys = [needed(x) for x in xs]
    pts = [(xs[0], ys[0])]
    pts += [(xs[i], ys[i]) for i in range(1, len(xs) - 1) if ys[i + 1] < ys[i]]
    pts.append((xs[-1], ys[-1]))

    def line_ok(a, b):
        (x0, y0), (x1, y1) = pts[a], pts[b]
        for x, y in zip(xs, ys):
            if x0 < x < x1:
                v = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
                if v < y - 1e-9 or v - y > MERGE_TOL + poly_spare(x):
                    return False
        return True

    def poly_spare(x):  # spare height of the unmerged corner chain at x
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0) - needed(x)
        return 0

    knots, i = [pts[0]], 0
    while i < len(pts) - 1:
        j = i + 1
        while j + 1 < len(pts) and line_ok(i, j + 1):
            j += 1
        knots.append(pts[j])
        i = j
    return knots


def late(needed):
    """needed(), assuming each re-wrap happens up to LATE_WRAP px later (plus SCROLLBAR px in columns where a desktop
    window is plausible); the layout switch itself is exact."""
    def f(c):
        back = LATE_WRAP + (SCROLLBAR if c >= SCROLLBAR_FROM else 0)
        side = [c - d * 0.5 for d in range(int(back * 2) + 1)]
        return max(needed(x) for x in side if (x <= LAYOUT_SWITCH) == (c <= LAYOUT_SWITCH))
    return f


def build(heights):
    needed = late(needed_fn(heights))
    phone = fit(needed, 280, LAYOUT_SWITCH)                       # the phone layout, as a chain of segments
    y_phone_end = phone[-1][1]
    wide_start = needed(LAYOUT_SWITCH + 1)                         # the list layout, first width
    wide_steps = []                                                # later drops within the list layout
    last = wide_start
    for i in range(2 * (LAYOUT_SWITCH + 1), 2 * 780 + 1):
        x = i / 2
        if needed(x + 0.5) < last:
            wide_steps.append((x + 0.5, last - needed(x + 0.5)))   # at the width where the lower height applies
            last = needed(x + 0.5)
    return phone, y_phone_end, wide_start, wide_steps


def height(c, model):
    phone, y_end, wide_start, wide_steps = model
    h = phone[0][1] + MARGIN
    for (x0, y0), (x1, y1) in zip(phone, phone[1:]):
        h += (y1 - y0) / (x1 - x0) * min(max(c - x0, 0), x1 - x0)
    h += min(max((c - LAYOUT_SWITCH) * STEEP, 0), wide_start - y_end)
    for x, drop in wide_steps:
        h -= min(max((c - x) * STEEP, 0), drop)
    return h


def css_height(model):
    phone, y_end, wide_start, wide_steps = model
    parts = [f"{phone[0][1] + MARGIN}px"]
    for (x0, y0), (x1, y1) in zip(phone, phone[1:]):
        slope = round((y0 - y1) / (x1 - x0), 4)
        parts.append(f"- {slope} * clamp(0px, {COL} - {x0:g}px, {x1 - x0:g}px)")
    parts.append(f"+ clamp(0px, ({COL} - {LAYOUT_SWITCH}px) * {STEEP}, {wide_start - y_end}px)")
    for x, drop in wide_steps:
        parts.append(f"- clamp(0px, ({COL} - {x:g}px) * {STEEP}, {drop}px)")
    return "calc(" + " ".join(parts) + ")"


def main():
    heights = {int(k): v for k, v in json.load(open(os.path.join(HERE, "heights.json"))).items()}
    model = build(heights)
    needed = late(needed_fn(heights))
    print(f"phone layout: {len(model[0]) - 1} segments; list layout: starts at {model[2]} px, "
          f"{len(model[3])} drop(s)")

    # the rounded slopes in the CSS, not the exact ones, are what the browser uses: check those
    phone = model[0]
    rounded = [phone[0]]
    for (x0, y0), (x1, y1) in zip(phone, phone[1:]):
        rounded.append((x1, rounded[-1][1] - round((y0 - y1) / (x1 - x0), 4) * (x1 - x0)))
    checked = (rounded, model[1], model[2], model[3])

    bands = [(320, 359, "small phones"), (360, 430, "phones"), (431, 714, "large phones, small tablets"),
             (715, 859, "tablets, small windows"), (860, 1600, "desktop")]
    rows = len(load_rows())
    measured = needed_fn(heights)
    worst = None
    print(f"spare height (formula minus the timeline as measured), px, shared by {rows} rows")
    for lo, hi, label in bands:
        cs = [col(vw) for vw in range(lo, hi + 1)]
        worst_case = min(height(c, checked) - needed(c) for c in cs)        # with late wraps and a Windows scrollbar
        spare = [height(c, checked) - measured(c) for c in cs]              # what most readers get
        worst = worst_case if worst is None else min(worst, worst_case)
        print(f"  {label:28s} {lo}–{hi}: {min(spare):5.1f} to {max(spare):5.1f}  (up to {max(spare) / rows:.1f} per row;"
              f" {worst_case:4.1f} at worst)")
    if worst < 0:
        print(f"  ! the formula is up to {-worst:.1f} px short somewhere")
        raise SystemExit(1)

    style = f"display:block; width:100%; height:{css_height(model)}; margin:40px 0; border:0;"
    shortcode = f'[iframe src="{URL}" title="{TITLE}" style="{style}" scrolling="auto" loading="lazy"][/iframe]'
    with open(os.path.join(ROOT, "embed-shortcode.txt"), "w", encoding="utf-8") as fh:
        fh.write(shortcode + "\n")

    test = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>2026_090 shortcode · test page</title>
  <link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400&display=swap" rel="stylesheet">
  <style>
    /* a stand-in for a Mongabay article: the theme's .ph--40 container and 780 px column, Public Sans 16/24 */
    body {{ margin: 0; background: #ffffff; color: #092f29; font: 16px/24px "Public Sans", sans-serif; }}
    .ph--40 {{ max-width: 1280px; margin: 0 auto; padding: 24px clamp(20px, 1px + 5vw, 40px); }}
    .inner {{ max-width: 780px; margin: 0 auto; }}
    .inner p {{ margin: 0 0 24px; }}
  </style>
</head>
<body>
<div class="ph--40"><div class="inner">
  <p>Article text before the graphic. This paragraph stands in for the story text above the embed.</p>
  <!-- the shortcode's output, with src pointing at this local copy -->
  <iframe src="../?fill=1" title="{TITLE}" style="{style}" scrolling="auto"></iframe>
  <p>Article text after the graphic. This paragraph shows the gap a reader sees below the embed.</p>
</div></div>
</body>
</html>
"""
    with open(os.path.join(HERE, "shortcode-test.html"), "w", encoding="utf-8") as fh:
        fh.write(test)
    print(f"\nwrote embed-shortcode.txt ({len(shortcode)} characters) and dev/shortcode-test.html")


if __name__ == "__main__":
    main()
