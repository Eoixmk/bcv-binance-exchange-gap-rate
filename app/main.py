from typing import Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.utils.bcv_scraper import get_bcv_rate
from app.utils.binance_p2p_list import get_binance_p2p_rate


class RatesResponse(BaseModel):
    bcv: Optional[float]
    binance_p2p: Optional[float]
    promedio: Optional[float]
    status: Dict[str, bool]


app = FastAPI(title="Dolar Venezuela API Proxy")


@app.get("/rates", response_model=RatesResponse)
def read_rates():
    bcv_price = get_bcv_rate()
    binance_price = get_binance_p2p_rate()

    available_rates = [
        rate for rate in (bcv_price, binance_price)
        if rate is not None and rate > 0
    ]
    promedio = sum(available_rates) / len(available_rates) if available_rates else None

    return {
        "bcv": round(bcv_price, 2) if bcv_price is not None else None,
        "binance_p2p": round(binance_price, 2) if binance_price is not None else None,
        "promedio": round(promedio, 2) if promedio is not None else None,
        "status": {
            "bcv": bcv_price is not None and bcv_price > 0,
            "binance_p2p": binance_price is not None and binance_price > 0,
        },
    }
