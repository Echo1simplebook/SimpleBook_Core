import re
import os
import sys
import json

# -------------------------------------------
# Resolve input file
# -------------------------------------------
DEFAULT_FILE = "../statements/ocr_july_cleaned_v2.txt"

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), DEFAULT_FILE)
    )

if not os.path.exists(input_file):
    print(f"[ERROR] Input file not found: {input_file}")
    sys.exit(1)

print(f"[INFO] Using input file: {input_file}")

# -------------------------------------------
# Load lines
# -------------------------------------------
with open(input_file, "r") as f:
    lines = [line.rstrip("\n") for line in f]

# -------------------------------------------
# Clean dash variations
# -------------------------------------------
def clean_dashes(text: str) -> str:
    return (
        text.replace("—", "-")
        .replace("–", "-")
        .replace("―", "-")
        .replace("−", "-")
        .replace("—", "-")
    )

# -------------------------------------------
# Find OTHER CREDITS section starts
# -------------------------------------------
section_starts = []

for i, line in enumerate(lines):
    cleaned = clean_dashes(line.upper()).replace(" ", "")
    if "OTHERCREDITS" in cleaned:
        section_starts.append(i + 1)

if not section_starts:
    print("[ERROR] OTHER CREDITS section not found.")
    sys.exit(1)

# -------------------------------------------
# Find section ends
# -------------------------------------------
section_ends = []

for start in section_starts:
    for j in range(start, len(lines)):
        check = clean_dashes(lines[j].upper()).replace(" ", "")

        if (
            "OTHERDEBITS" in check
            or "CHECKS" in check
            or "DEPOSITS" in check
            or "BALANCE" in check
        ):
            section_ends.append(j)
            break

# -------------------------------------------
# Merge section blocks
# -------------------------------------------
combined = []

for s, e in zip(section_starts, section_ends):
    combined.extend(lines[s:e])

# -------------------------------------------
# Remove continuation lines
# -------------------------------------------
filtered = []

for line in combined:
    if "*** CONTINUED" in line.upper():
        continue
    filtered.append(line)

combined = filtered

# -------------------------------------------
# Remove duplicates
# -------------------------------------------
deduped = []
seen = set()

for line in combined:
    if line not in seen:
        deduped.append(line)
        seen.add(line)

combined = deduped

# -------------------------------------------
# Parse entries
# -------------------------------------------
amount_pattern = re.compile(r"(\d{1,3}(?:,\d{3})*\.\d{2})")
date_pattern = re.compile(r"\b\d{2}/\d{2}\b")

parsed = []

for raw in combined:
    line = " ".join(raw.split())
    if not line:
        continue

    amt_match = amount_pattern.search(line)
    if not amt_match:
        continue

    amount = float(amt_match.group(1).replace(",", ""))
    dates = date_pattern.findall(line)
    date = dates[-1] if dates else "UNKNOWN"

    desc = line[:amt_match.start()].strip()

    parsed.append({
        "date": date,
        "amount": round(amount, 2),
        "description": desc
    })

# -------------------------------------------
# Save JSON
# -------------------------------------------
output_file = os.path.join(
    os.path.dirname(__file__),
    "module2_othercredits.json"
)

with open(output_file, "w") as f:
    json.dump(parsed, f, indent=4)

# -------------------------------------------
# Show output
# -------------------------------------------
print("\n--- OTHER CREDITS (Module 2) ---\n")

total = sum(item["amount"] for item in parsed)

for item in parsed:
    print(f"{item['date']} | ${item['amount']:,.2f} | {item['description']}")

print(f"\nTOTAL Other Credits: ${total:,.2f}")
print(f"[OK] Saved JSON → {output_file}")