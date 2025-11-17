def extract_other_debits(transactions: list[dict]) -> list[dict]:
    """
    Takes a list of transactions (already filtered for a month)
    and returns NON-CHECK debits (card charges, ACH debits, etc.).

    Rules:
      - amount < 0.0  → it's a debit
      - BUT if it's a check (CHECKNUM present or TRNTYPE == CHECK or NAME contains 'CHECK')
        → skip it (checks are handled by checks_parser)
    """

    other_debits: list[dict] = []

    for tx in transactions:
        amount = tx.get("amount", 0.0)
        if amount >= 0:
            # not a debit, skip
            continue

        checknum = tx.get("checknum")
        tx_type = (tx.get("type") or "").upper()
        name = (tx.get("name") or "").upper()

        # Is this a check? If so, let the checks module own it.
        is_check = (
            checknum is not None
            or tx_type == "CHECK"
            or "CHECK" in name
        )

        if is_check:
            continue

        memo = (tx.get("memo") or "")

        vendor = _extract_vendor(name, memo)

        other_debits.append({
            "amount": amount,
            "date": tx["posted_date"],
            "vendor": vendor,
            "fitid": tx["fitid"],
            "type": tx_type,
            "name": tx.get("name"),
            "memo": tx.get("memo"),
        })

    return other_debits


def _extract_vendor(name: str, memo: str) -> str:
    """
    Try to get a reasonable vendor name for non-check debits.

    Priority:
      1. MEMO, if it looks like a real description
      2. NAME, if present
      3. 'Unknown Vendor'
    """

    clean_name = (name or "").strip()
    clean_memo = (memo or "").strip()

    # Generic noise patterns we don't want to treat as vendor names
    generic_markers = [
        "DEBIT CARD PURCHASE",
        "ACH DEBIT",
        "DEBIT",
        "WITHDRAWAL",
        "TRANSFER",
        "ONLINE BANKING",
    ]

    memo_upper = clean_memo.upper()

    if clean_memo:
        if not any(marker in memo_upper for marker in generic_markers):
            return clean_memo.title()

    if clean_name:
        return clean_name.title()

    return "Unknown Vendor"