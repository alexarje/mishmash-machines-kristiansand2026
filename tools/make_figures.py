#!/usr/bin/env python3
"""Draws the SVG figures for the Machines session deck into images/.

Run from the repository root:  python tools/make_figures.py
No dependencies. Colours follow the deck's blue palette. The slides invert
figures in dark mode with a CSS filter, so everything is drawn for a white
background. Layered figures (fig-x-0.svg, fig-x-1.svg, ...) share one viewBox;
each later layer only contains what it adds, and the slide stacks them.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "images")

INK, MUTED, LINE = "#1a202c", "#718096", "#cbd5e0"
BLUE, BLUE_LIGHT, BLUE_PALE = "#2b6cb0", "#bee3f8", "#ebf4ff"
GREEN, GREEN_PALE, RED, RED_PALE, AMBER, AMBER_PALE = "#2f855a", "#f0fff4", "#c53030", "#fff5f5", "#b7791f", "#fffaf0"
FONT = "font-family='Inter, Helvetica Neue, Helvetica, Arial, sans-serif'"


def write(name, doc):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf8") as f:
        f.write(doc)
    print("wrote", name)


def svg(w, h, body, defs=""):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' {FONT}>\n"
            f"<defs>{defs}</defs>\n{body}\n</svg>\n")


def marker(mid, color):
    return (f"<marker id='{mid}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
            f"orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{color}'/></marker>")


def text(x, y, s, size=20, fill=INK, anchor="middle", weight="normal", extra=""):
    return (f"<text x='{x}' y='{y}' text-anchor='{anchor}' font-size='{size}' fill='{fill}' "
            f"font-weight='{weight}' {extra}>{s}</text>")


def lines(x, y, rows, size=18, fill=INK, anchor="middle", lh=1.3, weight="normal"):
    out = []
    for i, r in enumerate(rows):
        out.append(text(x, y + i * size * lh, r, size, fill, anchor, weight))
    return "".join(out)


def box(x, y, w, h, fill="white", stroke=LINE, sw=3, r=14):
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'/>"


def arrow(x1, y1, x2, y2, color=BLUE, sw=4, mid="a", dash=""):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' stroke-width='{sw}' marker-end='url(#{mid})'{d}/>"


# ---------------------------------------------------------------- 1 two roads
def two_roads():
    W, H = 1600, 700
    defs = marker("a", BLUE)
    rent = []
    rent.append(box(60, 80, 640, 560, RED_PALE, RED))
    rent.append(text(380, 150, "Rent a service", 40, RED, weight="bold"))
    rent.append(text(380, 195, "ChatGPT · Claude · Gemini · Suno · Runway · Midjourney", 18, MUTED))
    rent.append(lines(110, 260, ["+ the best models, today", "+ zero setup, pay per use", "+ works on any device"], 24, GREEN, "start"))
    rent.append(lines(110, 400, ["– no weights, no reproducibility", "– your data leave the room", "– terms and prices change", "– same for everyone, no yours"], 24, RED, "start"))
    rent.append(text(380, 600, "control: theirs", 22, MUTED))
    write("fig-two-roads-0.svg", svg(W, H, "".join(rent), defs))
    run = []
    run.append(box(900, 80, 640, 560, GREEN_PALE, GREEN))
    run.append(text(1220, 150, "Run it yourself", 40, GREEN, weight="bold"))
    run.append(text(1220, 195, "open models on hardware you or your institution control", 18, MUTED))
    run.append(lines(950, 260, ["+ full control, reproducible", "+ private: nothing leaves", "+ can be trained on your material"], 24, GREEN, "start"))
    run.append(lines(950, 400, ["– one step behind the frontier", "– you carry the setup", "– you pay the energy bill", "– needs hardware and time"], 24, RED, "start"))
    run.append(text(1220, 600, "control: yours", 22, MUTED))
    write("fig-two-roads-1.svg", svg(W, H, "".join(run), defs))
    mid = []
    mid.append(f"<rect x='700' y='250' width='200' height='220' rx='14' fill='{BLUE_PALE}' stroke='{BLUE}' stroke-width='3'/>")
    mid.append(lines(800, 300, ["The middle", "road"], 26, BLUE, weight="bold"))
    mid.append(lines(800, 370, ["open models,", "rented GPUs", "(HF, Mistral,", "EU providers)"], 18, INK))
    write("fig-two-roads-2.svg", svg(W, H, "".join(mid), defs))


# ---------------------------------------------------------------- 2 ladder
RUNGS = [
    ("Micro-\ncontroller", "Arduino, ESP32", "256 KB", "keyword spotting,\ngesture classes", "100–500 kr"),
    ("Single-board", "Raspberry Pi, Jetson", "4–16 GB", "small vision/audio,\nWhisper tiny", "1–5 000 kr"),
    ("Phone", "on-device models", "6–12 GB", "1–3B LLM,\ncamera, mic", "5–15 000 kr"),
    ("Tablet", "any brand", "8–16 GB", "like a phone,\nbigger screen", "5–20 000 kr"),
    ("Laptop", "unified or discrete memory", "16–64 GB", "7–14B chat, Whisper,\nRAVE on stage", "15–40 000 kr"),
    ("Laptop\nwith GPU", "RTX 4070–5090 mobile", "8–24 GB VRAM", "diffusion, fine-tune\nsmall models", "25–60 000 kr"),
    ("Desktop /\nworkstation", "big GPU or large unified memory", "32–512 GB", "70B local, train\nsmall models, serve", "40–150 000 kr"),
]


def ladder():
    W, H = 1700, 800
    n = len(RUNGS)
    x0, step, bw = 60, 228, 200
    base, mem, models = [], [], []
    for i, (name, ex, memv, use, price) in enumerate(RUNGS):
        x = x0 + i * step
        top = 560 - i * 36
        base.append(box(x, top, bw, 770 - top, "white", LINE))
        base.append(lines(x + bw / 2, top + 44, name.split("\n"), 26, INK, weight="bold"))
        base.append(text(x + bw / 2, top + 44 + 26 * 1.3 * len(name.split("\n")), ex, 16, MUTED))
        base.append(lines(x + bw / 2, 700, use.split("\n"), 17, INK))
        base.append(text(x + bw / 2, 750, price, 16, MUTED))
        mem.append(f"<rect x='{x+20}' y='{top-52}' width='{bw-40}' height='40' rx='8' fill='{BLUE_PALE}' stroke='{BLUE}' stroke-width='2'/>")
        mem.append(text(x + bw / 2, top - 25, memv, 19, BLUE, weight="bold"))
    write("fig-ladder-0.svg", svg(W, H, "".join(base)))
    mem.append(text(1500, 250, "memory (RAM, VRAM or unified)", 20, BLUE, weight="bold"))
    write("fig-ladder-1.svg", svg(W, H, "".join(mem)))
    # model sizes as pills spanning rungs
    def pill(i0, i1, y, label, col):
        xa = x0 + i0 * step + 10; xb = x0 + i1 * step + bw - 10
        return (f"<rect x='{xa}' y='{y}' width='{xb-xa}' height='36' rx='18' fill='{col}' opacity='.92'/>"
                + text((xa + xb) / 2, y + 25, label, 18, "white", weight="bold"))
    models.append(pill(0, 1, 40, "TinyML · RAVE (real-time audio)", GREEN))
    models.append(pill(2, 4, 85, "1–8B LLM at 4-bit (≈1–5 GB) · Whisper · small diffusion", BLUE))
    models.append(pill(4, 6, 130, "14–30B (≈10–20 GB) · SDXL, FLUX · fine-tuning", "#553c9a"))
    models.append(pill(6, 6, 175, "70B+ (≈40 GB)", RED))
    write("fig-ladder-2.svg", svg(W, H, "".join(models)))


def memory():
    W, H = 1600, 620
    b = []
    b.append(text(800, 70, "parameters × bytes per parameter ≈ memory", 40, INK, weight="bold"))
    rows = [("7–8B", "4-bit", "≈ 5 GB", "any recent laptop or phone", GREEN),
            ("30B", "4-bit", "≈ 20 GB", "laptop with 32 GB unified, or a 24 GB GPU", BLUE),
            ("70B", "4-bit", "≈ 40 GB", "large unified memory, or two big GPUs", "#553c9a"),
            ("70B", "16-bit", "≈ 140 GB", "a server, or Fox", RED)]
    y = 150
    for p, q, m, where, col in rows:
        b.append(box(80, y, 1440, 80, "white", col))
        b.append(text(200, y + 52, p, 34, col, weight="bold"))
        b.append(text(400, y + 52, q, 26, MUTED))
        b.append(text(600, y + 52, m, 34, INK, weight="bold"))
        b.append(text(1100, y + 52, where, 24, INK))
        y += 100
    write("fig-memory.svg", svg(W, H, "".join(b)))


# ---------------------------------------------------------------- 3 stair
STAIRS = [
    ("Shared server", "a GPU box in the lab,\nssh, first come first served", "colleagues"),
    ("VDI", "virtual desktop, licensed\nsoftware, rarely a real GPU", "employees"),
    ("Institutional HPC", "UiO Fox · NTNU IDUN · UiA DGX\nUiB and UiT local clusters", "own staff, students via a project"),
    ("National", "Sigma2/NRIS: Olivia 448 GH200,\nSaga · KI-fabrikken", "researchers, by application"),
    ("European", "LUMI (Kajaani), LUMI-AI,\nEuroHPC AI Factories", "big projects, by call"),
]


def stair():
    W, H = 1700, 800
    defs = marker("a", BLUE) + marker("r", RED)
    base, more = [], []
    x0, step, bw = 60, 320, 290
    for i, (name, desc, who) in enumerate(STAIRS):
        x = x0 + i * step
        top = 520 - i * 80
        base.append(box(x, top, bw, 660 - top, "white", LINE))
        base.append(text(x + bw / 2, top + 45, name, 28, INK, weight="bold"))
        base.append(lines(x + bw / 2, top + 85, desc.split("\n"), 17, INK))
        base.append(text(x + bw / 2, 640, who, 17, MUTED))
    write("fig-stair-0.svg", svg(W, H, "".join(base), defs))
    more.append(arrow(120, 100, 1580, 100, BLUE, 5, "a"))
    more.append(text(850, 80, "more compute · more people can share it · more data next to it", 24, BLUE, weight="bold"))
    more.append(arrow(1580, 730, 120, 730, RED, 5, "r"))
    more.append(text(850, 775, "more waiting · more paperwork · less interactive · batch, not a rehearsal", 24, RED, weight="bold"))
    write("fig-stair-1.svg", svg(W, H, "".join(more), defs))


# ---------------------------------------------------------------- 4 frontends and api
def frontends():
    W, H = 1600, 760
    defs = marker("a", BLUE)
    b = []
    b.append(f"<circle cx='800' cy='380' r='110' fill='{BLUE_PALE}' stroke='{BLUE}' stroke-width='4'/>")
    b.append(lines(800, 372, ["the model", "(local or remote)"], 24, BLUE, weight="bold"))
    fams = [("Chat", ["ChatGPT · Claude · Gemini", "institution-hosted: UiO GPT, GPT NTNU, Copilot", "Open WebUI · LM Studio · Jan"], 60, 60),
            ("Code and agents", ["VS Code + Copilot / Continue / Cline", "Claude Code · Cursor · Aider", "Jupyter · Educloud On Demand"], 1040, 60),
            ("Creative tools", ["Max/MSP + nn~ · FluCoMa · Pure Data", "Ableton + Neutone · TouchDesigner", "ComfyUI · Unity/Unreal · p5.js + ml5"], 60, 500),
            ("Programmatic", ["Python: PyTorch, transformers, diffusers", "llama.cpp · MLX · Ollama · vLLM", "any OpenAI-compatible endpoint"], 1040, 500)]
    for name, items, x, y in fams:
        b.append(box(x, y, 500, 200, "white", LINE))
        b.append(text(x + 250, y + 45, name, 28, INK, weight="bold"))
        b.append(lines(x + 250, y + 90, items, 19, INK))
    for x1, y1 in [(560, 160), (1040, 160), (560, 600), (1040, 600)]:
        b.append(arrow(x1, y1, 800 + (110 if x1 > 800 else -110) * 0.75, 380 + (70 if y1 > 380 else -70), BLUE, 3, "a"))
    write("fig-frontends.svg", svg(W, H, "".join(b), defs))


def api():
    W, H = 1600, 660
    defs = marker("a", BLUE)
    b = []
    b.append(box(60, 200, 420, 220, BLUE_PALE, BLUE))
    b.append(lines(270, 270, ["one script,", "one Max patch,", "one notebook"], 30, BLUE, weight="bold"))
    b.append(text(270, 395, "base_url = ...", 22, MUTED, extra="font-family='Menlo, Consolas, monospace'"))
    targets = [("laptop", "Ollama · LM Studio · llama.cpp", GREEN), ("lab server", "vLLM · Open WebUI", GREEN),
               ("Fox / Olivia", "vLLM behind a tunnel", BLUE), ("EU provider", "Mistral · Scaleway · HF", BLUE),
               ("commercial", "OpenAI · Anthropic · Google", RED)]
    y = 60
    for name, sub, col in targets:
        b.append(box(1000, y, 540, 84, "white", col))
        b.append(text(1030, y + 38, name, 26, col, "start", "bold"))
        b.append(text(1030, y + 68, sub, 18, MUTED, "start"))
        b.append(arrow(490, 310, 995, y + 42, BLUE, 3, "a"))
        y += 108
    b.append(text(800, 635, "the same OpenAI-compatible API on all of them: change one line, keep the workflow", 24, INK, weight="bold"))
    write("fig-api.svg", svg(W, H, "".join(b), defs))


# ---------------------------------------------------------------- 6 spectrum of MishMash use cases
CASES = [  # name, WP, compute 0..1, sensitivity 0..1, colour
    ("Musician on stage", "WP1", 0.12, 0.15, GREEN),
    ("Filmmaker", "WP2", 0.45, 0.50, BLUE),
    ("Music therapist", "WP3", 0.18, 0.92, RED),
    ("Teacher in a school", "WP4", 0.04, 0.70, AMBER),
    ("Cultural institution", "WP5", 0.55, 0.60, "#553c9a"),
    ("National Library", "WP6", 0.95, 0.55, INK),
    ("Designer / rescue", "WP7", 0.40, 0.80, "#2c7a7b"),
]


def spectrum():
    W, H = 1600, 860
    defs = marker("a", MUTED)
    L, R, T, B = 320, 1520, 60, 740
    base = []
    base.append(arrow(L, B, R + 20, B, MUTED, 3, "a"))
    base.append(arrow(L, B, L, T - 20, MUTED, 3, "a"))
    for f, lab in [(0.02, "laptop, phone"), (0.3, "studio GPU"), (0.55, "Fox"), (0.8, "Olivia"), (0.98, "LUMI")]:
        x = L + f * (R - L)
        base.append(f"<line x1='{x}' y1='{B}' x2='{x}' y2='{B+12}' stroke='{MUTED}' stroke-width='2'/>")
        base.append(text(x, B + 40, lab, 19, MUTED))
    base.append(text((L + R) / 2, B + 85, "compute needed", 26, INK, weight="bold"))
    for f, lab in [(0.1, "own material"), (0.5, "rights-encumbered"), (0.9, "personal / health")]:
        y = B - f * (B - T)
        base.append(text(L - 15, y + 7, lab, 19, MUTED, "end"))
    base.append(text(60, (T + B) / 2, "data sensitivity", 26, INK, weight="bold", extra=f"transform='rotate(-90 60 {(T+B)/2})'"))
    write("fig-spectrum-0.svg", svg(W, H, "".join(base), defs))
    pts = []
    for name, wp, cx, sy, col in CASES:
        x = L + cx * (R - L); y = B - sy * (B - T)
        pts.append(f"<circle cx='{x}' cy='{y}' r='26' fill='{col}' opacity='.9'/>")
        pts.append(text(x, y + 7, wp[2], 20, "white", weight="bold"))
        dy = -40 if name != "Teacher in a school" else 55
        pts.append(text(x, y + dy, name, 22, col, weight="bold"))
    write("fig-spectrum-1.svg", svg(W, H, "".join(pts), defs))


def workflow(name, title, stages, note):
    W, H = 1600, 440
    defs = marker("a", BLUE)
    b = [text(800, 60, title, 34, INK, weight="bold")]
    labels = ["prototype small and local", "scale up only for training", "bring it back to the room"]
    for i, (head, body) in enumerate(stages):
        x = 60 + i * 520
        b.append(box(x, 110, 460, 280, BLUE_PALE if i == 1 else "white", BLUE if i == 1 else LINE))
        b.append(text(x + 230, 150, labels[i], 18, MUTED))
        b.append(text(x + 230, 200, head, 28, INK, weight="bold"))
        b.append(lines(x + 230, 245, body, 20, INK))
        if i < 2:
            b.append(arrow(x + 470, 250, x + 515, 250, BLUE, 4, "a"))
    write(f"fig-workflow-{name}.svg", svg(W, H, "".join(b), defs))


def workflows():
    workflow("musician", "WP1 · A musician on stage",
             [("Record", ["own material,", "a few hours of audio,", "on the laptop"]),
              ("Train RAVE", ["overnight on a studio GPU", "or a Fox job;", "the model is ~30 MB"]),
              ("Play", ["nn~ in Max on the laptop,", "milliseconds of latency,", "nothing leaves the studio"])],
             "the model is yours, trained on your sound, and runs without internet")
    workflow("film", "WP2 · A filmmaker",
             [("Sketch", ["storyboards with an open", "image model (FLUX, SDXL)", "on a laptop with GPU"]),
              ("Generate", ["open video models (Wan, LTX)", "on a workstation or", "an EU-hosted provider"]),
              ("Cut", ["into the edit; provenance", "and licence of every model", "documented for rights"])],
             "the open route is one step behind Runway, and the rights are yours to defend")
    workflow("teacher", "WP4 · A teacher in a school",
             [("Browser only", ["Chromebooks, Feide,", "no GPU, pupils' data;", "institution-hosted chat"]),
              ("Offline where it matters", ["Whisper on the teacher's", "laptop for transcripts;", "nothing uploaded"]),
              ("In the classroom", ["free, Norwegian, GDPR-safe", "creative tools; the scarcest", "resource in the whole map"])],
             "no compute problem, but an access and language problem")
    workflow("nb", "WP6 · The National Library",
             [("Prepare", ["petabytes of text, audio,", "images, film; copyright", "and public-sector duty"]),
              ("Train", ["multimodal Norwegian model", "on Olivia or LUMI,", "months of allocation"]),
              ("Release", ["open weights on Hugging Face;", "the musician in WP1", "downloads them"])],
             "the loop closes: national compute upstream, a laptop downstream")


def loop():
    W, H = 1600, 520
    defs = marker("a", BLUE)
    b = []
    b.append(box(60, 160, 440, 200, BLUE_PALE, BLUE))
    b.append(lines(280, 230, ["Researcher", "trains on Olivia / LUMI"], 28, BLUE, weight="bold"))
    b.append(box(580, 160, 440, 200, "white", LINE))
    b.append(lines(800, 230, ["Open release", "weights, data card, licence"], 28, INK, weight="bold"))
    b.append(box(1100, 160, 440, 200, GREEN_PALE, GREEN))
    b.append(lines(1320, 230, ["Musician, teacher,", "filmmaker: laptop"], 28, GREEN, weight="bold"))
    b.append(arrow(505, 260, 575, 260, BLUE, 4, "a"))
    b.append(arrow(1025, 260, 1095, 260, BLUE, 4, "a"))
    b.append(text(800, 440, "when the loop works: compute upstream, open models downstream", 28, INK, weight="bold"))
    write("fig-loop.svg", svg(W, H, "".join(b), defs))


if __name__ == "__main__":
    two_roads(); ladder(); memory(); stair(); frontends(); api(); spectrum(); workflows(); loop()
