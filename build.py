#!/usr/bin/env python3
"""
Build script: assembles src/ modules into a single salad-merged.html.

Usage: python3 build.py
Output: /tmp/salad-merged.html
"""

import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'src')
OUTPUT = '/tmp/salad-merged.html'

def read(path):
    with open(path, 'r') as f:
        return f.read()

def main():
    # 1. Read and merge CSS
    css_order = ['variables.css', 'layout.css', 'components.css', 'reviews.css', 'mobile.css']
    css_parts = []
    for fname in css_order:
        fpath = os.path.join(SRC, 'css', fname)
        if os.path.exists(fpath):
            css_parts.append(read(fpath))
    merged_css = '\n'.join(css_parts)
    print(f"CSS: {len(css_order)} files merged ({len(merged_css):,} bytes)")

    # 2. Read JS
    js_path = os.path.join(SRC, 'js', 'nav.js')
    js_content = read(js_path) if os.path.exists(js_path) else ''
    print(f"JS:  nav.js ({len(js_content):,} bytes)")

    # 3. Read sections in order
    section_files = sorted(glob.glob(os.path.join(SRC, 'sections', '*.html')))
    sections_html = []
    for fpath in section_files:
        fname = os.path.basename(fpath)
        content = read(fpath)
        sections_html.append(content)
        print(f"Section: {fname} ({len(content):,} bytes)")
    merged_sections = '\n'.join(sections_html)

    # 4. Read index.html shell and assemble
    shell = read(os.path.join(SRC, 'index.html'))

    # Replace placeholders
    style_block = f'<style>\n{merged_css}\n</style>'
    script_block = f'<script>\n{js_content}\n</script>'

    # Hero is the first section file (00-hero.html)
    hero_html = sections_html[0] if sections_html else ''
    body_sections = '\n'.join(sections_html[1:])  # everything after hero

    output = shell
    output = output.replace('<!-- {CSS_PLACEHOLDER} -->', style_block)
    output = output.replace('<!-- {HERO_PLACEHOLDER} -->', hero_html)
    output = output.replace('<!-- {SECTIONS_PLACEHOLDER} -->', body_sections)
    output = output.replace('<!-- {JS_PLACEHOLDER} -->', script_block)

    # 5. Write output
    with open(OUTPUT, 'w') as f:
        f.write(output)

    size = os.path.getsize(OUTPUT)
    print(f"\n✅ Built: {OUTPUT}")
    print(f"   Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
    print(f"   Sections: {len(section_files)}")
    print(f"   CSS files: {len(css_order)}")

    # 6. Verify
    # Check all section IDs are present
    expected_ids = ['growth', 'stores', 'reviews', 'menu', 'customers', 'predictive', 'opportunities', 'platform']
    missing = [sid for sid in expected_ids if f'id="{sid}"' not in output]
    if missing:
        print(f"\n⚠️  Missing section IDs: {missing}")
    else:
        print(f"   All {len(expected_ids)} section IDs present ✓")

    # Check CSS variables
    if '--ink:' in output and '--primary:' in output:
        print("   CSS variables present ✓")
    else:
        print("   ⚠️  CSS variables might be missing!")

    if size < 1_000_000:
        print(f"   ⚠️  Output smaller than expected ({size:,} < 1,000,000)")

if __name__ == '__main__':
    main()
