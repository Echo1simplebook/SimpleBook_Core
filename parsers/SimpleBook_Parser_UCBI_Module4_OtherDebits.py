import os
import sys
import re
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
with open(input_file, "r", encoding="utf-8", errors="replace") as f:
    lines = [line.rstrip("\n") for line in f]

# -------------------------------------------------
# Normalize OCR dash variants
# -------------------------------------------------
def clean_dashes(text):
    return (
        text.replace("—", "-")
            .replace("–", "-")
            .replace("―", "-")
            .replace("−", "-")
    )

# -------------------------------------------------
# Find FIRST "--- OTHER DEBITS ---"
# -------------------------------------------------
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    cleaned = clean_dashes(line).upper().replace(" ", "")
    if cleaned == "---OTHERDEBITS---":      # exact match
        start_idx = i + 1
        break

if start_idx is None:
    print("[ERROR] OTHER DEBITS section not found.")
    sys.exit(1)

# -------------------------------------------------
# Find section END (first DAILY BALANCE after this)
# -------------------------------------------------
end_markers = [
    "DAILY BALANCE", "DAILYBALANCE", "BALANCE",
    "DAILY  BALANCE", "DA1LY", "DAlLY"
]

for j in range(start_idx, len(lines)):
    if any(marker in lines[j].upper() for marker in end_markers):
        end_idx = j
        break

if end_idx is None:
    end_idx = start_idx + 60  # safety net

raw_section = lines[start_idx:end_idx]

# -------------------------------------------------
# Clean continuation markers & deduplicate
# -------------------------------------------------
cleaned = []
seen = set()

for line in raw_section:
    if "*** CONTINUED" in line.upper():
        continue
    if line not in seen:
        cleaned.append(line)
        seen.add(line)

# -------------------------------------------------
# Patterns
# -------------------------------------------------
amount_pattern = re.compile(r"(\d{1,3}(?:,\d{3})*\.\d{2})")
date_pattern = re.compile(r"\b\d{2}/\d{2}\b")

parsed = []

# -------------------------------------------------
# Parse each cleaned line
# -------------------------------------------------
for raw in cleaned:
    line = " ".join(raw.split())
    if not line:
        continue

    amt_match = amount_pattern.search(line)
    if not amt_match:
        continue  # cannot parse → skip entirely

    amount = float(amt_match.group(1).replace(",", ""))

    dates = date_pattern.findall(line)
    date = dates[0] if len(dates) == 1 else (
        "UNKNOWN" if len(dates) == 0 else dates[0]
    )

    # Everything before the amount is the description
    description = line[:amt_match.start()].strip()

    if description == "":
        description = "UNKNOWN"

    parsed.append({
        "date": date,
        "amount": amount,
        "description": description
    })

# -------------------------------------------------
# Output summary
# -------------------------------------------------
print("\n--- OTHER DEBITS (Module 4) ---\n")

total = 0.0
for entry in parsed:
    print(f"{entry['date']} | ${entry['amount']:,.2f} | {entry['description']}")
    total += entry["amount"]

print(f"\nTOTAL Other Debits: ${total:,.2f}")

# -------------------------------------------------
# Save JSON
# -------------------------------------------------
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "module4_otherdebits.json")

with open(OUTPUT_JSON, "w") as f:
    json.dump(parsed, f, indent=4)

print(f"[OK] Saved JSON → {OUTPUT_JSON}")
