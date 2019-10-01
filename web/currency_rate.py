import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from web.models import *
from cfg import DB_STRING

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import date
import logging

engine = create_engine(DB_STRING, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler('web.log')
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)

currency1 = "UD"
currency2 = "RUB"

def get_currency_rate(currency1, currency2, date=date.today(), retries=2):
    date = str(date)
    request_url = f'https://api.ratesapi.io/api/{date}?base={currency1}&symbols={currency2}'
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        result = session.get(request_url, timeout=1)
        result.raise_for_status()
        return float(result.json()['rates'][currency2])
    except requests.RequestException as request_error:
        logger.info(f'Network error: {request_error}')
        return False
    except(ValueError, KeyError) as format_error:
        logger.info(f'Ошибка при обработке ответа от сервера: {format_error}')
        return False

# new_currency = Currency_Rate(2, 4, 23, date(2018,2,17))
# session.add(new_currency)

# rates = session.query(Currency_Rate).order_by("operation_date").all()




# session.commit()
# session.close()