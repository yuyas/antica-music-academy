# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-file static landing page for **Antica Music Academy** — a high-end music school based in Ebisu, Tokyo. The entire site lives in `index.html` (HTML + CSS, no JavaScript, no build step).

## Development

Open `index.html` directly in a browser. No build, install, or compile step required.

For a live-reload workflow, any static file server works:

```bash
npx serve .
# or
python -m http.server 8080
```

## Architecture

All markup, styles, and content are in a single `index.html`. There is no JavaScript.

**CSS design tokens** (`:root` variables at the top of the `<style>` block):
- `--bg`, `--panel`, `--panel-soft` — dark background layers
- `--accent` (`#d9ba7b`), `--accent-deep` (`#b89355`) — gold accent palette
- `--text`, `--text-muted` — foreground colors

**Page sections** (each is a `<section>` with an `id`):
- `#concept` — hero / school overview
- `#features` — three educational value cards (`.grid-3`)
- *(unnamed)* — instrument grid (`.service-grid`)
- `#program` — three program cards by life stage (`.program-table`)
- `#access` — studio / online access grid (`.access-grid`)
- *(unnamed)* — enrollment flow steps (`.flow-list`)
- `#contact` — CTA box with mailto links

**Responsive breakpoints:**
- `≤980px` — hero, grid-3, program-table, access-grid collapse to single column; service-grid and flow-list go 2-column
- `≤640px` — nav hidden, service-grid and flow-list go single column

## Contact / Email

CTA buttons link to `mailto:info@antica-music-academy.jp` with pre-filled subjects (URL-encoded Japanese). Update the `href` values in the `#contact` section when the email address changes.
