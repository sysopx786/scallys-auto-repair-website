#!/usr/bin/env python3
"""Builds the Scally's logo, favicons and Open Graph image. Run from the site root: python3 src/logo.py
Needs: pip install fonttools brotli pillow; rsvg-convert on PATH."""
import subprocess
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'assets/img'
RED, RED_D = '#B3261E', '#E06A5E'
INK, INK_D = '#14213A', '#F1EEE6'


def font(name, wght):
    return instantiateVariableFont(TTFont(ROOT / f'assets/fonts/{name}.woff2'), {'wght': wght})


def text_path(f, s, size, x, y, track=0.0):
    """Return (svg path d, advance width) for string s at baseline (x, y)."""
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f['hmtx']
    upm = f['head'].unitsPerEm
    k = size / upm
    pen = SVGPathPen(gs)
    cx = x
    for ch in s:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        cx += hmtx[g][0] * k + track * size
    return pen.getCommands(), cx - x - track * size


BR, IN = font('bricolage', 800), font('inter', 700)


def mark(x, y, s, fill, fg):
    """Rounded square badge with a bold S."""
    d, w = text_path(BR, 'S', s * 0.78, 0, 0)
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*0.24:.1f}" fill="{fill}"/>'
            f'<path transform="translate({x + (s - w) / 2:.1f},{y + s * 0.78:.1f})" d="{d}" fill="{fg}"/>')


def logo(ink, red, path):
    word, ww = text_path(BR, "Scally's", 96, 132, 92)
    sub, sw = text_path(IN, 'AUTO REPAIR · SINCE 1987', 25, 136, 136, track=0.12)
    W = int(132 + max(ww, sw + 4) + 14)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 160" role="img" aria-label="Scally\'s Auto Repair">'
           f'{mark(8, 22, 108, red, "#FFFFFF")}<path d="{word}" fill="{ink}"/><path d="{sub}" fill="{red}"/></svg>')
    (IMG / path).write_text(svg)
    return W


w = logo(INK, RED, 'logo-flat.svg')
logo(INK_D, RED_D, 'logo-flat-dark.svg')
print('logo width', w)

fav = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{mark(0, 0, 64, RED, "#FFFFFF")}</svg>'
(IMG / 'favicon.svg').write_text(fav)
for size, name in [(32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), '-o', str(IMG / name), str(IMG / 'favicon.svg')], check=True)

# Open Graph image, 1200x630
word, ww = text_path(BR, "Scally's Auto Repair", 92, 96, 300)
l2, _ = text_path(IN, 'Primos, PA · Since 1987', 40, 100, 372)
l3, _ = text_path(IN, '610-626-4700 · Official PA inspection station', 34, 100, 520)
og = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
      f'<rect width="1200" height="630" fill="#14213A"/><rect y="600" width="1200" height="30" fill="{RED}"/>'
      f'{mark(96, 96, 104, RED, "#FFFFFF")}<path d="{word}" fill="#F1EEE6"/><path d="{l2}" fill="#E06A5E"/>'
      f'<path d="{l3}" fill="#B3BDD0"/></svg>')
tmp = ROOT / 'src/.og.svg'
tmp.write_text(og)
subprocess.run(['rsvg-convert', '-w', '1200', '-h', '630', '-o', str(ROOT / 'src/.og.png'), str(tmp)], check=True)
subprocess.run(['convert', str(ROOT / 'src/.og.png'), '-quality', '86', str(IMG / 'og-image.jpg')], check=True)
tmp.unlink(); (ROOT / 'src/.og.png').unlink()
print('ok')
