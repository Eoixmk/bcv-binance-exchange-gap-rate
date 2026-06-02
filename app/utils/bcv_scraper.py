import requests
from bs4 import BeautifulSoup
from app.config import settings

def get_bcv_rate() -> float:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        # Nota: verify=False se mantiene por los problemas de SSL del BCV
        response = requests.get(settings.BCV_URL, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            dolar_container = soup.find('div', id='dolar')
            if dolar_container:
                price_text = dolar_container.find('strong').text.strip()
                price_float = float(price_text.replace('.', '').replace(',', '.'))
                return price_float
        return 0.0
    except Exception:
        return 0.0