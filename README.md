# Backend - BCV Binance Exchange Rate Gap

API en FastAPI para consultar tasas de cambio en Venezuela desde dos fuentes:

- BCV: tasa oficial publicada en el sitio del Banco Central de Venezuela.
- Binance P2P: tasa USDT/VES desde el endpoint publico P2P de Binance.

El backend expone un endpoint que devuelve ambas tasas y un promedio simple entre ellas.

## Requisitos

- Python 3.9 o superior
- `pip`
- Entorno virtual recomendado

Dependencias usadas por la aplicacion:

- `fastapi`
- `uvicorn`
- `requests`
- `beautifulsoup4`
- `python-dotenv`

## Instalacion

Desde esta carpeta `backend/`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Variables de entorno

La configuracion se carga desde un archivo `.env` en la raiz del backend.

Ejemplo:

```env
BCV_URL=https://www.bcv.org.ve/
BINANCE_P2P_URL=https://www.binance.com/bapi/c2c/v1/public/c2c/agent/ad-list
```

Si no se definen estas variables, la aplicacion usa esos mismos valores por defecto.

## Ejecucion local

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

La API quedara disponible en:

```text
http://127.0.0.1:8000
```

La documentacion interactiva de FastAPI se puede abrir en:

```text
http://127.0.0.1:8000/docs
```

## Endpoint

### `GET /rates`

Consulta las tasas del BCV y Binance P2P, y devuelve un promedio.

Ejemplo:

```bash
curl http://127.0.0.1:8000/rates
```

Respuesta:

```json
{
  "bcv": 120.5,
  "binance_p2p": 135.2,
  "promedio": 127.85,
  "status": {
    "bcv": true,
    "binance_p2p": true
  }
}
```

Campos:

- `bcv`: tasa obtenida desde el sitio del BCV.
- `binance_p2p`: tasa USDT/VES obtenida desde Binance P2P.
- `promedio`: promedio simple entre las tasas disponibles.
- `status`: indica si cada fuente respondio con una tasa valida.

Si una fuente externa falla, su valor sera `null` y su estado sera `false`. Si ambas fallan, `promedio` tambien sera `null`.

## Pruebas

```bash
source venv/bin/activate
python -B -m unittest discover -s tests
```

## Estructura

```text
app/
  main.py                    # Punto de entrada FastAPI y rutas HTTP
  config.py                  # Carga variables de entorno
  utils/
    bcv_scraper.py           # Obtiene y parsea la tasa del BCV
    binance_p2p_list.py      # Obtiene la tasa desde Binance P2P
```

## Notas

- El scraper del BCV usa `verify=False` por problemas conocidos con SSL en el sitio del BCV.
- Las funciones de consulta devuelven `None` si una fuente externa falla, no responde o cambia su formato.
- Binance P2P se consulta con filtros para `VES`, `USDT`, tipo `SELL` y algunos bancos locales.
