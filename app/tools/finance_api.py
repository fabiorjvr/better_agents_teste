import os
from typing import Dict, List


def get_returns(symbols: List[str]) -> Dict[str, float]:
    provider = os.getenv("FINANCE_PROVIDER", "stub")
    data = {
        "PETR4": 1.2,
        "VALE3": -0.7,
        "ITUB4": 0.5,
    }
    result: Dict[str, float] = {}
    for s in symbols:
        key = s.upper()
        val = data.get(key, 0.0)
        result[key] = val
    return result

