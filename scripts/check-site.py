#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


IGNORED_SCHEMES = {"data", "http", "https", "mailto", "tel"}
FORBIDDEN_NAMES = {"CLAUDE.md", "netlify.toml"}
FORBIDDEN_SUFFIXES = {".docx"}


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        for name in ("href", "src", "poster"):
            value = attributes.get(name)
            if value:
                self.references.append(value)

        srcset = attributes.get("srcset")
        if srcset:
            self.references.extend(item.strip().split()[0] for item in srcset.split(","))


def resolve_reference(site_root: Path, source: Path, reference: str) -> Path | None:
    if reference.startswith(("#", "//")):
        return None

    parsed = urlsplit(reference)
    if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
        return None

    path = unquote(parsed.path)
    if not path:
        return None

    if path.startswith("/"):
        target = site_root / path.lstrip("/")
    else:
        target = source.parent / path

    target = Path(os.path.abspath(target))

    if target.is_dir():
        target = target / "index.html"

    return target


def main() -> int:
    site_root = Path(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "_site"))
    if not site_root.is_dir():
        print(f"Site directory not found: {site_root}", file=sys.stderr)
        return 1

    errors: list[str] = []

    for file in site_root.rglob("*"):
        if not file.is_file():
            continue
        if file.name in FORBIDDEN_NAMES or file.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"Forbidden production file: {file.relative_to(site_root)}")

    for html_file in site_root.rglob("*.html"):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for reference in parser.references:
            target = resolve_reference(site_root, html_file, reference)
            if target is None:
                continue
            if not target.is_relative_to(site_root):
                errors.append(
                    f"Reference escapes site root in {html_file.relative_to(site_root)}: "
                    f"{reference}"
                )
            elif not target.is_file():
                errors.append(
                    f"Broken reference in {html_file.relative_to(site_root)}: {reference}"
                )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("Production artifact checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
