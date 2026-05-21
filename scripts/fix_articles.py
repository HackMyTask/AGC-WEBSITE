"""
Fix common article quality issues:
1. Duplicate "What is What is" headings → "What is"
2. Short descriptions expanded to 120-155 chars
"""

import os
import re

GLOSSARY_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "glossary")

CLUSTER_SUFFIX = {
    "ai-basics": "understand the fundamentals of artificial intelligence.",
    "llms": "understand large language models and how they work.",
    "prompt-engineering": "get better results from AI through effective prompting.",
    "ai-tools": "use AI tools and applications in your daily life.",
    "ai-agents": "understand autonomous AI systems and how they operate.",
    "ai-infrastructure": "learn about the technology powering AI systems.",
    "ai-safety": "understand how to keep AI safe and trustworthy.",
}


def fix_heading(content: str) -> str:
    return content.replace("## What is What is ", "## What is ")


def expand_description(desc: str, title: str, cluster: str) -> str:
    if len(desc) >= 120:
        return desc

    topic = title.lower().replace("what is ", "").strip()

    suffix = CLUSTER_SUFFIX.get(cluster, "explained in plain language.")

    expanded = f"{desc.rstrip('.')}. Learn what {topic} is and {suffix}"

    if len(expanded) > 155:
        expanded = expanded[:152].rstrip() + "..."

    return expanded


def fix_file(filepath: str) -> tuple[bool, bool]:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fixed_heading = False
    fixed_desc = False

    new_content = fix_heading(content)
    if new_content != content:
        fixed_heading = True
        content = new_content

    frontmatter_match = re.match(
        r"^---\s*\n(.*?)\n---", content, re.DOTALL
    )
    if not frontmatter_match:
        return fixed_heading, False

    frontmatter = frontmatter_match.group(1)
    desc_match = re.search(r'^description:\s*"(.+)"', frontmatter, re.MULTILINE)
    title_match = re.search(r'^title:\s*"(.+)"', frontmatter, re.MULTILINE)
    cluster_match = re.search(r'^cluster:\s*"(.+)"', frontmatter, re.MULTILINE)

    if not (desc_match and title_match):
        return fixed_heading, False

    desc = desc_match.group(1)
    if len(desc) >= 100:
        return fixed_heading, False

    title = title_match.group(1)
    cluster = cluster_match.group(1) if cluster_match else ""

    new_desc = expand_description(desc, title, cluster)

    old_line = f'description: "{desc}"'
    new_line = f'description: "{new_desc}"'
    content = content.replace(old_line, new_line)
    fixed_desc = True

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return fixed_heading, fixed_desc


def main():
    files = sorted(os.listdir(GLOSSARY_DIR))
    md_files = [f for f in files if f.endswith(".md")]

    heading_fixed = 0
    desc_fixed = 0
    total = len(md_files)

    for fname in md_files:
        filepath = os.path.join(GLOSSARY_DIR, fname)
        h_fixed, d_fixed = fix_file(filepath)
        if h_fixed:
            heading_fixed += 1
        if d_fixed:
            desc_fixed += 1

    print(f"Total files: {total}")
    print(f"Duplicate headings fixed: {heading_fixed}")
    print(f"Short descriptions expanded: {desc_fixed}")


if __name__ == "__main__":
    main()
