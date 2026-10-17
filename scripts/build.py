#!/usr/bin/env python3
"""Generate the static homepage from data/profile.json; Python standard library only."""
import argparse
import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = lambda value: html.escape(str(value), quote=True)


def external(url, label, css="", extra=""):
    return f'<a href="{E(url)}" target="_blank" rel="noopener noreferrer" class="{E(css)}" {extra}>{label}</a>'


def bibtex(paper):
    names = paper.get("bib_authors", paper["authors"])
    names = [n if "," in n else f'{n.split()[-1]}, {" ".join(n.split()[:-1])}' for n in names]
    rows = [("title", "{" + paper["title"] + "}"), ("author", " and ".join(names)),
            ("journal", paper["journal"]), ("year", str(paper["year"])), ("volume", paper["volume"])]
    if paper["number"]:
        rows.append(("number", paper["number"]))
    rows.extend([("pages", paper["pages"].replace("–", "--")), ("doi", paper["doi"])])
    return "@article{" + paper["id"] + ",\n" + ",\n".join(f"  {key} = {{{value}}}" for key, value in rows) + "\n}"


def authors(paper):
    return ", ".join(f'<strong>{E(name)}</strong>' if name in ("Ningyuan Xu", "Xu, N.", "Xu, Ningyuan") else E(name)
                     for name in paper.get("display_authors", paper["authors"]))


def journal(paper):
    issue = f'({E(paper["number"])})' if paper["number"] else ""
    return f'<em>{E(paper["journal"])}</em> {paper["year"]}, {E(paper["volume"])}{issue}, {E(paper["pages"])}.'


def make_head(p, title=None, path="/", description=None):
    title = title or f'{p["name"]} | Surface Science & Soft Matter'
    desc = description or p["description"]
    canonical = p["site_url"].rstrip("/") + path
    person = {"@context": "https://schema.org", "@type": "Person", "name": p["name"],
              "url": p["site_url"] + "/", "jobTitle": p["role"],
              "affiliation": {"@type": "CollegeOrUniversity", "name": p["affiliation"]},
              "sameAs": [x["url"] for x in p["profiles"]], "knowsAbout": p["interests"]}
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="author" content="{E(p['name'])}">
  <meta name="theme-color" content="#196659">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="{E(canonical)}">
  <link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/css/style.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{E(canonical)}">
  <meta property="og:image" content="{E(p['site_url'])}/assets/images/social-card.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ningyuan Xu — Surface science and computational soft matter">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{json.dumps(person, ensure_ascii=False).replace('<', chr(92) + 'u003c')}</script>
  <script src="assets/js/main.js" defer></script>
