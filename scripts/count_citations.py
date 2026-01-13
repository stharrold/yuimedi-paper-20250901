# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0

import re


def get_cited_keys(md_file):
    with open(md_file) as f:
        content = f.read()
    # Matches @key inside brackets or standalone @key
    keys = re.findall(r"@([a-zA-Z0-9_]+)", content)
    return set(keys)


def get_bib_categories(bib_file):
    key_category = {}
    current_key = None
    with open(bib_file) as f:
        for line in f:
            line = line.strip()
            # Match start of entry: @article{key,
            m_key = re.match(r"@\w+\{([a-zA-Z0-9_]+),", line)
            if m_key:
                current_key = m_key.group(1)

            # Match note field: note = {Original citation: [A1]},
            if current_key:
                m_note = re.search(r"note\s*=\s*\{Original citation: \[(A|I)\d+\]\}", line)
                if m_note:
                    category = "Academic" if m_note.group(1) == "A" else "Industry"
                    key_category[current_key] = category
    return key_category


cited_keys = get_cited_keys("paper.md")
bib_cats = get_bib_categories("references.bib")

academic_count = 0
industry_count = 0
uncategorized_count = 0

for key in cited_keys:
    if key in bib_cats:
        if bib_cats[key] == "Academic":
            academic_count += 1
        else:
            industry_count += 1
    else:
        # If not found or no note, check if it looks like a known key structure or count as uncategorized
        # Some might not have the note field if they are new
        uncategorized_count += 1
        print(f"Uncategorized: {key}")

print(f"Academic: {academic_count}")
print(f"Industry: {industry_count}")
print(f"Uncategorized: {uncategorized_count}")
print(f"Total: {academic_count + industry_count + uncategorized_count}")
