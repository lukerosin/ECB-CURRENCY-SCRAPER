import re
import sqlite3
import threading
import Queue
import feedparser  # available at http://feedparser.org

from urllib import urlopen
from BeautifulSoup import BeautifulSoup

THREAD_LIMIT = 20
jobs = Queue.Queue(0)
rss_to_process = Queue.Queue(THREAD_LIMIT)

DATABASE = "db.sqlite3"

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# insert initial values into feed database
c.execute('CREATE TABLE IF NOT EXISTS "currencies_currency" ('
          '"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, '
          '"url" varchar(200) NOT NULL, '
          '"name" varchar(30) NOT NULL);')
c.execute(
    'CREATE TABLE IF NOT EXISTS "currencies_history" ('
    '"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, '
    '"pub_date" datetime NOT NULL, '
    '"rate" varchar(10) NOT NULL, '
    '"currency_id" integer NOT NULL REFERENCES "currencies_currency" ("id") DEFERRABLE INITIALLY DEFERRED);')

c.execute('CREATE INDEX "currencies_history_currency_id_f8c441f3" ON "currencies_history" ("currency_id");')

source = urlopen('https://www.ecb.europa.eu/home/html/rss.en.html').read()

title = re.compile(r'<a class="rss" href=".*">(.*\(\w{3}\))</a>')
link = re.compile(r'<a class="rss" href="(.*)">.*</a>')

find_title = re.findall(title, source)
find_link = re.findall(link, source)

c.execute("INSERT INTO RSSFeeds(url) VALUES('http://www.halotis.com/feed/');")

feeds = c.execute('SELECT id, url FROM RSSFeeds').fetchall()


def store_feed_items(id, items):
    """ Takes a feed_id and a list of items and stored them in the DB """
    for entry in items:
        c.execute('SELECT id from currencies_currency WHERE url=?', (entry.link,))
        if len(c.fetchall()) == 0:
            c.execute('INSERT INTO currencies_currency (id, url, name) VALUES (?,?,?)',
                      (id, entry.url, entry.name))


# strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed)

def thread():
    while True:
        try:
            id, feed_url = jobs.get(False)  # False = Don't wait
        except Queue.Empty:
            return

        entries = feedparser.parse(feed_url).entries
        rss_to_process.put((id, entries), True)  # This will block if full


for info in feeds:  # Queue them up
    jobs.put([info['id'], info['url']])

for n in xrange(THREAD_LIMIT):
    t = threading.Thread(target=thread)
    t.start()

while threading.activeCount() > 1 or not rss_to_process.empty():
    # That condition means we want to do this loop if there are threads
    # running OR there's stuff to process
    try:
        id, entries = rss_to_process.get(False, 1)  # Wait for up to a second
    except Queue.Empty:
        continue

    store_feed_items(id, entries)

conn.commit()