</head>'''


def footer(p):
    updated = date.fromisoformat(p["updated"]).strftime("%d %b %Y")
    return f'''<footer class="footer"><div class="wrap footer-inner">
      <span>© {p['updated'][:4]} {E(p['name'])} · Last updated {updated}</span>
      <div class="footer-links">{external('https://github.com/NingyuanXu0', 'GitHub ↗')}<a href="files/publications.bib" download>Bibliography ↓</a><a href="#top">Back to top ↑</a></div>
    </div></footer><div class="live-message" role="status" aria-live="polite" aria-atomic="true"></div>'''


def section_head(number, title, note=""):
    return f'<div class="section-top"><div class="section-heading"><span class="section-label">{number}</span><h2>{title}</h2></div>{note}</div>'


def make_home(p):
    profile_links = "".join(external(x["url"], f'<span class="profile-symbol" aria-hidden="true">{E(x["short"])}</span><span><span class="profile-name">{E(x["name"])}</span><span class="profile-detail">{E(x["detail"])}</span></span><span class="arrow" aria-hidden="true">↗</span>', "profile-link") for x in p["profiles"])
    interests = "".join(f'<li>{E(x)}</li>' for x in p["interests"])
    about = "".join(f'<p>{E(x)}</p>' for x in p["about"])
    research = ""
    for item in p["research"]:
        more_link = (" " + external(item["link"], "Read the paper ↗")) if item.get("link") else ""
        research += f'''<article class="research-card" id="research-{E(item['id'])}">
          <div class="research-image"><img src="{E(item['image'])}" alt="{E(item['alt'])}" width="320" height="210" loading="lazy"><small>CONCEPTUAL ILLUSTRATION</small></div>
          <div class="research-body"><p class="research-meta">{E(item['category'])}</p><h3>{E(item['title'])}</h3><p class="research-description">{E(item['description'])}</p>
            <div class="tags">{''.join(f'<span class="tag">{E(x)}</span>' for x in item['tags'])}</div>
            <div class="research-bottom"><span class="research-status">{E(item['status'])}</span></div>
            <details class="research-details"><summary>Research details</summary><p>{E(item['details'])}{more_link}</p></details>
          </div></article>'''
    papers = ""
    for item in p["publications"]:
        kind = "review" if item["type"] == "Review" else "research"
        first = '<span class="first-author">First author</span>' if item["first_author"] else ""
        papers += f'''<article class="publication" data-type="{kind}" id="{E(item['id'])}">
          <div class="pub-year">{item['year']}</div><div class="pub-body"><div class="pub-kicker"><span>{E(item['type'])}</span>{first}</div>
            <h3 class="pub-title">{external('https://doi.org/' + item['doi'], E(item['title']))}</h3>
            <p class="authors">{authors(item)}</p><p class="journal">{journal(item)}</p><p class="pub-summary">{E(item['summary'])}</p>
            <div class="pub-links">{external('https://doi.org/' + item['doi'], 'DOI ↗')}
              <details class="bibtex"><summary>BibTeX</summary><pre id="bib-{E(item['id'])}">{E(bibtex(item))}</pre><button type="button" class="copy-button" data-copy-target="bib-{E(item['id'])}">Copy BibTeX</button></details>
            </div></div></article>'''
    education = "".join(f'''<li><time>{E(x['dates'])}</time><h4>{E(x['school'])}</h4><p class="degree">{E(x['degree'])}</p><p class="note">{E(x['note'])}</p></li>''' for x in p["education"])
    experience = "".join(f'''<li><time>{E(x['dates'])}</time><h4>{E(x['title'])}</h4><p class="degree">{E(x['organisation'])}</p><p class="note">{E(x['note'])}</p></li>''' for x in p["appointments"])
    skills = "".join(f'<div class="skill"><h4>{E(x["label"])}</h4><p>{E(x["text"])}</p></div>' for x in p["skills"])
    honours = "".join(f'<li class="honour"><span class="honour-year">{E(x["year"])}</span><div><h3>{E(x["title"])}</h3><p>{E(x["detail"])}</p></div></li>' for x in p["honours"])
    emails = "".join(f'''<div class="academic-email"><div class="school-line">{E(x['school'])}<span>{E(x['period'])}</span></div>{''.join(f'<a href="mailto:{E(a)}">{E(a)}</a>' for a in x['addresses'])}</div>''' for x in p["academic_emails"])
    review_count = sum(x["type"] == "Review" for x in p["publications"])
    return make_head(p) + f'''
