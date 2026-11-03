#!/usr/bin/env bash
set -euo pipefail

output_dir="${1:-_site}"

if [[ -e "$output_dir" ]]; then
  echo "Output directory already exists: $output_dir" >&2
  exit 1
fi

mkdir -p "$output_dir"

cp index.html CNAME "$output_dir/"
cp LOGO.svg アンティカ音楽学院.svg "$output_dir/"
cp flyer_AnticaMusicAcademy_20260707.pdf "$output_dir/"
cp 20260825_ShunTominaga.pdf "$output_dir/"
cp 20261006_beautiful_musicians_flyer.pdf "$output_dir/"

while IFS= read -r -d '' file; do
  destination="$output_dir/$file"
  mkdir -p "$(dirname "$destination")"
  cp "$file" "$destination"
done < <(find images -type f \( \
  -iname '*.avif' -o \
  -iname '*.gif' -o \
  -iname '*.jpeg' -o \
  -iname '*.jpg' -o \
  -iname '*.png' -o \
  -iname '*.svg' -o \
  -iname '*.webp' \
\) -print0)

cp -r ambassadors "$output_dir/"
cp -r news "$output_dir/"

if find "$output_dir" -type f \( \
  -iname '*.docx' -o \
  -name 'CLAUDE.md' -o \
  -name 'netlify.toml' \
\) -print -quit | grep -q .; then
  echo "Internal file detected in production artifact" >&2
  exit 1
fi
