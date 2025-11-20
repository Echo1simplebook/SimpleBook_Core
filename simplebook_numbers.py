import re
from typing import Optional

def smart_amount_parser(raw: str) -> Optional[float]:
    """
    Convert a bank-style amount string into a float.

    Handles:
      - Commas as thousand separators:  "4,000.00" -> 4000.00
      - Optional decimals:              "1234" -> 1234.00
      - Negatives:                      "-123.45", "(123.45)" -> -123.45
      - Leading/trailing junk:          "  $4,000.00 " -> 4000.00

    Returns None if it can't make sense of the string.
    """
    if raw is None:
        return None

    s = raw.strip()
    if not s:
        return None

    # detect negative
    negative = False
    if "(" in s and ")" in s:
        negative = True
    if "-" in s:
        negative = True

    # strip wrappers
    s = (s.replace("(", "")
         .replace(")", "")
         .replace("$", "")
         .replace("£", "")
         .replace("€", "")
         .replace("+", "")
         .replace("-", "")
         .replace(" ", ""))

    # must contain digits
    if not re.search(r"\d", s):
        return None

    # comma/decimal handling
    if "," in s and "." in s:
        s = s.replace(",", "")
    else:
        if "," in s and "." not in s:
            parts = s.split(",")
            if len(parts[-1]) == 2:
                s = s.replace(".", "")
                s = s.replace(",", ".")
            else:
                s = s.replace(",", "")

    try:
        value = float(s)
    except ValueError:
        return None

    if negative:
        value = -value

    return value