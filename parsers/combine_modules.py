import json
import os

# Path to combined file
COMBINED_JSON = os.path.join(os.path.dirname(__file__), "combined_output.json")

def load_data(path):
-   return json.load(f)

data = load_data(COMBINED_JSON)

total_deposits = sum(d["amount"] for d in data.get("deposits", []))
total_credits  = sum(c["amount"] for c in data.get("other_credits", []))
total_checks   = sum(c["amount"] for c in data.get("checks", []))
total_debits   = sum(d["amount"] for d in data.get("other_debits", []))

total_income    = round(total_deposits + total_credits, 2)
total_expenses  = round(abs(total_checks) + abs(total_debits), 2)
net_change      = round(total_income - total_expenses, 2)

# ----------------------------------------
# Summary Report
# ----------------------------------------
print("\n" + "="*40)
print("     📊 Monthly Transaction Summary")
print("="*40)
print(f"Deposits:            ${total_deposits:,.2f}")
print(f"Other Credits:       ${total_credits:,.2f}")
print(f"Checks Written:     -${abs(total_checks):,.2f}")
print(f"Other Debits:       -${abs(total_debits):,.2f}")
print("-" * 40)
print(f"Total Income:        ${total_income:,.2f}")
print(f"Total Expenses:     -${total_expenses:,.2f}")
print("="*40)
print(f"NET CHANGE:          ${net_change:,.2f}")
print("="*40 + "\n")