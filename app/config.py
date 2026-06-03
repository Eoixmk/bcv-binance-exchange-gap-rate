import os
from dotenv import load_dotenv

# Cargamos el archivo .env
load_dotenv()

class Settings:
    BCV_URL: str = os.getenv("BCV_URL", "https://www.bcv.org.ve/")
    BINANCE_P2P_URL: str = os.getenv("BINANCE_P2P_URL", "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search")

settings = Settings()