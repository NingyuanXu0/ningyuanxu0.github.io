#!/usr/bin/env python3
"""Create original conceptual vector illustrations; these are not experimental data."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/images"
INK, BLUE, LIGHT, WARM = "#537ba8", "#245c9e", "#d5e4f5", "#d0b69a"


def svg(body, width=320, height=210):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">{body}</svg>'


def cube(x, y, s=22, rotation=0, fill=LIGHT):
    return f'''<g transform="translate({x} {y}) rotate({rotation})" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"><path d="M0 {-s} {s} {-s/2} {s} {s/2} 0 {s} {-s} {s/2} {-s} {-s/2}Z" fill="{fill}"/><path d="M0 0 {s} {-s/2}M0 0 {-s} {-s/2}M0 0V{s}"/><path d="M0 {-s}V0" stroke-opacity=".3"/></g>'''


def dot(x, y, r=2.5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}" fill-opacity=".35"/>'


def draw():
    OUT.mkdir(parents=True, exist_ok=True)
    body = '<path d="M25 164 153 79 295 153" stroke="#89a5c4" stroke-width=".8" stroke-dasharray="3 5"/>'
    centres = [(89,73,19,-12),(157,54,20,6),(222,80,19,16),(64,124,21,11),(133,112,25,-4),(210,131,23,-11),(164,167,21,17),(266,159,17,5)]
    for x,y,s,r in centres:
        body += cube(x,y,s,r)
    for i in range(24):
        x=27+(i*43)%266; y=22+(i*31)%173
        if all(math.hypot(x-cx,y-cy)>s*1.35 for cx,cy,s,_ in centres):
            body+=dot(x,y,2+(i%3)*.4)
    (OUT/'assembly.svg').write_text(svg(body), encoding='utf-8')
    body = f'<path d="M19 145H301V180H19Z" fill="#dfebf7" fill-opacity=".6" stroke="{INK}" stroke-width="1"/><path d="M20 146c14-18 20-12 30-1s19-16 31-6 21-17 35-4 23-14 35-3 18-12 30-2 22-13 34-3 18-12 30-1 24-12 39-1 14 1 17 3" stroke="{BLUE}" stroke-width="1.4"/>'
    for x,y,r in [(44,162,10),(88,161,14),(137,158,12),(187,160,15),(234,160,12),(277,163,10)]:
        body+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f8fafc" fill-opacity=".6" stroke="{INK}" stroke-width="1"/><circle cx="{x}" cy="{y}" r="{r-3}" stroke="{INK}" stroke-width=".5" stroke-dasharray="2 3"/>'
    body += f'<path d="M126 123c-20-14-26-41-12-61 15-23 48-29 72-12 23 16 28 46 9 65-17 19-48 22-69 8Z" fill="#9dbfe5" fill-opacity=".65" stroke="{BLUE}" stroke-width="1.5"/><path d="M125 65c-7 8-11 18-10 29" stroke="#f8fafc" stroke-width="4" stroke-linecap="round"/><path d="M223 52v54m-5-6 5 6 5-6" stroke="{INK}" stroke-width="1" stroke-dasharray="2 3"/>'
    (OUT/'wetting.svg').write_text(svg(body), encoding='utf-8')
    body = ''
    for x in range(25,296,18):
        body+=f'<path d="M{x} 135v48" stroke="{INK}" stroke-width="1" stroke-opacity=".7"/>'
    for y in range(137,184,11):
        body+=f'<path d="M25 {y}h270" stroke="{INK}" stroke-width="1" stroke-opacity=".7"/>'
    body+=f'<circle cx="66" cy="63" r="21" fill="#acc9eb" stroke="{INK}" stroke-width="1.2"/><path d="M146 92c-22 0-34 11-31 21s72 9 74-1-20-20-43-20Z" fill="#acc9eb" stroke="{INK}" stroke-width="1.2"/><path d="M232 120c-12-8-18-24-14-36 4-14 17-28 24-39 6 12 20 25 24 39 5 16-1 32-15 37" fill="#acc9eb" stroke="{INK}" stroke-width="1.2"/><path d="M98 68h25m-6-4 6 4-6 4M179 65h25m-6-4 6 4-6 4M66 96v23m-4-5 4 5 4-5" stroke="{INK}" stroke-width="1"/><path d="M112 193h76" stroke="{WARM}" stroke-width="2"/>'
    (OUT/'droplets.svg').write_text(svg(body), encoding='utf-8')
    body=''
    for x in range(25,411,24):
        for y in range(28,361,24):
            body+=f'<circle cx="{x}" cy="{y}" r=".65" fill="#829fbe" fill-opacity=".35"/>'
    body+=f'<path d="m58 191 178-49 140 80-180 53Z" fill="#cbdff4" fill-opacity=".58" stroke="{BLUE}" stroke-width="1.2"/><path d="M58 191v25l138 83 180-53v-24M196 275v24" stroke="{INK}" stroke-width="1"/>'
    for x,y,r in [(99,200,11),(133,218,15),(175,242,12),(211,238,13),(249,225,15),(286,213,12),(244,180,12),(205,190,11),(165,195,10),(283,189,9),(325,228,8)]:
        body+=f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.57}" fill="#e4eef9" stroke="{INK}" stroke-width=".9"/><path d="M{x-r} {y}a{r} {r*.9} 0 0 0 {r*2} 0" stroke="{INK}" stroke-width=".7"/>'
    body+=f'<path d="M124 171c-22-14-30-43-20-68 13-35 52-48 82-31 32 17 43 56 23 82-18 23-57 32-85 17Z" fill="#8eb5e0" fill-opacity=".85" stroke="{BLUE}" stroke-width="1.6"/><path d="M120 105c-7 10-9 23-6 33" stroke="#f5f9ff" stroke-width="5" stroke-linecap="round"/>'
    body+=cube(275,304,22,-8)+cube(328,277,18,8)+cube(227,330,15,13)
    body+=f'<path d="M77 121H45V67m0 0-4 7m4-7 4 7M338 258l32 17v55h-28m6-4-6 4 6 4" stroke="{INK}" stroke-width=".8"/><circle cx="45" cy="121" r="2.3" fill="{BLUE}"/><path d="m147 51 51-13" stroke="{WARM}" stroke-width="2"/>'
    for x,y in [(296,331),(313,340),(365,294),(206,305),(255,348)]:
        body+=dot(x,y,2.2)
    (OUT/'interface.svg').write_text(svg(body,420,375), encoding='utf-8')
    social=f'''<rect width="1200" height="630" fill="#f8fafc"/><path d="M65 70h1070" stroke="#d4dfeb"/><text x="70" y="117" fill="{BLUE}" font-family="Arial,sans-serif" font-size="17" letter-spacing="3">RESEARCH / NANYANG TECHNOLOGICAL UNIVERSITY</text><text x="66" y="290" fill="#213047" font-family="Georgia,serif" font-size="100">Ningyuan Xu</text><text x="70" y="356" fill="{BLUE}" font-family="Georgia,serif" font-size="34">Surface science &amp;</text><text x="70" y="405" fill="{BLUE}" font-family="Georgia,serif" font-size="34">computational soft matter</text><text x="70" y="550" fill="#4b5c72" font-family="Arial,sans-serif" font-size="22">ningyuanxu.com</text><g transform="translate(724 122) scale(.98)">{body}</g>'''
    (OUT/'social-card.svg').write_text(svg(social,1200,630), encoding='utf-8')
    try:
        import cairosvg
        cairosvg.svg2png(url=str(OUT/'social-card.svg'),write_to=str(OUT/'social-card.png'))
    except ImportError:
        try:
            import fitz
            with fitz.open(OUT/'social-card.svg') as document:
                zoom = 1200 / document[0].rect.width
                document[0].get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(OUT/'social-card.png')
        except ImportError:
            print('Optional SVG renderer unavailable; retain the checked-in social-card.png.')
    print('Original conceptual illustration assets generated.')


if __name__=='__main__':
    draw()
