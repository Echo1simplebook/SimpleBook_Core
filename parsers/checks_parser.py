from parsers.qfx_parser import filter_by_month


def extract_checks(transactions: list[dict]) -> list[dict]:
    """
    Takes a full transaction list and returns only CHECK transactions.
    Logic:
        - If CHECKNUM exists → it's a check.
        - If TRNTYPE == 'CHECK' → it's a check.
        - If NAME contains 'CHECK' → treat it as a check.
    """

    checks = []

    for tx in transactions:
        checknum = tx.get("checknum")
        tx_type = tx.get("type", "").upper()
        name = (tx.get("name") or "").upper()
        memo = (tx.get("memo") or "").upper()

        is_check = (
            checknum is not None
            or tx_type == "CHECK"
            or "CHECK" in name
        )

        if not is_check:
            continue

        vendor = _extract_vendor(name, memo, checknum)

        checks.append({
            "checknum": checknum,
            "amount": tx["amount"],
            "date": tx["posted_date"],
            "vendor": vendor,
            "fitid": tx["fitid"],
        })

    return checks


def _extract_vendor(name: str, memo: str, checknum: str | None) -> str:
    """
    Extracts the most likely vendor name.
    Priority:
        1. MEMO if it's not just 'CHECK ####'
        2. NAME if it looks like a vendor
        3. 'Unknown Vendor ####' fallback
    """

    # Clean up text
    clean_name = name.strip()
    clean_memo = memo.strip()

    # If memo contains a vendor name instead of "CHECK ####"
    if clean_memo and not clean_memo.startswith("CHECK"):
        return clean_memo.title()

    # If name looks like a vendor, not "CHECK PAID" or "CHECK #123"
    if clean_name and not clean_name.startswith("CHECK"):
        return clean_name.title()

    # Fallback
    if checknum:
        return f"Unknown Vendor #{checknum}"

    return "Unknown Vendor"