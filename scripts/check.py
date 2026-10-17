#!/usr/bin/env python3
"""Static release checks: links, metadata, supplied contact details and bibliography."""
import argparse
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_EMAILS = {
    "2022190906016@std.uestc.edu.cn", "nyxu.work@outlook.com",
    "2840141x@student.gla.ac.uk", "nyxu@std.uestc.edu.cn",
    "NINGYUAN004@e.ntu.edu.sg", "nyxu.work@gmail.com",
}
REQUIRED_PROFILES = {
    "github.com/NingyuanXu0", "orcid.org/0009-0001-2545-4370",
    "scholar.google.com.hk/citations", "www.researchgate.net/profile/Xu-Ningyuan",
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.assets, self.labels = [], [], [], []
        self.h1s, self.meta, self.json_ld = 0, {}, []
        self.in_json, self.json_buffer = False, ""
        self.errors = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1s += 1
        if tag == "a":
            if not attrs.get("href"):
                self.errors.append("Anchor without a real href")
            else:
                self.links.append(attrs["href"])
            if attrs.get("target") == "_blank" and "noopener" not in attrs.get("rel", ""):
                self.errors.append("External new-tab link missing noopener")
        if tag == "img":
            if "alt" not in attrs:
                self.errors.append("Image without alt text")
            if not attrs.get("width") or not attrs.get("height"):
                self.errors.append("Image without explicit dimensions")
        if tag in ("img", "script") and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") in ("stylesheet", "icon"):
            self.assets.append(attrs["href"])
        if tag == "meta":
            self.meta[attrs.get("name", attrs.get("property", ""))] = attrs.get("content", "")
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json, self.json_buffer = True, ""

    def handle_data(self, data):
        self.labels.append(data)
        if self.in_json:
            self.json_buffer += data

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            self.json_ld.append(json.loads(self.json_buffer))
            self.in_json = False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?", default=ROOT)
    base = parser.parse_args().directory.resolve()
    profile = json.loads((ROOT / "data/profile.json").read_text(encoding="utf-8"))
    pages, errors = {}, []
    for filename in ("index.html", "cv.html", "404.html"):
        page = Page()
        page.feed((base / filename).read_text(encoding="utf-8"))
        pages[filename] = page
        errors.extend(f"{filename}: {x}" for x in page.errors)
        duplicates = [key for key, value in Counter(page.ids).items() if value > 1]
        if duplicates:
            errors.append(f"{filename}: duplicate IDs {duplicates}")
        if page.h1s != 1:
            errors.append(f"{filename}: expected exactly one h1")
        for asset in page.assets:
            asset_url = urlsplit(asset)
            if not asset_url.scheme and not (base / unquote(asset_url.path)).is_file():
                errors.append(f"{filename}: missing asset {asset}")
    for filename, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme in ("https", "mailto"):
                continue
            if url.scheme:
                errors.append(f"{filename}: unsupported link scheme {link}")
                continue
            target_name = unquote(url.path) or filename
            target = base / target_name
            if not target.is_file():
                errors.append(f"{filename}: broken local link {link}")
            if url.fragment and target_name in pages and url.fragment not in pages[target_name].ids:
                errors.append(f"{filename}: missing anchor {link}")
    home = pages["index.html"]
    emails = {x.removeprefix("mailto:") for x in home.links if x.startswith("mailto:")}
    expected_emails = REQUIRED_EMAILS | {person["email"] for person in profile["supervisors"]}
    if emails != expected_emails:
        errors.append(f"Homepage contact mismatch: missing={expected_emails-emails}, extra={emails-expected_emails}")
    for page_name in ("index.html", "cv.html"):
        page = pages[page_name]
        text = " ".join(page.labels)
        for person in profile["supervisors"]:
            for link in (person["group_url"], person["scholar_url"], "mailto:" + person["email"]):
                if link not in page.links:
                    errors.append(f"{page_name}: missing supervisor link {link}")
        for patent in profile["patents"]:
            if patent["id"] not in page.ids or patent["application_number"] not in text:
                errors.append(f"{page_name}: missing patent application {patent['application_number']}")
            if patent["publication_number"] and (patent["publication_number"] not in text or patent["url"] not in page.links):
                errors.append(f"{page_name}: missing public patent record {patent['publication_number']}")
    for profile in REQUIRED_PROFILES:
        if not any(profile in link for link in home.links):
            errors.append("Missing requested academic profile: " + profile)
    for page_name in ("index.html", "cv.html"):
        page = pages[page_name]
        for meta in ("description", "viewport", "og:title", "og:image"):
            if not page.meta.get(meta):
                errors.append(f"{page_name}: missing {meta} metadata")
        if not page.json_ld or page.json_ld[0].get("@type") != "Person":
            errors.append(f"{page_name}: missing valid Person structured data")
    if not (base / "assets/images/social-card.png").is_file():
        errors.append("Missing raster social preview image")
    if (base / "files/publications.bib").read_text().count("@article{") != 3:
        errors.append("Bibliography should contain three published articles")
    for filename in ("sitemap.xml",):
        ET.parse(base / filename)
    for asset in (base / "assets/images").glob("*.svg"):
        ET.parse(asset)
    if not (base / ".nojekyll").exists():
        errors.append("Missing .nojekyll")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(pages)} HTML pages, all local assets/anchors, 6 owner email addresses, 3 supervisors with group/Scholar/email links, 3 patent applications, 4 profiles, 3 BibTeX entries, JSON-LD and XML.")
    print("External profile destinations are supplied links; availability or login requirements remain controlled by those services.")


if __name__ == "__main__":
    main()
