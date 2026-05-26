#!/usr/bin/env python3
import csv, os
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
total_dups = 0

for f in sorted(os.listdir(DATA_DIR)):
    if not f.startswith("terms_") or not f.endswith(".csv"):
        continue
    path = os.path.join(DATA_DIR, f)
    dups = defaultdict(list)
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader, start=2):
            slug = row["slug"].strip()
            dups[slug].append(i)

    file_dups = {slug: lines for slug, lines in dups.items() if len(lines) > 1}
    if file_dups:
        print(f"{f}:")
        for slug, lines in sorted(file_dups.items()):
            print(f"  slug=\"{slug}\" on lines {lines}")
            total_dups += len(lines) - 1
    else:
        print(f"{f}: clean")

print(f"\nTotal duplicate rows to remove: {total_dups}")
