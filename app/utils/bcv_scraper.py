import logging
import warnings
from typing import Optional

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

from app.config import settings

logger = logging.getLogger(__name__)


def get_bcv_rate() -> Optional[float]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    try:
        # Nota: verify=False se mantiene por los problemas de SSL del BCV
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            response = requests.get(
                settings.BCV_URL,
                headers=headers,
                verify=False,
                timeout=10,
            )

        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        dolar_container = soup.find("div", id="dolar")
        price_node = dolar_container.find("strong") if dolar_container else None

        if price_node is None:
            logger.warning("BCV response did not include the expected dolar price node")
            return None

        price_text = price_node.text.strip()
        return float(price_text.replace(".", "").replace(",", "."))
    except (requests.RequestException, TypeError, ValueError) as exc:
        logger.warning("Could not fetch BCV rate: %s", exc)
        return None
