#!/usr/bin/env python3
"""Generate the static homepage from data/profile.json; Python standard library only."""
import argparse
import html
import json
import re
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
    return f'''<footer class="footer"><div class="wrap footer-inner"><span>© {p['updated'][:4]} {E(p['name'])} · Updated {updated}</span><a href="#top">Back to top ↑</a></div></footer><div class="live-message" role="status" aria-live="polite" aria-atomic="true"></div>'''


def section_head(title, note=""):
    return f'<div class="section-top"><h2>{title}</h2>{note}</div>'


def human_date(value):
    return date.fromisoformat(value).strftime("%d %b %Y")


def make_supervisors(p, heading_level=4):
    cards = []
    for person in p["supervisors"]:
        cards.append(f'''<article class="supervisor" id="supervisor-{E(person['id'])}">
          <h{heading_level}>{E(person['title'])} {E(person['name'])}</h{heading_level}>
          <p class="supervisor-role">{E(person['role'])} · {E(person['affiliation'])}</p>
          <a class="supervisor-email" href="mailto:{E(person['email'])}">{E(person['email'])}</a>
          <div class="supervisor-links">{external(person['group_url'], 'Group website ↗')}{external(person['scholar_url'], 'Google Scholar ↗')}</div>
        </article>''')
    return '<div class="supervisor-grid">' + "".join(cards) + '</div>'


def make_patents(p):
    entries = []
    for item in p["patents"]:
        title = external(item["url"], E(item["title"])) if item["url"] else E(item["title"])
        inventors = authors({"authors": item["inventors"]})
        publication = ""
        if item["publication_number"]:
            publication = f'<p class="patent-record">Published {human_date(item["publication_date"])} · {external(item["url"], E(item["publication_number"]))}</p>'
        elif item["status"] == "Application accepted":
            publication = '<p class="patent-record">Application accepted</p>'
        entries.append(f'''<article class="patent" id="{E(item['id'])}">
          <div class="pub-year">{item['year']}</div>
          <div class="patent-body">
            <h3 class="patent-title">{title}</h3>
            <p class="authors">{inventors}</p>
            <p class="patent-record">Application No. <span class="record-number">{E(item['application_number'])}</span> · Filed {human_date(item['filing_date'])}</p>
            {publication}
          </div>
        </article>''')
    return '<div class="patent-list">' + "".join(entries) + '</div>'


