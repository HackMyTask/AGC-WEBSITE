#!/usr/bin/env python3
import csv, json, os, re, sys

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
BATCH_DIR = os.path.join(os.path.dirname(__file__), "data")

def slugify(term):
    s = re.sub(r"^what\s+is\s+", "", term, flags=re.IGNORECASE).strip()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return "what-is-" + s.strip("-")

def existing_slugs():
    slugs = set()
    for f in sorted(os.listdir(DATA_DIR)):
        if not f.startswith("terms_") or not f.endswith(".csv"):
            continue
        path = os.path.join(DATA_DIR, f)
        with open(path, newline="", encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                slugs.add(row["slug"].strip())
    return slugs

def load_batches():
    all_terms = []
    for f in sorted(os.listdir(BATCH_DIR)):
        if not f.startswith("terms_batch_") or not f.endswith(".json"):
            continue
        path = os.path.join(BATCH_DIR, f)
        with open(path, "r", encoding="utf-8-sig") as fh:
            data = json.load(fh)
        for entry in data:
            if isinstance(entry, dict) and "value" in entry:
                entry = entry["value"]
            if not isinstance(entry, (list, tuple)) or len(entry) < 4:
                continue
            term = entry[0]
            cluster = entry[1]
            keywords = entry[2]
            priority = entry[3]
            all_terms.append((term, cluster, keywords, priority))
    return all_terms

def main():
    existing = existing_slugs()
    print(f"Existing terms in CSVs: {len(existing)}")

    terms = load_batches()
    print(f"Loaded {len(terms)} terms from batch files")

    added = 0
    skipped = 0
    by_file = {}

    VALID_CLUSTERS = {
        "ai-basics", "ai-agents", "ai-safety", "ai-tools", "ai-infrastructure",
        "ai-coding", "ai-creative", "ai-voice", "ai-business", "ai-data",
        "ai-education", "ai-robotics", "ai-finance", "ai-healthcare",
        "ai-research", "ai-gaming", "prompt-engineering", "llms",
        "ai-multimodal"
    }

    for term, cluster, keywords, priority in terms:
        if cluster not in VALID_CLUSTERS:
            print(f"  WARNING: unknown cluster '{cluster}' for '{term}'")
            continue
        slug = slugify(term)
        if slug in existing:
            skipped += 1
            continue
        existing.add(slug)
        concept = re.sub(r"^[Ww]hat\s+[Ii]s\s+", "", term).strip()
        first = concept[0].upper() if concept else "M"
        if first.isalpha():
            filename = f"terms_{first.lower()}.csv"
        else:
            filename = "terms_misc.csv"
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            filename = "terms_misc.csv"
            path = os.path.join(DATA_DIR, filename)
        by_file.setdefault(filename, []).append((term, slug, cluster, "pending", priority, keywords))
        added += 1

    if not by_file:
        print("\nAll terms already exist. Nothing to add.")
        return

    print(f"\nAdding {added} new terms ({skipped} skipped, already exist):")
    for filename, rows in sorted(by_file.items()):
        path = os.path.join(DATA_DIR, filename)
        file_exists = os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as fh:
            if not file_exists:
                fh.write("term,slug,cluster,status,priority,keywords\n")
            w = csv.writer(fh, quoting=csv.QUOTE_ALL)
            for r in rows:
                w.writerow([r[0], r[1], r[2], r[3], str(r[4]), r[5]])
        print(f"  {filename}: +{len(rows)} terms")

    new_total = len(existing)
    print(f"\nTotal: {added} added, {skipped} skipped")
    print(f"New CSV total: {new_total} terms")

if __name__ == "__main__":
    main()
