import re
import os
import sys
import json

# -------------------------------------------------
# Resolve input file
# -------------------------------------------------
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

# -------------------------------------------------
# Load lines
# -------------------------------------------------
with open(input_file, "r") as f:
    lines = [line.rstrip("\n") for line in f]

# -------------------------------------------------
# Normalize text
# -------------------------------------------------
def clean(text: str) -> str:
    return (
        text.replace("—", "-")
            .replace("–", "-")
            .replace("―", "-")
            .replace("−", "-")
    )

# -------------------------------------------------
# Locate CHECKS section
# -------------------------------------------------
start = None
end = None

for i, line in enumerate(lines):
    cleaned = clean(line.upper()).replace(" ", "")
    if "CHECKS" in cleaned:
        start = i + 1
        break

if start is None:
    print("[ERROR] CHECKS section not found.")
    sys.exit(1)

# Look for end markers
for j in range(start, len(lines)):
    chk = clean(lines[j].upper()).replace(" ", "")
    if (
        "BALANCE" in chk or
        "DEPOSITS" in chk or
        "OTHERCREDITS" in chk or
        "OTHERDEBITS" in chk
    ):
        end = j
        break

if end is None:
    end = len(lines)

section = lines[start:end]

# -------------------------------------------------
# Deduplicate OCR repeats
# -------------------------------------------------
deduped = []
seen = set()

for line in section:
    line = line.strip()
    if line and line not in seen:
        deduped.append(line)
        seen.add(line)

section = deduped

# -------------------------------------------------
# Patterns
# -------------------------------------------------
amount_pattern = re.compile(r"(\d{1,3}(?:,\d{3})*\.\d{2})")
checknum_pattern = re.compile(r"\b\d{3,6}\b")
date_pattern = re.compile(r"\b\d{2}/\d{2}\b")

# -------------------------------------------------
# Parse checks
# -------------------------------------------------
parsed = []

for raw in section:
    line = " ".join(raw.split())
    if not line:
        continue

    amt_match = amount_pattern.search(line)
    if not amt_match:
        continue

    amount = float(amt_match.group(1).replace(",", ""))

    # Date = last date in line
    dates = date_pattern.findall(line)
    date = dates[-1] if dates else "UNKNOWN"

    # Check number = first standalone 4–6 digit number
    nums = checknum_pattern.findall(line)
    checknum = nums[0] if nums else "UNKNOWN"

    desc = line[:amt_match.start()].strip()

    parsed.append({
        "check_number": checknum,
        "date": date,
        "amount": amount,
        "description": desc
    })

# -------------------------------------------------
# Output
# -------------------------------------------------
print("\n--- CHECKS (Module 3) ---\n")

total = 0.0
for item in parsed:
    print(f"{item['date']} | Check {item['check_number']} | ${item['amount']:,.2f} | {item['description']}")
    total += item["amount"]

print(f"\nTOTAL Checks: ${total:,.2f}")

# Save JSON
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "module3_checks.json")
with open(OUTPUT_JSON, "w") as f:
    json.dump(parsed, f, indent=4)

print(f"[OK] Saved JSON → {OUTPUT_JSON}")
