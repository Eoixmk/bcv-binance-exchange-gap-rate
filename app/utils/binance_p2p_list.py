import requests
from app.config import settings

def get_binance_p2p_rate() -> float:
    params = {
        "fiat": "VES",
        "asset": "USDT",
        "tradeType": "SELL",
        "page": 1,
        "rows": 3,
        "payTypes": ["BancoDeVenezuela", "Banesco"]  # Filtro corregido para bancos reales
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    
    try:
        response = requests.get(settings.BINANCE_P2P_URL, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if res_json and "data" in res_json and "items" in res_json["data"]:
                items = res_json["data"]["items"]
                if len(items) > 0:
                    return float(items[0]["price"])
        return 0.0
    except Exception:
        return 0.0