def make_home(p):
    profile_links = "".join(external(x["url"], E(x["name"]) + ' ↗') for x in p["profiles"])
    research = ""
    for item in p["research"]:
        if not item.get("show_on_homepage", True):
            continue
        research += f'''<article class="research-card" id="research-{E(item['id'])}">
          <p class="research-context">{E(item['status'])}</p>
          <h3>{E(item.get('homepage_title', item['title']))}</h3>
          <p>{E(item.get('homepage_description', item['description']))}</p>
        </article>'''
    papers = ""
    for item in p["publications"]:
        first = '<span class="first-author">First author</span>' if item["first_author"] else ""
        papers += f'''<article class="publication" id="{E(item['id'])}">
          <div class="pub-year">{item['year']}</div>
          <div class="pub-body">
            <div class="pub-kicker"><span>{E(item['type'])}</span>{first}</div>
            <h3 class="pub-title">{external('https://doi.org/' + item['doi'], E(item['title']))}</h3>
            <p class="authors">{authors(item)}</p>
            <p class="journal">{journal(item)}</p>
            <details class="bibtex"><summary>BibTeX</summary>
              <pre id="bib-{E(item['id'])}">{E(bibtex(item))}</pre>
              <div class="citation-actions"><button type="button" class="copy-button" data-copy-target="bib-{E(item['id'])}">Copy BibTeX</button><a href="files/{E(item['id'])}.bib" download>Download .bib</a></div>
            </details>
          </div>
        </article>'''
    education = ""
    for item in p["education"]:
        note = f'<p class="note">{E(item["note"])}</p>' if item["note"] else ""
        education += f'''<li><time>{E(item['dates'])}</time><h4>{E(item['school'])}</h4><p class="degree">{E(item['degree'])}</p>{note}</li>'''
    experience = "".join(f'''<li><time>{E(x['dates'])}</time><h4>{E(x['title'])}</h4><p class="degree">{E(x['organisation'])}</p><p class="note">{E(x['note'])}</p></li>''' for x in p["appointments"] if x.get("show_on_homepage", True))
    emails = "".join(f'''<div class="academic-email"><h4>{E(x['school'])}</h4>{''.join(f'<a href="mailto:{E(a)}">{E(a)}</a>' for a in x['addresses'])}</div>''' for x in p["academic_emails"])
    return make_head(p) + f'''
<body id="top">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header"><div class="wrap header-inner">
    <a class="brand" href="#top" aria-label="Ningyuan Xu home">Ningyuan Xu</a>
    <nav class="site-nav" id="site-nav" aria-label="Main navigation">
      <a href="#about">About</a><a href="#research">Research</a><a href="#publications">Publications</a><a href="#patents">Patents</a><a href="#background">Background</a><a href="#contact">Contact</a><a href="cv.html">CV ↗</a>
    </nav>
    <div class="header-controls">
      <button type="button" class="icon-button theme-toggle" aria-label="Switch to dark theme" aria-pressed="false" title="Dark theme"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M20.5 14.5A9 9 0 0 1 9.5 3.5a9 9 0 1 0 11 11Z"/></svg></button>
      <button type="button" class="icon-button menu-toggle" aria-label="Toggle navigation" aria-controls="site-nav" aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
    </div>
  </div></header>
  <main id="main" class="wrap">
    <section id="about" class="hero" aria-labelledby="hero-title">
      <p class="eyebrow">M.Sc. student · Nanyang Technological University, Singapore</p>
      <h1 id="hero-title">{E(p['name'])}</h1>
      <p class="subtitle">{E(p['tagline'])}</p>
      <p class="hero-intro">{E(p['intro'])}</p>
      <div class="hero-links"><a href="mailto:{E(p['primary_email'])}">{E(p['primary_email'])}</a><a href="cv.html">Academic CV ↗</a></div>
      <div class="profile-links" aria-label="Academic profiles">{profile_links}</div>
    </section>
    <section id="research" class="section" aria-labelledby="research-heading">
      {section_head('<span id="research-heading">Research</span>')}
      <div class="research-list">{research}</div>
    </section>
    <section id="publications" class="section" aria-labelledby="publications-heading">
      {section_head('<span id="publications-heading">Publications</span>', '<a class="text-link" href="files/publications.bib" download>Download bibliography ↓</a>')}
      <div class="publications-list">{papers}</div>
    </section>
    <section id="patents" class="section" aria-labelledby="patents-heading">
      {section_head('<span id="patents-heading">Patent applications</span>')}
      <p class="section-intro">First inventor on all three applications.</p>
      {make_patents(p)}
    </section>
    <section id="background" class="section" aria-labelledby="background-heading">
      {section_head('<span id="background-heading">Background</span>', '<a class="text-link" href="cv.html">Full academic CV ↗</a>')}
      <div class="background-grid">
        <div><h3 class="column-heading">Education</h3><ol class="timeline">{education}</ol></div>
        <div><h3 class="column-heading">Research appointments</h3><ol class="timeline">{experience}</ol></div>
      </div>
      <div class="supervisors" id="supervisors"><h3 class="column-heading">Supervisors</h3>{make_supervisors(p)}</div>
    </section>
    <section id="contact" class="section contact" aria-labelledby="contact-heading">
      {section_head('<span id="contact-heading">Contact</span>')}
      <div class="contact-panel">
        <div class="personal-emails"><a class="primary-email" href="mailto:{E(p['primary_email'])}">{E(p['primary_email'])}</a><a href="mailto:{E(p['secondary_email'])}">{E(p['secondary_email'])}</a></div>
        <details class="academic-emails"><summary>Academic email addresses</summary><div class="academic-email-list">{emails}</div></details>
      </div>
    </section>
  </main>
  {footer(p)}
</body></html>'''


