# Ningyuan Xu

Academic website of Ningyuan Xu, featuring research in surface and interface science, colloidal assembly, and computational soft matter.

- [Visit the website](https://ningyuanxu.com/)
- [Academic CV](https://ningyuanxu.com/cv.html)
- [Contact and guestbook](https://ningyuanxu.com/#contact)

## Project structure

| Path | Purpose |
| --- | --- |
| `data/profile.json` | Single source of truth for all page content |
| `scripts/build.py` | Generates `index.html`, `cv.html`, `404.html`, BibTeX files, `sitemap.xml` and `robots.txt` |
| `scripts/check.py` | Release checks: links, anchors, metadata, contact details and bibliography |
| `scripts/draw_assets.py` | Regenerates the conceptual SVG illustrations and social card |
| `assets/css/style.css` | Design tokens, light/dark themes, responsive layout and print styles |
| `assets/js/` | Progressive enhancements (theme, navigation, copy buttons, guestbook, analytics) |

## Development

The site is static and needs only the Python standard library (3.9+).

```bash
python3 scripts/build.py          # regenerate the pages after editing data/profile.json
python3 scripts/check.py          # validate the generated site
python3 -m http.server 8000       # preview at http://localhost:8000
```

Edit content in `data/profile.json` and templates in `scripts/build.py`; the HTML files in the repository root are build output and should not be edited by hand.
