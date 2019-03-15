import re
import sqlite3

import requests
import urllib.request

DATABASE = "db.sqlite3"

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
c = conn.cursor()

prefix = 'https://www.ecb.europa.eu'
currency_link_pattern = re.compile(br'<a class="rss" href="(.*)">(.*\(\w{3}\))</a>')
pub_date_rate_pattern = re.compile(br'(\d{4}-\d{2}-\d{2}).*?(\d+\.\d+)', re.DOTALL)


with urllib.request.urlopen('https://www.ecb.europa.eu/home/html/rss.en.html') as response:
    source = response.read()

    feeds_info = re.findall(currency_link_pattern, source)


def store_feed_items(entries):
    """ Takes a currency feeder data and store them in the DB """
    for entry in entries:
        url = prefix + entry[0].decode()
        name = entry[1].decode()
        c.execute('SELECT id from currencies_currency WHERE url=? AND name=?', (url, name))
        if len(c.fetchall()) == 0:
            c.execute('INSERT INTO currencies_currency(url, name) VALUES (?,?)', (url, name))

        currency_id = c.execute('SELECT id FROM currencies_currency WHERE url=? AND name=?', (url, name)).fetchone()[0]

        r = requests.get(url)
        content = r.content
        currencies = re.findall(pub_date_rate_pattern, content)
        for currency in currencies:
            pub_date = currency[0].decode()
            rate = currency[1].decode()
            c.execute('SELECT id from currencies_history WHERE pub_date=? AND rate=?', (pub_date, rate))
            if len(c.fetchall()) == 0:
                c.execute('INSERT INTO currencies_history(pub_date, rate, currency_id) VALUES (?,?,?)',
                          (pub_date, rate, currency_id))


store_feed_items(feeds_info)


conn.commit()
