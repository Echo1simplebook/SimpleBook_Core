def combine_credits(deposits: list[dict], other_credits: list[dict]) -> list[dict]:
    """
    Combines deposit credits and other credits into a single list
    and sorts them by date (oldest → newest).
    """

    combined = []

    # Normalize deposits
    for d in deposits:
        combined.append({
            "amount": d["amount"],
            "date": d["date"],
            "source": d.get("source"),
            "fitid": d["fitid"],
            "type": "DEPOSIT",
            "raw": d
        })

    # Normalize other credits
    for oc in other_credits:
        combined.append({
            "amount": oc["amount"],
            "date": oc["date"],
            "source": oc.get("source"),
            "fitid": oc["fitid"],
            "type": "OTHER_CREDIT",
            "raw": oc
        })

    # Sort by date
    combined.sort(key=lambda x: x["date"])

    return combined