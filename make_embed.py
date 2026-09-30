#!/usr/bin/env python3
"""
Mongabay 2026_090 - embed kit for the interactive timeline.

- Copies the static graphic to assets/static-fallback.png: index.html shows it to readers without JavaScript.
- Writes that image's alt text into index.html, from content.js.
- Writes embed.html, the code to paste into a WordPress Custom HTML block.

Run it after fig1_build.py, and again whenever content.js, the static graphic or the URL below changes.

    python3 make_embed.py
"""
import html
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- settings
EMBED_URL = "https://YOUR-HOST/2026_090_timeline/index.html"   # where index.html will be hosted: set before pasting
SECRET = "dsf090"             # links the iframe to its height messages; letters and digits only, unique on the page
INITIAL_HEIGHT = 930          # px: the height the iframe keeps if nothing on the page resizes it (the tallest
                              # layout, a 320 px phone, measures 924 px)
# the static graphic; point this at the final JPG once it is exported from Illustrator
FALLBACK_SRC = os.path.join(HERE, "..", "output", "Fig_1_India_DSF_policy_timeline_preview.png")


def load_js(path):
    """The JSON object assigned in a content.js-style file."""
    return json.loads(re.search(r"=\s*(\{.*\})\s*;\s*$", open(path, encoding="utf-8").read(), re.S).group(1))


C = load_js(os.path.join(HERE, "content.js"))


def main():
    # 1. fallback image, under a fixed name so index.html doesn't change when the source does
    ext = os.path.splitext(FALLBACK_SRC)[1].lower()
    fallback = "assets/static-fallback" + ext
    for old in ("assets/static-fallback.png", "assets/static-fallback.jpg"):
        if old != fallback and os.path.exists(os.path.join(HERE, old)):
            os.remove(os.path.join(HERE, old))
    shutil.copyfile(FALLBACK_SRC, os.path.join(HERE, fallback))

    # 2. alt text: the title, then every period and its title, verbatim from content.js
    alt = C["title"] + ". " + " ".join(f"{e['date']}: {e['title']}." for e in C["events"])
    block = (f'<noscript><img class="tl-fallback" src="{fallback}" width="1350" height="1080" '
             f'alt="{html.escape(alt, quote=True)}"></noscript>')
    path = os.path.join(HERE, "index.html")
    page = open(path, encoding="utf-8").read()
    page, n = re.subn(r"(<!-- fallback:start[^>]*-->\s*).*?(\s*<!-- fallback:end -->)",
                      lambda m: m.group(1) + block + m.group(2), page, flags=re.S)
    if n != 1:
        raise SystemExit("index.html: fallback markers not found")
    open(path, "w", encoding="utf-8").write(page)

    # 3. the WordPress embed code
    title = html.escape(f"{C['title']} (interactive timeline)", quote=True)
    snippet = f"""<!-- Mongabay 2026_090: {C['title']}. Paste into a Custom HTML block. -->
<iframe title="{title}" src="{EMBED_URL}#?secret={SECRET}" data-secret="{SECRET}"
  width="100%" height="{INITIAL_HEIGHT}" frameborder="0" scrolling="no" loading="lazy"></iframe>
<script>
/* Fits the iframe to the timeline's height. WordPress's own wp-embed.js does the same when the story also has a
   related-story card; this covers stories without one. If the script is removed, the iframe keeps its height. */
window.addEventListener("message", function (e) {{
  var d = e.data;
  if (!d || d.message !== "height" || d.secret !== "{SECRET}") return;
  var f = document.querySelector('iframe[data-secret="{SECRET}"]');
  if (f && e.source === f.contentWindow) f.height = d.value;
}});
</script>
"""
    open(os.path.join(HERE, "embed.html"), "w", encoding="utf-8").write(snippet)
    print(f"wrote {fallback}, the alt text in index.html, and embed.html (URL: {EMBED_URL})")
    if "YOUR-HOST" in EMBED_URL:
        print("NOTE: set EMBED_URL at the top of this script to the hosted address before pasting embed.html")


if __name__ == "__main__":
    main()
