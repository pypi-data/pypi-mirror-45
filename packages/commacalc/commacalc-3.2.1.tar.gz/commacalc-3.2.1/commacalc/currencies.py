# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import os
import pickle
from stat import ST_MTIME
from time import time
import threading


_SYMBOLS = {
    '$': "USD",
    '£': "GBP",
    '€': "EUR",
    '¥': "CNY",
    '₽': "RUB",
}


def replace_symbols(input_):
    """replace €123 with EUR*123"""
    for symbol, code in _SYMBOLS.items():
        input_ = input_.replace(symbol, code+'*')
    return input_


RATES_URLS = [
    ("https://www.cnb.cz/cs/financni_trhy/devizovy_trh/"
     "kurzy_devizoveho_trhu/denni_kurz.txt"),
    ("https://www.cnb.cz/cs/financni_trhy/devizovy_trh/"
     "kurzy_ostatnich_men/kurzy.txt")
]
RATES_PICKLE = os.path.expanduser("~/.rates.pickle")

rates = {}


def _download():
    import httplib2
    import csv
    import io

    h = httplib2.Http()

    for url in RATES_URLS:
        response, content = h.request(url)

        reader = csv.reader(io.StringIO(content.decode()), delimiter='|')
        next(reader)    # header
        next(reader)    # column names
        for row in reader:
            try:
                country, currname, amount, currcode, rate = row
                rates[currcode] = float(rate.replace(',', '.')) / int(amount)
            except ValueError:
                "Invalid row"


def _dump():
    with open(RATES_PICKLE, mode="wb") as f:
        pickle.dump(rates, f)


def _dl_n_dump():
    _download()
    _dump()


def _load():
    global rates

    with open(RATES_PICKLE, mode="rb") as f:
        rates = pickle.load(f)

    globals().update(rates)


def rate(currency):
    """Get exchange rate (ČNB)

    :param currency:    Code of currency (e.g. "USD" or "EUR")
    :returns:           Exchange rate in CZK
    """
    if not rates:
        if not os.path.exists(RATES_PICKLE):
            _download()
            threading.Thread(target=_dump).start()
        elif time() - os.stat(RATES_PICKLE)[ST_MTIME] > 86400:
            _load()
            threading.Thread(target=_dl_n_dump).start()
        else:
            _load()

    return rates[currency]


# curencies
dollar = rate("USD")
euro = rate("EUR")
sterling = rate("GBP")
ruble = rate("RUB")
yen = rate("JPY")


if __name__ == "__main__":
    print(f"USD: {USD}")    # noqa: F821
    print(f"EUR: {EUR}")    # noqa: F821
    print(f"VND: {VND}")    # noqa: F821
