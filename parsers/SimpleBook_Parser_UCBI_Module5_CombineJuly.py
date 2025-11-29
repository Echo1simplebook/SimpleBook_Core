import os
import json

# -------------------------------------------------
# Helper to load JSON output from a module
# -------------------------------------------------
def load_json(path):
    if not os.path.exists(path):
        print(f"[ERROR] Missing file: {path}")
        return []
    with open(path, "r") as f:
        return json.load(f)

# -------------------------------------------------
# Correct folder with the actual JSON files
# -------------------------------------------------
BASE_DIR = "/Users/christhomas/PycharmProjectsSimpleBook_Parser/modules"

DEPOSITS_JSON      = os.path.join(BASE_DIR, "module1_deposits.json")
OTHERCREDITS_JSON  = os.path.join(BASE_DIR, "module2_othercredits.json")
CHECKS_JSON        = os.path.join(BASE_DIR, "module3_checks.json")
OTHERDEBITS_JSON   = os.path.join(BASE_DIR, "module4_otherdebits.json")

# -------------------------------------------------
# Load all module outputs
# -------------------------------------------------
deposits     = load_json(DEPOSITS_JSON)
othercredits = load_json(OTHERCREDITS_JSON)
checks       = load_json(CHECKS_JSON)
otherdebits  = load_json(OTHERDEBITS_JSON)

# -------------------------------------------------
# Combine all records into one list
# -------------------------------------------------
combined = deposits + othercredits + checks + otherdebits

# -------------------------------------------------
# Output combined file
# -------------------------------------------------
output_path = os.path.join(BASE_DIR, "combined_output.json")
with open(output_path, "w") as f:
    json.dump(combined, f, indent=2)

print(f"[✅] Combined file written to: {output_path}")