<body id="top"><a class="skip" href="#main">Skip to content</a>
  <header class="site-header"><div class="wrap header-inner">
    <a class="brand" href="#top" aria-label="Ningyuan Xu home"><span class="brand-mark" aria-hidden="true">nx</span><span class="brand-text">NINGYUAN XU</span></a>
    <nav class="site-nav" id="site-nav" aria-label="Main navigation"><a href="#about">About</a><a href="#research">Research</a><a href="#publications">Publications</a><a href="#background">Background</a><a href="#contact">Contact</a><a href="cv.html">CV ↗</a></nav>
    <div class="header-controls"><button type="button" class="icon-button theme-toggle" aria-label="Switch to dark theme" aria-pressed="false" title="Dark theme"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M20.5 14.5A9 9 0 0 1 9.5 3.5a9 9 0 1 0 11 11Z"/></svg></button><button type="button" class="icon-button menu-toggle" aria-label="Toggle navigation" aria-controls="site-nav" aria-expanded="false"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button></div>
  </div></header>
  <main id="main" class="wrap">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-copy"><p class="eyebrow"><span class="status-dot" aria-hidden="true"></span>M.SC. STUDENT · NTU, SINGAPORE</p><h1 id="hero-title">{E(p['name'])}</h1><p class="subtitle">{E(p['tagline'])}</p><p class="hero-intro">{E(p['intro'])}</p><div class="hero-actions"><a class="button" href="#research">Explore my research <span aria-hidden="true">↓</span></a><a class="text-link" href="mailto:{E(p['primary_email'])}">Get in touch <span class="arrow" aria-hidden="true">↗</span></a></div></div>
      <figure class="hero-figure"><div class="figure-frame"><div class="micro"><span>STRUCTURE · INTERACTION · FUNCTION</span><span>NX / 01</span></div><img src="assets/images/interface.svg" width="420" height="375" alt="Conceptual illustration connecting a water droplet on a structured surface with a collection of polyhedral particles."></div><figcaption><span>Interfaces, from surfaces to assemblies.</span><span>Conceptual illustration</span></figcaption></figure>
    </section>
    <div class="profile-bar" aria-label="Academic profiles">{profile_links}</div>
    <section id="about" class="section" aria-labelledby="about-heading">
      {section_head('01', '<span id="about-heading">About</span>', '<a href="cv.html" class="text-link">View academic CV <span aria-hidden="true">↗</span></a>')}
      <div class="about-grid"><div class="about-copy">{about}</div><aside class="interest-panel"><h3>Research interests</h3><ul>{interests}</ul></aside></div>
    </section>
    <section id="research" class="section" aria-labelledby="research-heading">
      {section_head('02', '<span id="research-heading">Research</span>', '<span class="section-note">Experiment & computation</span>')}
      <div class="research-list">{research}</div>
    </section>
    <section id="publications" class="section" aria-labelledby="publications-heading">
      {section_head('03', '<span id="publications-heading">Publications</span>', external(p['profiles'][0]['url'], 'Google Scholar <span aria-hidden="true">↗</span>', 'text-link'))}
      <div class="filters" role="group" aria-label="Filter publications"><button type="button" class="filter" data-filter="all" aria-pressed="true">All publications ({len(p['publications'])})</button><button type="button" class="filter" data-filter="review" aria-pressed="false">Reviews ({review_count})</button><button type="button" class="filter" data-filter="research" aria-pressed="false">Research articles ({len(p['publications']) - review_count})</button></div>
      <div class="publications-list">{papers}</div>
    </section>
    <section id="background" class="section" aria-labelledby="background-heading">
      {section_head('04', '<span id="background-heading">Background</span>')}
      <div class="background-grid"><div><h3 class="column-heading">Education</h3><ol class="timeline">{education}</ol></div><div><h3 class="column-heading">Research & teaching</h3><ol class="timeline">{experience}</ol></div></div>
      <div class="skills-grid">{skills}</div>
    </section>
    <section id="honours" class="section" aria-labelledby="honours-heading">
      {section_head('05', '<span id="honours-heading">Selected honours</span>')}
      <ul class="honours-grid">{honours}</ul>
    </section>
    <section id="contact" class="section contact" aria-labelledby="contact-heading">
      {section_head('06', '<span id="contact-heading">Contact</span>', '<span class="section-note">Singapore</span>')}
      <div class="contact-panel"><div class="contact-intro"><h3>Research conversations welcome.</h3><p>For research enquiries and academic correspondence, please use my personal email.</p><a class="primary-email" href="mailto:{E(p['primary_email'])}">{E(p['primary_email'])}</a><a class="email-secondary" href="mailto:{E(p['secondary_email'])}">{E(p['secondary_email'])}</a><div class="email-tools"><button type="button" class="copy-button" data-copy-text="{E(p['primary_email'])}">Copy primary email</button><a href="mailto:{E(p['primary_email'])}" class="text-link">Write an email <span aria-hidden="true">↗</span></a></div></div>
        <div class="academic-emails"><h3>Academic email addresses</h3><p>Listed in order of study: UESTC → Glasgow → NTU.</p>{emails}</div>
      </div>
    </section>
  </main>
  {footer(p)}
