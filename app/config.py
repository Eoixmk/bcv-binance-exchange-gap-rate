import os
from dotenv import load_dotenv

# Cargamos el archivo .env
load_dotenv()

class Settings:
    BCV_URL: str = os.getenv("BCV_URL", "https://www.bcv.org.ve/")
    BINANCE_P2P_URL: str = os.getenv("BINANCE_P2P_URL", "https://www.binance.com/bapi/c2c/v1/public/c2c/agent/ad-list")

settings = Settings()