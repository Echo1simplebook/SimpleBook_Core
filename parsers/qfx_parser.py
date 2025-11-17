import re
from datetime import datetime


def parse_qfx_file(filepath: str) -> list[dict]:
    """
    Reads a QFX file and returns a list of normalized transaction dictionaries.
    """

    with open(filepath, "r", errors="ignore") as f:
        text = f.read()

    # Extract every <STMTTRN> ... </STMTTRN> block
    blocks = re.findall(r"<STMTTRN>(.*?)</STMTTRN>", text, flags=re.DOTALL)

    transactions = []

    for block in blocks:
        tx_type = _extract_tag(block, "TRNTYPE")
        posted_raw = _extract_tag(block, "DTPOSTED")
        amount_raw = _extract_tag(block, "TRNAMT")
        fitid = _extract_tag(block, "FITID")
        checknum = _extract_tag(block, "CHECKNUM")
        name = _extract_tag(block, "NAME")
        memo = _extract_tag(block, "MEMO")

        # Normalize fields
        posted_date = _normalize_qfx_date(posted_raw)
        amount = float(amount_raw) if amount_raw else 0.0

        transactions.append({
            "type": tx_type,
            "posted_raw": posted_raw,
            "posted_date": posted_date,
            "amount": amount,
            "fitid": fitid,
            "checknum": checknum,
            "name": name,
            "memo": memo,
        })

    return transactions


def _extract_tag(block: str, tag: str) -> str | None:
    """
    Returns the text inside <TAG> ... or None if not found.
    """
    match = re.search(rf"<{tag}>(.*?)(?=<|$)", block, flags=re.DOTALL)
    return match.group(1).strip() if match else None


def _normalize_qfx_date(raw: str | None) -> str | None:
    """
    Converts QFX DTPOSTED values like:
    '20240701120000.000[-5:EST]'
    into '2024-07-01'.

    Returns None if raw is missing.
    """
    if not raw:
        return None

    # Extract first 8 digits YYYYMMDD
    match = re.match(r"(\d{8})", raw)
    if not match:
        return None

    yyyymmdd = match.group(1)
    dt = datetime.strptime(yyyymmdd, "%Y%m%d")
    return dt.strftime("%Y-%m-%d")


# ---------------------------
# Utility: Filter by month
# ---------------------------
def filter_by_month(transactions: list[dict], year: int, month: int) -> list[dict]:
    """
    Filters transactions to a specific year/month.
    """

    month_str = f"{year:04d}-{month:02d}-"

    return [tx for tx in transactions if tx["posted_date"] and tx["posted_date"].startswith(month_str)]