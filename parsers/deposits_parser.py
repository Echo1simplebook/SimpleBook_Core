def extract_deposits(transactions: list[dict]) -> list[dict]:
    """
    Extracts ALL deposits (credits) from a month of transactions.
    Rules:
        - amount > 0.0  → it's a credit
        - TRNTYPE may be 'CREDIT', 'DEPOSIT', 'DIRECTDEP', etc.
        - Excludes 'OTHER CREDITS' (handled in another module)
          but for now we treat ALL credits as deposits and classify later.
    """

    deposits: list[dict] = []

    for tx in transactions:
        amount = tx.get("amount", 0.0)
        if amount <= 0:
            continue  # not a deposit

        tx_type = (tx.get("type") or "").upper()
        name = (tx.get("name") or "").strip()
        memo = (tx.get("memo") or "").strip()

        vendor = _extract_source(name, memo)

        deposits.append({
            "amount": amount,
            "date": tx["posted_date"],
            "source": vendor,
            "fitid": tx["fitid"],
            "type": tx_type,
            "name": tx.get("name"),
            "memo": tx.get("memo"),
        })

    return deposits


def _extract_source(name: str, memo: str) -> str:
    """
    Attempts to determine the 'source' of a deposit.
    Examples:
      - 'Mobile Deposit' → likely checks
      - 'Zelle From John Doe' → tenant/customer
      - 'Deposit' → Unknown
      - 'ACH CREDIT' → electronic deposit
    """

    clean_name = name.strip() if name else ""
    clean_memo = memo.strip() if memo else ""

    # Cases where memo holds the useful source name
    if clean_memo and clean_memo not in ("DEPOSIT", "MOBILE DEPOSIT", "TRANSFER"):
        return clean_memo.title()

    # Otherwise fallback to NAME
    if clean_name and clean_name not in ("DEPOSIT", "CREDIT", "TRANSFER"):
        return clean_name.title()

    return "Unknown Source"