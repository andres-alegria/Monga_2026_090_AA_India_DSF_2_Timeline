# 2026_090 · India's deep-sea fishing policy: 1950s to present

An interactive timeline for a Mongabay story. The 11 policy shifts sit on a shared 1950–2027 time axis, and the chosen
one's full text appears in a reading card. Choosing a period never changes the page's height; only the width does.
Live at https://monga2026090aaindiadsf2timeline.vercel.app

## Files

| File | What it holds |
|---|---|
| `index.html` | Page skeleton, and the static fallback for browsers without JavaScript |
| `content.js` | All the text, verbatim from the reporter's brief, plus the axis and the interface labels |
| `style.css` | Mongabay Design System colours, type and layout. Tweak points are commented |
| `app.js` | Drawing, choosing a period, and the `?fill=1` mode |
| `assets/` | The lizard mark, the Phosphor icons (MIT licence), and the static fallback image |
| `make_embed.py` | Writes the fallback image's alt text into `index.html`, and swaps in a new image if given one |
| `embed-shortcode.txt` | **The WordPress embed: paste its contents into the post.** Built by `dev/embed_shortcode.py` |
| `dev/` | `measure.html` and `heights.json` (the timeline's height at every column width), `embed_shortcode.py`, and `shortcode-test.html`, a stand-in Mongabay article |

## Embedding in a Mongabay post

Mongabay posts take only the `[iframe]` shortcode, so the frame's height can't come from a script. Instead, the
shortcode's `style` works it out with a CSS formula:
- it gets the article column's width from the screen width, using Mongabay's theme rule;
- it gives a height a few pixels taller than the timeline needs at that width.

`?fill=1` in the URL makes the timeline stretch to fill the frame. The spare pixels are shared out between the rows
of the list, so they don't show as a gap. Inside an iframe the page also drops its side padding, so the title, panel
and source line up with the story text, as in 089. On 30 Sep 2026 it was checked from 320 to 1,600 px screen widths:
- the spare is at most 43 px (3.9 px per row), and 4 px on desktop;
- nothing overflows;
- 40 px to the next paragraph, as with Mongabay's figures.

Don't reuse another graphic's shortcode: the formula is fitted to this timeline's heights.

**When the content changes** (text, sizes or fonts), the heights change too:
1. Serve the repo root with `python3 -m http.server` and open `/dev/measure.html`. It measures every column width, with
   Rowan and with its Georgia fallback.
2. Save the JSON it prints as `dev/heights.json`.
3. Run `python3 dev/embed_shortcode.py`. It refits the formula, checks every screen width, and writes
   `embed-shortcode.txt` and `dev/shortcode-test.html`.
4. Replace the shortcode in the post.

## Fonts

Public Sans loads from Google Fonts. Rowan comes from the reader's installed copy or, failing that, from Mongabay's
own theme font, which the theme's server allows other sites to load.
