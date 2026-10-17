# Ningyuan Xu · Academic Homepage

A responsive academic homepage for **Ningyuan Xu**, M.Sc. student in Chemical Modelling at Nanyang Technological University, Singapore.

**Target public URL after deployment:** https://ningyuanxu0.github.io/

**GitHub account:** https://github.com/NingyuanXu0

中文发布和维护指南见 [START_HERE_zh.md](START_HERE_zh.md)。

## Publish on GitHub Pages

The repository contains complete, pre-generated HTML. No installation or build is required to publish it.

1. In the `NingyuanXu0` account, create a **public** repository named **`ningyuanxu0.github.io`**.
2. Upload the **contents** of this directory. `index.html` must be in the repository root.
3. Go to **Settings → Pages → Build and deployment → Source → Deploy from a branch**.
4. Select **main**, then **/(root)**, and click **Save**.
5. Wait for GitHub's Pages deployment to succeed. The public homepage will be at **https://ningyuanxu0.github.io/**.

If that repository already exists, inspect its current contents before adding this site. This source package does not assume the repository is empty or overwrite any existing GitHub content.

## Included

- English academic homepage with About, Research, Publications, Background, Honours and Contact sections.
- Responsive desktop/mobile layout, keyboard navigation, light/dark theme and reduced-motion support.
- Four requested profiles: Google Scholar, ORCID, ResearchGate and GitHub.
- All six supplied email addresses. Academic addresses appear in study order: UESTC, Glasgow, then NTU. UESTC and Glasgow were a joint programme during 2022–2026.
- Three published journal articles, DOI links, publication filters and BibTeX export/copy.
- A printable public academic CV at `cv.html`.
- Original conceptual SVG illustrations. These are visual motifs, not experimental data.
- Search/social metadata, Person structured data, sitemap, robots.txt, favicon and a 404 page.
- No external fonts, third-party scripts, analytics, forms or runtime framework.

## File map

| File | Purpose |
| --- | --- |
| `index.html` | Complete, pre-generated homepage; can be opened locally |
| `cv.html` | Public academic CV; print or save as PDF in the browser |
| `data/profile.json` | Main editable source for profile, research, education, publications and contacts |
| `assets/css/style.css` | Layout, responsive rules, colour themes and print styling |
| `assets/js/main.js` | Optional navigation, theme, filter and copy interactions |
| `assets/images/` | Original illustrations, favicon and social sharing image |
| `files/publications.bib` | All published articles in BibTeX |
| `scripts/build.py` | Standard-library Python generator |
| `scripts/check.py` | Static release checks |
| `scripts/draw_assets.py` | Optional illustration generation; assets are already included |
| `START_HERE_zh.md` | Chinese publishing and maintenance guide |
| `docs/REFERENCES.md` | Academic website examples and official deployment sources |
| `docs/VALIDATION.md` | What was verified and the remaining verification limits |

## Edit the content

Use Python **3.9 or newer**. The site generator and static checks have no third-party dependencies.

```bash
python3 scripts/build.py
python3 scripts/check.py
```

Edit `data/profile.json`, run those two commands, and commit the JSON plus the regenerated HTML, BibTeX and metadata. The browser does not fetch the JSON: all academic content remains visible when JavaScript is disabled.

Open `index.html` directly to review the local version. You can also use any static HTTP server in your own development environment. The copy buttons require the browser's clipboard permission or a secure context; text selection and the `.bib` download remain available.

To produce a clean deploy-only directory:

```bash
python3 scripts/build.py --output _site
python3 scripts/check.py _site
```

Upload the contents of `_site` if you only want to host the generated website. Keep the editable source separately in your repository if you choose that arrangement.

## Design references

This is an original static implementation informed by the content organisation and source examples in [Academic Pages](https://github.com/academicpages/academicpages.github.io), [al-folio](https://github.com/alshedivat/al-folio), and [Jon Barron's academic homepage](https://github.com/jonbarron/jonbarron.github.io). It does not depend on, fork, or include their theme implementation. See [docs/REFERENCES.md](docs/REFERENCES.md) for the specific source files examined.

## Content and licensing

The initial academic facts were prepared from the owner's CV dated 14 October 2026 and the links and contact addresses supplied by the owner. Publication DOIs were checked against publisher/indexing records. Manuscripts in preparation are not listed as published papers. Citation counts are linked through Google Scholar rather than embedded as a potentially stale number.

The implementation code and original illustrations are available under the MIT licence in `LICENSE`. Personal biographical information, publication titles and third-party names are not newly relicensed by this code licence. No publisher figures or article PDFs are bundled.
