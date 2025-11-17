def extract_other_credits(transactions: list[dict]) -> list[dict]:
    """
    Extracts credits that are NOT deposits.
    Logic:
        - amount > 0   → it's a credit
        - BUT if name or memo suggests 'DEPOSIT' → skip (handled by deposits parser)
        - Typical other credits:
            * ACH CREDIT
            * REFUND
            * BANK CORRECTION
            * INTEREST CREDIT
            * TRANSFER FROM …
            * REVERSALS
    """

    other_credits: list[dict] = []

    for tx in transactions:
        amount = tx.get("amount", 0.0)
        if amount <= 0:
            continue  # not a credit at all

        name = (tx.get("name") or "").upper()
        memo = (tx.get("memo") or "").upper()
        tx_type = (tx.get("type") or "").upper()

        # Is this a deposit? Skip it.
        deposit_indicators = [
            "ATM DEPOSIT",
            "DEPOSIT",
            "REGULAR DEPOSIT",
            "MOBILE DEPOSIT",
        ]

        if any(ind in name for ind in deposit_indicators):
            continue

        if any(ind in memo for ind in deposit_indicators):
            continue

        source = _extract_source(name, memo)

        other_credits.append({
            "amount": amount,
            "date": tx["posted_date"],
            "source": source,
            "fitid": tx["fitid"],
            "type": tx_type,
            "name": tx.get("name"),
            "memo": tx.get("memo"),
        })

    return other_credits


def _extract_source(name: str, memo: str) -> str:
    """
    Attempts to determine where this credit came from.
    """

    clean_name = (name or "").strip()
    clean_memo = (memo or "").strip()

    if clean_memo and clean_memo not in ("DEPOSIT", "MOBILE DEPOSIT"):
        return clean_memo.title()

    if clean_name and clean_name not in ("DEPOSIT", "CREDIT"):
        return clean_name.title()

    return "Unknown Source"