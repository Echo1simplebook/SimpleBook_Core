from parsers.combine_credits import combine_credits
from parsers.combine_debits import combine_debits
from parsers.qfx_parser import parse_qfx_file, filter_by_month
from parsers.checks_parser import extract_checks
from parsers.other_debits_parser import extract_other_debits
from parsers.deposits_parser import extract_deposits
from parsers.other_credits_parser import extract_other_credits

FILEPATH = "samples/July24.qfx"


def main():
    print("Loading QFX file...")
    transactions = parse_qfx_file(FILEPATH)
    print(f"Total transactions loaded: {len(transactions)}")

    # Filter month
    july = filter_by_month(transactions, 2024, 7)
    print(f"July transactions: {len(july)}")

    # Checks
    checks = extract_checks(july)
    print(f"July Checks: {len(checks)}")

    # Other Debits (non-check)
    other_debits = extract_other_debits(july)
    print(f"July Other Debits: {len(other_debits)}")

    # Combined Debits
    combined_debits = combine_debits(checks, other_debits)
    print(f"July Combined Debits: {len(combined_debits)}")

    # Deposits (credits)
    deposits = extract_deposits(july)
    print(f"July Deposits: {len(deposits)}")

    # Other Credits (non-deposit)
    other_credits = extract_other_credits(july)
    print(f"July Other Credits: {len(other_credits)}")

    # Combined Credits
    combined_credits = combine_credits(deposits, other_credits)
    print(f"July Combined Credits: {len(combined_credits)}")

    # ========== DEBITS SECTION ==========
    print("\nFIRST 5 CHECKS:\n")
    for c in checks[:5]:
        print(c)
        print()

    print("\nFIRST 5 OTHER DEBITS:\n")
    for d in other_debits[:5]:
        print(d)
        print()

    print("\nFIRST 5 COMBINED DEBITS:\n")
    for cd in combined_debits[:5]:
        print(cd)
        print()

    # ========== CREDITS SECTION ==========
    print("\nFIRST 5 DEPOSITS:\n")
    for dep in deposits[:5]:
        print(dep)
        print()

    print("\nFIRST 5 OTHER CREDITS:\n")
    for oc in other_credits[:5]:
        print(oc)
        print()

    print("\nFIRST 5 COMBINED CREDITS:\n")
    for cc in combined_credits[:5]:
        print(cc)
        print()


if __name__ == "__main__":
    main()