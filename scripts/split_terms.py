"""
Split data/terms.csv into per-letter files (by first letter of the concept, after "What is").
data/terms_a.csv, data/terms_b.csv, etc.
"""
import csv
import os
import re
from collections import defaultdict

SRC = "data/terms.csv"
DST = "data"

def concept_letter(term: str) -> str:
    """Extract first letter of the actual concept (strip 'What is a/an/the ')."""
    stripped = re.sub(r"^What\s+is\s+(a\s+|an\s+|the\s+)?", "", term, flags=re.IGNORECASE)
    return stripped[0].upper() if stripped else "Z"

rows_by_letter = defaultdict(list)
fieldnames = None

with open(SRC, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        letter = concept_letter(row["term"])
        rows_by_letter[letter].append(row)

total = 0
for letter in sorted(rows_by_letter):
    path = os.path.join(DST, f"terms_{letter.lower()}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_by_letter[letter])
    total += len(rows_by_letter[letter])
    print(f"  {path}: {len(rows_by_letter[letter])} terms")

print(f"\nDone. {total} terms split into {len(rows_by_letter)} files.")
