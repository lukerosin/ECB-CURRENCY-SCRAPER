# ECB-CURRENCY-SCRAPER


## How it works?
currency_scraper.py module fetches all RSS channels bound with a particular currency, which are accessible on the European Central Bank server. 
Data containing currencies conversion rates and it's published dates are stored in databased in relation 
to a particular currency. All data are presented in the endpoint implemented using Django technology.

## First start-up
* clone repository to your local directory
* run ecb\manager.py migrate
* run ecb\manage.py runserver
* run ecb\currency_scraper.py
* open http://127.0.0.1:8000/ in your web browser
 
#### Updating database 
* run ecb\currency_scraper.py
