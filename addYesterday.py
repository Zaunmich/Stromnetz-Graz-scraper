import stromnetzGrazScraper 
import influxDB 
from datetime import date, datetime, timedelta, time


# get yesterdays data
data = stromnetzGrazScraper.quickYesterdayData()
# write to database
influxDB.writeToInfluxDB(data)
