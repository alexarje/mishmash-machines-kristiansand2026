#!/usr/bin/env python3
"""Lag en flat PDF av reveal.js-lysbildene i index.html.

Tar skjermbilde av hvert lysbilde med headless Chrome i 1920 x 1080 (lys modus)
og setter dem sammen med Pillow. Kjøres fra presentation/-mappen:

    source .venv/bin/activate
    python tools/build_pdf.py            # skriver <navn>.pdf ved siden av index.html
    python tools/build_pdf.py --only 5/2 # tar bare ett lysbilde på nytt og bygger PDF-en igjen
"""
import argparse, os, re, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PRES = os.path.dirname(HERE)
INDEX = os.path.join(PRES, "index.html")
SHOTS = os.path.join(PRES, ".shots")

def slide_indices():
    html = open(INDEX, encoding="utf8").read()
    slides = html.split('<div class="slides">')[1].split("</div>\n</div>")[0]
    blocks = re.split(r"\n<section>\n", slides)[1:]
    return [(h, v) for h, b in enumerate(blocks) for v in range(len(re.findall(r"^  <section", b, re.M)))]

def shoot(h, v):
    out = os.path.join(SHOTS, f"s-{h:02d}-{v:02d}.png")
    subprocess.run(["timeout", "40", "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--window-size=1920,1080", "--virtual-time-budget=3000",
                    f"--screenshot={out}", f"file://{INDEX}?light&fragments=false#/{h}/{v}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="bare dette lysbildet, som h/v")
    ap.add_argument("--out", help="PDF-navn (standard: første *.pdf i mappen, ellers slides.pdf)")
    a = ap.parse_args()
    os.makedirs(SHOTS, exist_ok=True)
    idx = slide_indices()
    todo = [tuple(int(x) for x in a.only.split("/"))] if a.only else idx
    for h, v in todo:
        shoot(h, v); print("ok", f"{h}/{v}")
    # fjern skjermbilder av lysbilder som ikke finnes lenger
    keep = {f"s-{h:02d}-{v:02d}.png" for h, v in idx}
    for f in os.listdir(SHOTS):
        if f.endswith(".png") and f not in keep: os.remove(os.path.join(SHOTS, f))
    files = sorted(f for f in os.listdir(SHOTS) if f.endswith(".png"))
    ims = [Image.open(os.path.join(SHOTS, f)).convert("RGB") for f in files]
    out = a.out or next((f for f in os.listdir(PRES) if f.endswith(".pdf")), "slides.pdf")
    ims[0].save(os.path.join(PRES, out), save_all=True, append_images=ims[1:], resolution=144)
    print("pdf", out, len(ims), "sider")

if __name__ == "__main__":
    main()
