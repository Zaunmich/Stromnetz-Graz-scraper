# Stromnetz-Graz-scrapter
A simple script to scrape your smartmeter readings from https://webportal.stromnetz-graz.at/ to an InfluxDB instance

## Quickstart

### Pre-requisites

* You have done the opt-in for quarter-hourly smartmeter readings (check Stromnetz-Graz website on how to do it!)
* You have an InfluxDB instance running
* You have Python installed

### First-run

* Create virtual environment  ``python -m venv .venv``
* Activeate it. E.g. on windows ``\.venv\Scripts\activate``
* Install packages ``pip install -r requirements.txt``
* Rename ``config.py-example`` into ``config.py`` and fill out the required fields
* Add the https certificate from https://webportal.stromnetz-graz.at/ to ``cacert.pem`` (see ``stromnetzGrazScraper.py`` for more info)
* Run ``addAllPastDays.py`` to add the last 180 days to your database

### Daily runs

* Simply run ``addYesterday.py`` every day after midnight to add yesterday's data to your InfluxDB instance.

## Notes

# About the missing certificates

I have included the current certificates from https://webportal.stromnetz-graz.at/ in the repo as ``server.pem``. You can simply add those to the ``cacert.pem`` file.
Just be aware, that those certificates expire on Monday, April 17, 2023 at 1:59:59 AM. 
