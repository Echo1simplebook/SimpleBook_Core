import re
import os
import json
import sys

# -------------------------------------------------
# File resolution
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
# Helpers
# -------------------------------------------------
def clean_dashes(text: str) -> str:
    return (
        text.replace("—", "-")
        .replace("–", "-")
        .replace("―", "-")
        .replace("−", "-")
    )


amount_pattern = re.compile(r"(\d{1,3}(?:,\d{3})*\.\d{2})")
date_pattern   = re.compile(r"\b\d{2}/\d{2}\b")


# -------------------------------------------------
# Detect DEPOSITS section
# -------------------------------------------------
section_start = None
section_end   = None

for i, line in enumerate(lines):
    cleaned = clean_dashes(line.upper()).replace(" ", "")
    if "DEPOSITS" in cleaned:
        section_start = i + 1
        break

if section_start is None:
    print("[ERROR] Deposits section not found.")
    sys.exit(1)

# find end
for j in range(section_start, len(lines)):
    check = clean_dashes(lines[j].upper()).replace(" ", "")
    if (
        "BALANCE" in check
        or "OTHERDEBITS" in check
        or "OTHERDEBIT" in check
        or "CHECKS" in check
        or "OTHERCREDITS" in check
    ):
        section_end = j
        break

if section_end is None:
    section_end = len(lines)

deposit_lines = lines[section_start:section_end]

# -------------------------------------------------
# Parse entries
# -------------------------------------------------
parsed = []

for raw in deposit_lines:
    line = " ".join(raw.split())
    if not line.strip():
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

# -------------------------------------------------
# Save JSON output
# -------------------------------------------------
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "module1_deposits.json")

with open(OUTPUT_JSON, "w") as f:
    json.dump(parsed, f, indent=4)

# -------------------------------------------------
# Display summary
# -------------------------------------------------
print("\n--- DEPOSITS (Module 1) ---\n")

total = sum(item["amount"] for item in parsed)

for entry in parsed:
    print(f'{entry["date"]} | ${entry["amount"]:,.2f} | {entry["description"]}')

print(f"\nTOTAL Deposits: ${total:,.2f}")
print(f"[OK] Saved JSON → {OUTPUT_JSON}")