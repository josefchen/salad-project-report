# The Salad Project — Analytics Intelligence Report

Modular source structure for the TSP analytics report. The final output is always a **single self-contained HTML file** (for StaticCrypt encryption + GitHub Pages), but the source is split into maintainable modules.

## Structure

```
src/
  css/
    variables.css       # :root custom properties + reset
    layout.css          # .container, .section, .hero, .nav-bar, .kpi-grid
    components.css      # .card, .chart-*, .insight-*, .action-*, .badge*, .scorecard*
    reviews.css         # All .review-* classes
    mobile.css          # @media queries (768px, 480px, print)
  js/
    nav.js              # Navigation active-state + smooth scroll
  sections/
    00-hero.html        # Hero banner + KPI grid
    01-growth.html      # Section 01: Growth & Momentum
    02-stores.html      # Section 02: Store Performance
    02b-reviews.html    # Section 02b: What Customers Are Saying
    03-menu.html        # Section 03: Menu Intelligence
    04-customers.html   # Section 04: Customer Base
    05-predictive.html  # Section 05: Predictive Model
    06-opportunities.html  # Section 06+07: What To Do Next + Platform
  index.html            # Shell: <head>, nav-bar, footer, placeholders
build.py                # Assembler: src/ → salad-merged.html
```

## How to edit

### Edit a section
1. Edit `src/sections/XX.html`
2. Run `python3 build.py`
3. Output: `/tmp/salad-merged.html`

### Edit styles
1. Edit `src/css/XX.css`
2. Run `python3 build.py`

### Add a new section
1. Create `src/sections/NN-name.html` (numbered for sort order)
2. Run `python3 build.py` — it picks up files alphabetically

## Build

```bash
python3 build.py
```

Outputs `/tmp/salad-merged.html` with a summary of what was assembled.

## Encrypt & Deploy

```bash
# 1. Build
python3 build.py

# 2. Encrypt with StaticCrypt
npx staticrypt /tmp/salad-merged.html --password saladsforlife2026 --remember 0 -d /tmp/enc-out/

# 3. Inject TSP login page styling (if needed)

# 4. Push to GitHub Pages
git add -A
git commit -m "Update report"
git push origin main
```

## Notes

- **matplotlib SVG `<style>` blocks** (17 of them) live inside the section HTML files — they're part of the chart SVGs and must not be extracted to CSS files.
- The main CSS is split into 5 logical modules; the build script merges them back into a single `<style>` block.
- `nav.js` adds smooth scrolling and active-state highlighting to the sticky nav bar.
