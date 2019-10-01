import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from web.models import *
from cfg import DB_STRING
from web import app, render_template
engine = create_engine(DB_STRING, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/currency_rates')

def currency_rates():
    page_title = "Курсы валют"
    rates = session.query(Currency_Rate).order_by("operation_date").all()
    return render_template('currency_rates.html', page_title=page_title, rates=rates)


if __name__ == "__main__":
    app.run(debug=True)