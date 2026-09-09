# Building a Norwegian Ecosystem for AI and Creativity

Slides for the **Machines** session at the MishMash Opening Conference, Kilden, Kristiansand, 14 September 2026 (11:45–12:45). A ten-minute map of the AI tools and compute available in Norway, from a musician's laptop to the National Library training on Olivia, followed by a panel.

- Live slides: https://alexarje.github.io/mishmash-machines-kristiansand2026/
- Speaker notes: press `s`. Overview: `esc`. Jump to a strip: `g`, number, enter. Light/dark: `d`.
- Each horizontal strip has depth slides below it (down arrow) for the discussion.

## Editing

Everything is in `index.html` (reveal.js, vendored in `lib/`, no build step). Figures are SVGs in `images/`, drawn by `tools/make_figures.py`:

```bash
python3 tools/make_figures.py          # redraw the figures
python3 tools/build_pdf.py --out slides.pdf   # flat PDF via headless Chrome (needs Pillow)
```

Pushing to `main` deploys to GitHub Pages through `.github/workflows/pages.yml`.

## Session

Panel: four panelists, to be confirmed. Moderator: Alexander Refsum Jensenius.
