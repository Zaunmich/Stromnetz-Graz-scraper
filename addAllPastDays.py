import stromnetzGrazScraper 
import influxDB 

from datetime import date, datetime, timedelta, time



# get the token
token = stromnetzGrazScraper.getLoginToken()
# get meterID
meterPointID = stromnetzGrazScraper.getMeterID(token)

# add ALL past data
day = date.today()
while True:
    # build the time-frame of interest
    day = day - timedelta(days = 1)
    daystart = datetime.combine(day, time.min).astimezone()
    dayend = datetime.combine(day, time.max).astimezone()
    print(day.isoformat())
    # get the data
    data = stromnetzGrazScraper.getReadings(token,meterPointID,daystart,dayend)
    influxDB.writeToInfluxDB(data)

    # just in case....
    if day < date.today() - timedelta(days = 180):
        break