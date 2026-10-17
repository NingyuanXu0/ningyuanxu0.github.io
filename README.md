# Ningyuan Xu · Academic Homepage

A static academic homepage for Ningyuan Xu, M.Sc. student in Chemical Modelling at Nanyang Technological University, Singapore.

**Live website:** https://ningyuanxu0.github.io/

中文维护说明见 [START_HERE_zh.md](START_HERE_zh.md)。

## Content and design

- A concise homepage covering two research areas, three published papers, three first-inventor patent applications, education and research appointments.
- Complete author names in publication order, with Ningyuan Xu's position shown on every paper: 1/5, 6/12 and 3/9.
- Linked 2025 Journal Impact Factors and 2026 JCR quartiles in the homepage and CV.
- Supervisor email, group website and Google Scholar links for Ran Ni, Dehui Wang and Xu Deng.
- Arial/Helvetica body text with Georgia headings. Body text is 18px on desktop and 17px on phones; navigation is 16px and secondary text is generally 15–17px.
- A full, printable academic CV at `cv.html`, retaining detailed research, teaching, skills and selected honours.
- Google Scholar, ORCID, ResearchGate and GitHub profile links.
- All six owner email addresses. Additional academic addresses are available in an expandable contact section.
- DOI links, BibTeX display, copy and downloads; public records for the two published patent applications.
- Responsive navigation, light/dark themes, keyboard focus styles and reduced-motion support.
- Search/social metadata, sitemap, robots.txt, favicon and a custom 404 page.
- Local fonts and static files; no third-party scripts, analytics, forms or runtime framework.

## Edit and publish

GitHub Pages serves `main` → `/(root)` with HTTPS enabled. The generated HTML is committed alongside its editable source.

1. Edit `data/profile.json`.
2. Run the generator and release checks with Python 3.9 or newer:

   ```bash
   python3 scripts/build.py
   python3 scripts/check.py
   ```

3. Commit the JSON and regenerated files, then push to `main`. GitHub Pages publishes the new commit automatically.

The browser reads the generated HTML directly. Content remains available with JavaScript disabled.

To generate a separate deployment directory:

```bash
python3 scripts/build.py --output _site
python3 scripts/check.py _site
```

## File map

| File | Purpose |
| --- | --- |
| `data/profile.json` | Profile, papers, patents, supervisors, education and contacts |
| `scripts/build.py` | Standard-library Python generator for HTML, bibliography and metadata |
| `scripts/check.py` | Release checks for content, links, local assets and structured data |
| `index.html` | Generated homepage |
| `cv.html` | Generated public academic CV |
| `assets/css/style.css` | Typography, layout, responsive rules and print styling |
| `assets/js/main.js` | Navigation, theme, citation copy and print controls |
| `files/` | Published-paper BibTeX records |
| `assets/images/` | Favicon, social preview and original optional illustrations |
| `docs/REFERENCES.md` | Design references and sources used to verify added information |
| `docs/VALIDATION.md` | Release verification record |

Use `show_on_homepage` to select featured research and appointments while retaining full entries in the CV. Supervisor contact records are stored under `supervisors`; patent bibliography and filing/publication records are stored under `patents`.

Each publication's `authors` is the full ordered list; `author_position` is one-based and is checked against Ningyuan Xu's name. `journal_metrics` records the JIF data year, JCR release year, value, quartile and source links. Update the metric years together when adopting a later JCR release.

## Sources and licensing

Academic facts derive from the owner's CV and supplied records. Patent application numbers, dates and inventor order were checked against the supplied CNIPA publication documents and acceptance notice. Public patent links refer to application publications. See `docs/REFERENCES.md` for the correction to the high-reflectivity coating entry and the supervisor sources.

The original design references include Academic Pages, al-folio and Jon Barron's homepage. The site uses its own implementation.

Implementation code and original illustrations are covered by the MIT licence in `LICENSE`. The licence does not newly relicense personal biographical information, publication titles or third-party names. Publisher article PDFs and the supplied administrative receipt are not included in the repository.
