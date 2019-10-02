from datetime import date
import logging
import requests

import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from web.logs import logger
from cfg import DB_STRING
# from web.models import Currency_Rate, create_engine, sessionmaker

# engine = create_engine(DB_STRING, echo=True)

# Session = sessionmaker(bind=engine)
# session = Session()

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

def currency_page(session):
    page_title = "Курсы валют"
    rates = session.query(Currency_Rate).order_by("operation_date").all()
    return render_template('currency_rates.html', page_title=page_title, rates=rates)

# new_currency = Currency_Rate(2, 4, 23, date(2018,2,17))
# session.add(new_currency)

# session.commit()
# session.close()