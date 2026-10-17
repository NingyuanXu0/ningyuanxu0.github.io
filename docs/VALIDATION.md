# Release validation

Updated on 17 October 2026 for the readability, supervisor, patent, authorship, journal-metric and blue-theme revisions.

## Source checks

- Generated homepage, CV, bibliography, sitemap and 404 page with the standard-library Python builder.
- Checked local assets, internal anchors, duplicate IDs, headings, JSON-LD, sitemap XML and SVG XML.
- Checked all six owner email addresses and four academic/social profiles.
- Checked three supervisors' email, group and Google Scholar destinations in both the homepage and CV.
- Checked all three patent application entries and both public patent records in the homepage and CV.
- Checked the three published-paper BibTeX records.
- Checked complete author lists with 5, 12 and 9 names, owner positions 1, 6 and 3, and explicit first-author/co-author labels in the homepage and CV.
- Checked 2025 JIF values 23.7, 11.8 and 17.3, 2026 JCR Q1 labels and metric-source links.
- Regenerated the blue SVG illustrations and 1200 × 630 PNG social preview; synchronized the favicon, browser theme colour and custom 404 palette.
- Checked light and dark text colours against the page, surface and label backgrounds: all normal-text combinations exceed the WCAG AA 4.5:1 contrast threshold (minimum 6.07:1).
- JavaScript syntax and whitespace checks are run before publishing.

## Browser checks

- Inspected desktop rendering at 1280px and phone rendering at 390px, including the dark theme.
- Checked 320, 390, 768, 1024 and 1280px widths without horizontal overflow.
- Confirmed 18px Arial body text on desktop, 17px on phones, 16px navigation and author text, and 15px research metadata.
- Exercised mobile menu opening and closing, theme switching and BibTeX expansion; the browser reported successful citation copying.
- Checked supervisor cards, patent records and the expandable academic email list.
- Checked the CV in desktop and phone layouts before release.
- Rechecked the blue revision in desktop light/dark views and 390px homepage/CV views; no horizontal overflow.

## Content verification

Supervisor contact information was checked against NTU, X-MOL and UESTC faculty pages. Patent details were checked against the owner's two CNIPA application publications and the CNIPA acceptance notice. The high-reflectivity coating application number and co-inventor were corrected from the older CV to match the official publication.

Public record links identify published patent applications. External profile services control their own availability and login requirements. Email links provide contact destinations; mailbox delivery is outside these checks.

## Publishing

GitHub Pages serves the repository's main branch root over HTTPS. The deployment workflow and the live generated files are verified against the release commit when this revision is published.