</body></html>'''


def make_cv(p):
    edu = "".join(f'<div class="cv-entry"><h3>{E(x["school"])}</h3><time>{E(x["dates"])}</time><p>{E(x["degree"])}</p><p>{E(x["note"])}</p></div>' for x in p["education"])
    jobs = "".join(f'<div class="cv-entry"><h3>{E(x["title"])} · {E(x["organisation"])}</h3><time>{E(x["dates"])}</time><p>{E(x["note"])}</p></div>' for x in p["appointments"])
    research = "".join(f'<div class="cv-entry"><h3>{E(x["title"])}</h3><p>{E(x["details"])}</p></div>' for x in p["research"])
    pubs = "".join(f'<li class="cv-publication">{authors(x)}. {external("https://doi.org/" + x["doi"], E(x["title"]))}. {journal(x)} DOI: {E(x["doi"])}.</li>' for x in p["publications"])
    honours = "".join(f'<li>{E(x["title"])} — {E(x["detail"])} ({E(x["year"])}).</li>' for x in p["honours"])
    skills = "".join(f'<p><strong>{E(x["label"])}:</strong> {E(x["text"])}</p>' for x in p["skills"])
    profiles = "".join(external(x["url"], E(x["name"]) + " ↗") for x in p["profiles"])
    return make_head(p, p["name"] + " | Academic CV", "/cv.html") + f'''<body id="top"><main class="wrap cv-page"><div class="cv-toolbar"><a href="index.html" class="text-link">← Back to homepage</a><button type="button" class="button" data-print>Print / Save as PDF</button></div><header class="cv-head"><h1>{E(p['name'])}</h1><p>{E(p['role'])} · {E(p['affiliation'])}, {E(p['location'])}<br><a href="mailto:{E(p['primary_email'])}">{E(p['primary_email'])}</a> · <a href="{E(p['site_url'])}">{E(p['site_url'].removeprefix('https://'))}</a></p><div class="cv-profiles">{profiles}</div></header>
    <section class="cv-section"><h2>Research profile</h2><p>{E(p['intro'])}</p></section>
    <section class="cv-section"><h2>Education</h2>{edu}</section>
    <section class="cv-section"><h2>Research & teaching appointments</h2>{jobs}</section>
    <section class="cv-section"><h2>Selected research experience</h2>{research}</section>
    <section class="cv-section"><h2>Peer-reviewed publications</h2><ol class="cv-list">{pubs}</ol></section>
    <section class="cv-section"><h2>Technical skills</h2>{skills}</section>
    <section class="cv-section"><h2>Selected honours</h2><ul class="cv-list">{honours}</ul></section>
    <p class="cv-footnote">Public academic CV · Updated {E(p['updated'])}</p>
  </main><div class="live-message" role="status" aria-live="polite" aria-atomic="true"></div></body></html>'''


def validate_profile(p):
    if len({x["id"] for x in p["publications"]}) != len(p["publications"]):
        raise ValueError("Publication IDs must be unique")
    for link in p["profiles"]:
        if not link["url"].startswith("https://"):
            raise ValueError("Academic profile URLs must use HTTPS")
    for item in p["publications"]:
        if not item["doi"].startswith("10."):
            raise ValueError("Invalid DOI")
    date.fromisoformat(p["updated"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT, help="Output directory; defaults to repository root")
    args = parser.parse_args()
    out = args.output.resolve()
    if out == ROOT.parent or out in ROOT.parents:
        raise SystemExit("Refusing to write above the project root")
    p = json.loads((ROOT / "data/profile.json").read_text(encoding="utf-8"))
    validate_profile(p)
    out.mkdir(parents=True, exist_ok=True)
    if out != ROOT:
        shutil.copytree(ROOT / "assets", out / "assets", dirs_exist_ok=True)
    (out / "files").mkdir(exist_ok=True)
    (out / "index.html").write_text(make_home(p), encoding="utf-8")
    (out / "cv.html").write_text(make_cv(p), encoding="utf-8")
    all_bib = "\n\n".join(bibtex(x) for x in p["publications"]) + "\n"
    (out / "files/publications.bib").write_text(all_bib, encoding="utf-8")
    for paper in p["publications"]:
        (out / f'files/{paper["id"]}.bib').write_text(bibtex(paper) + "\n", encoding="utf-8")
    (out / ".nojekyll").touch()
    (out / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {p["site_url"]}/sitemap.xml\n', encoding="utf-8")
    urls = "".join(f'<url><loc>{E(p["site_url"] + path)}</loc><lastmod>{p["updated"]}</lastmod></url>' for path in ("/", "/cv.html"))
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (out / "404.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Ningyuan Xu</title><style>body{background:#fafaf7;color:#1d302f;font:16px/1.7 system-ui;margin:0;min-height:100vh;display:grid;place-items:center}main{max-width:480px;padding:35px}h1{font:52px Georgia,serif;margin:12px 0}small{font:12px monospace;color:#196659}a{color:#196659;text-underline-offset:5px}</style></head><body><main><small>404 / NINGYUAN XU</small><h1>Page not found.</h1><p>The page may have moved. You can find my research, publications and contact details on the homepage.</p><a href="https://ningyuanxu0.github.io/">Return to homepage →</a></main></body></html>''', encoding="utf-8")
    print(f"Built homepage, CV, bibliography and metadata in {out}")


if __name__ == "__main__":
    main()
