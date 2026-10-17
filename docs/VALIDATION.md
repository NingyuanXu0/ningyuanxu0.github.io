# Release validation

Prepared on 17 October 2026.

## Checked

- Python source compilation and generation of `index.html`, `cv.html`, bibliography and metadata.
- JavaScript syntax with `node --check assets/js/main.js`.
- Three generated HTML documents, a unique primary heading in each, duplicate IDs, image alt text and dimensions.
- Local image, stylesheet, script and file destinations, plus internal section anchors.
- All six email addresses exactly as supplied, including the case of the NTU address.
- All four requested academic/social destinations in the homepage.
- Three published papers with DOI links and three BibTeX records.
- JSON-LD parseability, sitemap XML, SVG XML and social image presence.
- A clean deploy-only output can be generated with the included builder and checked independently.

## Verification limits

Browser rendering and interactive behaviour were not exercised in this execution environment because the supported browser QA capability was unavailable. Responsive layout and accessibility features are implemented in the source; the static checks do not establish a rendered browser result.

GitHub repository creation, a GitHub Pages deployment and a successful public HTTP response have not been verified by this source-package validation. The target URL is not evidence of an active deployment.

Profile URLs were preserved from the owner's request. Google Scholar, ResearchGate, ORCID and publisher sites may impose their own login or access controls; the static checks do not assert that every external page can be fetched anonymously. Email links do not establish mailbox deliverability.
