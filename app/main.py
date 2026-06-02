from fastapi import FastAPI
import urllib3
from app.utils.bcv_scraper import get_bcv_rate
from app.utils.binance_p2p_list import get_binance_p2p_rate

# Deshabilitamos alertas visuales del SSL del BCV de manera global al inicio
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI(title="Dolar Venezuela API Proxy")

@app.get("/rates")
def read_rates():
    bcv_price = get_bcv_rate()
    binance_price = get_binance_p2p_rate()
    
    if bcv_price > 0 and binance_price > 0:
        promedio = (bcv_price + binance_price) / 2
    else:
        promedio = bcv_price if bcv_price > 0 else binance_price

    return {
        "bcv": round(bcv_price, 2),
        "binance_p2p": round(binance_price, 2),
        "promedio": round(promedio, 2)
    }