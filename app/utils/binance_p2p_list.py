import logging
from typing import Optional

import requests

from app.config import settings

logger = logging.getLogger(__name__)


def get_binance_p2p_rate() -> Optional[float]:
    payload = {
        "fiat": "VES",
        "asset": "USDT",
        "tradeType": "SELL",
        "page": 1,
        "rows": 3,
        "payTypes": ["BNC", "Banesco"],  # Solo BNC y Banesco
        "publisherType": None,  # None = sin filtro de comerciantes verificados
        "transAmount": "",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            settings.BINANCE_P2P_URL,
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

        res_json = response.json()
        items = res_json.get("data", [])
        if not items:
            logger.warning("Binance P2P response did not include rate items")
            return None

        return float(items[0]["adv"]["price"])
    except (requests.RequestException, KeyError, TypeError, ValueError) as exc:
        logger.warning("Could not fetch Binance P2P rate: %s", exc)
        return None
