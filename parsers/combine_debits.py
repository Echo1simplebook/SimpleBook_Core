from typing import List, Dict


def combine_debits(checks: List[Dict], other_debits: List[Dict]) -> List[Dict]:
    """
    Combine check debits and non-check debits into a single list.

    We do NOT add business logic here. This module only:
      - tags each record with a 'debit_kind'
      - returns a single combined list

    debit_kind:
      - 'CHECK'
      - 'OTHER_DEBIT'
    """

    combined: List[Dict] = []

    # Tag checks
    for c in checks:
        record = dict(c)  # shallow copy
        record["debit_kind"] = "CHECK"
        combined.append(record)

    # Tag other debits
    for d in other_debits:
        record = dict(d)  # shallow copy
        record["debit_kind"] = "OTHER_DEBIT"
        combined.append(record)

    return combined