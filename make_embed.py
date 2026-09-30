#!/usr/bin/env python3
"""
Mongabay 2026_090 - static fallback for the interactive timeline.

- Optionally copies a new static graphic to assets/static-fallback.png (or .jpg): index.html shows it to readers
  without JavaScript.
- Writes that image's alt text into index.html, from content.js.

Run it whenever content.js or the static graphic changes. The WordPress shortcode is built by dev/embed_shortcode.py.

    python3 make_embed.py                      # alt text only, keeps the current image
    python3 make_embed.py path/to/graphic.jpg  # also replaces the image, e.g. with the final JPG from Illustrator
"""
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_js(path):
    """The JSON object assigned in a content.js-style file."""
    return json.loads(re.search(r"=\s*(\{.*\})\s*;\s*$", open(path, encoding="utf-8").read(), re.S).group(1))


C = load_js(os.path.join(HERE, "content.js"))


def main():
    # 1. fallback image, under a fixed name so index.html doesn't change when the source does
    if len(sys.argv) > 1:
        src = sys.argv[1]
        fallback = "assets/static-fallback" + os.path.splitext(src)[1].lower()
        for old in ("assets/static-fallback.png", "assets/static-fallback.jpg"):
            if old != fallback and os.path.exists(os.path.join(HERE, old)):
                os.remove(os.path.join(HERE, old))
        shutil.copyfile(src, os.path.join(HERE, fallback))
    else:
        fallback = next(f for f in ("assets/static-fallback.png", "assets/static-fallback.jpg")
                        if os.path.exists(os.path.join(HERE, f)))

    # 2. alt text: the title, then every period and its title, verbatim from content.js
    alt = C["title"] + ". " + " ".join(f"{e['date']}: {e['title']}." for e in C["events"])
    block = (f'<noscript><img class="tl-fallback" src="{fallback}" width="1350" height="1080" '
             f'alt="{html.escape(alt, quote=True)}"></noscript>')
    path = os.path.join(HERE, "index.html")
    page = open(path, encoding="utf-8").read()
    page, n = re.subn(r"(<!-- fallback:start[^>]*-->).*?(<!-- fallback:end -->)",
                      lambda m: f"{m.group(1)}\n    {block}\n    {m.group(2)}", page, flags=re.S)
    if n != 1:
        raise SystemExit("index.html: fallback markers not found")
    open(path, "w", encoding="utf-8").write(page)
    print(f"wrote the alt text for {fallback} into index.html")


if __name__ == "__main__":
    main()
