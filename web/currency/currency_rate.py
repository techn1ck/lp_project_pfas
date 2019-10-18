from datetime import date
import logging
import requests

import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from web.logs import logger


def get_currency_rate(currency1="USD", currency2="RUB", date=date.today(), retries=2):
    date = str(date)
    request_url = f'https://api.ratesapi.io/api/{date}'
    params = {"base": currency1, "symbols": currency2}
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        result = session.get(request_url, params=params, timeout=1)
        result.raise_for_status()
        return float(result.json()['rates'][currency2])
    except requests.RequestException as request_error:
        logger.info(f'Network error: {request_error}')
        raise
    except(ValueError, KeyError) as format_error:
        logger.info(f'Ошибка при обработке ответа от сервера: {format_error}')
        raise