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
- Matching Gmail/Outlook type sizes and a public guestbook in Contact. Visitors read recent messages on the homepage and post through GitHub.
- DOI links, BibTeX display, copy and downloads; public records for the two published patent applications.
- Responsive navigation, light/dark themes, keyboard focus styles and reduced-motion support.
- An academic blue palette across links, author labels, the CV, favicon and social preview, with a navy dark theme.
- Search/social metadata, sitemap, robots.txt, favicon and a custom 404 page.
- Local fonts and static files; no third-party scripts, analytics or runtime framework. The guestbook reads the public GitHub API.

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
| `assets/js/guestbook.js` | Recent public guestbook messages, lazy loading and retry |
| `.github/ISSUE_TEMPLATE/guestbook.yml` | Labelled GitHub message form for visitors |
| `files/` | Published-paper BibTeX records |
| `assets/images/` | Favicon, social preview and original optional illustrations |
| `docs/REFERENCES.md` | Design references and sources used to verify added information |
| `docs/VALIDATION.md` | Release verification record |

Use `show_on_homepage` to select featured research and appointments while retaining full entries in the CV. Supervisor contact records are stored under `supervisors`; patent bibliography and filing/publication records are stored under `patents`.

Research entries can use `homepage_experience` for an additional paragraph describing experimental experience. The UESTC entry covers surface/interfacial physical chemistry and particle/coating preparation at laboratory and production scales.

Each publication's `authors` is the full ordered list; `author_position` is one-based and is checked against Ningyuan Xu's name. `journal_metrics` records the JIF data year, JCR release year, value, quartile and source links. Update the metric years together when adopting a later JCR release.

## Guestbook

The `guestbook` configuration identifies the repository and label. The homepage displays the five newest open issues with the `guestbook` label; GitHub handles posting, account sign-in and replies. The dedicated issue template applies this label. Close an issue or remove the label to hide it from the homepage. No access token is included in the site.

Messages load when the guestbook approaches the viewport and are rendered as plain text. A refresh button and GitHub links remain available if the public API is unavailable or rate-limited. Visitors can read messages without signing in; posting requires a GitHub account. Private enquiries use the email links.

## Sources and licensing

Academic facts derive from the owner's CV and supplied records. Patent application numbers, dates and inventor order were checked against the supplied CNIPA publication documents and acceptance notice. Public patent links refer to application publications. See `docs/REFERENCES.md` for the correction to the high-reflectivity coating entry and the supervisor sources.

The original design references include Academic Pages, al-folio and Jon Barron's homepage. The site uses its own implementation.

Implementation code and original illustrations are covered by the MIT licence in `LICENSE`. The licence does not newly relicense personal biographical information, publication titles or third-party names. Publisher article PDFs and the supplied administrative receipt are not included in the repository.