def make_cv(p):
    supervisor_map = {x["id"]: x for x in p["supervisors"]}
    edu = ""
    for item in p["education"]:
        notes = []
        if item["note"]:
            notes.append(E(item["note"]))
        if item.get("supervisor_ids"):
            people = [supervisor_map[key] for key in item["supervisor_ids"]]
            names = ", ".join(external(x["group_url"], E(x["title"] + " " + x["name"])) for x in people)
            notes.append(("Supervisor: " if len(people) == 1 else "Supervisors: ") + names)
        note = '<p>' + '<br>'.join(notes) + '</p>' if notes else ""
        edu += f'<div class="cv-entry"><h3>{E(item["school"])}</h3><time>{E(item["dates"])}</time><p>{E(item["degree"])}</p>{note}</div>'
    jobs = "".join(f'<div class="cv-entry"><h3>{E(x["title"])} · {E(x["organisation"])}</h3><time>{E(x["dates"])}</time><p>{E(x["note"])}</p></div>' for x in p["appointments"])
    research = "".join(f'<div class="cv-entry"><h3>{E(x["title"])}</h3><p>{E(x["details"])}</p></div>' for x in p["research"])
    pubs = "".join(f'<li class="cv-publication">{authors(x)}. {external("https://doi.org/" + x["doi"], E(x["title"]))}. {journal(x)} DOI: {E(x["doi"])}.</li>' for x in p["publications"])
    honours = "".join(f'<li>{E(x["title"])} — {E(x["detail"])} ({E(x["year"])}).</li>' for x in p["honours"])
    skills = "".join(f'<p><strong>{E(x["label"])}:</strong> {E(x["text"])}</p>' for x in p["skills"])
    profiles = "".join(external(x["url"], E(x["name"]) + " ↗") for x in p["profiles"])
    return make_head(p, p["name"] + " | Academic CV", "/cv.html") + f'''
<body id="top"><main class="wrap cv-page">
    <div class="cv-toolbar"><a href="index.html" class="text-link">← Back to homepage</a><button type="button" class="button" data-print>Print / Save as PDF</button></div>
    <header class="cv-head"><h1>{E(p['name'])}</h1><p>{E(p['role'])} · {E(p['affiliation'])}, {E(p['location'])}<br><a href="mailto:{E(p['primary_email'])}">{E(p['primary_email'])}</a> · <a href="{E(p['site_url'])}">{E(p['site_url'].removeprefix('https://'))}</a></p><div class="cv-profiles">{profiles}</div></header>
    <section class="cv-section"><h2>Research profile</h2><p>{E(p['intro'])}</p></section>
    <section class="cv-section"><h2>Education</h2>{edu}</section>
    <section class="cv-section"><h2>Research & teaching appointments</h2>{jobs}</section>
    <section class="cv-section"><h2>Selected research experience</h2>{research}</section>
    <section class="cv-section"><h2>Peer-reviewed publications</h2><ol class="cv-list">{pubs}</ol></section>
    <section class="cv-section"><h2>Patent applications</h2><p>First inventor on all three applications.</p>{make_patents(p)}</section>
    <section class="cv-section"><h2>Technical skills</h2>{skills}</section>
    <section class="cv-section"><h2>Selected honours</h2><ul class="cv-list">{honours}</ul></section>
    <section class="cv-section"><h2>Supervisors</h2>{make_supervisors(p, heading_level=3)}</section>
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
    supervisor_ids = {person["id"] for person in p["supervisors"]}
    if len(supervisor_ids) != len(p["supervisors"]):
        raise ValueError("Supervisor IDs must be unique")
    for person in p["supervisors"]:
        if not all(person[key].startswith("https://") for key in ("group_url", "scholar_url")):
            raise ValueError("Supervisor links must use HTTPS")
    for item in p["education"]:
        if not set(item.get("supervisor_ids", [])).issubset(supervisor_ids):
            raise ValueError("Unknown education supervisor")
    if len({item["id"] for item in p["patents"]}) != len(p["patents"]):
        raise ValueError("Patent IDs must be unique")
    for item in p["patents"]:
        if not re.fullmatch(r"\d{12}\.[\dX]", item["application_number"]):
            raise ValueError("Invalid patent application number")
        date.fromisoformat(item["filing_date"])
        if item["publication_number"]:
            if not re.fullmatch(r"CN\d{9}[ABC]", item["publication_number"]) or not item["url"].startswith("https://"):
                raise ValueError("Invalid public patent record")
            date.fromisoformat(item["publication_date"])
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
    (out / "404.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Ningyuan Xu</title><style>body{background:#fafaf7;color:#1d302f;font:18px/1.7 Arial,Helvetica,sans-serif;margin:0;min-height:100vh;display:grid;place-items:center}main{max-width:480px;padding:35px}h1{font:52px Georgia,serif;margin:12px 0}small{font:14px Arial,Helvetica,sans-serif;color:#196659}a{color:#196659;text-underline-offset:5px}</style></head><body><main><small>404 / NINGYUAN XU</small><h1>Page not found.</h1><p>The page may have moved. You can find my research, publications and contact details on the homepage.</p><a href="https://ningyuanxu0.github.io/">Return to homepage →</a></main></body></html>''', encoding="utf-8")
    print(f"Built homepage, CV, bibliography and metadata in {out}")


if __name__ == "__main__":
    main()
